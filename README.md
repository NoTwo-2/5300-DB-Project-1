# 5300-DB-Project-1

SQL DB normalization given database tables and functional dependencies

# Requirements

```
python3
pip install tabulate
```

Multivalued attributes are represented in the CSV file by putting a space between each value

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