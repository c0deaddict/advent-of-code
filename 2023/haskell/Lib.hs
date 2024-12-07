module Lib
  ( trim
  ) where

import Data.Char
import Data.List

trim = dropWhileEnd isSpace . dropWhile isSpace
