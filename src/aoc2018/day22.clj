(ns aoc2018.day22
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.test :as t]
            [clojure.pprint :refer [pprint]]
            [aoc2018.utils :refer :all]
            [loom.graph]
            [loom.alg]
            [clojure.data.priority-map :refer [priority-map]]))

;; puzzle input:
(def my-input
  {:depth 3198
   :target [12 757]})

(def test-data
  {:depth 510
   :target [10 10]})

(defn geologic-index [{:keys [grid target]} [x y]]
  (cond
    (or (= [x y] [0 0])
        (= [x y] target)) 0
    (= y 0) (* x 16807)
    (= x 0) (* y 48271)
    :else (* (get grid [(dec x) y])
             (get grid [x (dec y)]))))

(defn erosion-level [{:keys [depth] :as cave} pos]
  (mod (+ (geologic-index cave pos) depth) 20183))

(defn in-bounds? [[w h] [x y]]
  (and (<= 0 x w) (<= 0 y h)))

(defn around [[x y]]
  (filter (fn [[x y]] (and (>= x 0) (>= y 0)))
          [[x (dec y)]
           [(dec x) y]
           [(inc x) y]
           [x (inc y)]]))

(defn plot-cave [empty-cave target]
  (loop [wave #{[0 0]}
         cave (assoc empty-cave :grid {})]
    ;; determine region-type for wave
    (let [cave (reduce #(assoc-in % [:grid %2] (erosion-level % %2))
                       cave wave)]
      (if (contains? wave target)
        ;; target reached, stop here.
        cave
        ;; compute the next wave: all around current wave,
        ;; but exclude regions we have done already.
        (let [around-wave (filter #(in-bounds? target %)
                                  (mapcat around wave))
              next-wave (set (remove (:grid cave) around-wave))]
          (recur next-wave cave))))))

(defn region-type [erosion-level]
  (case (mod erosion-level 3)
    0 :rocky
    1 :wet
    2 :narrow))

(def region-risk-level {:rocky 0 :wet 1 :narrow 2})

(defn risk-level [{:keys [grid target]}]
  (->> grid
   (filter (comp #(in-bounds? target %) first))
   (vals)
   (map (comp region-risk-level region-type))
   (reduce +)))

(defn solve-part-1 [cave]
  (risk-level (plot-cave cave (:target cave))))

(def region-required-tools
  {:rocky #{:climbing-gear :torch}
   :wet #{:climbing-gear :neither}
   :narrow #{:torch :neither}})

(defn compute-vertices [grid]
  (->> grid
     (map-values region-type)
     (map-values region-required-tools)
     (mapcat (fn [[pos tools]] (map #(vector pos %) tools)))
     (set)))

;; Move from [pos tool] to [(around pos) tool]
;; If the new pos is found in vertices (ie. in bounds and tool
;; is sufficient for the new position.
;; Cost is 1 minute.
(defn compute-move-edges [vertices [pos tool]]
  (->>
   (around pos)
   (map #(vector % tool))
   (filter vertices)
   (map #(vector % 1))))

;; Switching tool (stays on same position), cost is 7 minutes.
(defn compute-switch-tool-edges [vertices [pos tool]]
  (->> vertices
     (filter (fn [[other-pos other-tool]]
               (and (= pos other-pos)
                    (not= tool other-tool))))
     (map #(vector % 7))))

(defn compute-edges [vertices v]
  (into {} (concat
            (compute-move-edges vertices v)
            (compute-switch-tool-edges vertices v))))

(defn to-graph [{:keys [grid target]}]
  (let [vertices (compute-vertices grid)]
    (->> vertices
       (map #(vector % (compute-edges vertices %)))
       (into {}))))

(defn manhattan-distance [[x1 y1] [x2 y2]]
  (+ (Math/abs (- x2 x1))
     (Math/abs (- y2 y1))))

(defn astar-dist [graph start end heur]
  (loop [frontier (priority-map start 0)
         cost-so-far {start 0}]
    (let [[current _] (peek frontier)
          frontier (pop frontier)]
      (println current)
      (cond
        (nil? current) nil
        (= current end) (cost-so-far end)
        :else
        (let [[frontier cost-so-far]
              (loop [frontier frontier
                     cost-so-far cost-so-far
                     [[next cost] & neighbours] (graph current)]
                (if (nil? next)
                  [frontier cost-so-far]
                  (let [new-cost (+ (cost-so-far current) cost)
                        cur-cost (get cost-so-far next)]
                    (if (or (nil? cur-cost)
                            (< new-cost cur-cost))
                      (recur (assoc frontier next (+ new-cost (heur end next)))
                             (assoc cost-so-far next new-cost)
                             neighbours)
                      (recur frontier cost-so-far neighbours)))))]
          (recur frontier cost-so-far))))))

(defn solve-part-2 [{:keys [target] :as input}]
  ;; search in an area twice the space to target.
  (let [bounds (map #(+ % 10) target)
        cave (plot-cave input bounds)
        graph (loom.graph/weighted-graph (to-graph cave))
        start [[0 0] :torch]
        end [target :torch]
        alg :astar-custom]
    (println target)
    (println (count (loom.graph/edges graph)))
    (case alg
      :astar-custom
      (astar-dist (to-graph cave) start [target :torch]
                  (fn [[a _] [b _]]
                    (manhattan-distance a b)))
      :astar-loom
      (loom.alg/astar-path graph start [target :torch]
                           (fn [[a _] [b _]]
                             (manhattan-distance a b)))
      :dijkstra
      (second (loom.alg/dijkstra-path-dist graph start end)))))

(defn main
  "Advent of Code 2018 - Day 22"
  [& args]
  (let [input my-input]
    (println (solve-part-1 input))
    (println (solve-part-2 input))))
