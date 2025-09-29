use std::collections::HashMap;
use std::collections::VecDeque;
use std::fs;
use std::sync::Arc;
use tokio::join;
use tokio::sync::Mutex;
use tokio::time::{self, Duration};

#[derive(Debug, Clone)]
struct Instruction {
    operation: String,
    register: String,
    parameter: Option<String>,
}

#[derive(Debug)]
struct Program {
    program_id: i64,
    registers: HashMap<String,i64>,
    queue: VecDeque<i64>,
    is_receiving: bool,
    messages_sent: i64,
}

impl Program {
    pub fn new(program_id: i64) -> Program {
        let mut registers: HashMap<String,i64> = HashMap::new();
        registers.insert(String::from("p"), program_id);

        Program {
            program_id: program_id,
            registers: registers,
            queue: VecDeque::<i64>::new(),
            is_receiving: false,
            messages_sent: 0,
        }
    }

    pub fn get_value(&self, parameter: Option<String>) -> i64 {
        let param_string = parameter.expect("Parameter cannot be None"); 

        match param_string.parse::<i64>() {
            Ok(value) => {
                value
            }
            Err(_) => {
                *self.registers.get(&param_string)
                    .expect(&format!("Parameter '{}' is neither a number nor a register.", param_string))
            }
        }
    }
}

#[tokio::main]
async fn main() {
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let instructions = parse_input(&input);
    
    // Run part 1 first
    part1(instructions.clone()).await;
    
    // Then run part 2
    let result = part2(instructions).await;
    println!("Part 2: {}", result);
}

async fn part1(instructions: Vec<Instruction>) {
    let mut program = Program::new(0);
    let mut idx: i64 = 0;
    let mut most_recent_sound: i64 = 0;

    while idx >= 0 && idx < instructions.len().try_into().unwrap() {
        let instruction = instructions[idx as usize].clone();
        if !program.registers.contains_key(instruction.register.as_str()) {
            program.registers.insert(instruction.register.clone(), 0);
        }

        match instruction.operation.as_str() {
            "snd" => {
                let register_value = program.get_value(Some(instruction.register.clone()));
                most_recent_sound = register_value;
            },
            "set" => {
                let new_value = program.get_value(instruction.parameter);
                program.registers.insert(instruction.register, new_value);
            },
            "add" => {
                let existing_value = program.get_value(Some(instruction.register.clone()));
                let operation_value = program.get_value(instruction.parameter);
                program.registers.insert(instruction.register, existing_value + operation_value);
            },
            "mul" => {
                let existing_value = program.get_value(Some(instruction.register.clone()));
                let operation_value = program.get_value(instruction.parameter);
                program.registers.insert(instruction.register, existing_value * operation_value);
            },
            "mod" => {
                let existing_value = program.get_value(Some(instruction.register.clone()));
                let operation_value = program.get_value(instruction.parameter);
                if operation_value > 0 {
                    program.registers.insert(instruction.register, existing_value % operation_value);
                }
            },
            "rcv" => {
                if program.get_value(Some(instruction.register.clone())) != 0 {
                    println!("Part 1: {}", most_recent_sound);
                    return;
                }
            },
            "jgz" => {
                let value = program.get_value(instruction.parameter);
                if program.get_value(Some(instruction.register.clone())) > 0 {
                    idx = idx + value;
                    continue;
                }
            },
            _ => {
                panic!("Unknown instruction operation: {}", instruction.operation);
            }
        }

        idx += 1;
    }
}

async fn part2(instructions: Vec<Instruction>) -> i64 {
    let program0 = Arc::new(Mutex::new(Program::new(0)));
    let program1 = Arc::new(Mutex::new(Program::new(1)));
    let result = run_programs(instructions.clone(), program0, program1).await;
    
    result
}

async fn run_programs(
    instructions: Vec<Instruction>,
    program0: Arc<Mutex<Program>>,
    program1: Arc<Mutex<Program>>,
) -> i64 {
    let is_canceled = Arc::new(Mutex::new(false));
    let instructions0 = instructions.clone();
    let instructions1 = instructions;

    let program0_execution = tokio::spawn(
        run_program(
            Arc::clone(&program0),
            instructions0,
            Arc::clone(&program1),
            Arc::clone(&is_canceled),
        )
    );

    let program1_execution = tokio::spawn(
        run_program(
            Arc::clone(&program1),
            instructions1,
            Arc::clone(&program0),
            Arc::clone(&is_canceled),
        )
    );

    let mut deadlock_count = 0;
    loop {
        time::sleep(Duration::from_millis(1)).await;

        let program0_guard = program0.lock().await;
        let program1_guard = program1.lock().await;

        let deadlock = (program0_guard.is_receiving && program0_guard.queue.is_empty())
            && (program1_guard.is_receiving && program1_guard.queue.is_empty());

        if deadlock {
            deadlock_count += 1;

            if deadlock_count >= 100 {
                *is_canceled.lock().await = true;
                break;
            }
        }
        else {
            deadlock_count = 0;
        }
    }

    let _ = join!(program0_execution, program1_execution);
    let final_program1_guard = program1.lock().await;
    final_program1_guard.messages_sent
}

async fn run_program(
    program: Arc<Mutex<Program>>, 
    instructions: Vec<Instruction>, 
    other_program: Arc<Mutex<Program>>,
    is_canceled: Arc<Mutex<bool>>,
) -> Result<(), tokio::task::JoinError> {

    let mut idx: i64 = 0;
    let mut iteration: i64 = 0;
    let mut most_recent_sound: i64 = 0;
    let mut part1_result: i64 = 0;

    while idx >= 0 && idx < instructions.len().try_into().unwrap() {
        // Periodically check if parent wants to cancel process
        if iteration % 100 == 0 {
            if *is_canceled.lock().await { 
                return Ok(()); 
            }
        }

        let instruction = instructions[idx as usize].clone();
        
        // Get a lock on our program
        let mut program_guard = program.lock().await;
        
        if !program_guard.registers.contains_key(instruction.register.as_str()) {
            program_guard.registers.insert(instruction.register.clone(), 0);
        }

        match instruction.operation.as_str() {
            "snd" => {
                let register_value = program_guard.get_value(Some(instruction.register.clone()));
                most_recent_sound = register_value;
                program_guard.messages_sent += 1;
                // Release our lock before sending to other program
                drop(program_guard);
                // Send message to other program
                {
                    let mut other_program_guard = other_program.lock().await;
                    other_program_guard.queue.push_back(register_value);
                }
                // Re-acquire our lock
                program_guard = program.lock().await;
            },
            "set" => {
                let new_value = program_guard.get_value(instruction.parameter);
                program_guard.registers.insert(instruction.register, new_value);
            },
            "add" => {
                let existing_value = program_guard.get_value(Some(instruction.register.clone()));
                let operation_value = program_guard.get_value(instruction.parameter);
                program_guard.registers.insert(instruction.register, existing_value + operation_value);
            },
            "mul" => {
                let existing_value = program_guard.get_value(Some(instruction.register.clone()));
                let operation_value = program_guard.get_value(instruction.parameter);
                program_guard.registers.insert(instruction.register, existing_value * operation_value);
            },
            "mod" => {
                let existing_value = program_guard.get_value(Some(instruction.register.clone()));
                let operation_value = program_guard.get_value(instruction.parameter);
                if operation_value > 0 {
                    program_guard.registers.insert(instruction.register, existing_value % operation_value);
                }
            },
            "rcv" => {
                if program_guard.get_value(Some(instruction.register.clone())) != 0 && part1_result == 0 && program_guard.program_id == 0 {
                    part1_result = most_recent_sound;
                    println!("Part 1: {}", part1_result);
                }

                // Try to receive a message
                if program_guard.queue.len() > 0 {
                    let new_value: i64 = program_guard.queue.pop_front()
                        .expect("Queue was unexpectedly empty after length check");
                    program_guard.registers.insert(instruction.register.clone(), new_value);
                } else {
                    // No message available, set receiving flag and wait
                    program_guard.is_receiving = true;
                }
            },
            "jgz" => {
                let value = program_guard.get_value(instruction.parameter);
                if program_guard.get_value(Some(instruction.register.clone())) > 0 {
                    idx = idx + value;
                    continue;
                }
            },
            _ => {
                panic!("Unknown instruction operation: {}", instruction.operation);
            }
        }

        idx += 1;
        iteration += 1;
    }

    // Program has reached the end of instructions
    let final_program_guard = program.lock().await;
    println!("Program {} done", final_program_guard.program_id);
    Ok(())
}


fn parse_input(input: &String) -> Vec<Instruction> {
    let lines: Vec<&str> = input.lines().map(|line| line.trim()).collect();
    let mut instructions: Vec<Instruction> = Vec::new();

    for line in lines.iter() {
        let instruction_parts: Vec<&str> = line.split_whitespace().collect();
        let mut parameter: Option<String> = None;
        if instruction_parts.len() > 2 {
            parameter = Some(instruction_parts[2].to_string());
        }
        instructions.push(
            Instruction {
                operation: instruction_parts[0].to_string(),
                register: instruction_parts[1].to_string(),
                parameter: parameter,
            }
        );
    }

    return instructions;
}