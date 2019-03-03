import argparse
import csv

def main(input_file, output_file):
    counter = 0
    majority_counter = 0
    half_counter = 0
    deny_majority = 0
    deny_half = 0
    output_majority_string_list = []
    output_half_string_list = []
    with open(input_file, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        has_majority = False # leading party has majority of seats
        has_half = False # leading party has exactly half of seats
        can_deny_majority = False # other parties can deny the leading party its majority if they united in one list
        can_deny_half = False # other parties can prevent the leading party from having half the seats if they united in one list
        nr_of_lists = 0 # number of competing lists/parties
        for row in csv_reader:
            # length of 4 would mean there was only one list, so analysis is unnecessary
            if len(row) >= 5:
                # column 3 identifies the number of united lists,
                # a value of 1 signifies it's the original data (no hypothetical unions yet)
                # in other words, it's the first row of results corresponding to a particular electoral district
                if int(row[3]) == 1:
                    nr_of_lists = len(row)-4 # the first four columns are not seat results
                    counter += 1
                    # column 4 identifies the number of seats of the leading party/list
                    # column 2 identifies the number of available seats in the district
                    if int(row[4]) == int(row[2]) / 2:
                        half_counter += 1
                        has_half = True
                    elif int(row[4]) > int(row[2]) / 2:
                        majority_counter += 1
                        has_majority = True
                else:
                    # if the leading party has a majority (cond.1) and this union of opposition parties can deny a majority (cond.3),
                    # and such a combination has not yet been found (i.e., can_deny_majority = false)(cond.2) then
                    # add the current combination to the corresponding output and set can_deny_majority flag to True.
                    if has_majority and not can_deny_majority and int(row[4]) <= int(row[2]) / 2:
                        can_deny_majority = True
                        output_majority_string_list.append("{:<40s}\t{:<40s}\t{:>5s}\t{:>5d}\t{:>5s}\n".format(
                            row[0],row[1],row[2],nr_of_lists,row[3]))
                    # if the leading party has half the seats (cond.1) and this union of opposition parties can prevent said party
                    # from keeping half the seats (cond.3), and such a combination has not yet been found (i.e., can_deny_half = false)(cond.2)
                    # then add the current combination to the corresponding output and set can_deny_half flag to True.
                    if has_half and not can_deny_half and int(row[4]) < int(row[2]) / 2:
                        can_deny_half = True
                        output_half_string_list.append("{:<40s}\t{:<40s}\t{:>5s}\t{:>5d}\t{:>5s}\n".format(
                            row[0],row[1],row[2],nr_of_lists,row[3]))
                # column 3 identifies the number of united lists,
                # a value of Nr_Of_Lists - 1 signifies it's the row considering the union of all parties except for the leading one
                # in other words, it's the last row of results corresponding to a particular electoral district
                if int(row[3]) == nr_of_lists - 1:
                    # if flags are activated, counters are incremented and flags reset
                    if can_deny_half:
                        deny_half += 1
                        can_deny_half = False
                    if can_deny_majority:
                        deny_majority += 1
                        can_deny_majority = False
                    has_majority = False
                    has_half = False
    output_majority_string_list.insert(0,"{}\t{}\t{}\n".format(counter, majority_counter, deny_majority))
    output_half_string_list.insert(0, "{}\t{}\t{}\n".format(counter, half_counter, deny_half))
    output_majority_string = ''.join(output_majority_string_list)
    output_half_string = ''.join(output_half_string_list)
    if output_file == "print":
        print(output_majority_string)
        print(output_half_string)
    else:
        with open(output_file, 'w') as output:
            output.write(output_majority_string)
            output.write(output_half_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="D'Hondt results analyser")
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")
    args = parser.parse_args()
    main(args.input_filename, args.output_filename)
