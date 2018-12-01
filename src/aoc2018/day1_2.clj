(ns aoc2018.day1_2
  (require [clojure.java.io :as io]
           [clojure.string :as s]))


(defn find-double
  "Add up the frequences, stop when a value is encountered for the
  second time"
  [[sum freq-set] f]
  (let [new-sum (+ sum f)]
    (if (contains? freq-set new-sum)
      (reduced new-sum)
      [new-sum (conj freq-set new-sum)])))

(defn main
  "Advent of Code 2018 - Day 1 part 2"
  [& args]
  (let [data-file (io/resource "day1_1.txt")
        lines (s/split-lines (slurp data-file))
        frequencies (map #(Integer/parseInt %) lines)]
    (println (reduce find-double [0 #{}] (cycle frequencies)))))
