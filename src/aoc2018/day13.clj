(ns aoc2018.day13
  (require [clojure.java.io :as io]
           [clojure.string :as str]
           [clojure.test :as t]))

(def data-file (io/resource "day13.txt"))

(defn read-data []
  (slurp data-file))

(def char-mapping
  {\- :track-horz
   \| :track-vert
   \/ :track-corner
   \\ :track-corner ;; ??
   \+ :intersection
   \< :train-left
   })

;; https://clojuredocs.org/clojure.core/to-array-2d
(defn parse [data]
  (->>
   data
   (str/split-lines)
   (map seq)
   (to-array-2d)))

(def test-data
  (str
#"/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   "))

(defn main
  "Advent of Code 2018 - Day 13"
  [& args]
  (let [tracks (parse (read-data))]
    (println "TODO")))
