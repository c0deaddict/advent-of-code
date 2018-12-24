(ns aoc2018.day18
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.test :as t]
            [clojure.pprint :refer [pprint]]
            [aoc2018.utils :refer :all]))

(def data-file (io/resource "day18.txt"))

(defn read-data [] (slurp data-file))

(def test-data (str
#".#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."))

(defn bounds [grid]
  (last (sort (map first grid))))

(def char-mapping
  {\. :open-ground
   \| :trees
   \# :lumberyard})

(defn to-grid [lines]
  (for [[y row] (map vector (range) lines)
        [x cell] (map vector (range) row)]
    [[y x] cell]))

(defn parse [data]
  (->> data
     (str/split-lines)
     (map #(map char-mapping %))
     (to-grid)
     (into {})))

(defn grid-str [grid]
  (let [[h w] (bounds grid)
        inv-mapping (clojure.set/map-invert char-mapping)]
    (for [y (range (inc h))]
      (apply str
             (for [x (range (inc w))
                   :let [cell (get grid [y x])]]
               (inv-mapping cell))))))

(defn print-grid [grid]
  (let [[h w] (bounds grid)
        inv-mapping (clojure.set/map-invert char-mapping)]
    (doseq [y (range (inc h))]
      (doseq [x (range (inc w))
              :let [cell (get grid [y x])]]
        (print (inv-mapping cell)))
      (println))))

(defn in-bounds? [[h w] [y x]]
  (and (<= 0 x w) (<= 0 y h)))

(defn around [bounds [y x]]
  (filter (partial in-bounds? bounds)
          [[(dec y) (dec x)]
           [(dec y) x]
           [(dec y) (inc x)]
           [y (dec x)]
           [y (inc x)]
           [(inc y) (dec x)]
           [(inc y) x]
           [(inc y) (inc x)]]))

(defn neighbours [grid bounds pos]
  (->>
   (around bounds pos)
   (select-keys grid)
   (vals)
   (group-by identity)
   (map-values count)
   (into {})))

(defmulti cell-step (fn [val neighbours] val))

(defmethod cell-step :open-ground [_ neighbours]
  (if (>= (get neighbours :trees 0) 3)
    :trees
    :open-ground))

(defmethod cell-step :trees [_ neighbours]
  (if (>= (get neighbours :lumberyard 0) 3)
    :lumberyard
    :trees))

(defmethod cell-step :lumberyard [_ neighbours]
  (if (and (pos? (get neighbours :lumberyard 0))
           (pos? (get neighbours :trees 0)))
    :lumberyard
    :open-ground))

(defn cell-step-map [grid bounds [pos val]]
  [pos (cell-step val (neighbours grid bounds pos))])

(defn step [grid]
  (let [b (bounds grid)]
    (into {} (pmap (partial cell-step-map grid b) grid))))

(defn run [grid]
  (iterate step grid))

(defn total-value [grid]
  (let [counts (->> grid
                (vals)
                (group-by identity)
                (map-values count)
                (into {}))]
    (* (get counts :trees 0)
       (get counts :lumberyard 0))))

(defn solve-part-1 [grid]
  (total-value (nth (run grid) 10)))

(defn find-cycle [generations]
  (loop [seen {}
         iter generations
         count 0]
    (let [state (first iter)
          state-str (grid-str state)]
      (if-let [prev-count (get seen state-str)]
        [prev-count (- count prev-count)]
        (recur (assoc seen state-str count)
               (rest iter)
               (inc count))))))

(defn solve-part-2 [grid]
  (let [q 1000000000
        generations (run grid)
        [cycle-start cycle-len] (find-cycle generations)
        i (+ cycle-start (mod (- q cycle-start) cycle-len))]
    (total-value (nth generations i))))

(defn main
  "Advent of Code 2018 - Day 18"
  [& args]
  (let [grid (parse (read-data))]
    (println (solve-part-1 grid))
    (println (solve-part-2 grid))))
