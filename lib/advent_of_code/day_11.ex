defmodule AdventOfCode.Day11 do
  import AdventOfCode.Utils
  alias AdventOfCode.Day05, as: IntCode

  defmodule State do
    defstruct pos: {0, 0}, dir: :up, image: %{}, painted: 0
  end

  def move({x, y}, dir) do
    case dir do
      :up -> {x, y - 1}
      :down -> {x, y + 1}
      :left -> {x - 1, y}
      :right -> {x + 1, y}
    end
  end

  def turn_left(dir) do
    case dir do
      :up -> :left
      :left -> :down
      :down -> :right
      :right -> :up
    end
  end

  def turn_right(dir) do
    case dir do
      :up -> :right
      :right -> :down
      :down -> :left
      :left -> :up
    end
  end

  def painter(pid, state = %{:image => image, :pos => pos}) do
    color = Map.get(image, pos)
    send(pid, {:input, color || 0})

    receive do
      {:output, _, new_color} ->
        unique = if color != nil, do: 0, else: 1
        image = Map.put(image, pos, new_color)
        state = %{state | image: image, painted: state.painted + unique}
        painter_wait_turn(pid, state)

      {:halt, _, _} ->
        state
    end
  end

  def painter_wait_turn(pid, state = %{:dir => dir, :pos => pos}) do
    dir =
      receive do
        {:output, _, 0} ->
          turn_left(dir)

        {:output, _, 1} ->
          turn_right(dir)

        {:halt, _, _} ->
          raise "expected a turn"
      end

    pos = move(pos, dir)
    state = %{state | dir: dir, pos: pos}

    painter(pid, state)
  end

  def spawn_robot(program, pid) do
    spawn_link(fn -> IntCode.run_async(program, pid) end)
  end

  def run_painter(program_str, image) do
    IntCode.parse(program_str)
    |> spawn_robot(self())
    |> painter(%State{image: image})
  end

  def part1(program_str) do
    run_painter(program_str, %{}).painted
  end

  def draw_image(image) do
    {{minx, miny}, {maxx, maxy}} = map_dimensions(image)

    for y <- miny..maxy do
      minx..maxx
      |> Enum.map(fn x ->
        case Map.get(image, {x, y}, 0) do
          0 -> "."
          1 -> "#"
        end
      end)
      |> IO.puts()
    end
  end

  def part2(program_str) do
    run_painter(program_str, %{{0, 0} => 1})
    |> Map.get(:image)
    |> draw_image
  end
end
