(ns aoc2018.day19
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.test :as t]
            [clojure.pprint :refer [pprint]]
            [aoc2018.utils :refer :all]))

(def data-file (io/resource "day19.txt"))

(defn read-data [] (slurp data-file))

(def test-data
"#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5")

(defn parse-header [line]
  (let [[_ ip] (re-matches #"#ip (\d+)" line)]
    (to-int ip)))

(defn parse-instr [line]
  (let [[op & args] (str/split line #" ")]
    (concat [(keyword  op)] (map to-int args))))

(defn parse [data]
  (let [[hdr & lines] (str/split-lines data)
        ip-reg (parse-header hdr)]
    {:ip-reg ip-reg
     :code (vec (map parse-instr lines))}))

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

(defn step [{:keys [ip-reg code]} reg-file]
  (let [ip (nth reg-file ip-reg)]
    (if (contains? code ip)
      (let [[op & args] (nth code ip)
            _ (print ip op args ": ")
            run-op ((opcodes reg-file) op)
            _ (print reg-file " => ")
            reg-file (apply run-op args)
            _ (println reg-file)]
        (update reg-file ip-reg inc))
      nil)))

(defn run [prog reg-file]
  (iterate (partial step prog) reg-file))

(defn solve-part-1 [{:keys [ip-reg] :as prog}]
  (->>
   (run prog (vec (repeat 6 0)))
   (take-while (comp not nil?))
   (last)
   (first)))

(defn find-cycle [generations]
  (loop [seen {}
         iter generations
         count 0]
    (let [state (first iter)]
      (if-let [prev-count (get seen state)]
        [prev-count (- count prev-count)]
        (recur (assoc seen state count)
               (rest iter)
               (inc count))))))

(defn solve-part-2 [{:keys [ip-reg] :as prog}]
  (->>
   (run prog [1 0 0 0 0 0])
   (take-while (comp not nil?))
   (last)
   (first)))

;; Solving part 2 took way too long.
;;
;; Translating the assembly code to (a rough) C implementation,
;; resulted in this program:
;;
;; int main(int argc, char **argv) {
;;     long long a = 0;
;;     long long c = 10551340;
;;     for (long long e = 1; e <= 10551340; e++) {
;;         for (long long b = 1; b <= 10551340; b++) {
;;             if (c == b * e) {
;;                 a = a + e;
;;             }
;;         }
;;     }
;;     printf("a=%llu\n", a);
;; }
;;
;; To calculate this would require about 10^14 loop cycles.
;; However, the inner loop can be rephrased in the problem:
;;
;;     a = sum of all factors of 10551340
;;
;; The answer to that question is calculated below.

;; https://rosettacode.org/wiki/Prime_decomposition
(defn factors
  "Return a list of factors of N."
  ([n]
    (factors n 2 ()))
  ([n k acc]
    (if (= 1 n)
      acc
      (if (= 0 (rem n k))
        (recur (quot n k) k (cons k acc))
        (recur n (inc k) acc)))))

(defn perms [opts n]
  (if (= n 1)
    (map vector opts)
    (mapcat #(for [o opts] (conj % o))
            (perms opts (dec n)))))

(defn factor-combine [f p]
  (reduce * (remove zero? (map * f p))))

(defn factor-perms [n]
  (let [f (factors n)
        p (perms [0 1] (count f))]
    (set (map (partial factor-combine f) p))))

(defn main
  "Advent of Code 2018 - Day 19"
  [& args]
  (let [prog (parse (read-data))]
    (println (solve-part-1 prog))
    ;; This takes *way* too long.
    ;; (println (solve-part-2 prog))
    (println (reduce + (factor-perms 10551340)))
    ))
