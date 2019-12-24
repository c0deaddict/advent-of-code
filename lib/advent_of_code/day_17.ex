defmodule AdventOfCode.Day17 do
  import AdventOfCode.Utils
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

  def neighbors_dirs({x, y}) do
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
      neighbors_dirs(pos)
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
    neighbors_dirs(pos)
    |> Enum.find(fn {_, pos} ->
      Map.has_key?(image, pos) and
        not MapSet.member?(visited, pos)
    end)
  end

  def move_across_intersection(image, pos, visited) do
    neighbors_dirs(pos)
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
      continue_stretch?(image, next_pos = move(pos, dir), visited) ->
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
        path = [{dir, steps + 2} | rest]
        find_path(image, next_pos, dir, visited, path)

      true ->
        # No more options, we should be done.
        all_pos = MapSet.new(Map.keys(image))
        empty = MapSet.new()
        ^empty = MapSet.difference(all_pos, visited)

        # TODO Step to our current position? or do we fall over the edge?
        # [{^dir, steps} | rest] = path
        # path = [{dir, steps + 1} | rest]
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
    {{minx, miny}, {maxx, maxy}} = map_dimensions(image)

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

  def find_repetitions(list, pattern) do
    list
    |> find_repetitions(pattern, length(pattern), 0, [])
    |> Enum.reverse()
  end

  def find_repetitions([], _, _, _, acc), do: acc

  def find_repetitions(list, pattern, len, offset, acc) do
    case Enum.split(list, len) do
      {^pattern, rest} ->
        find_repetitions(rest, pattern, len, offset + len, [offset | acc])

      _ ->
        find_repetitions(tl(list), pattern, len, offset + 1, acc)
    end
  end

  def sublists(list, min_len \\ 1, max_len \\ nil) do
    len = length(list)
    max_len = max_len || len

    for j <- min_len..max_len, i <- 0..(len - j) do
      Enum.slice(list, i, j)
    end
  end

  def encode_pattern(pattern) do
    pattern |> Enum.join(",")
  end

  def permutations([], _), do: [[]]
  def permutations(_, 0), do: [[]]

  def permutations(list, n) do
    for elem <- list,
        rest <- permutations(list -- [elem], n - 1) do
      [elem | rest]
    end
  end

  def permutations_in_order(list), do: permutations_in_order(list, length(list))

  def permutations_in_order(_, 0), do: [[]]
  def permutations_in_order([], _), do: []

  def permutations_in_order([head | tail], n) do
    for rest <- permutations_in_order(tail, n - 1) do
      [head | rest]
    end ++
      permutations_in_order(tail, n)
  end

  def cover_all?(slices, len) do
    {true, len - 1} ==
      slices
      |> Enum.sort_by(&elem(&1, 0))
      |> Enum.reduce({true, 0}, fn {start, end_}, {res, prev} ->
        {res and start == prev, end_}
      end)
  end

  def cover_permutations(slices, pos, len)
  def cover_permutations([], len, len), do: [[]]
  def cover_permutations([], _, _), do: []

  def cover_permutations([{pattern_idx, start, end_} | tail], pos, len) do
    if start == pos do
      # Take current slice and call recursively.
      for rest <- cover_permutations(tail, end_, len),
          do: [pattern_idx | rest]
    else
      []
    end ++ cover_permutations(tail, pos, len)
  end

  def compress(list) do
    sublists(list, 1, 10)
    |> Stream.filter(fn pattern ->
      String.length(encode_pattern(pattern)) <= 20
    end)
    |> Enum.map(fn pattern ->
      {pattern, find_repetitions(list, pattern)}
    end)
    |> permutations_in_order(3)
    |> Stream.map(fn patterns ->
      slices =
        patterns
        |> Stream.with_index()
        |> Stream.flat_map(fn {{pattern, slices}, pattern_idx} ->
          len = length(pattern)
          Enum.map(slices, &{pattern_idx, &1, &1 + len})
        end)
        |> Enum.sort_by(&elem(&1, 1))

      patterns = patterns |> Enum.map(&elem(&1, 0))
      {patterns, slices}
    end)
    |> Stream.filter(fn {_, slices} ->
      length(slices) <= 10
    end)
    |> Stream.map(fn {patterns, slices} ->
      slices
      |> cover_permutations(0, length(list))
      |> Enum.map(fn idxs -> {patterns, idxs} end)
    end)
    |> Stream.concat()
    |> Enum.take(1)
    |> hd
  end

  def drive_robot(robot, image, pos, dir) do
    # Idea: build up patterns while walking, at each step check if
    # a previous pattern can be used. If so, apply it and branch.
    # Also branch without applying it, and branch at each intersection
    # for the possible routes.
    path = find_path(image, pos, dir, MapSet.new(), [{dir, 0}])

    draw_path(image, pos, path)
    |> draw_image_map

    {_, first_steps} = hd(path)

    path =
      path
      |> Stream.zip(tl(path))
      |> Enum.flat_map(fn {{from_dir, _}, {to_dir, steps}} ->
        turn =
          case {from_dir, to_dir} do
            {:north, :east} -> "R"
            {:east, :south} -> "R"
            {:south, :west} -> "R"
            {:west, :north} -> "R"
            {:north, :west} -> "L"
            {:west, :south} -> "L"
            {:south, :east} -> "L"
            {:east, :north} -> "L"
          end

        [turn, Integer.to_string(steps)]
      end)

    path =
      if first_steps != 0 do
        [Integer.to_string(first_steps) | path]
      else
        path
      end

    {[a, b, c], main} = compress(path)
    main = Enum.map(main, &Enum.at(["A", "B", "C"], &1))

    robot
    |> qa("Main:", encode_pattern(main))
    |> qa("Function A:", encode_pattern(a))
    |> qa("Function B:", encode_pattern(b))
    |> qa("Function C:", encode_pattern(c))
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

    receive do
      {:output, _, score} -> score
    after
      3_000 -> nil
    end
  end
end
