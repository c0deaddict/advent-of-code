(ns aoc2018.day5
  (require [clojure.java.io :as io]
           [clojure.string :as str]
           [java-time :as time]
           [clojure.set]))

(def data-file (io/resource "day5.txt"))

(defn read-data []
  (-> (slurp data-file) str/trim seq))

(defn reactive? [x y]
  (and
   (= (str/lower-case x) (str/lower-case y))
   (not= x y)))

(defn compact [polymer]
  (loop [result []
         x (first polymer)
         y (second polymer)
         ys (rest (rest polymer))]
    (if (nil? x)
      nil
      (if (nil? y)
        (conj result x)
        (if (reactive? x y)
          (recur result (first ys) (second ys) (rest (rest ys)))
          (recur (conj result x) y (first ys) (rest ys)))))))

;; Liked this one: (iterate compact polymer) But couldn't find a nice
;; way to take from the infinite sequence until the length doesn't
;; increase anymore.
(defn full-compact [polymer]
  (loop [old-len (count polymer)
         compacted (compact polymer)]
    (let [new-len (count compacted)]
      (if (== old-len new-len)
        compacted
        (recur new-len (compact compacted))))))

(defn main
  "Advent of Code 2018 - Day 5"
  [& args]
  (let [polymer (read-data)]
    (println (count (full-compact polymer)))))
