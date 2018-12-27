(ns aoc2018.day20
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.test :as t]
            [clojure.pprint :refer [pprint]]
            [aoc2018.utils :refer :all]
            [loom.graph]
            [loom.alg]
            [loom.alg-generic]))

(def data-file (io/resource "day20.txt"))

(defn read-data [] (slurp data-file))

(def test-data-1 "^ENWWW(NEEE|SSE(EE|N))$")

(def test-data-2 "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$")

(def is-dir? #{\N \E \S \W})

(defn parse [data] (rest (seq data)))

(defn move [[x y] dir]
  (case dir
    \N [x (dec y)]
    \E [(inc x) y]
    \S [x (inc y)]
    \W [(dec x) y]))

(defn walk [stream]
  (loop [[x & xs] stream
         pos [0 0]
         doors []
         stack []]
    (case x
      ;; there is a door in this direction of current pos.
      (\N \E \S \W)
      (let [next (move pos x)]
        (recur xs next (conj doors [pos next]) stack))
      ;; start a branch. follow the first one depth first.
      \(
      (recur xs pos doors (conj stack pos))
      ;; exit a branch.
      \)
      (if (empty? stack)
        (throw (Exception. "unexpected ')'"))
        (recur xs (peek stack) doors (pop stack)))
      ;; choice, set pos to top of stack.
      \|
      (if (empty? stack)
        (throw (Exception. "expected a '(' before '|'"))
        (recur xs (peek stack) doors stack))
      ;; the end.
      \$
      (do (assert (empty? stack) "not all '(' have been closed.")
          (set doors))
      nil (throw (Exception. "unexpected EOF"))
      :else (throw (Exception. "unexpected char")))))

(defn adj-list [doors]
  (->> doors
     (mapcat (fn [[a b]] [[a b] [b a]]))  ;; doors are symmetric
     (group-by first)
     (map (fn [[k kvs]] [k (vec (set (map second kvs)))]))
     (into {})))

(defn to-graph [doors]
  (loom.graph/graph (adj-list doors)))

(defn bounds [doors]
  (let [positions (mapcat identity doors)]
    [(min-max (map first positions))
     (min-max (map second positions))]))

(defn has-door? [doors pos dir]
  (let [other-pos (move pos dir)]
    (or (contains? doors [pos other-pos])
        (contains? doors [other-pos pos]))))

(defn print-doors [doors]
  (let [[[x-min x-max] [y-min y-max]] (bounds doors)
        x-range (range x-min (inc x-max))
        wall \#
        horz-door? #(if (has-door? doors % %2) \- wall)
        vert-door? #(if (has-door? doors % %2) \| wall)]
    (println (apply str "    " (map #(format "%2d" %) x-range)))
    (doseq [y (range y-min (inc y-max))]
      (print "    ")
      (doseq [x x-range]
        (print wall) ;; NW
        (print (horz-door? [x y] \N)))
      (println wall)
      (print (str (format "%3d" y) " "))
      (doseq [x x-range]
        (print (vert-door? [x y] \W))
        (print (if (= [0 0] [x y]) \X \.)))
      (println (vert-door? [x-max y] \E)))
    (print "    ")
    (doseq [x x-range]
      (print wall) ;; SW
      (print (horz-door? [x y-max] \S)))
    (println wall)))

(defn solve-part-1 [graph]
  (dec (count (loom.alg/longest-shortest-path graph [0 0]))))

(defn solve-part-2 [graph]
  (->> graph
     (loom.graph/nodes)
     (pmap #(loom.alg/shortest-path graph [0 0] %))
     (map count)
     (map dec)
     (filter #(>= % 1000))
     (count)))

(defn main
  "Advent of Code 2018 - Day 20"
  [& args]
  (let [stream (parse (read-data))
        doors (walk stream)
        graph (to-graph doors)]
    (println (solve-part-1 graph))
    (println (solve-part-2 graph))))
