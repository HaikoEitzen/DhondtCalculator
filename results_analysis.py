import argparse
import csv

def main(input_file, output_file):
    counter = 0
    deny_majority = 0
    deny_half = 0
    output_string_list = []
    with open(input_file, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        can_deny_majority = False
        can_deny_half = False
        has_majority = False
        has_half = False
        for row in csv_reader:
            if len(row) >= 5:
                if int(row[3]) == 1:
                    if can_deny_half:
                        deny_half += 1
                        can_deny_half = False
                    if can_deny_majority:
                        deny_majority += 1
                        can_deny_majority = False
                    has_majority = False
                    has_half = False
                    counter += 1
                    if int(row[4]) == int(row[2]) / 2:
                        has_half = True
                    elif int(row[4]) > int(row[2]) / 2:
                        has_majority = True
                else:
                    if has_majority and int(row[4]) <= int(row[2]) / 2 and not can_deny_majority:
                        can_deny_majority = True
                        output_string_list.append("{:<40s}\t{:<40s}\t{:>5s}\t{:>5s}\t{:>5s}\n".format(
                            row[0],row[1],row[2],row[3],row[4]))
                    if has_half and int(row[4]) < int(row[2]) / 2 and not can_deny_half:
                        can_deny_half = True
                        output_string_list.append("{:<40s}\t{:<40s}\t{:>5s}\t{:>5s}\t{:>5s}\n".format(
                            row[0],row[1],row[2],row[3],row[4]))
    output_string_list.insert(0,"{}\t{}\t{}\n".format(counter, deny_majority, deny_half))
    output_string = ''.join(output_string_list)
    if output_file == "print":
        print(output_string)
    else:
        with open(output_file, 'w') as output:
            output.write(output_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="D'Hondt results analyser")
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")
    args = parser.parse_args()
    main(args.input_filename, args.output_filename)
