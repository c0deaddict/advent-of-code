defmodule AdventOfCode.Day19 do
  import AdventOfCode.Utils
  alias AdventOfCode.Day05, as: IntCode

  def scan(program, x, y) do
    hd(IntCode.run(program, [x, y]))
  end

  def scan_image(program, w, h) do
    for x <- 0..(w - 1), y <- 0..(h - 1), into: %{} do
      {{x, y}, scan(program, x, y)}
    end
  end

  def draw_image(image) do
    {{minx, miny}, {maxx, maxy}} = map_dimensions(image)

    for y <- miny..maxy do
      line =
        minx..maxx
        |> Enum.map(fn x ->
          case Map.get(image, {x, y}) do
            1 -> "#"
            _ -> "."
          end
        end)

      IO.puts(line)
    end

    image
  end

  def maybe_draw_image(image, false), do: image
  def maybe_draw_image(image, true), do: draw_image(image)

  def part1(input, visual \\ false) do
    input
    |> IntCode.parse()
    |> scan_image(50, 50)
    |> maybe_draw_image(visual)
    |> Enum.count(fn {_, value} -> value == 1 end)
  end

  def scan_find(program, y, x_range, value) do
    Enum.find_index(x_range, fn x -> scan(program, x, y) == value end)
  end

  def inf_range(start) do
    Stream.iterate(start, &(&1 + 1))
  end

  def scan_line(program, y, x_start, x_end) do
    x1 = x_start + scan_find(program, y, x_start..x_end, 1)
    x2 = x_end + scan_find(program, y, inf_range(x_end), 0)
    {x1, x2}
  end

  def scan_stream(program) do
    [
      {0, 0, 1},
      {1, nil, nil}
    ]
    |> Stream.concat(
      Stream.unfold({2, 3, 3}, fn {y, x1, x2} ->
        {x1, x2} = scan_line(program, y, x1, x2)
        {{y, x1, x2}, {y + 1, x1, x2}}
      end)
    )
  end

  def image_from_stream(stream) do
    stream
    |> Stream.map(fn {y, x1, x2} ->
      if x1 == nil or x2 == nil do
        []
      else
        for x <- x1..(x2 - 1) do
          {{x, y}, 1}
        end
      end
    end)
    |> Stream.concat()
    |> Map.new()
  end

  def part2(input) do
    program =
      input
      |> IntCode.parse()

    program
    |> scan_stream()
    |> Stream.drop(2)
    |> Stream.chunk_every(100, 1)
    |> Stream.map(fn win -> {hd(win), List.last(win)} end)
    |> Stream.drop_while(fn {top, bottom} ->
      {_, _, tx2} = top
      {_, bx1, _} = bottom
      bx1 > tx2 - 100
    end)
    |> Stream.take(1)
    |> Stream.map(&IO.inspect/1)
    |> Enum.map(fn {{y, _, x}, _} -> (x - 100) * 10000 + y end)
    |> hd
  end
end
