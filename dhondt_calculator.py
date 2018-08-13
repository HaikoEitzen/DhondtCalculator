def compute(nr_of_seats, vote_counts):
    grid = generate_grid(nr_of_seats, vote_counts)
    seat_allocation = compute_seat_allocation(grid)
    return seat_allocation


def generate_grid(nr_of_seats, vote_counts):
    # generate grid of vote quotient according to formula V/(s + 1)
    # where V is the number of votes of a given party and s the number of seats already awarded
    grid = [[int(votes / (seats_awarded + 1)) for seats_awarded in range(nr_of_seats)] for votes in vote_counts]
    return grid


def compute_seat_allocation(grid):
    vote_counts = len(grid)
    seat_allocation = [0] * vote_counts
    allocate_seats(seat_allocation, grid)
    return seat_allocation


def allocate_seats(seat_allocation, grid):
    nr_of_seats = len(grid[0])
    for seat in range(nr_of_seats):
        seat_allocation[next_seat(grid)] += 1


def next_seat(grid):
    current_max = -1
    for party, vote_quotients in enumerate(grid):
        for vq in vote_quotients:
            if vq > current_max:
                current_max, party_that_won_seat = vq, party
    grid[party_that_won_seat].remove(current_max)
    return party_that_won_seat