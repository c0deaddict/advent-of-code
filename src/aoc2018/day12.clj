(ns aoc2018.day12
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.test :as t]))

(def data-file (io/resource "day12.txt"))

(defn read-data []
  (let [lines (str/split-lines (slurp data-file))
        [_ initial-state] (str/split (first lines) #"initial state: ")
        rule-lines (rest (rest lines))]
    [initial-state rule-lines]))

(def char-to-plant {\. false \# true})

(defn parse-rule [line]
  (let [[_ pattern outcome] (re-matches #"([\.#]+) => ([\.#])" line)]
    [(map char-to-plant pattern)
     (char-to-plant (first (seq outcome)))]))

(defn parse [[initial-state rule-lines]]
  {:initial (map vector
                 (range)
                 (map char-to-plant initial-state))
   :rules (map parse-rule rule-lines)})

(defn make-partitions [state]
  (let [state-map (into {} state)
        [first-pot _] (first state)
        [last-pot _] (last state)
        start (- first-pot 2)
        end (+ last-pot 2)]
    (for [pot (range start (inc end))]
      [pot (map #(get state-map % false)
                (range (- pot 2) (+ pot 3)))])))

(defn rule-matches? [partition [pattern _]]
  (every? true? (map = partition pattern)))

(defn match-rules [partition rules]
  (->>
   rules
   (filter #(rule-matches? partition %))
   (first)
   (second)))

(defn trim-ends [state]
  (let [drop-empties #(drop-while (comp not second) %)]
    (->
     (sort-by first state)
     (drop-empties)
     (reverse)
     (drop-empties)
     (reverse))))

(defn next-partition [[pot partition] rules]
  (let [outcome (match-rules partition rules)]
    [pot (if (nil? outcome)   ;; no rules have matched
           (nth partition 2)  ;; keep current value
           outcome)]))

(defn next-generation [state rules]
  (->>
   (make-partitions state)
   (map #(next-partition % rules))
   (trim-ends)))

(defn iterate-generations [{:keys [initial rules]}]
  (iterate #(next-generation % rules) initial))

(defn render-state [state]
  (->>
   (sort-by first state)
   (map second)
   (map {false \. true \#})
   (apply str)))

(defn find-cycle [generations]
  (loop [visited {}
         iter generations
         count 0]
    (let [state (first iter)
          start-pot (first (first state))
          state-str (render-state state)]
      (if (contains? visited state-str)
        (let [[prev-count prev-pot] (get visited state-str)]
          [prev-count
           (- count prev-count)
           (- start-pot prev-pot)])
        (recur (assoc visited state-str [count start-pot])
               (rest iter)
               (inc count))))))

(defn solve-part-1 [generations]
  (let [gen-20 (nth generations 20)
        with-plants (filter second gen-20)]
    (println (reduce + (map first with-plants)))))

(defn solve-part-2 [generations]
  (let [num 50000000000
        [cycle-start cycle-time pot-shift] (find-cycle generations)
        num (- num cycle-start)
        pot-shift (* pot-shift (quot num cycle-time))
        relative-pot (+ cycle-start (mod num cycle-time))
        state (nth generations relative-pot)
        with-plants (filter second state)
        pots (map #(+ pot-shift %) (map first with-plants))]
    (println (reduce + pots))))

(defn main
  "Advent of Code 2018 - Day 12"
  [& args]
  (let [game (parse (read-data))
        generations (iterate-generations game)]
    (solve-part-1 generations)
    (solve-part-2 generations)))
