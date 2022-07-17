defmodule AdventOfCode.Day13 do
  import AdventOfCode.Utils
  alias AdventOfCode.Day05, as: IntCode

  defmodule State do
    defstruct image: %{}, ball: nil, score: nil, draw_lines: nil
  end

  @tiles %{
    0 => :empty,
    1 => :wall,
    2 => :block,
    3 => :paddle,
    4 => :ball
  }

  def receive_output() do
    receive do
      {:output, _, x} -> x
      {:halt, _, _} -> raise "expected output, got halt"
    end
  end

  @doc """
  Predict the x position of the ball when it finally reaches the paddle.
  """
  def predict_ball({x, y}, _, _, paddle, path) when y == paddle - 1, do: {x, path}
  def predict_ball({_, y}, _, _, paddle, _) when y >= paddle, do: raise("prediction error")

  def predict_ball({x, y}, dir = {dx, dy}, image, paddle, path) do
    path = [{x, y} | path]

    hit =
      [
        {{x + dx, y}, {-dx, dy}},
        {{x, y + dy}, {dx, -dy}},
        {{x + dx, y + dy}, {-dx, -dy}}
      ]
      |> Enum.find_value(fn {pos, dir} ->
        case Map.get(image, pos) do
          :block ->
            {Map.put(image, pos, :empty), dir}

          :wall ->
            {image, dir}

          _ ->
            nil
        end
      end)

    case hit do
      nil ->
        predict_ball({x + dx, y + dy}, dir, image, paddle, path)

      {image, dir} ->
        predict_ball({x, y}, dir, image, paddle, path)
    end
  end

  def player(pid, visual, state = %{:image => image}) do
    receive do
      {:output, _, x} ->
        y = receive_output()
        value = receive_output()

        if x == -1 and y == 0 do
          player(pid, visual, %{state | score: value})
        else
          player(pid, visual, %{state | image: Map.put(image, {x, y}, @tiles[value])})
        end

      {:request_input, _} ->
        # Find the ball.
        ball = find_key(image, :ball)

        draw_lines =
          if state.ball != nil do
            # Predict the direction of the ball.
            {bx1, by1} = state.ball
            {bx2, by2} = ball
            dir = {bx2 - bx1, by2 - by1}

            # Move paddle towards projected position of ball.
            {px, py} = find_key(image, :paddle)
            {target, path} = predict_ball(ball, dir, image, py, [])

            cond do
              px < target -> send(pid, {:input, 1})
              px > target -> send(pid, {:input, -1})
              true -> send(pid, {:input, 0})
            end

            if visual do
              if state.draw_lines != nil do
                IO.puts(IO.ANSI.cursor_up(state.draw_lines + 1))
              end

              lines =
                path
                |> Enum.reduce(image, fn pos, acc ->
                  Map.put(acc, pos, :path)
                end)
                |> Map.put(ball, :ball)
                |> Map.put({target, py}, :target)
                |> Map.put({px, py}, :paddle)
                |> draw_image

              IO.puts("")
              IO.puts("Score: #{state.score}")
              Process.sleep(50)

              lines + 2
            end
          else
            # Not sure yet where the ball is going.
            send(pid, {:input, 0})
            nil
          end

        player(pid, visual, %{state | ball: ball, draw_lines: draw_lines})

      {:halt, _, _} ->
        state
    end
  end

  def spawn_program(program, pid) do
    spawn_link(fn -> IntCode.run_async(program, pid) end)
  end

  def run(program, visual) do
    program
    |> spawn_program(self())
    |> player(visual, %State{})
  end

  def draw_image(image) do
    {{minx, miny}, {maxx, maxy}} = map_dimensions(image)

    for y <- miny..maxy do
      minx..maxx
      |> Enum.map(fn x ->
        case Map.get(image, {x, y}, :empty) do
          :empty -> " "
          :wall -> "#"
          :block -> "X"
          :paddle -> "_"
          :ball -> "o"
          :target -> "%"
          :path -> "."
        end
      end)
      |> IO.puts()
    end

    maxy - miny + 1
  end

  def part1(program_str) do
    %{:image => image} =
      program_str
      |> IntCode.parse()
      |> run(false)

    image |> Enum.count(fn {_, tile} -> tile == :block end)
  end

  def part2(program_str, visual \\ false) do
    %{:score => score} =
      program_str
      |> IntCode.parse()
      |> Map.put(0, 2)
      |> run(visual)

    score
  end
end
