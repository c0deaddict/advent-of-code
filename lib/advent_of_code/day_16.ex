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

  def transpose([]), do: []
  def transpose([[]|_]), do: []
  def transpose(a) do
    [Enum.map(a, &hd/1) | transpose(Enum.map(a, &tl/1))]
  end

  def phase(signal, len, times) do
    0..(len * times)-1
    |> Enum.map(fn out_pos ->
      pattern(out_pos, 1)
      |> Stream.drop(1)
      |> Stream.take(len * times)
      |> Enum.chunk_every(len)
      |> transpose()
      |> Enum.map(&Enum.sum/1)
      |> Stream.zip(signal)
      |> Enum.reduce(0, fn {a, b}, acc -> acc + a * b end)
      |> last_digit()
    end)
  end

  def correct_phase(signal, len, times) do
    0..(len * times)-1
    |> Enum.map(fn out_pos ->
      Stream.concat([0], signal)
      |> Stream.zip(pattern(out_pos, 1))
      |> Enum.reduce(0, fn {a, b}, acc -> acc + a * b end)
      |> last_digit()
    end)
  end

  def find_cycle(stream) do
    stream
    |> Enum.reduce_while(Map.new(), fn i, acc ->
      case Map.get(acc, i) do
        nil ->
          {:cont, Map.put(acc, i, map_size(acc))}

        start ->
          {:halt, {start, map_size(acc)}}
      end
    end)
  end

  def print(signal, len) do
    signal
    |> Enum.chunk_every(len)
    |> Enum.map(&Enum.join(&1, ""))
    |> Enum.join(" ")
    |> IO.puts
  end

  def run(signal, num_phases, times \\ 1) do
    len = length(signal)
    signal = repeat(signal, times)
    Stream.iterate(signal, &phase(&1, len, times))
    |> Stream.each(&print(&1, len))
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
    signal = parse("12345678")
    times = 2
    len = length(signal)
    num = 2

    signal
    |> repeat(times)
    |> Stream.iterate(&correct_phase(&1, len, times))
    |> Stream.each(&print(&1, len))
    |> Stream.drop(num)
    |> Enum.at(0)

    IO.puts("\nexperimental:\n")

    signal
    |> run(num, times)
  end
end
