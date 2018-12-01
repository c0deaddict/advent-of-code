(ns aoc2018.day1_1
  (require [clojure.java.io :as io]
           [clojure.string :as s]))

(defn main
  "Advent of Code 2018 - Day 1 part 1"
  (let [data-file (io/resource "day1_1.txt")
        lines (s/split-lines (slurp data-file))
        frequencies (map #(Integer/parseInt %) lines)]
    (println (reduce + frequencies))))
