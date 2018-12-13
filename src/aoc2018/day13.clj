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
   })

(def is-train?
  #{:train-north
   :train-east
   :train-south
   :trian-west})

(def is-train-horz?
  #{:train-east :train-west})

(def is-train-vert?
  #{:train-north :train-south})

(def is-straight?
  #{:track-horz :track-vert})

(def is-corner?
  #{:track-ne-sw-corner :track-nw-se-corner})

;; https://clojuredocs.org/clojure.core/to-array-2d
(defn parse [data]
  (->>
   data
   (str/split-lines)
   (map seq)
   (map #(map char-mapping %))
   (to-array-2d)))

(defn for-each-cell [grid]
  (let [height (alength grid)
        width (alength (aget grid 0))]
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
  nil)

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

(defn cyclic [coll n]
  (let [idx (mod (count coll) n)]
    (nth coll n)))

(defn turn-train [train]
  (let [turn (cyclic [:left :straight :right]
                     (:n-turns train))]
    ))

(defn move-train [grid train]
  (let [[x y] (:pos train)
        next-map {:train-north [x (dec y)]
                  :train-east [(inc x) y]
                  :train-south [x (inc y)]
                  :train-west [(dec x) y]}
        [x y] (get next-map (:dir train))
        train (assoc train :pos [x y])
        cell (aget grid x y)]
    (cond
      (is-straight? cell) train
      (is-corner? cell) (move-through-corner train cell)
      (= :track-intersect cell) (turn-train train)
      (nil? cell) (assert false "off grid")
      (is-train? cell) (assert false "trains should be off grid"))))

(defn main
  "Advent of Code 2018 - Day 13"
  [& args]
  (let [tracks (parse (read-data))]
    (println "TODO")))
