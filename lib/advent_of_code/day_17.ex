defmodule AdventOfCode.Day17 do
  alias AdventOfCode.Day05, as: IntCode

  def gather_image(robot, lines \\ "") do
    receive do
      {:output, _, ch} ->
        if ch == 10 and String.ends_with?(lines, "\n") do
          lines
        else
          gather_image(robot, lines <> List.to_string([ch]))
        end

      _ ->
        lines
    end
  end

  def spawn_program(program, pid) do
    spawn_link(fn -> IntCode.run_async(program, pid) end)
  end

  def parse_image(lines) do
    lines
    |> String.split("\n", trim: true)
    |> Stream.with_index()
    |> Enum.reduce(%{}, fn {line, y}, image ->
      line
      |> String.codepoints()
      |> Stream.with_index()
      |> Enum.reduce(image, fn
        {".", _}, image ->
          image

        {ch, x}, image ->
          tile =
            case ch do
              "#" -> :scaffold
              "^" -> {:robot, :up}
              "v" -> {:robot, :down}
              "<" -> {:robot, :left}
              ">" -> {:robot, :right}
            end

          Map.put(image, {x, y}, tile)
      end)
    end)
  end

  def neighbours({x, y}) do
    [
      {:north, {x, y - 1}},
      {:south, {x, y + 1}},
      {:west, {x - 1, y}},
      {:east, {x + 1, y}}
    ]
  end

  def find_intersections(image) do
    image
    |> Stream.map(fn {pos, _} -> pos end)
    |> Enum.filter(fn pos ->
      neighbours(pos)
      |> Stream.map(&elem(&1, 1))
      |> Enum.all?(&Map.has_key?(image, &1))
    end)
  end

  def align_param({x, y}), do: x * y

  def calibrate(image) do
    image
    |> find_intersections()
    |> Stream.map(&align_param/1)
    |> Enum.sum()
  end

  def part1(input) do
    input
    |> IntCode.parse()
    |> spawn_program(self())
    |> gather_image()
    |> parse_image()
    |> calibrate()
  end

  def send_line(robot, line) do
    (line <> "\n")
    |> String.to_charlist()
    |> Enum.each(&send(robot, {:input, &1}))
  end

  def drive_robot(robot, image, pos, dir, step \\ 0, input \\ true) do
    receive do
      {:request_input, _} when input ->
        IO.puts("input requested")

        case step do
          # Main:
          0 -> send_line(robot, "A,A,B,C,B,C,B,C")
          # Function A:
          1 -> send_line(robot, "R,8,R,8")
          # Function B:
          2 -> send_line(robot, "R,00000000,R,4,R,8")
          # Function C:
          3 -> send_line(robot, "L,6,L,2")
          # Continuous video feed?
          4 -> send_line(robot, "n")
        end

        drive_robot(robot, image, pos, dir, step + 1, false)

      {:request_input, _} ->
        drive_robot(robot, image, pos, dir, step, input)

      {:output, _, ch} ->
        IO.puts(List.to_string([ch]))
        drive_robot(robot, image, pos, dir, step, true)

      {:halt, _, _} ->
        raise "unexpected halt"
    end
  end

  def part2(input) do
    program = IntCode.parse(input)

    robot =
      program
      |> Map.put(0, 2)
      |> spawn_program(self())

    image =
      robot
      |> gather_image()
      |> parse_image()

    {pos, dir} =
      Enum.find_value(image, fn
        {pos, {:robot, dir}} -> {pos, dir}
        _ -> nil
      end)

    drive_robot(robot, image, pos, dir)
  end
end
