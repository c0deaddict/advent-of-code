(ns aoc2018.day16
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.test :as t]
            [clojure.pprint :refer [pprint]]
            [aoc2018.utils :refer :all]
            [rolling-stones.core :as sat]))

(def data-file (io/resource "day16.txt"))

(defn read-data [] (slurp data-file))

(defn parse-sample [[before instr after]]
  (let [[_ before ] (re-matches #"Before:\s*\[([^\]]+)\]" before)
        [_ after] (re-matches #"After:\s*\[([^\]]+)\]" after)
        before (vec (map to-int (str/split before #",\s*")))
        after (vec (map to-int (str/split after #",\s*")))
        instr (map to-int (str/split instr #"\s+"))]
    [before instr after]))

(defn parse [data]
  (->> data
     (str/split-lines)
     (remove empty?)
     (partition 3)
     (map parse-sample)))

(def prog-file (io/resource "day16_2.txt"))

(defn read-prog [] (slurp prog-file))

(defn parse-prog [data]
  (->> data
     (str/split-lines)
     (map #(str/split % #"\s+"))
     (map #(map to-int %))))

(defn opcodes [reg-file]
  (let [st (fn [i v] (assoc reg-file i v))
        stb (fn [i b] (st i (if b 1 0)))
        ld (fn [i] (nth reg-file i))]
    {:addr (fn [a b c] (st c (+ (ld a) (ld b))))
     :addi (fn [a b c] (st c (+ (ld a) b)))
     :mulr (fn [a b c] (st c (* (ld a) (ld b))))
     :muli (fn [a b c] (st c (* (ld a) b)))
     :banr (fn [a b c] (st c (bit-and (ld a) (ld b))))
     :bani (fn [a b c] (st c (bit-and (ld a) b)))
     :borr (fn [a b c] (st c (bit-or (ld a) (ld b))))
     :bori (fn [a b c] (st c (bit-or (ld a) b)))
     :setr (fn [a _ c] (st c (ld a)))
     :seti (fn [a _ c] (st c a))
     :gtir (fn [a b c] (stb c (> a (ld b))))
     :gtri (fn [a b c] (stb c (> (ld a) b)))
     :gtrr (fn [a b c] (stb c (> (ld a) (ld b))))
     :eqir (fn [a b c] (stb c (= a (ld b))))
     :eqri (fn [a b c] (stb c (= (ld a) b)))
     :eqrr (fn [a b c] (stb c (= (ld a) (ld b))))
     }))

(def all-opcodes (keys (opcodes [])))

(defn exec-instr [op args reg-file]
  (apply ((opcodes reg-file) op) args))

(defn match-opcodes [[before instr after]]
  (->> all-opcodes
     (map (fn [op]
            (if (= after (exec-instr op (rest instr) before))
              [op (first instr)]
              nil)))
     (remove nil?)))

(defn solve-part-1 [samples]
  (->> samples
     (map match-opcodes)
     (map count)
     (filter #(>= % 3))
     (count)))

(defn opcode-constraint [[op idx]]
  (->>
   (range (count all-opcodes))
   (remove #{idx})
   (map #(sat/! [op %]))
   (cons [op idx])
   (apply sat/AND)))

(defn solve-opcodes [samples]
  (->> samples
     (map match-opcodes)
     (map #(sat/exactly 1 (map opcode-constraint %)))
     (sat/solve-symbolic-formula)
     (filter sat/positive?)
     (into {})))

(defn run-prog [prog opcode-table]
  (reduce (fn [reg-file [opcode & args]]
            (exec-instr (opcode-table opcode)
                        args reg-file))
          [0 0 0 0]
          prog))

(defn solve-part-2 [samples prog]
  (let [solution (solve-opcodes samples)
        opcode-table (into {} (map swp solution))]
    (run-prog prog opcode-table)))

(defn main
  "Advent of Code 2018 - Day 16"
  [& args]
  (let [samples (parse (read-data))
        prog (parse-prog (read-prog))]
    (println (solve-part-1 samples))
    (println (solve-part-2 samples prog))))
