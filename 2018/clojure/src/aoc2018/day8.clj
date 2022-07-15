(ns aoc2018.day8
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.set]
            [clojure.pprint :refer [pprint]]))

(def data-file (io/resource "day8.txt"))

(defn read-data []
  (let [to-ints (fn [coll] (map #(Integer. %) coll))]
    (->
     (slurp data-file)
     (str/trim)
     (str/split #" ")
     (to-ints))))

(def test-data
  [2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2])

(defn parse [data]
  "Returns [tree data]"
  (let [[num-children num-metadata & data] data
        [children data] (nth (iterate
                              (fn [[result data]]
                                (let [[child data] (parse data)]
                                  [(conj result child) data]))
                              [[] data])
                             num-children)
        [metadata data] (split-at num-metadata data)]
    [[metadata children] data]))

(defn parse-root [data]
  (let [[tree data] (parse data)]
    (if (not (empty? data))
      (throw (Exception. "Data not fully parsed."))
      tree)))

(defn sum-metadata [tree]
  (let [[metadata children] tree
        own-sum (reduce + metadata)
        children-sum (reduce + (map sum-metadata children))]
    (+ own-sum children-sum)))

(defn node-value [node]
  (let [[metadata children] node]
    (if (empty? children)
      ;; no children: sum of metadata
      (reduce + metadata)
      ;; metadata are indices into childnodes.
      ;; indices that don't exist count as 0.
      (let [children-values (map node-value children)
            safe-indices (filter #(<= 1 % (count children)) metadata)
            get-child #(nth children-values (dec %))]
        (reduce + (map get-child safe-indices))))))

(defn main
  "Advent of Code 2018 - Day 8"
  [& args]
  (let [tree (parse-root (read-data))]
    (println (sum-metadata tree)
             (node-value tree))))
