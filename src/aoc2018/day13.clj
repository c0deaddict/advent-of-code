(ns aoc2018.day13
  (require [clojure.java.io :as io]
           [clojure.string :as str]
           [clojure.test :as t]))

(def data-file (io/resource "day13.txt"))

(defn read-data []
  (slurp data-file))

(def test-data
  (str
#"/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   "))

(def char-mapping
  {\- :track-horz
   \| :track-vert
   \/ :track-ne-sw-corner
   \\ :track-nw-se-corner
   \+ :track-intersect
   \^ :train-north
   \> :train-east
   \v :train-south
   \< :train-west
   \space nil
   })

(def is-train?
  #{:train-north
   :train-east
   :train-south
   :train-west})

(def is-train-horz?
  #{:train-east :train-west})

(def is-train-vert?
  #{:train-north :train-south})

(def is-straight?
  #{:track-horz :track-vert})

(def is-corner?
  #{:track-ne-sw-corner :track-nw-se-corner})

(def inv-char-mapping
  (clojure.set/map-invert char-mapping))

;; https://clojuredocs.org/clojure.core/to-array-2d
(defn parse [data]
  (->>
   data
   (str/split-lines)
   (map seq)
   (map #(map char-mapping %))
   (to-array-2d)))

(defn dims [grid]
  (let [height (alength grid)
        width (alength (aget grid 0))]
    [width height]))

(defn print-grid [grid trains]
  (let [[width height] (dims grid)
        trains-at (group-by :pos trains)]
    (doseq [y (range height)]
      (doseq [x (range width)
              :let [cell (aget grid y x)
                    trains (get trains-at [x y])]]
        (print
         (cond
           (empty? trains) (inv-char-mapping cell)
           (= 1 (count trains)) (inv-char-mapping (:dir (first trains)))
           :else \X)))
      (println))))

(defn for-each-cell [grid]
  (let [[width height] (dims grid)]
    (for [x (range width)
          y (range height)]
      [[x y] (aget grid y x)])))

(defn init-train [pos dir]
  {:pos pos
   :dir dir
   :n-turns 0})

(defn find-trains [grid]
  (->>
   (for-each-cell grid)
   (filter (comp is-train? second))
   (map #(apply init-train %))))

(defn replace-trains [grid trains]
  "Replace the initial position of trains with track"
  (doseq [{:keys [pos dir]} trains
          :let [[x y] pos]]
    ;; trains are always on straight tracks
    (aset grid y x
          (if (is-train-horz? dir)
            :track-horz
            :track-vert))))

(defn cyclic [coll n]
  (nth coll (mod n (count coll))))

(defn turn [train rel-turn]
  (let [compass [:train-north
                 :train-east
                 :train-south
                 :train-west
                 ]
        cur (.indexOf compass (:dir train))
        dir (cyclic compass (+ cur rel-turn))]
    (assoc train :dir dir)))

(defn move-through-corner [train corner]
  (let [corner-map {[:train-north :track-nw-se-corner] :train-west
                    [:train-south :track-nw-se-corner] :train-east
                    [:train-east :track-nw-se-corner] :train-south
                    [:train-west :track-nw-se-corner] :train-north
                    [:train-north :track-ne-sw-corner] :train-east
                    [:train-south :track-ne-sw-corner] :train-west
                    [:train-east :track-ne-sw-corner] :train-north
                    [:train-west :track-ne-sw-corner] :train-south}
        dir (corner-map [(:dir train) corner])]
    (assoc train :dir dir)))

(defn turn-train [train]
  ;; cycle through left, straight and right turn.
  (let [rel-turn (cyclic [-1 0 1] (:n-turns train))
        train (turn train rel-turn)]
    (update train :n-turns inc)))

(defn move-train [grid train]
  (let [[x y] (:pos train)
        _ (assert (not (nil? (:pos train))) train)
        next-map {:train-north [x (dec y)]
                  :train-east [(inc x) y]
                  :train-south [x (inc y)]
                  :train-west [(dec x) y]}
        [x y] (get next-map (:dir train))
        train (assoc train :pos [x y])
        cell (aget grid y x)]
    (cond
      (is-straight? cell) train
      (is-corner? cell) (move-through-corner train cell)
      (= :track-intersect cell) (turn-train train)
      (nil? cell) (assert false "off grid")
      (is-train? cell) (assert false "trains should be off grid")
      :else (assert false (str "unknown state in grid: " cell)))))

(defn tick [grid trains]
  "Trains are moved in order of their pos."
  (loop [moved []
         to-move (sort-by :pos trains)]
    (if (empty? to-move)
      moved
      (let [t (move-train grid (first to-move))
            trains-at (set (map :pos (concat moved to-move)))]
        (if (contains? trains-at (:pos t))
          {:collision (:pos t)}
          (recur (conj moved t) (rest to-move)))))))

(defn run [grid trains]
  (iterate (partial tick grid) trains))

(defn find-collision [iter]
  (->>
   (map :collision iter)
   (drop-while nil?)
   (first)))

(defn solve-part-1 [grid trains]
  (->>
   (run grid trains)
   (find-collision)
   (str/join ",")))

(defn main
  "Advent of Code 2018 - Day 13"
  [& args]
  (let [grid (parse (read-data))
        trains (find-trains grid)]
    (replace-trains grid trains)
    (println (solve-part-1 grid trains))))

