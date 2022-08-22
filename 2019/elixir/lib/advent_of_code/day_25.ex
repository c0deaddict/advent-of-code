defmodule AdventOfCode.Day25 do
  alias AdventOfCode.Day05, as: IntCode
  alias AdventOfCode.Day17, as: Ascii
  import AdventOfCode.Utils, only: [permutations: 2]
  alias Graph.Edge

  @debug false

  def spawn_program(program, pid) do
    spawn_link(fn -> IntCode.run_async(program, pid) end)
  end

  def debug(data) do
    if @debug, do: IO.puts(data)
    data
  end

  def read_question(output \\ []) do
    receive do
      {:output, _, ch} ->
        read_question([ch | output])

      {:request_input, _} when output == [] ->
        read_question(output)

      {:request_input, _} ->
        {:question, debug(Enum.reverse(output) |> List.to_string())}

      {:halt, _, _} ->
        {:halt, debug(Enum.reverse(output) |> List.to_string())}
    end
  end

  def parse_question({:question, question}) do
    [room, story, "Doors here lead:" | rest] =
      question
      |> String.split("\n")
      |> Enum.map(&String.trim/1)
      |> Enum.filter(&(&1 != ""))

    room = room |> String.trim("==") |> String.trim()

    {doors, rest} = Enum.split_while(rest, &String.starts_with?(&1, "- "))
    doors = doors |> Enum.map(&String.trim(&1, "- "))

    {items, message} =
      case rest do
        ["Items here:" | items] ->
          items =
            items
            |> Enum.reverse()
            |> tl
            |> Enum.map(&String.trim(&1, "- "))

          {items, nil}

        ["Command?"] ->
          {[], nil}

        [message | _rest] ->
          {[], message}
      end

    if message != nil do
      {:bounced, room, story, doors, message}
    else
      {:enter, room, story, doors, items}
    end
  end

  def send_line(robot, answer, read \\ false) do
    if read do
      {:question, _} = read_question()
    end

    Ascii.send_line(robot, debug(answer))
  end

  def find_key(map, value) do
    map
    |> Enum.find(fn {_, v} -> v == value end)
    |> elem(0)
  end

  def inverse_door(door) do
    case door do
      "north" -> "south"
      "east" -> "west"
      "south" -> "north"
      "west" -> "east"
    end
  end

  def safe_item(item) do
    case item do
      "molten lava" -> false
      "giant electromagnet" -> false
      "escape pod" -> false
      "photons" -> false
      "infinite loop" -> false
      _ -> true
    end
  end

  def traverse(robot, graph \\ Map.new(), prev \\ nil, inventory \\ MapSet.new()) do
    {result, room, story, doors, items} =
      read_question()
      |> parse_question()

    send_line(robot, "inv")

    graph =
      case prev do
        {prev_room, prev_door} ->
          Map.update!(graph, prev_room, fn {story, items, doors} ->
            {story, items, Map.put(doors, prev_door, room)}
          end)

        nil ->
          graph
      end

    cond do
      result == :bounced ->
        # We get rejected, probably from weight detection.
        {room, graph, inventory}

      Map.has_key?(graph, room) ->
        # We have visited this room before.
        {room, graph, inventory}

      true ->
        # Take all items.
        inventory =
          Enum.reduce(items, inventory, fn item, inventory ->
            if safe_item(item) do
              send_line(robot, "take #{item}", true)
              MapSet.put(inventory, item)
            else
              inventory
            end
          end)

        graph = Map.put(graph, room, {story, items, Map.new()})

        {graph, inventory} =
          Enum.reduce(
            doors,
            {graph, inventory},
            fn door, {graph, inventory} ->
              # Enter door.
              send_line(robot, door, true)
              {next_room, graph, inventory} = traverse(robot, graph, {room, door}, inventory)

              graph =
                Map.update!(graph, room, fn {story, items, doors} ->
                  {story, items, Map.put(doors, door, next_room)}
                end)

              # Go back.
              send_line(robot, inverse_door(door), true)
              {graph, inventory}
            end
          )

        {room, graph, inventory}
    end
  end

  def dijkstra(graph, start, target) do
    Enum.reduce(graph, Graph.new(), fn {from, {_story, _items, doors}}, acc ->
      Enum.reduce(doors, acc, fn {_, to}, acc ->
        Graph.add_edge(acc, Edge.new(from, to, weight: 1))
      end)
    end)
    |> Graph.dijkstra(start, target)
  end

  def path_to_steps(graph, [from | rest]), do: path_to_steps(graph, from, rest, [])
  def path_to_steps(_graph, _from, [], acc), do: acc

  def path_to_steps(graph, from, [to | rest], acc) do
    {_story, _items, doors} = graph[from]
    path_to_steps(graph, to, rest, [find_key(doors, to) | acc])
  end

  def drop_all(robot, inventory) do
    for item <- inventory do
      send_line(robot, "drop #{item}", true)
    end
  end

  def part1(input) do
    robot = input |> IntCode.parse() |> spawn_program(self())
    {start, graph, inventory} = traverse(robot)

    # Compute the shortest path to the pressure sensitive floor.
    target = "Pressure-Sensitive Floor"
    reverse_steps = path_to_steps(graph, dijkstra(graph, start, target))

    # Walk up to the room before pressure sensitive floor.
    [enter | reverse_steps] = reverse_steps

    Enum.reverse(reverse_steps)
    |> Enum.each(fn step ->
      send_line(robot, step, true)
    end)

    # Drop all inventory on the floor.
    inventory = Enum.to_list(inventory)
    drop_all(robot, inventory)

    # Try each permutation of inventory.
    1..length(inventory)
    |> Stream.map(&permutations(inventory, &1))
    |> Stream.concat()
    |> Enum.find_value(fn inventory ->
      # Pick up items from the floor.
      for item <- inventory do
        send_line(robot, "take #{item}", true)
      end

      # Try to enter the room.
      send_line(robot, enter, true)

      case read_question() do
        {:question, _question} ->
          send_line(robot, "inv", false)
          drop_all(robot, inventory)
          nil

        # Found it!
        {:halt, output} ->
          output
      end
    end)
    |> IO.puts()
  end

  def part2(_input) do
  end
end
