(ns aoc2018.day14
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.test :as t]))

(def my-input 652601)

;; https://stackoverflow.com/a/29942388/248948
(defn digits [n]
  (if (zero? n)
    [0]
    (->> n
       (iterate #(quot % 10))
       (take-while pos?)
       (mapv #(mod % 10))
       rseq)))

(defn recipe [[scores idx-a idx-b]]
  (let [scores (last scores)
        a (nth scores idx-a)
        b (nth scores idx-b)
        sum (+ a b)
        d0 (mod sum 10)
        d1 (quot sum 10)
        make-result (fn [scores cnt]
                      (let [idx-a (mod (+ idx-a a 1) cnt)
                            idx-b (mod (+ idx-b b 1) cnt)]
                        [scores idx-a idx-b]))]
    (if (zero? d1)
      (make-result [(conj scores d0)]
                   (inc (count scores)))
      (make-result [(conj scores d1) (conj scores d1 d0)]
                   (inc (inc (count scores)))))))

(defn make-recipes []
  (iterate recipe [[[] [3] [3 7]] 1 0]))

(defn ten-scores-after [n]
  (->>
   (make-recipes)
   (map first)   ;; only scores
   (map last)    ;; only last score
   (drop-while #(< (count %) (+ n 10)))
   (first)
   (drop n)
   (take 10)
   (apply str)))

(t/deftest test-ten-scores-after
  (t/is (= (ten-scores-after 9) "5158916779"))
  (t/is (= (ten-scores-after 5) "0124515891"))
  (t/is (= (ten-scores-after 18) "9251071085"))
  (t/is (= (ten-scores-after 2018) "5941429882")))

(defn ends-with? [pattern scores]
  (let [start (- (count scores) (count pattern))]
    (if (neg? start)
      false
      (= pattern (subvec scores start)))))

(defn score-stream []
  (->>
   (make-recipes)
   (map first)
   (apply concat)))

(defn count-recipes-before [pattern]
  (- (->>
      (score-stream)
      (map (partial ends-with? pattern))
      (take-while false?)
      (count))
     (count pattern)))

(t/deftest test-count-recipes-before
  (t/is (= (count-recipes-before (digits 51589)) 9))
  (t/is (= (count-recipes-before [0 1 2 4 5]) 5))
  (t/is (= (count-recipes-before (digits 92510)) 18))
  (t/is (= (count-recipes-before (digits 59414)) 2018)))

(defn main
  "Advent of Code 2018 - Day 14"
  [& args]
  (println (ten-scores-after my-input))
  (println (count-recipes-before (digits my-input))))
