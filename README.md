_This is one of the steps in the Truss interview process. If you've
stumbled upon this repository and are interested in a career with
Truss, like I am, [check out their jobs page](https://truss.works/jobs)._

# Truss Software Engineering Interview - Monique Murphy

## Introduction

This is a tool that reads a CSV formatted file on `stdin` and
emits a normalized CSV formatted file on `stdout`. 

Normalized, in this case, means:

* The entire CSV is in the UTF-8 character set.
* The `Timestamp` column in output is formatted in ISO-8601 format.
* The `Timestamp` column is assumed to be in US/Pacific time;
  it is converted to US/Eastern in the output.
* All `ZIP` codes should be formatted as 5 digits. If there are less
  than 5 digits, zipcode is printed with leading zeroes in the output
  (Excel will automatically remove these leading zeroes, so it is
  worth checking in a plain text editor as well)
* The `FullName` column is converted to uppercase in the output. 
  There are some non-English names.
* The `Address` column is passed through as is, except for
  Unicode validation. 
* The `FooDuration` and `BarDuration` columns are in HH:MM:SS.MS
  format (where MS is milliseconds); they are converted to the
  total number of seconds expressed in floating point format
  in the output, unrounded.
* The `TotalDuration` column is filled with the sum of
  `FooDuration` and `BarDuration` in the output.
* The `Notes` column is free form text input by end-users.
  This data is not changed in the output, other than invalid UTF-8
  characters being replaced with the Unicode Replacement Character.

Input documents should be in UTF-8 and any times
that are missing timezone information are assumed to be in US/Pacific. 
If a character is invalid, it is replaced with the Unicode Replacement
Character in the output. If that replacement makes data invalid (for example,
because it turns a date field into something unparseable), a warning is
printed to `stderr` and that row is dropped from the output.

## Instructions

### The preferred OS is macOS 10.15.
1. Clone this repo to your local machine. Navigate to the `truss-interview` folder.
2. Create a Python virtualenv with your tool of choice. 
3. Run `pip -r install requirements.txt` for necessary packages. 
4. Run `python3 normalizer.py name-of-input.csv name-of-output.csv` 
(for example: `python3 normalizer.py sample.csv output.csv`)
5. Check your current directory for the generated csv with the output name given.
6. (Optional) Use test CSVs provided in folder.

## Test CSV List and Descriptions
* **sample.csv** - sample data without errors
* **sample-with-broken-utf8.csv** - sample data with a non-Unicode character in one Notes field
* **sample-with-broken-utf8-broken-bar-duration.csv** - sample data with a non-Unicode character
in the first row of the BarDuration column
* **sample-with-broken-utf8-broken-date.csv** - sample data with a non-Unicode character in the
first row of the Timestamp column
* **sample-with-broken-utf8-broken-foo-duration.csv** - sample data with a non-Unicode character
in the first row of the FooDuration column
* **sample-with-broken-utf8-broken-zip.csv** - sample data with a non-Unicode character in the
first row of the Zip column
* **sample-with-broken-utf8-urc-address.csv** - sample data with a non-Unicode character in the
first row of the Address column
* **sample-with-broken-utf8-urc-name.csv** - sample data with a non-Unicode character in the first
row of the FullName column
* **sample-with-broken-utf8-urc-notes2.csv** - sample data with a non-Unicode character in the
first row of the Notes column
* **sample-with-broken-utf8-urc-totalduration.csv** - sample data with a non-Unicode character in
the first row of the TotalDuration column



