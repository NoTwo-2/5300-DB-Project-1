import table

def is_1nf(my_table: table.Table) -> bool:
    '''
    This takes in a table and returns True if it is in 1nf
    '''
    for tuple in my_table.tuples:
        for value in tuple:
            if " " in value:
                return False
    return True

def first_normal_form(my_table: table.Table) -> list[table.Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in first normal forms
    
    Note: tuples with multivalue attributes will have spaces deliniating the different individual values
    '''
    # We know we will only get back one table from 1nf
    new_table = table.Table(my_table.columns)
    new_table.primary_key = my_table.primary_key
    new_table.funct_depends = my_table.funct_depends
    
    new_tuples: 'list[tuple]' = []
    
    for tuple in my_table.tuples:
        new_tuples.append(tuple)
        for value in tuple:
            if not (" " in value):
                continue
            # Remove the original tuple from new_tuples if it exists, and replace it with singe valued tuples
            if tuple in new_tuples:
                new_tuples.remove(tuple)
            
            value_index = tuple.index(value)
            value_list = value.split()
            for new_val in value_list:
                new_tuple = tuple[:value_index] + (new_val,) + tuple[value_index+1:]
                new_tuples.append(new_tuple)
    new_table.add_tuples(new_tuples)
    
    return [new_table]

def is_2nf(my_table: table.Table) -> bool:
    '''
    This takes in a table and returns True if it is in 2nf
    '''
    primes = my_table.get_primes()
    non_primes = list(range(len(my_table.columns)))
    for attr in primes:
        non_primes.remove(attr)
    
    for attr in non_primes:
        if my_table.is_partially_dependant(attr):
            return False
    return True

def convert_index(index: int, old_columns: list[str], new_columns: list[str]) -> int:
    '''
    This takes in an index in the old and two columns and outputs the index in the new
    '''
    old_col = old_columns[index]
    new_index = new_columns.index(old_col)
    return new_index

def second_normal_form(my_table: table.Table) -> list[table.Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in second normal forms
    '''
    primes = my_table.get_primes()
    non_primes = list(range(len(my_table.columns)))
    for attr in primes:
        non_primes.remove(attr)
    
    new_dependancies: 'list[tuple[list[int], list[int]]]' = []
    # For each non-prime attribute, check if its determinant is a proper subset of the primary key
    for attr in non_primes:
        valid_non_prime = not my_table.is_partially_dependant(attr)
        if valid_non_prime:
            continue
        
        # Find the functional dependency that corresponds with this attribute 
        # And add it to the list of new dependencies
        determinant = my_table.get_determinant(attr)
        dependants = my_table.get_dependants(determinant)
        new_depend = (determinant, dependants)
        if not (new_depend in new_dependancies):
            new_dependancies.append(new_depend)
    
    # Now that we have all the dependancies that will be the basis of our new tables,
    # We need to construct our new tables
    new_tables: list[table.Table] = []
    for funct_depend in new_dependancies:
        table_funct_depends = [funct_depend]
        table_mvds: list[tuple[int, tuple[int, int]]] = []
        table_columns: list[int] = []

        det, dep = funct_depend
        funct_depend_attributes = det.copy()
        funct_depend_attributes.extend(dep.copy())

        # Add attributes to the new columns
        table_columns.extend(funct_depend_attributes)
        # First, we find if any multivalued functional dependencies described by any attributes in our set of columns
        # And if we do, we add them to mvds
        for attr in table_columns:
            mvd_dependant = my_table.get_mvd_dependants(attr)
            if len(mvd_dependant) == 0:
                continue
            new_mvd = (attr, mvd_dependant)
            table_mvds.append(new_mvd)

        # Last, we need to find any transitive functional dependencies in our columns, and take them with us
        for det, dep in my_table.funct_depends:
            determinant_in_col = all(attr in table_columns for attr in det)
            if determinant_in_col:
                new_dependants: list[int] = []
                for attr in dep:
                    if not (attr in table_columns):
                        continue
                    new_dependants.append(attr)
                if len(new_dependants) == 0:
                    continue
                new_dependancy = (det, new_dependants)
                if new_dependancy in table_funct_depends:
                    continue
                table_funct_depends.append(new_dependancy)

        # Construct the table!
        table_columns.sort()
        new_columns = [my_table.columns[i] for i in table_columns]
        new_table = table.Table(new_columns)
        new_pk = [convert_index(i, my_table.columns, new_table.columns) for i in funct_depend[0]]
        new_table.primary_key = new_pk
        for det, dep in table_funct_depends:
            new_det = [convert_index(i, my_table.columns, new_table.columns) for i in det]
            new_dep = [convert_index(i, my_table.columns, new_table.columns) for i in dep]
            new_table.funct_depends.append((new_det, new_dep))
        for det, dep in table_mvds:
            new_det = convert_index(det, my_table.columns, new_table.columns)
            new_dep = tuple([convert_index(i, my_table.columns, new_table.columns) for i in dep])
            new_table.multi_funct_depends.append((new_det, new_dep))
        new_table.multi_funct_depends = table_mvds
        new_tables.append(new_table)

        # Having constructed our new tables, we now need to add all the tuples back into them
        new_tuples: list[tuple[str]] = []
        for tup in my_table.tuples:
            new_tuple: tuple[str] = tuple([tup[i] for i in table_columns])
            if not (new_tuple in new_tuples):
                new_tuples.append(new_tuple)
        new_table.add_tuples(new_tuples)

    return new_tables
        

def third_normal_form(my_table: table.Table) -> list[table.Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in third normal forms
    '''
    pass

def boyce_codd_normal_form(my_table: table.Table) -> list[table.Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in boyce codd normal forms
    '''
    pass

def forth_normal_form(my_table: table.Table) -> list[table.Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in fourth normal forms
    '''
    pass

def fifth_normal_form(my_table: table.Table) -> list[table.Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in fifth normal forms
    '''
    pass