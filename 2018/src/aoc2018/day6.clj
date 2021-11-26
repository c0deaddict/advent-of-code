(ns aoc2018.day6
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.set]
            [clojure.pprint :refer [pprint]]))

(def data-file (io/resource "day6.txt"))

(defn parse-coord [str]
  (map #(Integer. %) (str/split str #", ")))

(defn read-data []
  (->>
   (slurp data-file)
   str/split-lines
   (map parse-coord)))

(def test-data
  [[1, 1]
   [1, 6]
   [8, 3]
   [3, 4]
   [5, 5]
   [8, 9]])

(defn min-max [coll]
  [(reduce min coll)
   (reduce max coll)])

(defn bounds [coords]
  (let [[x-min x-max] (min-max (map first coords))
        [y-min y-max] (min-max (map second coords))]
    [[x-min y-min]
     [(+ 1 x-max) (+ 1 y-max)]]))

(defn expand-bounds [d [[x-min y-min] [x-max y-max]]]
  [[(- x-min d) (- y-min d)]
   [(+ x-max d) (+ y-max d)]])

(defn enumerate-fields [[[x-min y-min] [x-max y-max]]]
  (for [x (range x-min x-max)
        y (range y-min y-max)]
    [x y]))

(defn manhattan-distance [[x1 y1] [x2 y2]]
  (+ (Math/abs (- x2 x1))
     (Math/abs (- y2 y1))))

(defn find-closest [coords pt]
  (let [determine-winner (fn [[[idx a-dst] [_ b-dst] & _]]
                           (if (= a-dst b-dst) nil idx))]
    (->>
     (map #(manhattan-distance pt %) coords)
     (map-indexed vector) ;; give each coordinate an index
     (sort-by second)
     determine-winner)))

(defn map-values
  [f m]
  (into {} (map (fn [[k v]] [k (f v)]) m)))

(defn count-closest [coords]
  (->>
   (enumerate-fields (bounds coords))
   (pmap #(find-closest coords %))
   (filter identity)
   (group-by identity)
   (map-values count)
   (sort-by second)))

;; everything that is closest to the bounds is infinite.
(defn find-infinites [coords]
  (let [[[x-min y-min] [x-max y-max]] (bounds coords)]
    (->>
     (concat
      (for [x (range x-min x-max)]
        [x y-min])
      (for [x (range x-min x-max)]
        [x y-max])
      (for [y (range y-min y-max)]
        [x-min y])
      (for [y (range y-min y-max)]
        [x-max y]))
     (pmap #(find-closest coords %))
     (filter identity)
     set)))

(defn sum-distances [coords pt]
  (reduce + (map #(manhattan-distance pt %) coords)))

(defn size-of-safe-region [coords limit]
  (let [n (count coords)
        d (int (Math/ceil (/ limit n)))]
    (->>
     (expand-bounds d (bounds coords))
     enumerate-fields
     (pmap #(sum-distances coords %))
     (filter #(< % limit))
     count)))

(defn main
  "Advent of Code 2018 - Day 6"
  [& args]
  (let [coords (read-data)
        closest (count-closest coords)
        infinites (find-infinites coords)
        not-in-infinites #(not (contains? infinites (first %)))]
    (println (second (last (filter not-in-infinites closest)))
             (size-of-safe-region coords 10000))))
