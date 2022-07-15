(ns aoc2018.day2
  (:require [clojure.java.io :as io]
            [clojure.string :as s]
            [clojure.test :refer [deftest is testing]]))

(defn parse [data]
  (s/split data #"\s+"))

(defn part1 [input]
  (reduce *
          (reduce
           (fn [acc box]
             (let [freqs (clojure.set/map-invert (frequencies (seq box)))]
               (map #(if (freqs %1) (+ 1 %2) %2) [2 3] acc)))
           [0 0]
           input)))

(defn compare-ids
  "Compare ids `a` and `b` returning the letters that match."
  [a b]
  (apply str
         (map first
              (filter #(apply = %)
                      (map vector (seq a) (seq b))))))


(defn cart [colls]
  (if (empty? colls)
    '(())
    (for [x (first colls)
          more (cart (rest colls))]
      (cons x more))))

(defn find-first
  [f coll]
  (first (filter f coll)))

(defn is-prototype
  [[a b]]
  (=
   (- (count a) 1)
   (count (compare-ids a b))))

(defn part2 [input]
  (let [cart-ids (cart (list input input))
        [a b] (find-first is-prototype cart-ids)]
    (compare-ids a b)))

(defn main
  "Advent of Code 2018 - Day 2"
  [& args]
  (let [data-file (io/resource "day2.txt")
        input (parse (slurp data-file))]
    (println "Part 1:" (part1 input))
    (println "Part 2:" (part2 input))))

(deftest test-part1
  (let [data "abcdef bababc abbcde abcccd aabcdd abcdee ababab"]
    (is (= (part1 (parse data)) 12))))

(deftest test-part2
  (let [data "abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz"]
    (is (= (part2 (parse data)) "fgij"))))
