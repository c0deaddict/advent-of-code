(ns aoc2018.day2_1
  (:require [clojure.java.io :as io]
            [clojure.string :as s]))


;; https://stackoverflow.com/a/1677927/248948
(defn letter-counts
  [str]
  (let [grouped (group-by identity (seq str))]
    (into {} (for [[k v] grouped] [k (count v)]))))


(defn main
  "Advent of Code 2018 - Day 2 part 1"
  [& args]
  (let [data-file (io/resource "day2.txt")
        boxes-ids (s/split-lines (slurp data-file))
        boxes-counts (map letter-counts boxes-ids)
        count-two (count (filter #(contains? (set (vals %)) 2) boxes-counts))
        count-three (count (filter #(contains? (set (vals %)) 3) boxes-counts))]
    (println (str (* count-two count-three)))))
