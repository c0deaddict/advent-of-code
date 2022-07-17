defmodule AdventOfCode.Day05 do
  defmodule State do
    defstruct program: %{}, input: nil, output: nil, ip: 0, rb: 0
  end

  def swap({a, b}), do: {b, a}

  def parse(program_str) do
    program_str
    |> String.trim()
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
    |> Enum.with_index()
    |> Enum.map(&swap/1)
    |> Map.new()
  end

  def is_halt(state) do
    state.program[state.ip] == 99
  end

  def incr_ip(state, increment) do
    %{state | ip: state.ip + increment}
  end

  def load(_, addr) when addr < 0, do: raise("invalid addr")

  def load(state, addr) do
    Map.get(state.program, addr, 0)
  end

  def store(state, out, value) do
    %{state | program: Map.put(state.program, out, value)}
  end

  def op_add(state, a, b, out) do
    state
    |> store(out, a + b)
    |> incr_ip(4)
  end

  def op_multiply(state, a, b, out) do
    state
    |> store(out, a * b)
    |> incr_ip(4)
  end

  def op_input(state, out) do
    {value, new_input} = state.input.()

    %{state | input: new_input || state.input}
    |> store(out, value)
    |> incr_ip(2)
  end

  def op_output(state, value) do
    if value == nil do
      raise "output nil is not allowed"
    end

    new_output = state.output.(value)

    %{state | output: new_output || state.output}
    |> incr_ip(2)
  end

  def op_jump_if_true(state, test, branch) do
    if test != 0 do
      %{state | ip: branch}
    else
      incr_ip(state, 3)
    end
  end

  def op_jump_if_false(state, test, branch) do
    if test == 0 do
      %{state | ip: branch}
    else
      incr_ip(state, 3)
    end
  end

  def op_less_than(state, a, b, out) do
    state
    |> store(out, if(a < b, do: 1, else: 0))
    |> incr_ip(4)
  end

  def op_equals(state, a, b, out) do
    state
    |> store(out, if(a == b, do: 1, else: 0))
    |> incr_ip(4)
  end

  def op_adjust_rb(state, offset) do
    %{state | rb: state.rb + offset}
    |> incr_ip(2)
  end

  def run_op(state) do
    opcode = load(state, state.ip)

    {op, num_args, out_args} =
      case rem(opcode, 100) do
        1 -> {&op_add/4, 3, [2]}
        2 -> {&op_multiply/4, 3, [2]}
        3 -> {&op_input/2, 1, [0]}
        4 -> {&op_output/2, 1, []}
        5 -> {&op_jump_if_true/3, 2, []}
        6 -> {&op_jump_if_false/3, 2, []}
        7 -> {&op_less_than/4, 3, [2]}
        8 -> {&op_equals/4, 3, [2]}
        9 -> {&op_adjust_rb/2, 1, []}
        99 -> raise "halt"
        x -> raise "unknown op #{x}"
      end

    {args, _} =
      1..num_args
      |> Enum.map(&load(state, state.ip + &1))
      |> Enum.with_index()
      |> Enum.map_reduce(div(opcode, 100), fn {arg, i}, modes ->
        is_out = Enum.member?(out_args, i)

        arg =
          if is_out do
            case(rem(modes, 10)) do
              # Position mode.
              0 -> arg
              # Immediate mode.
              1 -> arg
              # Relative mode.
              2 -> arg + state.rb
              x -> raise "unknown mode #{x}"
            end
          else
            case(rem(modes, 10)) do
              # Position mode.
              0 -> load(state, arg)
              # Immediate mode.
              1 -> arg
              # Relative mode.
              2 -> load(state, arg + state.rb)
              x -> raise "unknown mode #{x}"
            end
          end

        {arg, div(modes, 10)}
      end)

    apply(op, [state | args])
  end

  def run_program(state) do
    if is_halt(state) do
      state
    else
      run_program(run_op(state))
    end
  end

  # Elixir has really immutable state. Closing over the list is not enough to
  # keep state. By returning a new function we can keep state.
  def input_from_list(input_list) do
    fn ->
      case input_list do
        [] ->
          raise "input exhausted"

        [value | rest] ->
          {value, input_from_list(rest)}
      end
    end
  end

  def output_to_list(output_list) do
    fn
      nil -> output_list
      value -> output_to_list([value | output_list])
    end
  end

  def run(program, input_list) do
    state = %State{
      program: program,
      input: input_from_list(input_list),
      output: output_to_list([])
    }

    state = run_program(state)
    Enum.reverse(state.output.(nil))
  end

  def run_async(program, parent_pid) do
    input = fn ->
      send(parent_pid, {:request_input, self()})

      receive do
        {:input, value} ->
          {value, nil}
      end
    end

    output = fn value ->
      send(parent_pid, {:output, self(), value})
      nil
    end

    state = %State{
      program: program,
      input: input,
      output: output
    }

    state = run_program(state)
    send(parent_pid, {:halt, self(), state})
  end

  def part1(program_str) do
    program_str
    |> parse
    |> run([1])
    |> List.last()
  end

  def part2(program_str) do
    program_str
    |> parse
    |> run([5])
    |> List.last()
  end
end
