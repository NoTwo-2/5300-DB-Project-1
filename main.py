import table
import csv_parser
import normalizer

def input_funct_depends(my_table: table.Table) -> None:
    '''
    This will take in a table object, prompt the user for functional dependencies, and add them in the table
    '''
    print()
    counter = 0
    for col in my_table.columns:
        print(f"{counter}) {col}")
        counter += 1
    print(
        "Please input any valid functional dependencies, or hit enter if finished\n"
        "Note: if there are any transitive FDs a->b,c and c->d, write them as a->b,c,d and c->d\n"
        "Format: 0, 1 -> 2, 3"
    )
    done = False
    while not done:
        entry = input(": ")
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
        
        try:
            streterminant = [int(attr.strip()) for attr in spleterminant]
            strependant = [int(attr.strip()) for attr in splependant]
        except ValueError as err:
            print(f"Something was wrong with your input: {err}")
            continue
        try:
            for i in streterminant:
                my_table.columns[i]
            for i in strependant:
                my_table.columns[i]
            my_table.funct_depends.append((streterminant, strependant))
            print(f"Added {[my_table.columns[i] for i in streterminant]} -> {[my_table.columns[i] for i in strependant]} to list of functional dependencies.")
        except IndexError as err:
            print(f"One or more of your attributes entered had an issue: {err}")
            continue
        
    
def input_mvds(my_table: table.Table) -> None:
    '''
    This will take in a table object, prompt the user for multivalue functional dependencies, and add them in the table
    '''
    print()
    counter = 0
    for col in my_table.columns:
        print(f"{counter}) {col}")
        counter += 1
    print("Please input any valid multivalue functional dependencies, or hit enter if finished\nFormat: Determinant ->-> Dependant ")
    done = False
    while not done:
        entry = input(": ")
        if entry.strip() == "":
            return
        if not ("->->" in entry):
            print("You did not include an '->->'in your definition. Please try again.")
            continue
        splentry = entry.split("->->")
        
        determinant = splentry[0]
        dependant = splentry[1]
        
        try:
            numerminant = int(determinant.strip())
            numendant = int(dependant.strip())
        except ValueError as err:
            print(f"Something was wrong with your input: {err}")
            continue
        
        try:
            my_table.columns[numerminant]
            my_table.columns[numendant]
            my_table.multi_funct_depends.append((numerminant, numendant))
            print(f"Added {my_table.columns[numerminant]} ->-> {my_table.columns[numendant]} to list of functional dependencies.")
        except RuntimeError as err:
            print(f"One or more of your attributes entered had an issue: {err}")
            continue

def input_primary_key(my_table: table.Table) -> None:
    '''
    This will take in a table object, prompt the user for the primary key, and set the primary key in the table
    '''
    print()
    candidate_keys = my_table.get_candidate_keys()
    counter = 0
    for key in candidate_keys:
        print(f"{counter}) {[my_table.columns[i] for i in key]}")
        counter += 1
    print("Please select a candidate key to be a primary key")
    done = False
    while not done:
        entry = input(": ")
        try:
            nentry = int(entry.strip())
        except ValueError as err:
            print(f"Something was wrong with your input: {err}")
            continue
            
        try:
            my_table.primary_key = candidate_keys[nentry]
            done = True
        except IndexError as err:
            print(f"Something was wrong with your input: {err}")
            
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
        print_str = ""
        for my_table in table_list:
            match form_counter:
                case 1:
                    print_str = "Normalized to 1st normal form"
                    new_table_list += normalizer.first_normal_form(my_table)
                case 2:
                    print_str = "Normalized to 2nd normal form"
                    new_table_list += normalizer.second_normal_form(my_table)
                case 3:
                    print_str = "Normalized to 3rd normal form"
                    new_table_list += normalizer.third_normal_form(my_table)
                case 4:
                    print_str = "Normalized to Boyce Codd normal form"
                    new_table_list += normalizer.boyce_codd_normal_form(my_table)
                case 5:
                    print_str = "Normalized to 4th normal form"
                    new_table_list += normalizer.forth_normal_form(my_table)
                case 6:
                    print_str = "Normalized to 5th normal form"
                    new_table_list += normalizer.fifth_normal_form(my_table)
                case _:
                    raise RuntimeError(f"What.")
        print(f"-----====={print_str}=====-----")
        for new_table in new_table_list:
            print()
            new_table.print_table()
            new_table.print_primary_key()
            new_table.print_functional_dependencies()
            new_table.print_mvds()
        table_list = new_table_list
    return table_list

def main():
    my_table = create_table()
    
    input_funct_depends(my_table)
    input_primary_key(my_table)
    input_mvds(my_table)
    
    normal_form = int(input(
        "Please enter the form you would like to normalize to\n"
        "1) First normal form\n"
        "2) Second normal form\n"
        "3) Third normal form\n"
        "4) Boyce Codd normal form\n"
        "5) Fourth normal form\n"
        "6) Fifth normal form\n"
        "Form: "
    ))
    
    print("\n-----=====Original Table=====-----")
    my_table.print_table()
    my_table.print_primary_key()
    my_table.print_functional_dependencies()
    my_table.print_mvds()
    
    normalize_to_form(my_table, normal_form)
    
    # ---------------=================== DEBUG ===================-------------------

def debug_main(my_table: table.Table):
    print("\n----=====Original Table=====-----")
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
    
    fnf_tables: list[table.Table] = normalizer.first_normal_form(my_table)
    print("\n-----=====First Normal Form=====-----")
    print(fnf_tables)
    for fnf in fnf_tables:
        fnf.print_table()
        fnf.print_functional_dependencies()
        fnf.print_mvds()
    
    snf_tables: list[table.Table] = []
    for fnf in fnf_tables:
        snf_tables.extend(normalizer.second_normal_form(fnf))
    
    print("\n-----=====Second Normal Form=====-----")
    for snf in snf_tables:
        snf.print_table()
        snf.print_primary_key()
        snf.print_functional_dependencies()
        snf.print_mvds()
    
    tnf_tables: list[table.Table] = []
    for snf in snf_tables:
        tnf_tables.extend(normalizer.third_normal_form(snf))
    
    print("\n-----=====Third Normal Form=====-----")
    for tnf in tnf_tables:
        tnf.print_table()
        tnf.print_primary_key()
        tnf.print_functional_dependencies()
        tnf.print_mvds()
        
    bcnf_tables: list[table.Table] = []
    for tnf in tnf_tables:
        bcnf_tables.extend(normalizer.boyce_codd_normal_form(tnf))
    
    print("\n-----=====Boyce Codd Normal Form=====-----")
    for bcnf in bcnf_tables:
        bcnf.print_table()
        bcnf.print_primary_key()
        bcnf.print_functional_dependencies()
        bcnf.print_mvds()

def debug():
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
        ("Course", "Professor"),
        ("Course", "BuildingID"),
        ("StudentID", "Course"),
        ("StudentID", "Professor")
    )
    
    debug_main(my_table)

def debug2():
    csv_cols, csv_rows = csv_parser.parse_csv("example2.csv")
    my_table = table.Table(csv_cols, csv_rows)
    
    my_table.set_primary_key(["Property_id#"])
    my_table.set_functional_dependencies(
        (["Property_id#"], ["County_name", "Lot#", "Area", "Price", "Tax_rate"]),
        (["County_name", "Lot#"], ["Property_id#", "Area", "Price", "Tax_rate"]),
        (["County_name"], ["Tax_rate"]),
        (["Area"], ["Price"])
    )
    
    debug_main(my_table)
    
def debug3():
    csv_cols, csv_rows = csv_parser.parse_csv("example3.csv")
    my_table = table.Table(csv_cols, csv_rows)
    
    my_table.set_primary_key(["Ssn", "Pnumber"])
    my_table.set_functional_dependencies(
        (["Ssn", "Pnumber"], ["Hours"]),
        (["Ssn"], ["Ename"]),
        (["Pnumber"], ["Pname", "Plocation"])
    )
    
    debug_main(my_table)
    
def debug4():
    csv_cols, csv_rows = csv_parser.parse_csv("example4.csv")
    my_table = table.Table(csv_cols, csv_rows)
    
    my_table.set_primary_key(["Property_id#"])
    my_table.set_functional_dependencies(
        (["Property_id#"], ["County_name", "Lot#", "Area"]),
        (["County_name", "Lot#"], ["Property_id#", "Area"]),
        (["Area"], ["County_name"])
    )
    
    debug_main(my_table)


if __name__ == "__main__":
    main()
    #debug()
    #debug2()
    #debug3()
    #debug4()