defmodule AdventOfCode.Day16 do
  def parse(input) do
    input
    |> String.trim()
    |> String.codepoints()
    |> Enum.map(&String.to_integer/1)
  end

  def last_digit(value), do: abs(rem(value, 10))

  def gcd(a, 0), do: a
  def gcd(a, b), do: gcd(b, rem(a, b))

  def lcm(a, b), do: div(a * b, gcd(a, b))

  def pattern(out_pos, c) do
    for(i <- [0, c, 0, -c], _ <- 0..out_pos, do: i)
    |> Stream.cycle()
  end

  def phase(signal, times) do
    signal_len = length(signal)

    0..(signal_len - 1)
    |> Enum.map(fn out_pos ->
      cycle =
        if out_pos == 0 do
          signal_len
        else
          # IO.inspect({signal_len, out_pos*4, lcm(signal_len, out_pos*4)})
          lcm(signal_len, out_pos * 4)
        end

      const =
        if cycle < signal_len do
          div(signal_len, cycle)
        else
          1
        end

      # IO.inspect({cycle, const})

      Stream.concat([0], repeat(signal, times))
      |> Enum.take(cycle + 1)
      |> Stream.zip(pattern(out_pos, const))
      |> Enum.reduce(0, fn {a, b}, acc -> acc + a * b end)
      |> last_digit()
    end)
  end

  def run(signal, num_phases, times \\ 1) do
    Stream.iterate(signal, &phase(&1, times))
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

  def repeat(stream, times) do
    [stream]
    |> Stream.cycle()
    |> Stream.take(times)
    |> Stream.concat()
  end

  def part2(input) do
    input
    |> parse
    |> run(1, 10000)
  end
end
