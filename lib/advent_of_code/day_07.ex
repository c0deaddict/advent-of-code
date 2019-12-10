defmodule AdventOfCode.Day07 do
  alias AdventOfCode.Day05, as: IntCode

  def permutations([]), do: [[]]

  def permutations(list) do
    for elem <- list, rest <- permutations(list -- [elem]) do
      [elem | rest]
    end
  end

  def run_amps(program, phase_settings) do
    phase_settings
    |> Enum.reduce(0, fn phase, acc ->
      IntCode.run(program, [phase, acc]) |> hd
    end)
  end

  def part1(program_str) do
    program = IntCode.parse(program_str)

    0..4
    |> Enum.to_list()
    |> permutations
    |> Enum.map(fn phase_settings ->
      result = run_amps(program, phase_settings)
      [result | phase_settings]
    end)
    |> Enum.max_by(&hd/1)
  end

  def run_async(program, parent_pid) do
    input = fn ->
      receive do
        {:input, value} ->
          {value, nil}
      end
    end

    output = fn value ->
      send(parent_pid, {:output, self(), value})
      nil
    end

    state = IntCode.run_program({program, {input, output}, 0})
    send(parent_pid, {:halt, self(), state})
  end

  def rotate_left(list), do: tl(list) ++ [hd(list)]

  def run_amps_feedback(program, phase_settings) do
    my_pid = self()

    # Spawn a process for each phase.
    phases =
      phase_settings
      |> Enum.map(fn phase ->
        pid = spawn_link(fn -> run_async(program, my_pid) end)
        # Initialize with phase.
        send(pid, {:input, phase})
        pid
      end)

    # Send input to first phase.
    send(hd(phases), {:input, 0})

    # Connect the phases and gather the results.
    phases
    |> Enum.zip(rotate_left(phases))
    |> Map.new()
    |> feedback_loop(nil)
  end

  def feedback_loop(route_map, last_output) when route_map == %{} do
    last_output
  end

  def feedback_loop(route_map, last_output) do
    receive do
      {:output, sender, value} ->
        case route_map[sender] do
          nil ->
            feedback_loop(route_map, value)

          next_phase ->
            send(next_phase, {:input, value})
            feedback_loop(route_map, value)
        end

      {:halt, sender, _} ->
        feedback_loop(Map.delete(route_map, sender), last_output)
    end
  end

  def part2(program_str) do
    program = IntCode.parse(program_str)

    5..9
    |> Enum.to_list()
    |> permutations
    |> Enum.map(fn phase_settings ->
      result = run_amps_feedback(program, phase_settings)
      [result | phase_settings]
    end)
    |> Enum.max_by(&hd/1)
  end
end
