use lib::run;
use std::collections::HashMap;

const NUM_ROOMS: usize = 4;
const NUM_SPOTS: usize = 7;

const ROOM_POSITION: [u32; 4] = [3, 5, 7, 9];
const SPOT_POSITION: [u32; 7] = [1, 2, 4, 6, 8, 10, 11];

type Rooms = [Vec<usize>; NUM_ROOMS];

#[derive(Clone, Eq, PartialEq, Hash)]
struct State {
    rooms: Rooms,
    spots: [Option<usize>; NUM_SPOTS],
    depth: usize,
}

type Input = Rooms;

fn parse_input(input: &str) -> Input {
    let pods: Vec<_> = input
        .chars()
        .filter(|c| c.is_alphabetic())
        .map(State::pod_index)
        .collect();

    pods.chunks(4)
        .fold([vec![], vec![], vec![], vec![]], |mut rooms, layer| {
            for (i, &pod) in layer.iter().enumerate() {
                rooms[i].insert(0, pod);
            }
            rooms
        })
}

fn energy_per_step(pod: usize) -> usize {
    let mut res = 1;
    for _ in 0..pod {
        res *= 10;
    }
    return res;
}

impl State {
    fn pod_index(c: char) -> usize {
        (c as u32 - 'A' as u32) as usize
    }

    fn spot_index(spot: u32) -> Option<usize> {
        SPOT_POSITION.iter().position(|&i| i == spot)
    }

    fn is_organized(&self) -> bool {
        self.rooms
            .iter()
            .enumerate()
            .all(|(i, v)| v.len() == self.depth && v.iter().all(|&pod| pod == i))
    }

    /// Rooms that have a pod (on top) that can move.
    fn rooms_with_moveable_pods(&self) -> Vec<usize> {
        self.rooms
            .iter()
            .enumerate()
            .filter_map(|(i, v)| v.iter().find(|&&pod| pod != i).map(|_| i))
            .collect()
    }

    /// Test if the a pod can move into it's room.
    fn can_pod_move_into_room(&self, pod: usize) -> bool {
        // Room has a place left.
        self.rooms[pod].len() < self.depth &&
            // All pods in the room are right.
            self.rooms[pod].iter().all(|&v| v == pod)
    }

    /// Test if a spot position is free. A position can be right above a room,
    /// in which case it is always free.
    fn is_spot_free(&self, spot: u32) -> bool {
        match Self::spot_index(spot) {
            None => true,
            Some(i) => self.spots[i].is_none(),
        }
    }

    /// Test if a pod can be moved between spots.
    fn is_path_free(&self, from: u32, to: u32, exclude_from: bool) -> bool {
        if from == to {
            true
        } else {
            let mut range = match exclude_from {
                false if from < to => from..=to,
                true if from < to => from + 1..=to,
                false => to..=from,
                true => to..=from - 1,
            };
            range.all(|s| self.is_spot_free(s))
        }
    }

    /// Try to move pod into spot.
    fn move_pod_into_spot(&self, pod: usize, from: u32, to: u32) -> Option<State> {
        if self.is_spot_free(to) && self.is_path_free(from, to, false) {
            let mut state = self.clone();
            state.spots[Self::spot_index(to).unwrap()] = Some(pod);
            Some(state)
        } else {
            None
        }
    }

    /// Pods in spots.
    fn pods_in_spots(&self) -> Vec<(u32, usize)> {
        self.spots
            .iter()
            .zip(SPOT_POSITION)
            .filter_map(|(spot, pos)| spot.map(|pod| (pos, pod)))
            .collect()
    }

    fn clear_spot(&mut self, spot: u32) {
        if let Some(i) = Self::spot_index(spot) {
            self.spots[i] = None;
        }
    }
}

fn find_minimal_energy(state: &State, cache: &mut HashMap<State, Option<usize>>) -> Option<usize> {
    // state.print();

    if let Some(&result) = cache.get(&state) {
        return result;
    }

    if state.is_organized() {
        return Some(0);
    }

    let mut paths = vec![];

    // All pods that can move out of a room.
    for room in state.rooms_with_moveable_pods() {
        let mut state = state.clone();
        let pod = state.rooms[room].pop().unwrap();
        let from = ROOM_POSITION[room];
        let steps = state.depth - state.rooms[room].len();

        // Move to all available spots.
        for &to in SPOT_POSITION.iter() {
            if let Some(state) = state.move_pod_into_spot(pod, from, to) {
                let steps = steps + if from < to { to - from } else { from - to } as usize;
                let energy = steps * energy_per_step(pod);
                if let Some(sub_energy) = find_minimal_energy(&state, cache) {
                    paths.push(energy + sub_energy);
                }
            }
        }
    }

    // Try to move pods in spots to their room.
    for (from, pod) in state.pods_in_spots() {
        // Move directly to a room if possible.
        let to = ROOM_POSITION[pod];
        if state.can_pod_move_into_room(pod) && state.is_path_free(from, to, true) {
            let mut steps = if from < to { to - from } else { from - to } as usize;
            steps += state.depth - state.rooms[pod].len();
            let energy = steps * energy_per_step(pod);
            let mut state = state.clone();
            state.rooms[pod].push(pod);
            state.clear_spot(from);
            if let Some(sub_energy) = find_minimal_energy(&state, cache) {
                paths.push(energy + sub_energy);
            }
        }
    }

    let result = paths.iter().cloned().min();
    cache.insert(state.clone(), result);
    return result;
}

fn part_01(input: &Input) -> usize {
    let state = State {
        rooms: input.clone(),
        spots: [None; NUM_SPOTS],
        depth: 2,
    };
    find_minimal_energy(&state, &mut HashMap::new()).unwrap()
}

fn part_02(input: &Input) -> usize {
    let mut rooms = input.clone();

    // Add the following between the first and last rooms:
    //
    //   #D#C#B#A#
    //   #D#B#A#C#
    //
    rooms[0].insert(1, State::pod_index('D'));
    rooms[0].insert(1, State::pod_index('D'));
    rooms[1].insert(1, State::pod_index('C'));
    rooms[1].insert(1, State::pod_index('B'));
    rooms[2].insert(1, State::pod_index('B'));
    rooms[2].insert(1, State::pod_index('A'));
    rooms[3].insert(1, State::pod_index('A'));
    rooms[3].insert(1, State::pod_index('C'));

    let state = State {
        rooms,
        spots: [None; NUM_SPOTS],
        depth: 4,
    };
    find_minimal_energy(&state, &mut HashMap::new()).unwrap()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    #############
    #...........#
    ###B#C#B#D###
      #A#D#C#A#
      #########
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 12521)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 44169)
    }
}
