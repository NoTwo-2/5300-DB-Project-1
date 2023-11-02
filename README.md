# 5300-DB-Project-1

SQL DB normalization given database tables and functional dependencies

# Requirements

```
python3 // install the latest version plz
pip install tabulate
```

Multivalued attributes are represented in the CSV file by putting a space between each value

# Description

Here we have a python3 project to take in a CSV file containing a table, primary key, and functional dependencies. The program will then ask the user to input the desired normal form to normalize the table to, and the program will output the normalized tables in stdout.

- The `main.py` file handles all user input. It is also used for debugging purposes.
- The `csv_parser.py` file handles the parsing of the csv file containing the table data.
- The `table.py` file contains the class definition for the representation of our table. This is how we store and manipulate the table data in the program. There are various getter functions as well for things like a list of super keys, candidate keys, etc.
- The `normalizer.py` file contains all the helper functions that normalize the table.

## Program Flow
- `main.py` asks the user for the input data for the table. 
- `csv_parser.py` is called to parse the csv file. 
- The table data is then passed into the constructor in `table.py` and a table object is built.
- `main.py` asks the user for additional data, such as functional dependencies, the primary key, and multivalue functional dependencies. The table object is updated with these values.
- `main.py` asks the user what normal form they would like to normalize to.
- The corresponding functions in `normalizer.py` are sequentially called and the normalized tables are returned.
- The normalized tables are outputted.

# Assignment Guidelines

## Objectives (as seen on the Canvas project page)

To develop a program that takes a dataset (relation) and functional dependencies as input, normalizes the relations based on the provided functional dependencies, produces SQL queries to generate the normalized database tables, and optionally determines the highest normal form of the input table.

### Inputs:

- Dataset (Relation)
- Functional Dependencies
- Choice of the highest normal form to reach (1NF, 2NF, 3NF, BCNF, 4NF, 5NF)
- Option to find the highest normal form of the input table (optional)

### Desired Outputs:

- SQL Queries to generate the normalized database tables.
- The highest normal form of the input table (if opted).

### Core Components:

- Input Parser: To parse the input dataset and functional dependencies.
- Normalizer: To normalize the dataset based on functional dependencies.
- SQL Query Generator: To generate SQL queries for normalized tables.
- Normal Form Finder: To find the highest normal form of the input table.

### Deliverables:

- Source Code: Well-commented source code in the language of your choice.
- Code Description: Detailed documentation describing the flow, logic, and methodology of the code.
- Output File: A text file containing generated SQL queries and the highest normal form of the input table (if opted)