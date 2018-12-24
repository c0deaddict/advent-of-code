(ns aoc2018.day17
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.test :as t]
            [clojure.pprint :refer [pprint]]
            [aoc2018.utils :refer :all]))

(def data-file (io/resource "day17.txt"))

(defn read-data [] (slurp data-file))

(def test-data
"x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504")

(defn parse-sample [[before instr after]]
  (let [[_ before ] (re-matches #"Before:\s*\[([^\]]+)\]" before)
        [_ after] (re-matches #"After:\s*\[([^\]]+)\]" after)
        before (vec (map to-int (str/split before #",\s*")))
        after (vec (map to-int (str/split after #",\s*")))
        instr (map to-int (str/split instr #"\s+"))]
    [before instr after]))

(defn parse-vein [str]
  (if-let [[_ & args] (re-matches #"x=(\d+), y=(\d+)\.\.(\d+)" str)]
    (let [[x y1 y2] (map to-int args)]
      [[x x] [y1 y2]])
    (if-let [[_ & args] (re-matches #"y=(\d+), x=(\d+)\.\.(\d+)" str)]
      (let [[y x1 x2] (map to-int args)]
        [[x1 x2] [y y]])
      (assert false))))

(defn bounds [veins]
  [(min-max (mapcat first veins))
   (min-max (mapcat second veins))])

(defn make-vein [[[x1 x2] [y1 y2]]]
  (for [x (range x1 (inc x2))
        y (range y1 (inc y2))]
    [[x y] :clay]))

(defn make-tiles [veins]
  (let [[[x-min x-max] [y-min y-max]] (bounds veins)]
    {:tiles (into {} (mapcat make-vein veins))
     :x-min (dec x-min) ;; water can flow to left and
     :x-max (inc x-max) ;; right of outer x-bounds.
     :y-min y-min
     :y-max y-max}))

(defn parse [data]
  (->> data
     (str/split-lines)
     (map parse-vein)
     (make-tiles)))

(defn print-tiles [{:keys [tiles x-min x-max y-min y-max]}]
  (let [x-range (range x-min (inc x-max))
        width (- (inc x-max) x-min)]
    (doseq [i (range 2 -1 -1)]
      (println (apply str "     " (take width (map (partial nth-digit i) x-range)))))
    (doseq [y (range (inc y-max))]
      (print (format "%4d " y))
      (doseq [x x-range
              :let [v (get tiles [x y])]]
        (print
         (cond
           (and (= y 0) (= x 500)) \+
           (= :clay v) \#
           (= :rest v) \~
           (= :flow v) \|
           :else \.)))
      (println))))

(defn up [[x y]] [x (dec y)])
(defn down [[x y]] [x (inc y)])
(defn move-x [dir [x y]] [(dir x) y])

(defn clay-beside-me [tiles dir pos]
  (= :clay (get tiles (move-x dir pos))))

(defn clay-below-me [tiles pos]
  (#{:clay :rest} (get tiles (down pos))))

(defn scan-in-dir [tiles dir start]
  (loop [pos start]
    (cond
      (clay-beside-me tiles dir pos) [pos :side]
      (not (clay-below-me tiles pos)) [pos :down]
      :else (recur (move-x dir pos)))))

(defn fill-line [tiles [left-x left-y] [right-x right-y] v]
  (assert (= left-y right-y))
  (reduce #(assoc % [%2 left-y] v)
          tiles
          (range left-x (inc right-x))))

(defn flow [start {:keys [tiles y-max] :as state}]
  (loop [pos start
         tiles tiles
         queue []]
    (assert (not (neg? (second pos))))
    ;; if we flow beyond y-max we're done.
    ;; we're also done when hitting a tile marked :flow,
    ;; that means we've visited that before.
    (if (or (> (second pos) y-max) (= :flow (get tiles (down pos))))
      ;; close of this flow and continue with queue.
      (let [tiles (assoc tiles pos :flow)]
        (if (empty? queue)
          (assoc state :tiles tiles)
          (recur (first queue) tiles (rest queue))))
      ;; scan both left and right of our current pos
      ;; for either a :down or :side hit.
      ;; :down means we've found a pos that has no :clay or :rest
      ;; beneath it.
      ;; :side means we've hit a :clay on the left or right side.
      (let [[left left-hit] (scan-in-dir tiles dec pos)
            [right right-hit] (scan-in-dir tiles inc pos)
            fill #(fill-line tiles left right %)]
        (cond
          ;; hit clay on both sides, fill with :rest and go up.
          (= :side left-hit right-hit)
          (recur (up pos) (fill :rest) queue)
          ;; left side went down, flow there first.
          ;; if the right side also went down, queue that.
          ;; except if left and right are equal.
          (= :down left-hit)
          (recur (down left) (fill :flow)
                 (if (and (= :down right-hit) (not= left right))
                   (conj queue (down right))
                   queue))
          ;; right side only.
          (= :down right-hit)
          (recur (down right) (fill :flow) queue)
          ;; shouldn't happen.
          :else (assert false))))))

(defn solve-part-1 [state]
  (->> state
     (flow [500 0])
     (:tiles)
     (filter (comp #(>= % (:y-min state)) second first))
     (vals)
     (filter #{:flow :rest})
     (count)))

(defn main
  "Advent of Code 2018 - Day 17"
  [& args]
  (let [state (parse (read-data))]
    (println (solve-part-1 state))))
