#!/usr/bin/env python

import os
import sys
import csv
import pandas as pd
import re
from dateutil import parser
from datetime import timedelta


def main(filename):
    # Write a temp csv with non-UTF-8 characters replaced with the Unicode Replacement Character
    write_replaced_csv(filename)

    # Remove SettingsWithCopyWarning from pandas
    pd.options.mode.chained_assignment = None

    # Import as pandas data frame, get rid of the temp CSV
    data = pd.read_csv('temp.csv')
    os.remove('temp.csv')

    rows_to_remove = []

    rows_to_remove += convert_datetimes(data['Timestamp'])
    rows_to_remove += convert_zipcodes(data['ZIP'])

    # Format zip codes with leading zeroes, up to 5
    data['ZIP'] = data['ZIP'].apply(lambda x: '{0:0>5}'.format(x))

    convert_names(data['FullName'])
    rows_to_remove += convert_to_seconds(data, 'FooDuration')
    rows_to_remove += convert_to_seconds(data, 'BarDuration')
    data['TotalDuration'] = data['FooDuration'] + data['BarDuration']

    # remove any rows with non-Unicode characters that caused an error
    rows_to_remove = list(set(rows_to_remove))
    for i in rows_to_remove:
        data = data.drop([i])

    output_filename = str(sys.argv[2])
    data.to_csv(output_filename, index=False, header=True, encoding='utf-8')


def write_replaced_csv(filename):
    """Write a temporary CSV that replaces non-Unicode characters with the Unicode Replacement Character."""
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    with open('temp.csv', 'w') as g:
        for line in lines:
            g.write(line)


def convert_datetimes(timestamp_data):
    """Replace column datetimes with U.S. Eastern Time in ISO-8601 format. If there are non-UTF-8 characters in this
    field, return the rows to be removed."""
    error_indices = []
    for i in range(0, len(timestamp_data)):
        try:
            datetime_obj = parser.parse(timestamp_data[i])
            datetime_obj = datetime_obj + timedelta(hours=3)
            timestamp_data[i] = datetime_obj.isoformat()
        except parser.ParserError:
            sys.stderr.write('Warning: Invalid character in date field.\n')
            error_indices.append(i)

    return error_indices

def convert_zipcodes(zipcode_data):
    """Place leading zeroes in zipcodes. If there are non-UTF-8 characters in this field, return the rows to be
    removed."""
    error_indices = []
    for i in range(0, len(zipcode_data)):
        try:
            int(zipcode_data[i])
        except ValueError:
            sys.stderr.write('Warning: Invalid character in zipcode field.\n')
            error_indices.append(i)

    return error_indices


def convert_names(names_data):
    """Replace names in FullName column with uppercase version, including non-English characters."""
    for i in range(0, len(names_data)):
        uppercase = names_data[i].upper()
        names_data[i] = uppercase


def convert_to_seconds(data, column_name):
    """Replace column with string in format HH:MM:SS.MSS with seconds, unrounded. Make a note of any values that have
    the Unicode Replacement Character in them and mark those rows for removal."""
    hours_mins_regex = r'(\d+:)' # match 01:02:
    seconds_regex = r':\d+\.\d+' # match :12.345
    error_indices = []

    for i in range(0, len(data[column_name])):
        value = data[column_name][i]
        total_milliseconds = 0
        total_seconds = 0

        if '�' in value:
            error_indices.append(i)
            sys.stderr.write('Invalid non-Unicode character found in %s field. \n' % column_name)
        else:
            hours_mins = re.findall(hours_mins_regex, value)
            seconds = re.findall(seconds_regex, value)

            no_colons_hours_mins = []
            for num in hours_mins:
                int_num = int(num.replace(':', ''))
                no_colons_hours_mins.append(int_num)

            no_colons_seconds = []
            for num in seconds:
                no_colons_seconds.append(float(num.replace(':', '')))

            total_milliseconds += convert_hour_to_milliseconds(no_colons_hours_mins[0])
            total_milliseconds += convert_minutes_to_milliseconds(no_colons_hours_mins[1])
            total_milliseconds += convert_seconds_to_milliseconds(no_colons_seconds[0])

            total_seconds = total_milliseconds / 1000.0

        data[column_name][i] = total_seconds

    return error_indices


def convert_hour_to_milliseconds(hours):
    return hours * 3600000


def convert_minutes_to_milliseconds(minutes):
    return minutes * 60000


def convert_seconds_to_milliseconds(seconds):
    return seconds * 1000


if __name__== "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Please provide the name of your input file and output file, in that order, after "
                         "normalizer.py\n")
        sys.exit(2)
    main(sys.argv[1])

