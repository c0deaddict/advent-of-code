use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap, HashSet};
use std::hash::Hash;

#[derive(Copy, Clone, Eq, PartialEq)]
struct NodeWithCost<N: Eq> {
    cost: usize,
    node: N,
}

impl<N: Eq> Ord for NodeWithCost<N> {
    fn cmp(&self, other: &Self) -> Ordering {
        other.cost.cmp(&self.cost)
    }
}

impl<N: Eq> PartialOrd for NodeWithCost<N> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn reconstruct_path<'a, N: Eq + Hash + Copy>(
    came_from: HashMap<N, N>,
    node: &'a N,
) -> Vec<N> {
    let mut path = Vec::new();
    while let Some(node) = came_from.get(&node) {
        path.push(*node);
    }
    path.reverse();
    return path;
}

// https://en.wikipedia.org/wiki/A*_search_algorithm
pub fn astar<'a, N: Eq + Hash + Copy>(
    start: &'a N,
    adjacent: impl Fn(&N) -> Vec<(usize, N)>,
    h: impl Fn(&N) -> usize,
    is_target: impl Fn(&N) -> bool,
) -> Vec<N> {
    let mut open_queue = BinaryHeap::new();
    let mut open_set = HashSet::from([*start]);
    let mut g_score = HashMap::from([(*start, 0)]);
    let mut came_from = HashMap::new();
    open_queue.push(NodeWithCost {
        cost: 0,
        node: *start,
    });

    while let Some(NodeWithCost { cost: _, node }) = open_queue.pop() {
        if is_target(&node) {
            return reconstruct_path(came_from, &node);
        }

        open_set.remove(&node);

        for (time, child) in adjacent(&node) {
            let g = g_score[&node] + time;
            if !g_score.contains_key(&child) || g < *g_score.get(&child).unwrap() {
                g_score.insert(child, g);
                let f = g + h(&child);
                if !open_set.contains(&child) {
                    open_set.insert(child);
                    open_queue.push(NodeWithCost {
                        cost: f,
                        node: child,
                    });
                }
                came_from.insert(child, node);
            }
        }
    }

    unreachable!("The loop should always return");
}
