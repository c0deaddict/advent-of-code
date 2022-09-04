defmodule AdventOfCode.Day22 do
  import AdventOfCode.Utils, only: [gcd: 2]

  def parse(input) do
    input
    |> String.trim()
    |> String.split("\n")
    |> Enum.map(fn line ->
      case Regex.run(~r/^([[:alpha:] ]+)(?:\s+(-?\d+))?$/, String.trim(line)) do
        [_, "deal into new stack"] -> :new_stack
        [_, "cut", num] -> {:cut, String.to_integer(num)}
        [_, "deal with increment", num] -> {:deal, String.to_integer(num)}
      end
    end)
  end

  defp mod(x, y) when x > 0, do: rem(x, y)
  defp mod(x, y) when x < 0, do: rem(x, y) + y
  defp mod(0, _y), do: 0

  def find_index(ops, n, i) do
    Enum.reduce(ops, i, fn op, j ->
      case op do
        :new_stack -> n - 1 - j
        {:cut, num} -> mod(j - num, n)
        {:deal, num} -> mod(j * num, n)
      end
    end)
  end

  def shuffle(input, n) do
    ops = parse(input)

    0..(n - 1)
    |> Enum.map(&{find_index(ops, n, &1), &1})
    |> Enum.sort_by(&elem(&1, 0))
    |> Enum.map(&elem(&1, 1))
  end

  def part1(input) do
    n = 10007

    parse(input)
    |> find_index(n, 2019)
  end

  # solve c in: b*c mod m = a (mod m)
  # https://www.geeksforgeeks.org/modular-division/
  def divmod(a, b, m) do
    if gcd(b, m) != 1 do
      raise "inverse does not exist"
    end

    rem(powmod(b, m - 2, m) * rem(a, m), m)
  end

  def at_index(ops, n, i) do
    Enum.reduce(Enum.reverse(ops), i, fn op, j ->
      case op do
        :new_stack -> n - 1 - j
        {:cut, num} -> mod(j + num, n)
        {:deal, num} -> divmod(j, num, n)
      end
    end)
  end

  def optimize(ops, n) do
    Enum.reduce(ops, {0, 1}, fn op, {cut, deal} ->
      {cut, deal} =
        case op do
          :new_stack ->
            # new_stack = [{:deal, -1}, {:cut, 1}]
            {-cut + 1, -deal}

          {:cut, num} ->
            {cut + num, deal}

          {:deal, num} ->
            {cut * num, deal * num}
        end

      {mod(cut, n), mod(deal, n)}
    end)
  end

  # https://www.geeksforgeeks.org/modular-exponentiation-power-in-modular-arithmetic/
  def powmod(x, y, p) do
    case rem(x, p) do
      0 -> 0
      x -> powmod(x, y, p, 1)
    end
  end

  def powmod(_, 0, _, res), do: res

  def powmod(x, y, p, res) do
    res =
      if rem(y, 2) == 1 do
        rem(res * x, p)
      else
        res
      end

    y = div(y, 2)
    x = rem(x * x, p)

    powmod(x, y, p, res)
  end

  def repeat(ops, n, times) do
    {cut, deal} = optimize(ops, n)
    new_deal = powmod(deal, times, n)
    new_cut = divmod(cut * mod(new_deal - 1, n), deal - 1, n)
    {new_cut, new_deal}
  end

  def summary_to_ops({cut, deal}) do
    [
      {:deal, deal},
      {:cut, cut}
    ]
  end

  def part2(input) do
    n = 119_315_717_514_047
    times = 101_741_582_076_661

    repeat(parse(input), n, times)
    |> summary_to_ops
    |> at_index(n, 2020)
  end
end
