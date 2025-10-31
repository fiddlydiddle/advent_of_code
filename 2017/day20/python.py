import math

class Particle:
    def __init__(self, idx, position, velocity, acceleration):
        self.idx = idx
        # Position, velocity, and acceleration are tuples, e.g. (1,0,-1)
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.has_collided = False # Part 2: detect collisions between particles


def main():
    input = open('/home/john/Documents/Projects/advent_of_code/2017/day20/input.txt', 'r').readlines()
    particles = parse_input(input)
    particles = part1(particles)
    print(f"Remaining particles: {len(particles)}") # Part 2: Return number of particles left after removing collided particles in part 1


def part1(particles):
    # Run several iterations of particle movement
    # See if patterns emerge about closest particle
    for i in range(10000):
        closest_distance = math.inf
        closest_particle = None
        # Part 2: Keep track of occupied positions for collision detection
        # Map has position tuples as keys and current particle at that position as values
        unique_positions = {} 
        for particle in particles:
            particle = move_particle(particle)

            # Part 2: Collision detection
            if str(particle.position) not in unique_positions:
                # First particle in this iteration to occupy this position
                unique_positions[str(particle.position)] = particle 
            else:
                # Collision
                particle.has_collided = True
                unique_positions[str(particle.position)].has_collided = True


            (position_x, position_y, position_z) = particle.position
            distance = abs(position_x) + abs(position_y) + abs(position_z)
            if (distance < closest_distance):
                closest_distance = distance
                closest_particle = particle
        
        # Part 2: filter out particles that collided
        particles = list(filter(lambda particle: particle.has_collided == False, particles))
        # Part 1: Closest particle
        print(f"Closest particle: {closest_particle.idx}, Distance: {closest_distance}")

    return particles


def move_particle(particle):
    (acceleration_x, acceleration_y, acceleration_z) = particle.acceleration
    (velocity_x, velocity_y, velocity_z) = particle.velocity
    (position_x, position_y, position_z) = particle.position

    # Update velocity based on acceleration
    velocity_x += acceleration_x
    velocity_y += acceleration_y
    velocity_z += acceleration_z

    # Update position based on velocity
    position_x += velocity_x
    position_y += velocity_y
    position_z += velocity_z

    # Final update to particle and return
    particle.velocity = (velocity_x, velocity_y, velocity_z)
    particle.position = (position_x, position_y, position_z)
    return particle


def parse_input(input):
    particles = []
    for idx, line in enumerate(input):
        line = line.rstrip()
        position, velocity, acceleration = line.split(', ')
        position = parse_coordinates(position)
        velocity = parse_coordinates(velocity)
        acceleration = parse_coordinates(acceleration)
        particles.append(Particle(idx, position, velocity, acceleration))
    return particles


def parse_coordinates(input):
    start = input.index('<')
    end = input.index('>')
    num_string = input[start + 1: end]
    x_val, y_val, z_val = num_string.split(',')
    return (int(x_val), int(y_val), int(z_val))


main()