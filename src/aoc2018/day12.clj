(ns aoc2018.day12
  (require [clojure.java.io :as io]
           [clojure.string :as str]
           [clojure.test :as t]))

(def data-file (io/resource "day12.txt"))

(defn read-data []
  (let [lines (str/split-lines (slurp data-file))
        [_ initial-state] (str/split (first lines) #"initial state: ")
        rule-lines (rest (rest lines))]
    [initial-state rule-lines]))

(def test-data
  ["#..#.#..##......###...###"
   ["...## => #"
    "..#.. => #"
    ".#... => #"
    ".#.#. => #"
    ".#.## => #"
    ".##.. => #"
    ".#### => #"
    "#.#.# => #"
    "#.### => #"
    "##.#. => #"
    "##.## => #"
    "###.. => #"
    "###.# => #"
    "####. => #"]])

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
  (for [[pot val] state]
    [pot (map #(get state % false)
              (range (- pot 2) (+ pot 3)))]))

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
   (map #(if % \# \.))
   (apply str)))

(defn main
  "Advent of Code 2018 - Day 12"
  [& args]
  (println nil))
