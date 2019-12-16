defmodule AdventOfCode.Day15 do
  alias AdventOfCode.Day05, as: IntCode

  defmodule State do
    defstruct image: %{}, pos: {0, 0}, oxygen: nil, path: []
  end

  def encode_dir(dir) do
    case dir do
      :north -> 1
      :south -> 2
      :west -> 3
      :east -> 4
    end
  end

  def move({x, y}, dir) do
    case dir do
      :north -> {x, y - 1}
      :south -> {x, y + 1}
      :west -> {x - 1, y}
      :east -> {x + 1, y}
    end
  end

  def receive_output() do
    receive do
      {:output, _, x} -> x
      {:halt, _, _} -> raise "expected output, got halt"
    end
  end

  def neighbours({x, y}) do
    [
      {:north, {x, y - 1}},
      {:south, {x, y + 1}},
      {:west, {x - 1, y}},
      {:east, {x + 1, y}}
    ]
  end

  @doc """
  Find all unexplored positions that are reachable.
  """
  def unexplored(image, pos = {x, y}, seen \\ MapSet.new()) do
    seen = MapSet.put(seen, pos)

    neighbours(pos)
    |> Enum.reject(fn {_, pos} -> MapSet.member?(seen, pos) end)
    |> Enum.reject(fn {_, pos} -> Map.get(image, pos) == :wall end)
    |> Enum.map(fn {dir, pos} ->
      if Map.has_key?(image, pos) do
        unexplored(image, pos, seen)
        |> Enum.map(&[dir | &1])
      else
        # Found an unexplored tile.
        [[dir]]
      end
    end)
    |> Enum.concat()
  end

  def find_oxygen(droid, visual, state = %{:path => []}) do
    case unexplored(state.image, state.pos) do
      [] ->
        # nothing more to explore, we're done.
        state

      paths ->
        shortest_path =
          paths
          |> Enum.min_by(&length/1)

        find_oxygen(droid, visual, %{state | path: shortest_path})
    end
  end

  def find_oxygen(droid, visual, state = %{:image => image, :pos => pos, :path => [step | next_path]}) do
    state = %{state | path: next_path }
    pos = move(pos, step)

    send(droid, {:input, encode_dir(step)})

    new_state =
      receive do
        {:output, _, 0} ->
          %{state | image: Map.put(image, pos, :wall)}

        {:output, _, 1} ->
          image = Map.put(image, pos, :empty)
          %{state | image: image, pos: pos}

        {:output, _, 2} ->
          image = Map.put(image, pos, :oxygen)
          %{state | pos: pos, oxygen: pos}
      end

    if visual do
      IO.puts("")

      new_state.image
      |> Map.put(new_state.pos, :droid)
      |> draw_image

      # Process.sleep(250)
    end

    find_oxygen(droid, visual, new_state)
  end

  def spawn_program(program, pid) do
    spawn_link(fn -> IntCode.run_async(program, pid) end)
  end

  def run(program, visual) do
    program
    |> spawn_program(self())
    |> find_oxygen(visual, %State{})
  end

  def draw_image(image) do
    keys = Map.keys(image)

    {{minx, _}, {maxx, _}} = Enum.min_max_by(keys, &elem(&1, 0))
    {{_, miny}, {_, maxy}} = Enum.min_max_by(keys, &elem(&1, 1))

    IO.puts(String.duplicate("-", maxx - minx + 3))

    for y <- miny..maxy do
      line =
        minx..maxx
        |> Enum.map(fn x ->
          case Map.get(image, {x, y}) do
            nil -> " "
            :empty -> "."
            :wall -> "#"
            :droid -> "D"
            :path -> "*"
          end
        end)

      IO.puts(["|", line, "|"])
    end

    IO.puts(String.duplicate("-", maxx - minx + 1))

    maxy - miny + 3
  end

  def part1(program_str, visual \\ false) do
    %{:image => image, :oxygen => oxygen} =
      program_str
      |> IntCode.parse()
      |> run(visual)

    # neighbours
    nbs = fn pos ->
      neighbours(pos)
      |> Enum.map(&elem(&1, 1))
      |> Enum.reject(&(Map.get(image, &1) == :wall))
    end

    # edge cost is constant.
    dist = fn a, b -> 1 end

    # estimated cost = manhattan distance.
    h = fn {ax, ay}, {bx, by} ->
      abs(ax - bx) + abs(ay - by)
    end

    shortest_path = Astar.astar({nbs, dist, h}, {0, 0}, oxygen)

    if visual do
      shortest_path
      |> Enum.reduce(image, fn pos, acc ->
        Map.put(acc, pos, :path)
      end)
      |> draw_image
    end

    length(shortest_path)
  end

  def part2(program_str, visual \\ false) do
  end
end
