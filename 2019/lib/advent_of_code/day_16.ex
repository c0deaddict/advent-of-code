defmodule AdventOfCode.Day16 do
  import AdventOfCode.Utils

  def parse(input) do
    input
    |> String.trim()
    |> String.codepoints()
    |> Enum.map(&String.to_integer/1)
  end

  def last_digit(value), do: abs(rem(value, 10))

  def pattern_at(out_pos, idx) do
    out_pos = out_pos + 1
    cycle = 4 * out_pos

    case div(rem(idx, cycle), out_pos) do
      0 -> 0
      1 -> 1
      2 -> 0
      3 -> -1
    end
  end

  def phase(signal, len) do
    0..(len - 1)
    |> Enum.map(fn out_pos ->
      Stream.concat([0], signal)
      |> Stream.with_index()
      |> Enum.reduce(0, fn {x, idx}, acc ->
        acc + x * pattern_at(out_pos, idx)
      end)
      |> last_digit()
    end)
  end

  def run(signal, num_phases) do
    len = length(signal)

    Stream.iterate(signal, &phase(&1, len))
    |> Stream.drop(num_phases)
    |> Enum.at(0)
  end

  def part1(input) do
    input
    |> parse
    |> run(100)
    |> Enum.take(8)
    |> Enum.join()
  end

  def phase_part2(signal) do
    signal
    |> Enum.reverse()
    |> Enum.reduce([], fn
      x, [] -> [x]
      x, acc -> [rem(hd(acc) + x, 10) | acc]
    end)
  end

  def part2(input) do
    offset =
      input
      |> String.slice(0..6)
      |> String.to_integer()

    times = 10000
    signal = parse(input)
    len = length(signal) * times
    phases = 100
    # From 1/2 of total signal we can ignore all but the 1's in the pattern, and
    # do a running modulo 10.
    if offset <= div(len, 2) do
      raise "offset too small for optimization"
    end

    # We are only interested in out_pos >= offset, so we can drop all numbers
    # before it. Since the multiplication pattern for those position is all
    # zeroes.
    signal
    |> repeat(10000)
    |> Stream.drop(offset)
    |> Enum.to_list()
    |> Stream.iterate(&phase_part2/1)
    |> Stream.drop(phases)
    |> Enum.at(0)
    |> Enum.take(8)
    |> Enum.join()
  end
end
