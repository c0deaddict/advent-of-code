import Data.List

main = do
  contents <- readFile "../input/day_1.txt"
  let top = topGroups . groupLines . lines $ contents
  print . head $ top
  print . sum . take 3 $ top

groupLines :: [String] -> [[String]]
groupLines l = group' l [] where
  group' [] acc = [reverse acc]
  group' ("":xs) acc = reverse acc : group' xs []
  group' (x:xs) acc = group' xs (x : acc)

sumGroups :: [[String]] -> [Int]
sumGroups = map (sum . map read)

topGroups = reverse . sort . sumGroups
