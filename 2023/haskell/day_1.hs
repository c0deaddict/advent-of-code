{-# LANGUAGE QuasiQuotes #-}

import Test.HUnit
import Text.RawString.QQ

import Data.Char
import Data.List

import Lib

main = do
  input <- fmap parseInput (readFile "../input/day_1.txt")
  runTestTT tests
  print . part1 $ input
  print . part2 $ input

parseInput = lines . trim

firstAndLast digits = 10 * head digits + last digits

part1 :: [String] -> Int
part1 input = sum (map (firstAndLast . map digitToInt . filter isDigit) input)

digitStrings :: [String]
digitStrings =
  ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

findDigitString line =
  let findPrefix' line [] = Nothing
      findPrefix' line ((i, x):xs)
        | x `isPrefixOf` line = Just i
        | otherwise = findPrefix' line xs
   in findPrefix' line (zip [1 ..] digitStrings)

parseDigits [] = []
parseDigits line@(x:xs)
  | isDigit x = digitToInt x : parseDigits xs
  | Just d <- findDigitString line = d : parseDigits xs
  | otherwise = parseDigits xs

part2 :: [String] -> Int
part2 input = sum (map (firstAndLast . parseDigits) input)

example1 =
  [r|
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
|]

part1_test = TestCase (assertEqual "example1" (part1 (parseInput example1)) 142)

example2 =
  [r|
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
|]

part2_test = TestCase (assertEqual "example2" (part2 (parseInput example2)) 281)

tests = TestList [TestLabel "part1" part1_test, TestLabel "part2" part2_test]
