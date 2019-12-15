defmodule AdventOfCode.Day14 do
  def parse_part(str) do
    [amount_str, chemical] = String.split(str, " ", trim: true)
    {String.to_integer(amount_str), chemical}
  end

  def parse_reaction(line) do
    [input_str, output_str] = String.split(line, "=>", trim: true)

    inputs =
      input_str
      |> String.split(",", trim: true)
      |> Enum.map(&parse_part/1)

    {inputs, parse_part(output_str)}
  end

  def parse(input) do
    input
    |> String.split("\n", trim: true)
    |> Enum.map(&parse_reaction/1)
  end

  def output_map(reactions) do
    reactions
    |> Enum.reduce(%{}, fn {inputs, {amount, chemical}}, acc ->
      case Map.get(acc, chemical) do
        nil -> Map.put(acc, chemical, {amount, inputs})
        _ -> raise "chemical #{chemical} is produced by multiple reactions"
      end
    end)
  end

  def do_resolve(_, "ORE", amount, acc) do
    Map.update(acc, "ORE", -amount, &(&1 - amount))
  end

  def do_resolve(output_map, chem, amount, acc) do
    {out_amount, inputs} = Map.get(output_map, chem)
    num = div(amount + out_amount - 1, out_amount)
    excess = out_amount * num - amount

    inputs
    |> Enum.reduce(acc, fn {in_amount, in_chem}, acc ->
      resolve(output_map, in_chem, num * in_amount, acc)
    end)
    |> Map.update(chem, excess, &(&1 + excess))
  end

  def resolve(output_map, chem, amount, acc \\ %{}) do
    case Map.get(acc, chem, 0) do
      leftover when leftover >= amount ->
        Map.update!(acc, chem, &(&1 - amount))

      leftover when leftover > 0 ->
        acc = Map.delete(acc, chem)
        do_resolve(output_map, chem, amount - leftover, acc)

      _ ->
        do_resolve(output_map, chem, amount, acc)
    end
  end

  def part1(input) do
    parse(input)
    |> output_map()
    |> resolve("FUEL", 1)
    |> Map.get("ORE")
    |> abs
  end

  def part2(args) do
  end
end
