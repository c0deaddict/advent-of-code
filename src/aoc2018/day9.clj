(ns aoc2018.day9
  (require [clojure.java.io :as io]
           [clojure.string :as str]
           [clojure.set]
           [clojure.pprint :refer [pprint]]))

;; https://stackoverflow.com/a/24553906/248948
(defn drop-nth [n coll]
  (keep-indexed #(if (not= %1 n) %2) coll))

;; https://stackoverflow.com/a/26442057/248948
(defn insert-at [coll idx val]
  (let [[before after] (split-at idx coll)]
    (vec (concat before [val] after))))

(defn clockwise [circle current shift]
  (mod (+ current shift) (count circle)))

(defn do-move [circle current marble]
  (if (zero? (mod marble 23))
    ;; multiple of 23
    (let [extract (clockwise circle current -7)
          score (nth circle extract)
          circle (drop-nth extract circle)
          current (clockwise circle current -6)]
      [circle current (+ marble score)])
    ;; normal flow
    (let [current (clockwise circle current 2)
          circle (insert-at circle current marble)]
      [circle current 0])))

(defn high-score [num-players num-marbles]
  nil)

(defn main
  "Advent of Code 2018 - Day 9"
  [& args]
  (println nil))
