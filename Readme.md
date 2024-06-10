# Pysenpai_sql

This is a extension library for the pysenpai-2. Pysenpai is used for Lovelaces exercises especially to test the code answers. Pysenpai_sql extends Pysenpai-2 to also be able to test sql query exercises. This extension can be used to test basic sql querys (SELECT, INSERT, CREATE, DELETE, UPDATE).

NOTE: This project is still on progress and will improve

## Installation

To install the extension you should have installed Pysenpai-2 to be able to use Pysenpai_sql. To install Pysenpai_sql go to pysenpai_sql library where the setup.py is located. From there run the following command.

Python3 install .

## Usage

This is designed to be used in Lovelace, by feeding the required files, after installed on Lovelace server only the main file needs to be fed. Can also be used/tested locally on command line.

To use the library you will need to adjust the "main" testfile to match the specific exercise type. For an example on a SELECT_test_main_py you would have to insert test type:

test_type = "SELECT"

Reference answer:

```sql
correct_answer = ("SELECT name FROM Artist WHERE artistId IN (SELECT artistId FROM ArtWork WHERE type == 'painting') ORDER BY name ASC;")
```

And also if you would like the exercise to have better feedback you would have to make a specific tests to be able to give advanced feedback.

Remember this is not a finished version and we are improving the usage all the time.

You would also need a sql file where the answer is located eg. select_data.sql (name does not matter).

To run the program you need to use the following command from the directory containing the script:

```python
python3 sql_tests/sqlTester.py -l fi answer.sql reference.sql
```

Where "SELECT_test_main.py" is the file where the main is located, can be different for different tests. "fi" being the chosen output language it can be "fi" or "en". And "select_data.sql" being the sql file that contains the sql query to be tested.

## Testing

Tests can be run by going to `sql_tests` directory and running `pytest` command.

```bash
cd sql_tests
pytest
```
Tha main test file is located at `tests_test_sqlTester.py`. 

New test cases for existing queries (UPDATE, SELECT, CREATE, DELETE, ALTER, INSERT) can be added by creating a new directory (fe. case_1) under the queries `xx_test_files` directory (fe. select_test_files).

The case directory should contain at least three files:

1) `ref.sql` which contains the reference answer. All answers are compared against this one.

2) `fail_(x).sql` contains a query that should be failed by the program.

3) `pass_(x).sql` contains a query that shold be passed by the program.

Multiple fail or pass files can exist for a case and they will all be tested agains the reference answer. If a failing query is passed or vica versa, pytest will mark the query as failed and print an error.