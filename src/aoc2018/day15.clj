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

(defn map-index [f coll]
  (zipmap (map f coll) coll))

(defn extract-units [grid]
  "Extract units from the grid, leaving only walls/empty."
  (loop [to-process (filter (comp #{:goblin :elf} second) grid)
         next-id 0
         units []
         grid grid]
    (if (empty? to-process)
      {:grid grid
       :bounds (bounds grid)
       :units (map-index :id units)}
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
    (->> units
       (vals)
       (filter not-my-type)
       (map-index :pos))))

(defn pick-target [game me targets]
  "Returns [path target-pos]"
  (let [graph (to-graph game)]
    (->>
     (keys targets)                        ;; want only pos of targets
     (map #(vector %1 (around game %1)))   ;; pos => [around1...N]}
     (map-flatten)                         ;; [[pos around1] [pos around2]]
     (map (fn [[k v]] [v k]))              ;; swap key and vals (around => pos)
     (group-by first)                      ;; around1 => [pos1, pos2]
     (map-values #(map second %))          ;; strip keys out of groups
     (map-first #(loom.alg/bf-path graph (:pos me) %))
     (remove (comp nil? first))
     (map-flatten)
     (sort-by (juxt (comp count first)     ;; length of path
                    second                 ;; target pos
                    (comp second first)))  ;; first step
     (first))))

(defn try-move [game me targets]
  (let [[path _] (pick-target game me targets)
        move-to (second path)]
    (if (nil? move-to)
      ;; no target to move to, end turn.
      game
      ;; move closer to target.
      (do
        (assert (contains? (set (around game (:pos me))) move-to))
        (assert (is-empty? (:grid game) move-to))
        (-> game
           (assoc-in [:grid (:pos me)] nil)
           (assoc-in [:grid move-to] (:id me))
           (assoc-in [:units (:id me) :pos] move-to))))))

(defn attack [game me adjacent-targets]
  ;; select target with fewest hp
  ;; when in tie: sort by reading order.
  (println "attack" adjacent-targets)
  game)

(defn step [{:keys [grid units] :as game} me]
  (let [targets (find-targets game me)
        adjacent-targets (select-keys targets (around game (:pos me)))]
    (cond
      ;; no targets remain: combat ends.
      (empty? targets) nil
      ;; there is a target around me: attack.
      (not (empty? adjacent-targets)) (attack game me adjacent-targets)
      ;; else: try to move one step towards the closest target.
      :else (try-move game me targets))))

(defn round [{:keys [units] :as game}]
  (reduce
   (fn [game id]
     (if-let [me (get-in game [:units id])]
       ;; unit is alive, do step
       (if-let [new-game (step game me)]
         new-game
         (reduced nil))  ;; game ends, short circuit
       ;; unit is dead
       game))
   game
   (map (comp :id second) units)))

(defn run [game]
  (iterate round game))

(defn main
  "Advent of Code 2018 - Day 15"
  [& args]
  (println nil))
