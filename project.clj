(defproject aoc2018 "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [[org.clojure/clojure "1.9.0"]
                 [clojure.java-time "0.3.2"]
                 [aysylu/loom "0.5.4"]
;;                 [org.clojure/spec.alpha "0.2.176"]
                 [org.clojure/spec.alpha "0.1.143"]
                 [rolling-stones "1.0.0-SNAPSHOT"]
                 [instaparse "1.4.10"]]
  :main ^:skip-aot aoc2018.core
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}}
  :jvm-opts ["-Xmx8G"])
