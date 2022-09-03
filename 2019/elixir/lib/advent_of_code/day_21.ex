defmodule AdventOfCode.Day21 do
  import AdventOfCode.Utils
  alias AdventOfCode.Day05, as: IntCode
  alias AdventOfCode.Day17, as: Ascii

  def print_output(robot, line \\ "") do
    receive do
      {:output, _, res} when res > 255 ->
        res

      {:output, _, ch} ->
        if ch == 10 do
          IO.puts(line)
          print_output(robot, "")
        else
          print_output(robot, line <> List.to_string([ch]))
        end

      {:halt, _, _} ->
        nil
    end
  end

  def instruct_springdroid(robot, mode, script) do
    robot
    |> Ascii.qa("Input instructions:", script)
    |> Ascii.send_line(mode)
    |> Ascii.drain()
  end

  def spawn_program(program, pid) do
    spawn_link(fn -> IntCode.run_async(program, pid) end)
  end

  def format_script([]), do: []

  def format_script([{op, x, y} | program]) do
    op =
      case op do
        :and -> "AND"
        :or -> "OR"
        :not -> "NOT"
      end

    ["#{op} #{x} #{y}" | format_script(program)]
  end

  def part1(input) do
    # !(A AND B AND C) AND D AND (E OR (!E AND H))
    springscript = [
      {:or, "A", "T"},
      {:and, "B", "T"},
      {:and, "C", "T"},
      {:not, "T", "T"},
      {:and, "D", "T"},
      {:or, "T", "J"}
    ]

    input
    |> IntCode.parse()
    |> spawn_program(self())
    |> instruct_springdroid("WALK", format_script(springscript))
    |> print_output()
  end

  def reg_idx("T"), do: 0
  def reg_idx("J"), do: 1

  def reg_idx(reg) when reg >= "A" and reg <= "I" do
    2 + (hd(String.to_charlist(reg)) - hd('A'))
  end

  def compile_op({op, x, y}) do
    op_fun =
      case op do
        :and -> fn a, b -> a and b end
        :or -> fn a, b -> a or b end
        :not -> fn a, _ -> not a end
      end

    x_idx = reg_idx(x)
    y_idx = reg_idx(y)

    fn regs ->
      a = elem(regs, x_idx)
      b = elem(regs, y_idx)
      put_elem(regs, y_idx, op_fun.(a, b))
    end
  end

  def compile_script(program) do
    ops = Enum.map(program, &compile_op/1)

    fn input ->
      regs =
        List.to_tuple(input)
        |> Tuple.insert_at(0, false)
        |> Tuple.insert_at(0, false)

      regs = Enum.reduce(ops, regs, fn op, regs -> op.(regs) end)

      elem(regs, 1)
    end
  end

  def part2(input) do
    # !(A AND B AND C) AND D AND (E OR (!E AND H))
    springscript = [
      {:or, "A", "T"},
      {:and, "B", "T"},
      {:and, "C", "T"},
      {:not, "T", "T"},
      {:and, "D", "T"},
      {:or, "T", "J"},
      {:not, "E", "T"},
      {:and, "H", "T"},
      {:or, "E", "T"},
      {:and, "T", "J"}
    ]

    input
    |> IntCode.parse()
    |> spawn_program(self())
    |> instruct_springdroid("RUN", format_script(springscript))
    |> print_output()
  end
end
