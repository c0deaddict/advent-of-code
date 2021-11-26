(ns aoc2018.utils
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.test :as t]
            [clojure.pprint :refer [pprint]]))

(defn to-int [s] (Integer. s))

(defn dup [x] [x x])

(defn swp [[x y]] [y x])

(defn map-values [f m]
  (map (fn [[k v]] [k (f v)]) m))

(defn pmap-values [f m]
  (pmap (fn [[k v]] [k (f v)]) m))

(defn map-flatten [m]
  (apply concat
         (map (fn [[k v]]
                (map (fn [v'] [k v']) v))
              m)))

(defn map-first [f m]
  (map (fn [[k v]] [(f k) v]) m))

(defn min-max [coll]
  [(reduce min coll)
   (reduce max coll)])

(defn exp [x n]
  (reduce * (repeat n x)))

(defn nth-digit [idx num]
  (mod (quot num (exp 10 idx)) 10))
