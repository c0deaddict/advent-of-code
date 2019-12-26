defmodule AdventOfCode.Day23 do
  import AdventOfCode.Utils
  alias AdventOfCode.Day05, as: IntCode

  defp input() do
    receive do
      {:input, {x, y}} ->
        {x, fn -> {y, &input/0} end}
    after
      0 ->
        {-1, nil}
    end
  end

  defp output(parent_pid, address) do
    fn dest ->
      fn x ->
        fn y ->
          send(parent_pid, {:output, dest, {x, y}})
          output(parent_pid, address)
        end
      end
    end
  end

  def run_computer(program, parent_pid, address) do
    input_address = fn ->
      {address, &input/0}
    end

    state = %IntCode.State{
      program: program,
      input: input_address,
      output: output(parent_pid, address)
    }

    state = IntCode.run_program(state)
    send(parent_pid, {:halt, address, state})
  end

  def spawn_computer(program, pid, address) do
    spawn_link(fn -> run_computer(program, pid, address) end)
  end

  def spawn_network(program, count) do
    0..(count - 1)
    |> Enum.map(fn address ->
      {address, spawn_computer(program, self(), address)}
    end)
    |> Map.new()
  end

  def process_packets_part1(network, address) do
    receive do
      {:output, ^address, {_, y}} ->
        y

      {:output, to, packet} ->
        pid = Map.get(network, to)
        send(pid, {:input, packet})
        process_packets_part1(network, address)

      {:halt, address} ->
        raise "unexpected halt of computer #{address}"
    end
  end

  def part1(input) do
    input
    |> IntCode.parse()
    |> spawn_network(50)
    |> process_packets_part1(255)
  end

  def part2(input) do
    input
  end
end
