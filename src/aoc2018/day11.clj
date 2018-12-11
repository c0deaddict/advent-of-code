(ns aoc2018.day11
  (require [clojure.java.io :as io]
           [clojure.string :as str]
           [clojure.test :as t]))

(def my-grid-serial 9995)

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

(defn grid-cells [serial]
  (into {}
        (for [x (range 0 300)
              y (range 0 300)]
          [[x y] (power-level x y serial)])))

(defn grid-3x3-squares [cells]
  (let [get-cell-power #(get cells %)
        sum-region #(reduce + (map get-cell-power %))]
    (for [x (range 0 298)
          y (range 0 298)]
      [[x y] ;; top-left coordinate
       (sum-region [[x y]
                    [(+ 1 x) y]
                    [(+ 2 x) y]
                    [x (+ 1 y)]
                    [(+ 1 x) (+ 1 y)]
                    [(+ 2 x) (+ 1 y)]
                    [x (+ 2 y)]
                    [(+ 1 x) (+ 2 y)]
                    [(+ 2 x) (+ 2 y)]])
       ])))

(defn main
  "Advent of Code 2018 - Day 11"
  [& args]
  (let [cells (grid-cells my-grid-serial)
        squares (grid-3x3-squares cells)
        [[x y] _] (last (sort-by second squares))]
    (println (str x "," y))))
