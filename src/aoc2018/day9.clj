(ns aoc2018.day9
  (require [clojure.java.io :as io]
           [clojure.string :as str]
           [clojure.set]
           [clojure.pprint :refer [pprint]]
           [clojure.test :as t]))

(definterface INode
  (getPrev [])
  (setPrev [v])
  (getNext [])
  (setNext [v]))

(deftype Node [data
               ^{:volatile-mutable true} prev
               ^{:volatile-mutable true} next]
  INode
  (getPrev [_] prev)
  (setPrev [this v] (set! prev v))
  (getNext [_] next)
  (setNext [this v] (set! next v)))

(defn new-circle []
  (let [head (Node. nil nil 0)]
    (.setPrev head head)
    (.setNext head head)
    head))

(defn move-left [head n]
  (nth (iterate #(.getPrev %) head)) n)

(defn move-right [head n]
  (nth (iterate #(.getNext %) head)) n)

(defn insert-node [head data]
  (let [next (.getNext head)
        node (Node. data head next)]
    (.setNext head node)
    (.setPrev next node)
    node))

;; https://stackoverflow.com/a/24553906/248948
(defn drop-nth [n coll]
  (keep-indexed #(if (not= %1 n) %2) coll))

;; https://stackoverflow.com/a/26442057/248948
(defn insert-at [coll idx val]
  (let [[before after] (split-at idx coll)]
    (vec (concat before [val] after))))

(defn clockwise [circle current shift]
  (mod (+ current shift) (count circle)))

(defn do-move [circle current marble]
  (if (zero? (mod marble 23))
    ;; multiple of 23
    (let [extract (clockwise circle current -7)
          points (nth circle extract)
          circle (into [] (drop-nth extract circle))
          current (clockwise circle extract 0)]
      [circle current (+ marble points)])
    ;; normal flow
    (let [current (clockwise circle current 2)
          circle (insert-at circle current marble)]
      [circle current 0])))

(defn run-game [num-players num-marbles]
  (loop [circle [0]
         current 0
         marble 1
         scores (zipmap (range num-players) (repeat 0))
         turns (cycle (range num-players))]
    (if (> marble num-marbles)
      scores
      (let [player (first turns)
            [circle current points] (do-move circle current marble)]
        ;; (println player circle current)
        (recur circle
               current
               (inc marble)
               (update scores player #(+ % points))
               (rest turns))))))

(defn high-score [scores]
  (last (sort (map second scores))))

(t/deftest test-high-scores
  (t/is (= 32 (high-score (run-game 9 25))))
  (t/is (= 8317 (high-score (run-game 10 1618))))
  (t/is (= 146373 (high-score (run-game 13 7999))))
  (t/is (= 2764 (high-score (run-game 17 1104))))
  (t/is (= 54718 (high-score (run-game 21 6111))))
  (t/is (= 37305 (high-score (run-game 30 5807)))))

(defn main
  "Advent of Code 2018 - Day 9"
  [& args]
  (println (high-score (run-game 429 70901))))
