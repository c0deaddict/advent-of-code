defmodule AdventOfCode.Day10 do
  def parse(input) do
    input
    |> String.split("\n", trim: true)
    |> Enum.with_index()
    |> Enum.flat_map(fn {line, y} ->
      line
      |> String.codepoints()
      |> Enum.with_index()
      |> Enum.map(fn
        {".", _} -> nil
        {"#", x} -> {x, y}
      end)
      |> Enum.reject(&is_nil/1)
    end)
    |> MapSet.new()
  end

  def gcd(a, 0), do: a
  def gcd(a, b), do: gcd(b, rem(a, b))

  def points_between({x1, y1}, {x2, y2}) do
    dx = x2 - x1
    dy = y2 - y1

    case abs(gcd(dx, dy)) do
      1 ->
        []

      divisor ->
        stepx = div(dx, divisor)
        stepy = div(dy, divisor)

        for i <- 1..(divisor - 1) do
          {x1 + i * stepx, y1 + i * stepy}
        end
    end
  end

  def find_blocked_by(asteroids, p1, p2) do
    points_between(p1, p2)
    |> Enum.filter(&MapSet.member?(asteroids, &1))
  end

  # There must not be an asteroid on any point between p1 and p2.
  def line_of_sight?(asteroids, p1, p2) do
    length(find_blocked_by(asteroids, p1, p2)) == 0
  end

  # Count to how many other asteroids we have a line of sight.
  def score(pos, asteroids) do
    MapSet.delete(asteroids, pos)
    |> Enum.map(&line_of_sight?(asteroids, pos, &1))
    |> Enum.count(& &1)
  end

  def find_best_asteroid(asteroids) do
    asteroids
    |> Enum.map(fn pos -> {pos, score(pos, asteroids)} end)
    |> Enum.max_by(fn {_, score} -> score end)
  end

  def part1(input) do
    asteroids = parse(input)
    {_, score} = find_best_asteroid(asteroids)
    score
  end

  def dimensions(asteroids) do
    width = Enum.max_by(asteroids, fn {x, _} -> x end)
    height = Enum.max_by(asteroids, fn {_, y} -> y end)
    {width, height}
  end

  def angle(asteroid, center) do
    {ax, ay} = asteroid
    {cx, cy} = center
    dx = ax - cx
    dy = ay - cy
    :math.atan2(dx, dy)
  end

  def vaporize_laser_pass(list) do
    # Vaporize all asteroids that are in line of sight.
    {done, todo} =
      Enum.split_with(list, fn {_, _, blocked_by} ->
        Enum.count(blocked_by) == 0
      end)

    done_set =
      done
      |> Enum.map(&elem(&1, 0))
      |> MapSet.new()

    # Remove vaporized asteroids from the blocked_by sets.
    todo =
      todo
      |> Enum.map(fn {pos, angle, blocked_by} ->
        {pos, angle, MapSet.difference(blocked_by, done_set)}
      end)

    done = Enum.map(done, &elem(&1, 0))

    {done, todo}
  end

  def vaporize_order(center, asteroids) do
    MapSet.delete(asteroids, center)
    |> Enum.map(fn pos ->
      blocked_by = MapSet.new(find_blocked_by(asteroids, pos, center))
      {pos, angle(pos, center), blocked_by}
    end)
    # Sort descending, up angle is first.
    |> Enum.sort_by(fn {_, angle, _} -> angle end, &>=/2)
    |> Stream.unfold(fn
      [] -> nil
      acc -> vaporize_laser_pass(acc)
    end)
    |> Stream.concat()
  end

  def part2(input) do
    asteroids = parse(input)
    {center, _} = find_best_asteroid(asteroids)

    {x, y} =
      vaporize_order(center, asteroids)
      |> Stream.drop(199)
      |> Stream.take(1)
      |> Enum.to_list()
      |> hd

    x * 100 + y
  end
end
