(ns aoc2018.day1
  (:require [clojure.java.io :as io]
            [clojure.string :as s]
            [clojure.test :refer [deftest is testing]]))

(defn parse [data]
  (map #(Integer/parseInt %)
       (s/split data #",?\s+")))

(defn part1 [input]
  (reduce + input))

(defn part2 [input]
  "Add up the frequences, stop when a value is encountered for the second time"
  (reduce
   (fn [[sum freq-set] freq]
     (let [new-sum (+ sum freq)]
       (if (contains? freq-set new-sum)
         (reduced new-sum)
         [new-sum (conj freq-set new-sum)])))
   [0 #{0}]
   (cycle input)))

(defn main [& args]
  "Advent of Code 2018 - Day 1"
  (let [data-file (io/resource "day1.txt")
        input (parse (slurp data-file))]
    (println "Part 1:" (part1 input))
    (println "Part 2:" (part2 input))))

(deftest test-part1
  (testing "example1"
    (is (= (part1 (parse "+1, +1, +1")) 3)))
  (testing "example1"
    (is (= (part1 (parse "+1, +1, -2")) 0)))
  (testing "example2"
    (is (= (part1 (parse "-1, -2, -3")) -6))))

(deftest test-part2
  (testing "example1"
    (is (= (part2 (parse "+1, -1")) 0)))
  (testing "example2"
    (is (= (part2 (parse "+3, +3, +4, -2, -4")) 10)))
  (testing "example3"
    (is (= (part2 (parse "-6, +3, +8, +5, -6")) 5)))
  (testing "example4"
    (is (= (part2 (parse "+7, +7, -2, -7, -4")) 14))))
