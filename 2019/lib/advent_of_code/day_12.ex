defmodule AdventOfCode.Day12 do
  def parse(input) do
    input
    |> String.split("\n", trim: true)
    |> Enum.map(fn line ->
      pos =
        Regex.run(~r/<x=(-?\d+), y=(-?\d+), z=(-?\d+)>$/, line)
        |> tl
        |> Enum.map(&String.to_integer/1)
        |> List.to_tuple()

      velocity = {0, 0, 0}
      {pos, velocity}
    end)
  end

  def gravity_axis(a, b) do
    cond do
      a == b -> 0
      a < b -> +1
      a > b -> -1
    end
  end

  def gravity_between({from, _}, {to, _}) do
    {x1, y1, z1} = from
    {x2, y2, z2} = to
    gx = gravity_axis(x1, x2)
    gy = gravity_axis(y1, y2)
    gz = gravity_axis(z1, z2)
    {gx, gy, gz}
  end

  def vector_add({x1, y1, z1}, {x2, y2, z2}) do
    {x1 + x2, y1 + y2, z1 + z2}
  end

  def gravity(target, moons) do
    (moons -- [target])
    |> Enum.map(&gravity_between(target, &1))
    |> Enum.reduce(&vector_add/2)
  end

  def simulate(moons) do
    Stream.unfold(moons, fn prev_moons ->
      # Update velocity by applying gravity.
      next_moons =
        prev_moons
        |> Enum.map(fn target = {pos, velocity} ->
          g = gravity(target, prev_moons)
          {pos, vector_add(velocity, g)}
        end)
        # Update positions by applying velocity.
        |> Enum.map(fn {pos, velocity} ->
          {vector_add(pos, velocity), velocity}
        end)

      {next_moons, next_moons}
    end)
  end

  def vector_len({x, y, z}) do
    abs(x) + abs(y) + abs(z)
  end

  def energy({pos, velocity}) do
    vector_len(pos) * vector_len(velocity)
  end

  def total_energy(moons) do
    moons
    |> Enum.map(&energy/1)
    |> Enum.sum()
  end

  def simulate_for(moons, steps) do
    simulate(moons)
    |> Stream.drop(steps - 1)
    |> Stream.take(1)
    |> Enum.to_list()
    |> hd
  end

  def part1(input) do
    parse(input)
    |> simulate_for(1000)
    |> total_energy
  end

  def find_cycle(stream) do
    stream
    |> Enum.reduce_while(Map.new(), fn i, acc ->
      case Map.get(acc, i) do
        nil ->
          {:cont, Map.put(acc, i, map_size(acc))}

        start ->
          {:halt, {start, map_size(acc)}}
      end
    end)
  end

  def select_dim(moons, dim) do
    moons
    |> Enum.map(fn {pos, velocity} ->
      {elem(pos, dim), elem(velocity, dim)}
    end)
  end

  def find_cycle_per_dim(simulation) do
    0..2
    |> Enum.map(fn dim ->
      simulation
      |> Stream.map(&select_dim(&1, dim))
      |> find_cycle
    end)
  end

  def gcd(a, 0), do: a
  def gcd(a, b), do: gcd(b, rem(a, b))
  def gcd(a, b, c), do: gcd(a, gcd(b, c))

  def lcm(a, b), do: div(a * b, gcd(a, b))

  def lcm(a, b, c) do
    lcm_bc = lcm(b, c)
    div(a * lcm_bc, gcd(a, lcm_bc))
  end

  def part2(input) do
    [{0, x}, {0, y}, {0, z}] =
      parse(input)
      |> simulate
      |> find_cycle_per_dim

    lcm(x, y, z)
  end
end
