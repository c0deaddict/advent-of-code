defmodule AdventOfCode.Day02 do
  def is_halt(program, ip) do
    elem(program, ip) == 99
  end

  def run_op(program, ip) do
    op = elem(program, ip)

    f =
      case op do
        99 -> raise "halt"
        1 -> &+/2
        2 -> &*/2
        _ -> raise "unknown op"
      end

    lhs_addr = elem(program, ip + 1)
    rhs_addr = elem(program, ip + 2)
    res_addr = elem(program, ip + 3)

    lhs = elem(program, lhs_addr)
    rhs = elem(program, rhs_addr)

    put_elem(program, res_addr, apply(f, [lhs, rhs]))
  end

  def run_program(program, ip) do
    if is_halt(program, ip) do
      program
    else
      run_program(run_op(program, ip), ip + 4)
    end
  end

  def part1(program) do
    compute_pair(program, 12, 2)
  end

  def compute_pair(program, noun, verb) do
    program
    |> put_elem(1, noun)
    |> put_elem(2, verb)
    |> run_program(0)
    |> elem(0)
  end

  def cart_product(l1, l2) do
    for i <- l1, j <- l2, do: {i, j}
  end

  def part2(program) do
    {noun, verb} =
      cart_product(0..99, 0..99)
      |> Enum.find(fn {noun, verb} ->
        compute_pair(program, noun, verb) == 19_690_720
      end)

    100 * noun + verb
  end
end
