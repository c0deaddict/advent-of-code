(ns aoc2018.day4
  (require [clojure.java.io :as io]
           [clojure.string :as str]
           [java-time :as time]
           [clojure.set]))

(defn parse-line
  [str]
  (let [regex #"^\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (?:Guard #(\d+) )?(.*)$"
        [_ year month day hour minute guard action] (re-matches regex str)]
    {:timestamp (time/local-date-time
                 (Integer. year)
                 (Integer. month)
                 (Integer. day)
                 (Integer. hour)
                 (Integer. minute))
     :guard (if (= nil guard) nil (Integer. guard))
     :action (case action
               "begins shift" :begin
               "falls asleep" :sleep
               "wakes up" :wakeup)}))

(def data-file (io/resource "day4.txt"))

(defn read-schedule []
  (map parse-line (sort (str/split-lines (slurp data-file)))))

(defn annotate-schedule [schedule]
  "Annotate the schedule with :guard and :elapsed"
  (first (reduce (fn [[result guard last-timestamp] rec]
                   (let [elapsed (if (not= nil last-timestamp)
                                   (time/as
                                    (time/duration last-timestamp (:timestamp rec))
                                    :minutes)
                                   nil)
                         next-acc (fn [rec]
                                    [(conj result (assoc rec :elapsed elapsed))
                                     (:guard rec)
                                     (:timestamp rec)])]
                     (if (= :begin (:action rec))
                       (next-acc rec)
                       (if (= nil guard)
                         (throw (AssertionError. "expected a begin shift"))
                         (next-acc (assoc rec :guard guard))))))
                 [[] nil nil] ; start with no current guard
                 schedule)))

(defn sleep-periods [annotated-schedule]
  "Extract the sleep periods from the annotated schedule"
  (let [init-guards (zipmap (set (map :guard annotated-schedule)) (repeat []))
        add-sleep (fn [res prev entry]
                    (update res (:guard prev) conj
                            {:start (:timestamp prev)
                             :elapsed (:elapsed entry)}))]
    (first (reduce (fn [[res prev awake] entry]
                     (case (:action entry)
                       :begin
                       (if (or (nil? prev) (not= (:action prev) :sleep))
                         ;; on with the next guard.
                         [res entry]
                         ;; previous guard was sleeping.
                         [(add-sleep res prev entry) entry])
                       :sleep
                       [res entry]
                       :wakeup
                       [(add-sleep res prev entry) entry]))
                   [init-guards nil true]
                   annotated-schedule))))

(defn sum-elapsed [periods]
  (reduce + (map :elapsed periods)))

(defn find-biggest-sleeper [sleep-periods]
  (apply max-key (comp sum-elapsed val) sleep-periods))

(defn sleep-minutes [periods]
  (for [{:keys [start elapsed]} periods]
    (let [start-min (time/as start :minute-of-hour)
          end-min (+ start-min elapsed)]
      (into [] (range start-min end-min)))))

(defn map-values
  [f m]
  (into {} (map (fn [[k v]] [k (f v)]) m)))

(defn group-minutes [minutes]
  (sort-by second (map-values count (group-by identity (apply concat minutes)))))

(defn find-sleepiest-minute [minutes]
  (first (last (group-minutes minutes))))


;; Strategy 1: Find the guard that has the most minutes asleep.
;;             What minute does that guard spend asleep the most?
(defn strategy-1 [periods]
  (let [g (find-biggest-sleeper periods)
        m (find-sleepiest-minute (sleep-minutes (val g)))]
    (* (key g) m)))


;; Strategy 2: Of all guards, which guard is most frequently asleep on
;; the same minute?
(defn strategy-2 [periods]
  "Returns [guard-id [sleepiest-minute frequency]]"
  ;; aggregate sleeping minutes and take the most frequent one (last).
  (let [sleepiest-minutes (map-values
                           (comp last group-minutes sleep-minutes)
                           periods)
        [guard [minute frequency]]
        (last (sort-by #(second (second %))
                       ;; filter out guards that haven't slept (nil).
                       (filter second sleepiest-minutes)))]
    (* guard minute)))

(defn main
  "Advent of Code 2018 - Day 4"
  [& args]
  (let [schedule (annotate-schedule (read-schedule))
        periods (sleep-periods schedule)]
    (println (strategy-1 periods))
    (println (strategy-2 periods))))
