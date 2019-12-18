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
              "^" -> {:robot, :north}
              "v" -> {:robot, :south}
              ">" -> {:robot, :east}
              "<" -> {:robot, :west}
            end

          Map.put(image, {x, y}, tile)
      end)
    end)
  end

  def neighbors({x, y}) do
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
      neighbors(pos)
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

  def read_line(result \\ []) do
    receive do
      {:output, _, 10} ->
        result |> Enum.reverse() |> List.to_string()

      {:output, _, ch} ->
        read_line([ch | result])

      {:halt, _, _} ->
        raise "unexpected halt, expected a line of output"
    end
  end

  def qa(robot, question, answer) do
    case read_line() do
      ^question -> IO.puts("Q: #{question}")
      "" -> raise read_line()
      err -> raise err
    end

    IO.puts("A: #{answer}")
    send_line(robot, answer)

    # For chaining.
    robot
  end

  def move({x, y}, dir) do
    case dir do
      :north -> {x, y - 1}
      :south -> {x, y + 1}
      :west -> {x - 1, y}
      :east -> {x + 1, y}
    end
  end

  def continue_stretch?(image, next_pos, visited) do
    Map.has_key?(image, next_pos) and not MapSet.member?(visited, next_pos)
  end

  def first_new_neighbor(image, pos, visited) do
    neighbors(pos)
    |> Enum.find(fn {_, pos} ->
      Map.has_key?(image, pos) and
        not MapSet.member?(visited, pos)
    end)
  end

  def move_across_intersection(image, pos, visited) do
    neighbors(pos)
    |> Enum.filter(fn {_, pos} -> Map.has_key?(image, pos) end)
    |> Enum.map(fn {dir, pos} -> {dir, move(pos, dir)} end)
    |> Enum.find(fn {_, pos} ->
      Map.has_key?(image, pos) and
        not MapSet.member?(visited, pos)
    end)
  end

  def find_path(image, pos, dir, visited, path) do
    visited = MapSet.put(visited, pos)

    cond do
      continue_stretch?(image, next_pos=move(pos, dir), visited) ->
        # Go straight for as long as possible.
        # Increase distance of current stretch.
        [{^dir, steps} | rest] = path
        path = [{dir, steps + 1} | rest]
        find_path(image, next_pos, dir, visited, path)

      next = first_new_neighbor(image, pos, visited) ->
        # Go to the first neighbor we have not visited yet.
        {next_dir, next_pos} = next
        path = [{next_dir, 1} | path]
        find_path(image, next_pos, next_dir, visited, path)

      next = move_across_intersection(image, pos, visited) ->
        # If we have visited all direct neighbors, we are at an intersection.
        # Move over the intersection, increase steps by 2.
        {^dir, next_pos} = next
        [{^dir, steps} | rest] = path
        path =[{dir, steps + 2} | rest]
        find_path(image, next_pos, dir, visited, path)

      true ->
        # No more options, we should be done.
        all_pos = MapSet.new(Map.keys(image))
        empty = MapSet.new()
        ^empty = MapSet.difference(all_pos, visited)

        Enum.reverse(path)
    end
  end

  def draw_path(image, _, []), do: image
  def draw_path(image, pos, [{_, 0} | path]), do: draw_path(image, pos, path)
  def draw_path(image, pos, [{dir, steps} | path]) do
    image = Map.put(image, pos, :path)
    draw_path(image, move(pos, dir), [{dir, steps - 1} | path])
  end

  def draw_image_map(image) do
    keys = Map.keys(image)

    {{minx, _}, {maxx, _}} = Enum.min_max_by(keys, &elem(&1, 0))
    {{_, miny}, {_, maxy}} = Enum.min_max_by(keys, &elem(&1, 1))

    for y <- miny..maxy do
      line =
        minx..maxx
        |> Enum.map(fn x ->
          case Map.get(image, {x, y}) do
            nil -> " "
            :path -> "$"
            {:robot, _} -> "X"
            _ -> "#"
          end
        end)

      IO.puts(line)
    end

    maxy - miny + 3
  end

  def drive_robot(robot, image, pos, dir) do
    path = find_path(image, pos, dir, MapSet.new(), [{dir, 0}])
    draw_path(image, pos, path)
    |> draw_image_map

    robot
    |> qa("Main:", "A,A,B,B,C,C,A,B,C")
    |> qa("Function A:", "R,8,R,8")
    |> qa("Function B:", "R,00000,R,4,R,8")
    |> qa("Function C:", "L,6,L,2")
    |> qa("Continuous video feed?", "n")

    robot
  end

  def drain(pid) do
    receive do
      {:request_input, _} ->
        drain(pid)
    after
      1 ->
        pid
    end
  end

  def draw_image(image) do
    image
    |> String.split("\n")
    |> Enum.each(&IO.puts/1)

    image
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
      |> draw_image()
      |> parse_image()

    {pos, dir} =
      Enum.find_value(image, fn
        {pos, {:robot, dir}} -> {pos, dir}
        _ -> nil
      end)

    robot
    |> drive_robot(image, pos, dir)
    |> drain()
    |> gather_image()
    |> draw_image()

    nil
  end
end
