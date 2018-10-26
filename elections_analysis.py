# -*- coding: utf-8 -*-
import argparse
import csv
import dhondt_calculator


def extract_data(filename):
    election_data = []
    with open(filename, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            constituency = row[0]
            location = row[1]
            nr_of_seats = int(row[2])
            vote_counts = []
            for vote_count in row[3:]:
                vote_counts.append(int(vote_count))
            election_data.append((constituency, location, nr_of_seats, vote_counts))
    return election_data


def compute_actual_results(election_data):
    # vote counts passed in descending order
    actual_results = [[row[0], row[1], row[2], dhondt_calculator.compute(row[2], sorted(row[3], reverse=True))] for row in election_data]
    return actual_results


def compute_hypothetical_results(election_data):
    # each tuple in coalition options has a number of members in coalition, and seat allocation
    hypothetical_results = [[row[0], row[1], row[2]] for row in election_data]
    for idx, row in enumerate(election_data):
        coalition_options = []
        vote_counts = sorted(row[3], reverse=True)
        coalition_members = 1
        # while there are at least 3 party lists so that 2 can form a coalition
        while len(vote_counts) - coalition_members > 1:
            coalition_members += 1
            # the hypothetical vote count is equal to the original but with the coalition member vote counts
            # replaced by a single vote count at the end of the array
            hypothetical_vote_counts = vote_counts[:-coalition_members] + [sum(vote_counts[-coalition_members:])]
            seats = dhondt_calculator.compute(row[2], hypothetical_vote_counts)
            coalition_options.append((coalition_members, seats))
        hypothetical_results[idx].append(coalition_options)
    return hypothetical_results


# generate file with actual and hypothetical results
def generate_result_file(filename, actual_results, hypothetical_results):
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for idx, row in enumerate(actual_results):
            actual_results_row = [row[0], row[1], row[2], 1]
            for elem in row[3]:
                actual_results_row.append(elem)
            csv_writer.writerow(actual_results_row)
            # hypothetical seat allocations
            if len(hypothetical_results[idx][3]) > 0:
                for coalition_option in hypothetical_results[idx][3]:
                    hypothetical_results_row = [row[0], row[1], row[2], coalition_option[0]]
                    for nr_of_seats in coalition_option[1]:
                        hypothetical_results_row.append(nr_of_seats)
                    csv_writer.writerow(hypothetical_results_row)


def main(input_file, output_file):
    # list of tuples: (legislature or electoral body, location or name, number of seats, vote counts)
    election_data = extract_data(input_file)
    # compute actual results for each legislature or electoral body
    # list of tuples: (legislature, location, number of seats, list of seat allocations)
    actual_results = compute_actual_results(election_data)
    # next, compute hypothetical results for each legislature considering coalitions of parties from last to second place
    hypothetical_results = compute_hypothetical_results(election_data)
    # produce csv file with results
    generate_result_file(output_file, actual_results, hypothetical_results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="D'Hondt Calculator")
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")
    args = parser.parse_args()
    main(args.input_filename, args.output_filename)