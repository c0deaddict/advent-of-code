import Data.Char
import Data.List

main = do
  input <- readFile "../input/day_1.txt"
  print . part1 $ input
  print . part2 $ input

firstAndLast digits = 10 * head digits + last digits

part1 :: String -> Int
part1 input = sum (map (firstAndLast . map digitToInt . filter isDigit) (lines input))

digitStrings = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
findDigitString line =
  let
    findPrefix' line [] = Nothing
    findPrefix' line ((i,x):xs)
      | x `isPrefixOf` line = Just i
      | otherwise = findPrefix' line xs
  in findPrefix' line (zip [1..] digitStrings)

parseDigits [] = []
parseDigits line@(x:xs)
  | isDigit x = digitToInt x : parseDigits xs
  | Just d <- findDigitString line = d : parseDigits xs
  | otherwise = parseDigits xs

part2 :: String -> Int
part2 input = sum (map (firstAndLast . parseDigits) (lines input))
