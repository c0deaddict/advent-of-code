(ns aoc2018.day21
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.test :as t]
            [clojure.pprint :refer [pprint]]
            [aoc2018.utils :refer :all]))

(def data-file (io/resource "day21.txt"))

(defn read-data [] (slurp data-file))

(defn parse-header [line]
  (let [[_ ip] (re-matches #"#ip (\d+)" line)]
    (to-int ip)))

(defn parse-instr [line]
  (let [[op & args] (str/split line #" ")]
    (concat [(keyword op)] (map to-int args))))

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

(def register-names [\a \b \c \d \e \f])

(def translate
  (let [reg register-names
        op (fn [sym a b] (str a " " sym " " b))
        st (fn [i v] (str (reg i) " = " v))]
    {:addr (fn [a b c] (st c (op "+" (reg a) (reg b))))
     :addi (fn [a b c] (st c (op "+" (reg a) b)))
     :mulr (fn [a b c] (st c (op "*" (reg a) (reg b))))
     :muli (fn [a b c] (st c (op "*" (reg a) b)))
     :banr (fn [a b c] (st c (op "&" (reg a) (reg b))))
     :bani (fn [a b c] (st c (op "&" (reg a) b)))
     :borr (fn [a b c] (st c (op "|" (reg a) (reg b))))
     :bori (fn [a b c] (st c (op "|" (reg a) b)))
     :setr (fn [a _ c] (st c (reg a)))
     :seti (fn [a _ c] (st c a))
     :gtir (fn [a b c] (st c (op ">" a (reg b))))
     :gtri (fn [a b c] (st c (op ">" (reg a) b)))
     :gtrr (fn [a b c] (st c (op ">" (reg a) (reg b))))
     :eqir (fn [a b c] (st c (op "==" a (reg b))))
     :eqri (fn [a b c] (st c (op "==" (reg a) b)))
     :eqrr (fn [a b c] (st c (op "==" (reg a) (reg b))))
     }))

(defn step [{:keys [ip-reg code]} reg-file]
  (let [ip (nth reg-file ip-reg)]
    (if (contains? code ip)
      (let [[op & args] (nth code ip)
            ;; _ (print ip op args ": ")
            run-op ((opcodes reg-file) op)
            ;; _ (print reg-file " => ")
            reg-file (apply run-op args)
            ;; _ (println reg-file)
            ]
        (update reg-file ip-reg inc))
      nil)))

(defn run [prog reg-file]
  (iterate (partial step prog) reg-file))

(defn run-until-halt [prog max-steps reg-0]
  (->>
   (run prog [reg-0 0 0 0 0 0])
   (take-while (comp not nil?))
   (take max-steps)
   (count)))

(defn print-prog [{:keys [ip-reg code]}]
  (println (str "ip=" (register-names ip-reg)))
  (doseq [[[op & args] line-num] (map vector code (range))]
    (println (str (format "%2d" line-num)
                  " " (apply (translate op) args)))))

;; Reverse engineering the assembly into a more readable/understandable code:
;;
;;     (print-prog (parse (read-data)))
;;
;; And some magic, led to to following C-like code:
;;
;; c = 0
;; do {
;;   b = c | 65536;
;;   c = 1250634;
;;   for (; b >= 256; b = b / 256) {
;;     e = b & 255;
;;     c = c + e;
;;     c = c & 16777215;
;;     c = c * 65899;
;;     c = c & 16777215;
;;   }
;; } while (c != a)
;;
;; Now we can compute the values of 'a' for which the program will halt:
(defn solutions []
  (let [iter #(loop [b (bit-or % 65536)
                     c 1250634]
               (let [c (let [e (bit-and b 0xff)
                              x (bit-and (+ c e) 0xffffff)]
                         (bit-and (* x 65899) 0xffffff))]
                 (if (< b 256)
                   c
                   (recur (quot b 256) c))))
        f (iterate iter 0)]
    f))

(defn solve-part-1 []
  (nth (solutions) 1))

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

;; A cycle exists in the lazy seq. The program halts as soon as 'c = a' so all
;; values after the first cycle can't be "reached" because the program will halt
;; on the first occurence of 'a'.
;; Therefore the maximum instructions executed is at the last value before the
;; start of the cycle.
(defn solve-part-2 []
  (let [s (solutions)
        [start length] (find-cycle s)]
    (nth s (+ start length -1))))

(defn main
  "Advent of Code 2018 - Day 21"
  [& args]
  (println (solve-part-1))
  (println (solve-part-2)))
