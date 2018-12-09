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

(defn pick-step [steps]
  (->>
   steps
   (filter (comp empty? second))
   (map first)
   sort
   first))

(defn determine-order [steps]
  (loop [result []
         remaining-steps steps]
    (if (empty? remaining-steps)
      (apply str result)
      (let [step (pick-step remaining-steps)]
        (if (nil? step)
          (throw (Exception. "Stuck."))
          (recur (conj result step)
                 (complete-step remaining-steps step)))))))

(defn step-runtime [step penalty]
  (+ (- (int step) (int \A)) 1 penalty))

(defn split-on [f coll]
  (let [{t true f false} (group-by f coll)]
    [t f]))

(defn compute-time [steps workers penalty]
  (loop [time 0
         remaining-steps steps
         free-workers workers
         running-jobs {}]
    (if (and (empty? remaining-steps) (empty? running-jobs))
      time
      (let [step (pick-step remaining-steps)]
        ;; is a worker available and is there work to be done?
        (if (and (pos? free-workers) (not (nil? step)))
          ;; start working on it.
          (recur time
                 (dissoc remaining-steps step)
                 (dec free-workers)
                 (assoc running-jobs step
                        (step-runtime step penalty)))
          ;; decrease time in all jobs.
          ;; complete all jobs that reached zero.
          (let [tick (map-values dec running-jobs)
                [done remaining-jobs] (split-on (comp zero? second) tick)]
            (recur (inc time)
                   (reduce complete-step remaining-steps
                           (map first done))
                   (+ free-workers (count done))
                   (into {} remaining-jobs))))))))

(defn main
  "Advent of Code 2018 - Day 7"
  [& args]
  (let [steps (parse (read-data))]
    (println (determine-order steps)
             (compute-time steps 5 60))))
