(ns aoc2018.day10
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.set]
            [clojure.pprint :refer [pprint]]
            [clojure.test :as t]))

(def data-file (io/resource "day10.txt"))

(defn read-data []
  (slurp data-file))

(def test-data
"position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>")

(defn parse-line [line]
  (let [regex #"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>"
        [_ x y vx vy] (re-matches regex line)
        to-int #(Integer. (str/trim %))]
    [[(to-int x) (to-int y)]
     [(to-int vx) (to-int vy)]]))

(defn parse [data]
  (map parse-line (str/split-lines data)))

(defn at-time [init-state time]
  (set (for [[[x y] [vx vy]] init-state]
         [(+ x (* vx time)) (+ y (* vy time))])))

(defn min-max [coll]
  [(reduce min coll)
   (reduce max coll)])

(defn bounds [points]
  (let [[x-min x-max] (min-max (map first points))
        [y-min y-max] (min-max (map second points))]
    [[x-min y-min]
     [(+ 1 x-max) (+ 1 y-max)]]))

(defn dim [[[x-min y-min] [x-max y-max]]]
  [(- x-max x-min) (- y-max y-min)])

(defn area [[width height]]
  (* width height))

(defn gcd [a b]
  (if (zero? b)
    a
    (recur b (mod a b))))

(defn make-picture [points]
  (let [[[x-min y-min] [x-max y-max]] (bounds points)]
    (for [y (range y-min y-max)]
      (map #(contains? points [% y])
           (range x-min x-max)))))

(defn render [picture]
  (let [to-char #(if % "#" " ")
        to-row #(apply str (map to-char %))]
    (str/join "\n" (map to-row picture))))

(defn compare-zip-with-index [coll]
  (map vector (range) coll (rest coll)))

(defn find-smallest-area [init-state]
  (let [pictures (map #(at-time init-state %) (range))
        lazy-area (map (comp area dim bounds) pictures)]
    (->>
     (compare-zip-with-index lazy-area)
     (drop-while (fn [[_ a b]] (> a b)))
     (first)
     (first))))

(defn solve-part-1 [init-state]
  (let [t (find-smallest-area init-state)]
    (println t)
    (->
     (at-time init-state t)
     (make-picture)
     (render)
     (print))))

(defn main
  "Advent of Code 2018 - Day 10"
  [& args]
  (let [init-state (parse (read-data))]
    (solve-part-1 init-state)))
