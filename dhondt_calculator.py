

# d'Hondt seating allocation method
def compute(nr_of_seats, vote_counts):
    # generate grid of vote quotient according to formula V/(s + 1)
    # where V is the number of votes of a given party and s the number of seats already awarded
    grid = [[int(votes / (seats_awarded + 1)) for seats_awarded in range(nr_of_seats)] for votes in vote_counts]
    # list of number of seats awarded to each party
    seats = [0] * len(vote_counts)
    # compute number of seats
    for seat in range(nr_of_seats):
        seats[next_seat(grid)] += 1
    return seats


# obtain next seat given computed vote grid
def next_seat(grid):
    # find the maximum element in the grid
    current_max = -1
    for index, row in enumerate(grid):
        for elem in row:
            if elem > current_max:
                current_max, max_index = elem, index
    # remove maximum from grid
    grid[max_index].remove(current_max)
    # return corresponding row (party/movement)
    return max_index