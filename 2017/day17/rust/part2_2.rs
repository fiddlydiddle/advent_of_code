#[derive(Clone, Copy)]
struct NodeIdx(usize);

struct Node<T> {
    data: T,
    prev: NodeIdx,
    next: NodeIdx,
}

struct List<T> {
    nodes: Vec<Node<T>>,
}

impl<T> List<T> {
    fn with_initial(data: T) -> (Self, NodeIdx) {
        let node = Node {
            data,
            prev: NodeIdx(0),
            next: NodeIdx(0),
        };
        let list = List { nodes: vec![node] };
        (list, NodeIdx(0))
    }

    fn insert_after(&mut self, idx: NodeIdx, data: T) -> NodeIdx {
        let next_idx = self.nodes[idx.0].next;
        let new_idx = NodeIdx(self.nodes.len());
        self.nodes.push(Node {
            data,
            prev: idx,
            next: next_idx,
        });
        self.nodes[idx.0].next = new_idx;
        self.nodes[next_idx.0].prev = new_idx;
        new_idx
    }

    fn step_forward(&self, mut idx: NodeIdx, steps: usize) -> NodeIdx {
        for _ in 0..steps {
            idx = self.nodes[idx.0].next;
        }
        idx
    }

    fn next(&self, idx: NodeIdx) -> NodeIdx {
        self.nodes[idx.0].next
    }

    fn value(&self, idx: NodeIdx) -> &T {
        &self.nodes[idx.0].data
    }
}

fn part2(num_steps_per_iteration: usize, num_iterations: usize) -> (usize, usize) {
    let (mut list, mut current_idx) = List::with_initial(0usize);
    let zero_idx = current_idx;
    list.nodes.reserve(num_iterations);

    for value_to_insert in 1..=num_iterations {
        let next_idx = list.step_forward(current_idx, num_steps_per_iteration);

        let inserted_idx = list.insert_after(next_idx, value_to_insert);
        current_idx = inserted_idx;
    }

    current_idx = list.next(current_idx);
    let current_val = *list.value(current_idx);
    let after_zero_val = *list.value(list.next(zero_idx));
    (current_val, after_zero_val)
}

fn main() {
    let (current_val, after0) = part2(304, 50_000_000);
    println!("{}", current_val);
    println!("{}", after0);
}