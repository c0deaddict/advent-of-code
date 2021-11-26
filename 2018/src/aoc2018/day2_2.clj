(ns aoc2018.day2_2
  (:require [clojure.java.io :as io]
            [clojure.string :as s]))

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

(defn main
  "Advent of Code 2018 - Day 2 part 2"
  [& args]
  (let [data-file (io/resource "day2.txt")
        boxes-ids (s/split-lines (slurp data-file))
        cart-ids (cart (list boxes-ids boxes-ids))
        [a b] (find-first is-prototype cart-ids)]
    (println (compare-ids a b))))
