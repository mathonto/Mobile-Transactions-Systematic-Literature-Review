import sys

import csv
import os
import webbrowser


def inspect_row(row: [str]) -> [str]:
    title = row[0]
    link = row[3]
    abstract_viewed = False

    option = None
    while option != 'y' and option != 'n':
        print('\033[92m' + f'"{title}"' + '\033[0m')
        print('Include?')
        option = input(
            '   y - yes\n' +
            '   n - no\n' +
            '   a - view abstract\n' +
            '   e - exit\n'
        )

        if option == 'y':
            row.append('y')
        elif option == 'n':
            row.append('n')
        elif option == 'a':
            abstract_viewed = True
            webbrowser.open(link)
        elif option == 'e':
            sys.exit()
        else:
            print('Unrecognized input')
        print()

    if abstract_viewed:
        row.append('abstract viewed')
    return row


def get_last_edited_link(edited_file_name: str) -> str:
    if not os.path.isfile(edited_file_name):
        return None

    with open(edited_file_name, 'r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]
        last_row = rows[-1]
        return last_row[3]


if __name__ == '__main__':
    file_name = sys.argv[1]
    edited_file_name = file_name.replace('.csv', '') + '-edited.csv'

    last_link = get_last_edited_link(edited_file_name)
    edited_file = open(edited_file_name, 'a')

    with open(file_name, 'r+') as csv_file:
        reader = csv.reader(csv_file)
        writer = csv.writer(edited_file)

        # skip header and resume editing
        next(reader, None)
        next(reader, None)
        if last_link is not None:
            print('Continuing where you left off...')
            while True:
                row = next(reader, None)
                if row[3] == last_link:
                    break

        for row in reader:
            row = inspect_row(row)
            writer.writerow(row)
