import table

def move_mvds(old_table: table.Table, new_table: table.Table) -> None:
    '''
    This takes in an old table and a new table
    and transfers any multifunctional dependencies that are still valid from the old to the new
    '''
    pass

def construct_table_from_funct_dep(old_table: table.Table, funct_depend: tuple[list[int], list[int]]) -> table.Table:
    '''
    This takes in an old table and a functional dependancy
    and returns a new table containing all relevant mvds and functional dependencies
    '''
    table_funct_depends: list[tuple[list[int], list[int]]] = []
    if len(funct_depend[1]) != 0:
        table_funct_depends.append(funct_depend)
    table_mvds: list[tuple[int, tuple[int, int]]] = []
    table_columns: list[int] = []

    # Add attributes from the functional dependency to the new columns
    det, dep = funct_depend
    funct_depend_attributes = det.copy()
    funct_depend_attributes.extend(dep.copy())
    table_columns.extend(funct_depend_attributes)
    
    # First, we find if any multivalued functional dependencies with all elements present in the new tables columns
    # And if we do, we add them to mvds
    for attr in table_columns:
        mvd_dependant = old_table.get_mvd_dependants(attr)
        if len(mvd_dependant) == 0:
            continue
        dep_in_col = all(attr in table_columns for attr in mvd_dependant)
        if not dep_in_col:
            continue
        new_mvd = (attr, mvd_dependant)
        table_mvds.append(new_mvd)

    # Last, we need to find any transitive functional dependencies in our columns, and take them with us
    for det, dep in old_table.funct_depends:
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
    new_table = construct_table(
        old_table=old_table, 
        new_col_indexes=table_columns, 
        primary_key=funct_depend[0], 
        functional_dependencies=table_funct_depends,
        multivalue_attributes=table_mvds
        )
    
    return new_table

def convert_index(index: int, old_columns: list[str], new_columns: list[str]) -> int:
    '''
    This takes in an index in the old and two columns and outputs the index in the new
    '''
    old_col = old_columns[index]
    new_index = new_columns.index(old_col)
    return new_index

def construct_table(
    old_table: table.Table,
    new_col_indexes: list[int],
    primary_key: list[int],
    functional_dependencies: list[tuple[list[int], list[int]]],
    multivalue_attributes: list[tuple[int, tuple[int, int]]]
    ) -> table.Table:
    '''
    This will take in an old table and other info needed, and construct and return a new one
    '''
    # Convert old indexes to new ones and construct the table with rows, the pk, fds, and mvds
    new_col_indexes.sort()
    new_columns = [old_table.columns[i] for i in new_col_indexes]
    new_table = table.Table(new_columns)
    new_pk = [convert_index(i, old_table.columns, new_table.columns) for i in primary_key]
    new_table.primary_key = new_pk
    for det, dep in functional_dependencies:
        new_det = [convert_index(i, old_table.columns, new_table.columns) for i in det]
        new_dep = [convert_index(i, old_table.columns, new_table.columns) for i in dep]
        new_table.funct_depends.append((new_det, new_dep))
    for det, dep in multivalue_attributes:
        new_det = convert_index(det, old_table.columns, new_table.columns)
        new_dep = tuple([convert_index(i, old_table.columns, new_table.columns) for i in dep])
        new_table.multi_funct_depends.append((new_det, new_dep))

    # Having constructed our new table, we now need to add all the tuples back into it
    for tup in old_table.tuples:
        new_tuple: tuple[str] = tuple([tup[i] for i in new_col_indexes])
        if not (new_tuple in new_table.tuples):
            new_table.add_tuple(new_tuple)
    return new_table

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
    new_table.multi_funct_depends = my_table.multi_funct_depends
    
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
    partial_dependancies = my_table.get_partial_dependencies()
    
    return len(partial_dependancies) == 0

def second_normal_form(my_table: table.Table) -> list[table.Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in second normal forms
    '''
    # Get the dependancies that will form the basis of our new tables
    new_dependancies: 'list[tuple[list[int], list[int]]]' = my_table.get_partial_dependencies()
    
    # Before we add the other tables, we need to make sure we still have a table with our full primary key in it
    # So, we add the primary key, and any dependants that arent covered by other tables and add it here
    pk_not_in_dependancies = all(my_table.primary_key != funct_depend[0] for funct_depend in new_dependancies)
    if pk_not_in_dependancies:
        pk_dependant = my_table.get_dependants(my_table.primary_key)
        for attr in pk_dependant:
            for det, dep in new_dependancies:
                if attr in dep:
                    pk_dependant.remove(attr)
        new_dependancies.append((my_table.primary_key, pk_dependant))
    
    # Now that we have all the dependancies that will be the basis of our new tables,
    # We need to construct our new tables
    new_tables: list[table.Table] = []
    # For each FD in the list, we make a new table with it IF a table with the same columns doesnt already exist
    for funct_depend in new_dependancies:
        new_table = construct_table_from_funct_dep(my_table, funct_depend)
        
        new_tables.append(new_table)

    return new_tables

def is_3nf(my_table: table.Table) -> bool:
    '''
    This takes in a table and returns True if it is in 3nf
    '''
    transitive_dependancies = my_table.get_transitive_dependancies()
    
    return len(transitive_dependancies) == 0

def third_normal_form(my_table: table.Table) -> list[table.Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in third normal forms
    '''
    new_dependancies: 'list[tuple[list[int], list[int]]]' = my_table.get_transitive_dependancies()
    
    # We need to add the primary key back to the list of new dependancies
    # And remove any determinants represented by any other table
    pk_dependant = my_table.get_dependants(my_table.primary_key)
    for attr in pk_dependant:
        for det, dep in new_dependancies:
            if attr in dep:
                pk_dependant.remove(attr)
    new_dependancies.append((my_table.primary_key, pk_dependant))
    
    # Now that we have all the dependancies that will be the basis of our new tables,
    # We need to construct our new tables
    new_tables: list[table.Table] = []
    # For each FD in the list, we make a new table with it IF a table with the same columns doesnt already exist
    for funct_depend in new_dependancies:
        new_table = construct_table_from_funct_dep(my_table, funct_depend)
        
        new_tables.append(new_table)

    return new_tables

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