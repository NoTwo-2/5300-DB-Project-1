import table
import csv_parser
import normalizer

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
            
def normalize_to_form(start_table: table.Table, form: int) -> list[table.Table]:
    '''
    This will take in a table object and a form as an int 1 -> 1st, 4 -> bc, 6 -> 5th\n
    This outputs a list of tables normalized to the given form
    '''
    form_counter = 0
    table_list = [start_table]
    while form_counter != form:
        print()
        form_counter += 1
        new_table_list: list[table.Table] = []
        for my_table in table_list:
            match form_counter:
                case 1:
                    print("Normalized to 1st normal form:")
                    new_table_list += normalizer.first_normal_form(my_table)
                case 2:
                    print("Normalized to 2nd normal form:")
                    new_table_list += normalizer.second_normal_form(my_table)
                case 3:
                    print("Normalized to 3rd normal form:")
                    new_table_list += normalizer.third_normal_form(my_table)
                case 4:
                    print("Normalized to Boyce Codd normal form:")
                    new_table_list += normalizer.boyce_codd_normal_form(my_table)
                case 5:
                    print("Normalized to 4th normal form:")
                    new_table_list += normalizer.forth_normal_form(my_table)
                case 6:
                    print("Normalized to 5th normal form:")
                    new_table_list += normalizer.fifth_normal_form(my_table)
                case _:
                    raise RuntimeError(f"What.")
        for new_table in new_table_list:
            new_table.print_table()
            new_table.print_primary_key()
            new_table.print_functional_dependencies()
        table_list = new_table_list
    return table_list

def main():
    # my_table = create_table()
    
    # input_primary_key(my_table)
    # input_funct_depends(my_table)
    
    # normal_form = int(input(
    #     "Please enter the form you would like to normalize to\n"
    #     "1) First normal form\n"
    #     "2) Second normal form\n"
    #     "3) Third normal form\n"
    #     "4) Boyce Codd normal form\n"
    #     "5) Fourth normal form\n"
    #     "6) Fifth normal form\n"
    #     "Form: "
    # ))
    
    # print("\nOriginal Table:")
    # my_table.print_table()
    # my_table.print_primary_key()
    # my_table.print_functional_dependencies()
    
    # my_normalized_tables = normalize_to_form(my_table, normal_form)
    
    
    # ---------------=================== DEBUG ===================-------------------
    
    
    csv_cols, csv_rows = csv_parser.parse_csv("example.csv")
    my_table = table.Table(csv_cols, csv_rows)
    
    my_table.set_primary_key(["StudentID", "Course", "Professor"])
    my_table.set_functional_dependencies(
        (["StudentID"], ["FirstName", "LastName"]),
        (["Course", "Professor"], ["CourseStart", "CourseEnd", "BuildingID", "BuildingName"]),
        (["Professor"], ["ProfessorEmail"]),
        (["BuildingID"], ["BuildingName"])
    )
    my_table.set_multivalue_funct_depends(
        ("Course", ("Professor", "BuildingID")),
        ("StudentID", ("Course", "Professor"))
    )
    
    print("\nOriginal Table:")
    my_table.print_table()
    my_table.print_primary_key()
    my_table.print_functional_dependencies()
    my_table.print_mvds()
    
    super_keys = my_table.get_superkeys()
    super_keys.sort(key=len)
    print(f"Super keys: ")
    for key in super_keys:
        print(key)
    candidate_keys = my_table.get_candidate_keys()
    print(f"Candidate keys:")
    for key in candidate_keys:
        print([my_table.columns[i] for i in key])
    
    new_tables = normalizer.first_normal_form(my_table)
    for my_table in new_tables:
        my_table.print_table()
        
    for my_table in new_tables:
        new_tables = normalizer.second_normal_form(my_table)
    
    for my_table in new_tables:
        my_table.print_table()


if __name__ == "__main__":
    main()