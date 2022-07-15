(ns aoc2018.day9
  (:require [clojure.java.io :as io]
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
  (let [head (Node. 0 nil nil)]
    (.setPrev head head)
    (.setNext head head)
    head))

(defn move-left [head n]
  (nth (iterate #(.getPrev %) head) n))

(defn move-right [head n]
  (nth (iterate #(.getNext %) head) n))

(defn insert-node [head data]
  (let [next (.getNext head)
        node (Node. data head next)]
    (.setNext head node)
    (.setPrev next node)
    node))

(defn remove-current [head]
  (let [next (.getNext head)
        prev (.getPrev head)]
    (.setNext prev next)
    (.setPrev next prev)
    [next (.-data head)]))

(defn circle-seq [head]
  (loop [result [(.-data head)]
         node (.getNext head)]
    (if (= node head)
      result
      (recur (conj result (.-data node))
             (.getNext node)))))

(defn do-move [circle marble]
  (if (zero? (mod marble 23))
    ;; multiple of 23
    (let [circle (move-left circle 7)
          [circle points] (remove-current circle)]
      [circle (+ marble points)])
    ;; normal flow
    (let [circle (move-right circle 1)
          circle (insert-node circle marble)]
      [circle 0])))

(defn run-game [num-players num-marbles]
  (loop [circle (new-circle)
         marble 1
         scores (zipmap (range num-players) (repeat 0))
         turns (cycle (range num-players))]
    (if (> marble num-marbles)
      scores
      (let [player (first turns)
            [circle points] (do-move circle marble)]
        ;; (println player (circle-seq circle))
        (recur circle
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
  (println (high-score (run-game 429 70901))
           (high-score (run-game 429 (* 100 70901)))))
