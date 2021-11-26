(ns aoc2018.day15
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.test :as t]
            [clojure.pprint :refer [pprint]]
            [loom.graph]
            [loom.alg]
            [loom.alg-generic]))

(def data-file (io/resource "day15.txt"))

(defn read-data [] (slurp data-file))

(def test-data-0 (str
#"#######
#.E...#
#.....#
#...G.#
#######"))

(def test-data-1 (str
#"#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"))

(def test-data-2 (str
#"#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######"))

(def test-data-3 (str
#"#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######"))

(def test-data-4 (str
#"#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######"))

(def test-data-5 (str
#"#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######"))

(def test-data-6 (str
#"#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"))

(def char-mapping
  {\# :wall
   \G :goblin
   \E :elf
   \. nil})

(def unit-char {:goblin \G :elf \E})

(defn to-grid [lines]
  (for [[y row] (map vector (range) lines)
        [x cell] (map vector (range) row)]
    [[y x] cell]))

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
       :units (map-index :id units)
       :round 0}
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
  (let [[height width] (bounds grid)]
    (println (apply str "   " (map #(quot % 10) (range (inc width)))))
    (println (apply str "   " (take (inc width) (cycle (range 10)))))
    (doseq [y (range (inc height))]
      (print (format "%2d " y))
      (doseq [x (range (inc width))
              :let [cell (get grid [y x])
                    unit (get units cell)]]
        (print
         (cond
           (= :wall cell) \#
           (nil? cell) \.
           (not (nil? unit)) (unit-char (:type unit))
           (integer? cell) \U)))
      (let [units-in-row (sort-by :pos
                                  (filter (comp #(= % y) first :pos)
                                          (vals units)))
            unit-status #(str (unit-char (:type %)) "(" (:hp %) ")")]
        (print "  " (str/join ", " (map unit-status units-in-row))))
      (println))))

(defn print-dist [{:keys [grid]} dist]
  (let [[height width] (bounds grid)]
    (doseq [y (range (inc height))]
      (doseq [x (range (inc width))
              :let [cell (get grid [y x])
                    d (get dist [y x])]]
        (print
         (cond
           (= :wall cell) " # "
           (nil? d) " . "
           :else (format "%2d " d))))
      (println))))

(defn dup [x] [x x])

(defn map-values [f m]
  (map (fn [[k v]] [k (f v)]) m))

(defn pmap-values [f m]
  (pmap (fn [[k v]] [k (f v)]) m))

(defn map-flatten [m]
  (apply concat
         (map (fn [[k v]]
                (map (fn [v'] [k v']) v))
              m)))

(defn map-first [f m]
  (map (fn [[k v]] [(f k) v]) m))

(defn in-bounds? [[h w] [y x]]
  (and (<= 0 x w) (<= 0 y h)))

(defn is-empty? [grid pos]
  (nil? (get grid pos)))

(defn all-around [{:keys [grid bounds]} [y x]]
  (filter (partial in-bounds? bounds)
          [[y (dec x)]
           [(dec y) x]
           [(inc y) x]
           [y (inc x)]]))

(defn around [{:keys [grid] :as game} pos]
  (filter (partial is-empty? grid)
          (all-around game pos)))

(defn find-targets [{:keys [units]} me]
  (let [not-my-type #(not= (:type %) (:type me))]
    (->> units
       (vals)
       (filter not-my-type)
       (map-index :pos))))

;; NOTE: loom did work, but it was too slow.
;; lee's algorithm is much quicker for shortest path
;; calculation in a maze.
(defn to-loom-graph [{:keys [grid] :as game} me]
  "Graph from me to all reachable positions"
  (->> grid
   (filter (comp #(or (nil? %) (= % (:id me))) second))
   (map (fn [[pos _]] [pos (around game pos)]))
   (into {})
   (loom.graph/graph)))

(defn shortest-path [game from to]
  (loom.alg/bf-path (to-loom-graph game) from to))

(defn all-shortest-paths [graph start end]
  (let [succ (loom.graph/successors graph)]
    (loom.alg-generic/bf-paths-bi succ succ start end)))

(defn to-graph [{:keys [grid] :as game} me]
  "Graph from me to all reachable positions"
  (->> grid
   (filter (comp #(or (nil? %) (= % (:id me))) second))
   (map (fn [[pos _]] [pos (around game pos)]))
   (into {})))

;; https://en.wikipedia.org/wiki/Lee_algorithm
(defn lee-algorithm [graph start end]
  (loop [wave #{end}
         depth 1
         result {end 0}]
    (let [next-wave (set (remove result (mapcat graph wave)))]
      (if (or (empty? next-wave) (contains? next-wave start))
        result
        (recur next-wave
               (inc depth)
               (merge result (zipmap next-wave (repeat depth))))))))

(defn pick-target [game me targets]
  "Returns first step to a shortest path to a pos around target"
  (let [graph (to-graph game me)
        around-me (around game (:pos me))]
    (->>
     (keys targets)
     (map (partial around game))
     (apply concat)
     (set)
     (map dup)
     (pmap-values (partial lee-algorithm graph (:pos me)))
     (map-values #(select-keys % around-me))
     (map-flatten) ;; around-target-pos => [first-step length]
     (sort-by (juxt (comp second second)   ;; length of path
                    first                  ;; around target pos
                    (comp first second)))  ;; first step
     (first)     ;; best result
     (second)    ;; [first-step length]
     (first))))  ;; first-step

(defn attack [game me targets]
  ;; pick target with fewest hp.
  ;; when in tie; pick the first in reading order (pos).
  (let [tgt (first (sort-by (juxt :hp :pos) (vals targets)))
        hp (- (:hp tgt) (:attack me))]
    (if (pos? hp)
      ;; target still alive, update game state.
      (assoc-in game [:units (:id tgt) :hp] hp)
      ;; target is dead, remove it from the units and grid.
      (-> game
       (update-in [:units] dissoc (:id tgt))
       (assoc-in [:grid (:pos tgt)] nil)))))

(defn try-attack
  ([game me targets]
   (try-attack game me targets identity))
  ([game me targets else]
   (assert (every? (comp pos? :hp second) targets))
   (let [positions (all-around game (:pos me))
         adjacent-targets (select-keys targets positions)]
     (if (empty? adjacent-targets)
       (else game)
       (attack game me adjacent-targets)))))

(defn try-move-and-attack [game me targets]
  (if-let [move-to (pick-target game me targets)]
    ;; move closer to target and try to attack.
    (do
      (assert (contains? (set (around game (:pos me))) move-to))
      (assert (is-empty? (:grid game) move-to))
      (try-attack
       (-> game
          (assoc-in [:grid (:pos me)] nil)
          (assoc-in [:grid move-to] (:id me))
          (assoc-in [:units (:id me) :pos] move-to))
       (assoc me :pos move-to)
       targets))
    ;; no target to move to, end turn.
    game
    ))

(defn turn [{:keys [grid units] :as game} me]
  (let [targets (find-targets game me)]
    (if (empty? targets)
      ;; no targets remain: combat ends.
      nil
      ;; try to attack, if not possible try to move closer to
      ;; a target and then try to attack again.
      (try-attack game me targets
                  #(try-move-and-attack % me targets)))))

(defn round [{:keys [units] :as game}]
  (do
    ;; (println "round" (:round game))
    (reduce
       (fn [game id]
         (if-let [me (get-in game [:units id])]
           ;; unit is alive, do step.
           (if-let [new-game (turn game me)]
             new-game
             ;; game ends, short circuit.
             (reduced (assoc game :ended true)))
           ;; unit is dead, ignore it.
           game))
       (update game :round inc)
       (map :id (sort-by :pos (vals units))))))

(defn run [game]
  (iterate round game))

(defn run-until-end [game]
  (first (drop-while (comp not :ended) (run game))))

(defn calculate-outcome [game]
  "Returns a tuple [round total-hp] which multiplied outcome."
  (let [total-hp (reduce + (map :hp (vals (:units game))))]
    [(dec (:round game)) total-hp]))

(defn solve-part-1 [game]
  (calculate-outcome (run-until-end game)))

(t/deftest test-part-1
  (t/is (= (solve-part-1 (parse test-data-1)) [47 590]))
  (t/is (= (solve-part-1 (parse test-data-2)) [37 982]))
  (t/is (= (solve-part-1 (parse test-data-3)) [46 859]))
  (t/is (= (solve-part-1 (parse test-data-4)) [35 793]))
  (t/is (= (solve-part-1 (parse test-data-5)) [54 536]))
  (t/is (= (solve-part-1 (parse test-data-6)) [20 937])))

(defn count-units-of-type [{:keys [units]} unit-type]
  (count (filter (comp #{unit-type} :type) (vals units))))

(defn run-with-upgraded-elves [{:keys [units] :as game} attack]
  (let [elves (filter (comp #{:elf} :type) (vals units))
        upgraded-game (reduce #(assoc-in % [:units %2 :attack] attack)
                              game (map :id elves))
        no-elf-died? #(= (count elves)
                         (count-units-of-type % :elf))]
    (println "upgraded elves to attack power" attack)
    (let [result (->>
                  (run upgraded-game)
                  (drop-while #(and (not (:ended %))
                                   (no-elf-died? %)))
                  (first))]
      (if (no-elf-died? result)
        result
        nil))))

(defn solve-part-2 [game]
  (->>
   (map (partial run-with-upgraded-elves game) (drop 4 (range)))
   (drop-while nil?)
   (first)
   (calculate-outcome)))

(t/deftest test-part-2
  (t/is (= (solve-part-2 (parse test-data-1)) [29 172]))
  (t/is (= (solve-part-2 (parse test-data-3)) [33 948]))
  (t/is (= (solve-part-2 (parse test-data-4)) [37 94]))
  (t/is (= (solve-part-2 (parse test-data-5)) [39 166]))
  (t/is (= (solve-part-2 (parse test-data-6)) [30 38])))

(defn main
  "Advent of Code 2018 - Day 15"
  [& args]
  (let [game (parse (read-data))]
    (println (apply * (solve-part-1 game)))
    (println (apply * (solve-part-2 game)))))
