(ns aoc2018.day7
  (require [clojure.java.io :as io]
           [clojure.string :as str]
           [clojure.set]
           [clojure.pprint :refer [pprint]]))

(def data-file (io/resource "day7.txt"))

(defn map-values
  [f m]
  (into {} (map (fn [[k v]] [k (f v)]) m)))

(defn parse-step [str]
  (let [regex #"^Step ([A-Z]) must be finished before step ([A-Z]) can begin\.$"
        [_ dependency step] (map (comp first seq) (re-matches regex str))]
    [step dependency]))

(defn read-data []
  (slurp data-file))

(defn add-initial-steps [steps]
  "Add all initial steps (steps that don't have a dependency)"
  (let [alphabet (set (apply concat (map second steps)))
        initial (clojure.set/difference alphabet (keys steps))]
    (merge steps (zipmap initial (repeat nil)))))

;; {step [dep1 dep2 ...]}
(defn parse [data]
  (->>
   data
   str/split-lines
   (map parse-step)
   (group-by first)
   (map-values #(map second %))
   add-initial-steps))

(def test-data
"Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.")

(defn complete-step [steps x]
  (map-values (fn [deps] (filter #(not= x %) deps))
              (dissoc steps x)))

(defn determine-order [steps]
  (loop [result []
         remaining-steps steps]
    (if (empty? remaining-steps)
      (apply str result)
      (let [choices (filter (comp empty? second) remaining-steps)
            step (first (sort (map first choices)))]
        (if (nil? step)
          (throw (Exception. "Stuck."))
          (recur (conj result step)
                 (complete-step remaining-steps step)))))))

(defn main
  "Advent of Code 2018 - Day 7"
  [& args]
  (let [steps (parse (read-data))]
    (println (determine-order steps))))
