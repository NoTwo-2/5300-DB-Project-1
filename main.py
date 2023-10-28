import table
import csv_parser

def input_funct_depends(my_table: table.Table) -> None:
    '''
    This will take in a table object, prompt the user for functional dependencies, and add them in the table
    '''
    done = False
    while not done:
        print()
        print(f"Columns: {my_table.columns}")
        entry = input("Please input any valid functional dependencies, or hit enter if finished\nFormat: Determinant1, Determinant2 -> Dependant1, Dependant2: ")
        if entry.strip() == "":
            return
        if not ("->" in entry):
            print("You did not include an '->'in your definition. Please try again.")
            continue
        splentry = entry.split("->")
        
        determinant = splentry[0]
        dependant = splentry[1]
        
        spleterminant = determinant.split(",")
        splependant = dependant.split(",")
        
        streterminant = [attr.strip() for attr in spleterminant]
        strependant = [attr.strip()for attr in splependant]
        
        try:
            my_table.set_functional_dependencies((streterminant, strependant))
            print(f"Added {entry.strip()} to list of functional dependencies.")
        except RuntimeError as err:
            print(f"One or more of your attributes entered had an issue: {err}")

def input_primary_key(my_table: table.Table) -> None:
    '''
    This will take in a table object, prompt the user for the primary key, and set the primary key in the table
    '''
    done = False
    while not done:
        print()
        print(f"Columns: {my_table.columns}")
        entry = input("Please input a valid primary key\nIf your key has multiple attributes, seperate them with a comma: ")
        splentry = entry.split(",")
        
        try:
            my_table.set_primary_key(attributes=[attr.strip() for attr in splentry])
            done = True
        except RuntimeError as err:
            print(f"One or more of your attributes entered had an issue: {err}")
            
def create_table() -> table.Table:
    '''
    This will prompt the user for a csv file, and return a table object with the data in the csv
    '''
    while True:
        print()
        csv = input("Please input a CSV file containing a single table: ")
        try:
            parsed_csv = csv_parser.parse_csv(csv)
            
            csv_cols = parsed_csv[0]
            csv_rows = parsed_csv[1]
            return table.Table(csv_cols, csv_rows)
        except FileNotFoundError as err:
            print(err)
        except RuntimeError as err:
            print(err)

def main():
    my_table = create_table()
    
    input_primary_key(my_table)
    input_funct_depends(my_table)
    
    my_table.print_table()
    my_table.print_primary_key()
    my_table.print_functional_dependencies()
    
if __name__ == "__main__":
    main()