(ns aoc2018.day3
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.set]))

(defn parse-claim
  [str]
  (let [regex #"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)"
        [_ claim-id left top width height] (re-matches regex str)]
    {:id (Integer. claim-id)
     :left (Integer. left)
     :top (Integer. top)
     :width (Integer. width)
     :height (Integer. height)}))

(defn make-claim
  [area-map claim]
  (let [left (:left claim)
        top (:top claim)
        right (+ left (:width claim))
        bottom (+ top (:height claim))]
    (into {} (reduce #(merge-with concat %1 %2)
                     area-map
                     (for [x (range left right)
                           y (range top bottom)]
                       {(list x y) [(:id claim)]})))))

(def data-file (io/resource "day3.txt"))

(defn read-claims []
  (map parse-claim (str/split-lines (slurp data-file))))

(defn make-area-map [claims]
  (reduce make-claim {} claims))

(defn overlapping [area-map]
  (filter #(> (count %) 1) (vals area-map)))

(defn count-overlaps [area-map]
  "Number of square inches that have more than one claim"
  (count (overlapping area-map)))

(defn find-claim-without-overlap [area-map claims]
  "ID of the claim that has no overlap at all"
  (let [claims-with-overlap (set (apply concat (overlapping area-map)))
        all-claims (set (map :id claims))]
    (clojure.set/difference all-claims claims-with-overlap)))

(defn main
  "Advent of Code 2018 - Day 3 (part 1 and 2)"
  [& args]
  (let [claims (read-claims)
        area-map (make-area-map claims)]
    (println
     (count-overlaps area-map)
     (find-claim-without-overlap area-map claims))))
