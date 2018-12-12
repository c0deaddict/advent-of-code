(ns aoc2018.day11
  (require [clojure.java.io :as io]
           [clojure.string :as str]
           [clojure.test :as t]))

(def my-grid-serial 9995)
(def grid-size 300)

(defn power-level [x y serial]
  (let [rack-id (+ x 10)
        level (* rack-id y)
        level (+ level serial)
        level (* level rack-id)
        level (mod (quot level 100) 10)
        level (- level 5)]
    level))

(t/deftest test-power-levels
  (t/is (= (power-level 3 5 8) 4))
  (t/is (= (power-level 122 79 57) -5))
  (t/is (= (power-level 217 196 39) 0))
  (t/is (= (power-level 101 153 71) 4)))

(defn region [x y size]
  (for [x (range x (+ x size))
        y (range y (+ y size))]
    [x y]))

(defn grid-cells [serial]
  (into {} (map
            (fn [[x y]]
              [[x y] (power-level x y serial)])
            (region 0 0 grid-size))))

(defn sum-region [cells region]
  (reduce + (map #(get cells %) region)))

(defn grid-squares [cells size]
  (for [x (range 0 (- (inc grid-size) size))
        y (range 0 (- (inc grid-size) size))]
    [[x y] ;; top-left coordinate
     (sum-region cells (region x y size))]))

(defn region-inc [x y size]
  (concat
   (for [x (range x (+ x size))]
     [x (+ y (dec size))])
   (for [y (range y (+ y (dec size)))]
     [(+ x (dec size)) y])))

(defn grid-squares-inc [cells prev size]
  (pmap (fn [[x y]]
          [[x y] ;; top-left coordinate
           (+ (get prev [x y])
              (sum-region cells (region-inc x y size)))])
        (region 0 0 (- (inc grid-size) size))))

(defn map-keys [f coll]
  (map (fn [[k v]] [(f k) v]) coll))

(defn find-best-grid-square [cells size-up-to]
  (first
   (reduce
    (fn [[best prev] size]
      (let [next (grid-squares-inc cells prev size)
            next-best (last (sort-by second next))]
        ;; (println size)
        [(if (or (nil? best)
                 (> (second next-best) (second best)))
           (conj next-best size)
           best)
         (into {} next)]))
    [nil cells]
    (range 2 (inc size-up-to)))))

(defn solve-part-1 [cells]
  (let [squares (grid-squares cells 3)
        [[x y] _] (last (sort-by second squares))]
    (println (str x "," y))))

(defn solve-part-2 [cells]
  (let [[[x y] _ size] (find-best-grid-square cells grid-size)]
    (println (str x "," y "," size))))

(defn main
  "Advent of Code 2018 - Day 11"
  [& args]
  (let [cells (grid-cells my-grid-serial)]
    (solve-part-1 cells)
    (solve-part-2 cells)))
