(ns aoc2018.day14
  (require [clojure.java.io :as io]
           [clojure.string :as str]
           [clojure.test :as t]))

(def my-input 652601)

;; https://stackoverflow.com/a/29942388
(defn digits [n]
  (->> n
     (iterate #(quot % 10))
     (take-while pos?)
     (mapv #(mod % 10))
     rseq))

(defn recipe [[scores idx-a idx-b]]
  (let [a (nth scores idx-a)
        b (nth scores idx-b)
        scores (apply conj scores (digits (+ a b)))
        idx-a (mod (+ idx-a a 1) (count scores))
        idx-b (mod (+ idx-b b 1) (count scores))]
    [scores idx-a idx-b]))

(defn make-recipes []
  (iterate recipe [[3 7] 0 1]))

(defn ten-scores-after [n]
  (->>
   (make-recipes)
   (drop-while #(< (count (first %)) (+ n 10)))
   (first)
   (first)
   (drop n)
   (take 10)
   (apply str)))

(t/deftest test-ten-scores-after
  (t/is (= (ten-scores-after 9) "5158916779"))
  (t/is (= (ten-scores-after 5) "0124515891"))
  (t/is (= (ten-scores-after 18) "9251071085"))
  (t/is (= (ten-scores-after 2018) "5941429882")))

(defn main
  "Advent of Code 2018 - Day 14"
  [& args]
  (println (ten-scores-after my-input)))
