(ns aoc2018.day15
  (require [clojure.java.io :as io]
           [clojure.string :as str]
           [clojure.test :as t]
           [clojure.pprint :refer [pprint]]
           [loom.graph]
           [loom.alg]))

(def data-file (io/resource "day15.txt"))

(defn read-data [] (slurp data-file))

(def test-data (str
#"#######
#E..G.#
#...#.#
#.G.#G#
#######"))

(def char-mapping
  {\# :wall
   \G :goblin
   \E :elf
   \. nil})

(defn to-grid [lines]
  (for [[y row] (map vector (range) lines)
        [x cell] (map vector (range) row)]
    [[x y] cell]))

(defn bounds [grid]
  (last (sort (map first grid))))

(defn extract-units [grid]
  "Extract units from the grid, leaving only walls/empty."
  (loop [to-process (filter (comp #{:goblin :elf} second) grid)
         next-id 0
         units []
         grid grid]
    (if (empty? to-process)
      {:grid grid
       :bounds (bounds grid)
       :units (map-index units :pos)}
      (let [[pos unit-type] (first to-process)
            unit {:pos pos
                  :id next-id
                  :type unit-type
                  :hp 200
                  :attack 3}]
        (recur
         (rest to-process)
         (inc next-id)
         (conj units unit)
         (assoc grid pos next-id))))))

(defn parse [data]
  (->> data
   (str/split-lines)
   (map seq)
   (map #(map char-mapping %))
   (to-grid)
   (into {})
   (extract-units)))

(defn print-game [{:keys [grid units]}]
  (let [[width height] (bounds grid)]
    (println (apply str "   " (map #(quot % 10) (range (inc width)))))
    (println (apply str "   " (take (inc width) (cycle (range 10)))))
    (doseq [y (range (inc height))]
      (print (format "%2d " y))
      (doseq [x (range (inc width))
              :let [cell (get grid [x y])
                    unit (get units [x y])]]
        (print
         (cond
           (= :wall cell) \#
           (nil? cell) \.
           (not (nil? unit)) ({:goblin \G :elf \E} (:type unit))
           (integer? cell) \U)))
      (println))))

(defn map-index [coll f]
  (zipmap (map f coll) coll))

(defn map-values [f m]
  (into {} (map (fn [[k v]] [k (f v)]) m)))

(defn map-flatten [m]
  (apply concat
         (map (fn [[k v]]
                (map (fn [v'] [k v']) v))
              m)))

(defn map-first [f m]
  (map (fn [[k v]] [(f k) v]) m))

(defn in-bounds? [[w h] [x y]]
  (and (<= 0 x w) (<= 0 y h)))

(defn is-empty? [grid pos]
  (nil? (get grid pos)))

(defn around [{:keys [grid bounds]} [x y]]
  (filter #(and (is-empty? grid %)
               (in-bounds? bounds %))
          [[x (dec y)]
           [(dec x) y]
           [(inc x) y]
           [x (inc y)]]))

(defn to-graph [{:keys [grid] :as game}]
  (->> grid
   (filter (comp #(or (nil? %) (integer? %)) second))
   (map (fn [[pos _]] [pos (around game pos)]))
   (into {})
   (loom.graph/graph)))

(defn shortest-path [game from to]
  (loom.alg/bf-path (to-graph game) from to))

(defn find-targets [{:keys [units]} me]
  (let [not-my-type #(not= (:type %) (:type me))]
    (into {} (filter (comp not-my-type second) units))))

(defn pick-target [game me targets]
  "Returns [path target-pos]"
  (let [graph (to-graph game)]
    (->>
     (keys targets)
     (map #(vector %1 (around game %1)))
     (map-flatten)
     (map (fn [[k v]] [v k])) ;; swap key and vals
     (group-by first)
     (map-first #(loom.alg/bf-path graph me %))
     (remove (comp nil? first))
;;     (map-flatten)
;;     (sort-by (juxt (comp count first) second))
;;     (first)
     )))

(defn step [{:keys [grid units] :as game} me]
  ;; 0. if no target remain, end the game.
  ;; 1: if there is a target with :pos (around me)
  ;;    then attack
  ;; 2. if there are no open squares in range of a target,
  ;;    end my turn.
  ;; 3. consider squares that are in range
  (let [targets (find-targets game)
        adjacent-targets (select-keys targets (around grid (:pos me)))]
    ;; if no targets remain: combat ends.
    (if (empty? targets)
      nil
      ;; if there is a target around me: attack.
      (if (not (empty? adjacent-targets))
        ;; select target with fewest hp
        ;; when in tie: sort by reading order.
        nil ;; todo call attack function
        ;; else: try to move closer to the closest target.
        (let [[path _] (move-pick-target grid me targets)
              move-to (first path)]
          (assert (contains? (set (around grid me)) (first path)))
          {:grid (assoc grid (:pos me) nil move-to (:id me))
           :units (update-in units [(:id me) ])})
          ;; update unit pos too.
         ))))

(defn round [grid units]
  ;; do each step of each unit
  )

(defn main
  "Advent of Code 2018 - Day 15"
  [& args]
  (println nil))
