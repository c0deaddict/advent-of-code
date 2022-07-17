defmodule AdventOfCode.Day23 do
  alias AdventOfCode.Day05, as: IntCode

  defp input(parent_pid, address, idle_count) do
    fn ->
      receive do
        {:input, {x, y}} ->
          {x,
           fn ->
             {y, input(parent_pid, address, 0)}
           end}
      after
        0 ->
          if idle_count > 100 do
            send(parent_pid, {:idle, address})
            {-1, input(parent_pid, address, 0)}
          else
            {-1, input(parent_pid, address, idle_count + 1)}
          end
      end
    end
  end

  defp output(parent_pid, address) do
    fn dest ->
      fn x ->
        fn y ->
          send(parent_pid, {:output, address, dest, {x, y}})
          output(parent_pid, address)
        end
      end
    end
  end

  def run_computer(program, parent_pid, address) do
    input_address = fn ->
      {address, input(parent_pid, address, 0)}
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
      {:output, _, ^address, {_, y}} ->
        y

      {:output, _, to, packet} ->
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

  def process_packets_part2(network) do
    idle_counts = for {addr, _} <- network, into: %{}, do: {addr, 0}
    process_packets_part2(network, idle_counts, nil)
  end

  def process_packets_part2(network, idle_counts, nat) do
    receive do
      {:output, _, 255, packet} ->
        process_packets_part2(network, idle_counts, packet)

      {:output, from, to, packet} ->
        pid = Map.get(network, to)
        send(pid, {:input, packet})
        idle_counts = Map.put(idle_counts, to, 0)
        idle_counts = Map.put(idle_counts, from, 0)
        process_packets_part2(network, idle_counts, nat)

      {:idle, address} ->
        idle_counts = Map.update!(idle_counts, address, &(&1 + 1))

        if Enum.all?(Map.values(idle_counts), &(&1 > 20)) do
          # Network is idle.
          IO.puts("sending NAT #{inspect(nat)} to address 0")
          pid = Map.get(network, 0)
          send(pid, {:input, nat})
          idle_counts = for {addr, _} <- idle_counts, into: %{}, do: {addr, 0}
          process_packets_part2(network, idle_counts, nat)
        else
          process_packets_part2(network, idle_counts, nat)
        end

      {:halt, address} ->
        raise "unexpected halt of computer #{address}"
    end

    # end
  end

  def part2(input) do
    input
    |> IntCode.parse()
    |> spawn_network(50)
    |> process_packets_part2()
  end
end
