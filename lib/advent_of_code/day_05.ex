defmodule AdventOfCode.Day05 do
  def parse(program_str) do
    program_str
    |> String.trim()
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
    |> List.to_tuple()
  end

  def is_halt(program, ip) do
    elem(program, ip) == 99
  end

  def op_add({program, io, ip}, lhs, rhs, res) do
    {put_elem(program, res, lhs + rhs), io, ip + 4}
  end

  def op_multiply({program, io, ip}, lhs, rhs, res) do
    {put_elem(program, res, lhs * rhs), io, ip + 4}
  end

  def op_input({program, {input, output}, ip}, res) do
    {value, new_input} = input.()
    program = put_elem(program, res, value)
    {program, {new_input || input, output}, ip + 2}
  end

  def op_output({program, {input, output}, ip}, res) do
    value = elem(program, res)

    if value == nil do
      raise "output nil is not allowed"
    end

    new_output = output.(value)
    {program, {input, new_output || output}, ip + 2}
  end

  def op_jump_if_true({program, io, ip}, test, branch) do
    ip = if test != 0, do: branch, else: ip + 3
    {program, io, ip}
  end

  def op_jump_if_false({program, io, ip}, test, branch) do
    ip = if test == 0, do: branch, else: ip + 3
    {program, io, ip}
  end

  def op_less_than({program, io, ip}, a, b, out) do
    value = if a < b, do: 1, else: 0
    program = put_elem(program, out, value)
    {program, io, ip + 4}
  end

  def op_equals({program, io, ip}, a, b, out) do
    value = if a == b, do: 1, else: 0
    program = put_elem(program, out, value)
    {program, io, ip + 4}
  end

  def run_op({program, io, ip}) do
    opcode = elem(program, ip)

    {op, num_args, out_args} =
      case rem(opcode, 100) do
        1 -> {&op_add/4, 3, [2]}
        2 -> {&op_multiply/4, 3, [2]}
        3 -> {&op_input/2, 1, [0]}
        4 -> {&op_output/2, 1, [0]}
        5 -> {&op_jump_if_true/3, 2, []}
        6 -> {&op_jump_if_false/3, 2, []}
        7 -> {&op_less_than/4, 3, [2]}
        8 -> {&op_equals/4, 3, [2]}
        99 -> raise "halt"
        x -> raise "unknown op #{x}"
      end

    {args, _} =
      1..num_args
      |> Enum.map(&elem(program, ip + &1))
      |> Enum.with_index()
      |> Enum.map_reduce(div(opcode, 100), fn {arg, i}, modes ->
        is_out = Enum.member?(out_args, i)

        arg =
          case rem(modes, 10) do
            # position mode, but not for out args
            0 when not is_out -> elem(program, arg)
            # immediate mode
            0 -> arg
            1 -> arg
            x -> raise "unknown mode #{x}"
          end

        {arg, div(modes, 10)}
      end)

    apply(op, [{program, io, ip} | args])
  end

  def run_program({program, io, ip}) do
    if is_halt(program, ip) do
      {program, io, ip}
    else
      run_program(run_op({program, io, ip}))
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
    io = {input_from_list(input_list), output_to_list([])}
    state = run_program({program, io, 0})
    {_, {_, output}, _} = state
    Enum.reverse(output.(nil))
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
