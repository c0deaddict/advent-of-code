use lib::run;

type Board = Vec<usize>;

#[derive(Debug)]
struct Input {
    numbers: Vec<usize>,
    boards: Vec<Board>,
}

fn parse_input(input: &str) -> Input {
    let mut chunks = input.split("\n\n");
    let first = chunks.next().unwrap();
    let numbers = first
        .trim()
        .split(',')
        .map(|s| s.parse().unwrap())
        .collect();

    let boards = chunks
        .map(|c| c.split_whitespace().map(|d| d.parse().unwrap()).collect())
        .collect();

    Input { numbers, boards }
}

fn sum_unmarked(board: &Vec<usize>, rows: &[[bool; 5]; 5]) -> usize {
    let mut sum = 0;
    for (i, val) in board.iter().enumerate() {
        if !rows[i / 5][i % 5] {
            sum += val;
        }
    }
    sum
}

fn part_01(input: &Input) -> usize {
    let mut rows = vec![[[false; 5]; 5]; input.boards.len()];
    let mut cols = vec![[[false; 5]; 5]; input.boards.len()];

    for number in &input.numbers {
        for (i, board) in input.boards.iter().enumerate() {
            for (j, val) in board.iter().enumerate() {
                if val != number {
                    continue;
                }

                let row = j / 5;
                let col = j % 5;
                rows[i][row][col] = true;
                cols[i][col][row] = true;

                if rows[i][row].iter().all(|x| *x) || cols[i][col].iter().all(|x| *x) {
                    // Bingo!
                    return number * sum_unmarked(board, &rows[i]);
                }
            }
        }
    }

    panic!("failed to find answer");
}

fn part_02(input: &Input) -> usize {
    let mut rows = vec![[[false; 5]; 5]; input.boards.len()];
    let mut cols = vec![[[false; 5]; 5]; input.boards.len()];
    let mut wins = vec![false; input.boards.len()];

    for number in &input.numbers {
        for (i, board) in input.boards.iter().enumerate() {
            for (j, val) in board.iter().enumerate() {
                if val != number {
                    continue;
                }

                let row = j / 5;
                let col = j % 5;
                rows[i][row][col] = true;
                cols[i][col][row] = true;

                if rows[i][row].iter().all(|x| *x) || cols[i][col].iter().all(|x| *x) {
                    wins[i] = true;
                    if wins.iter().all(|x| *x) {
                        // Last board to win.
                        return number * sum_unmarked(board, &rows[i]);
                    }
                }
            }
        }
    }

    panic!("failed to find answer");
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

    22 13 17 11  0
     8  2 23  4 24
    21  9 14 16  7
     6 10  3 18  5
     1 12 20 15 19

     3 15  0  2 22
     9 18 13 17  5
    19  8  7 25 23
    20 11 10 24  4
    14 21 16 12  6

    14 21 17 24  4
    10 16 15  9 19
    18  8 23 26 20
    22 11 13  6  5
     2  0 12  3  7
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 4512)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 1924)
    }
}
