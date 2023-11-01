from table import Table

def is_1nf(table: Table) -> bool:
    '''
    This takes in a table and returns True if it is in 1nf
    '''
    for tuple in table.tuples:
        for value in tuple:
            if " " in value:
                return False
    
    return True

def first_normal_form(table: Table) -> list[Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in first normal forms
    
    Note: tuples with multivalue attributes will have spaces deliniating the different individual values
    '''
    # We know we will only get back one table from 1nf
    new_table = Table(table.columns)
    new_table.primary_key = table.primary_key
    new_table.funct_depends = table.funct_depends
    
    new_tuples: 'list[tuple]' = []
    
    for tuple in table.tuples:
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
                

def second_normal_form(table: Table) -> list[Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in second normal forms
    '''
    pass

def third_normal_form(table: Table) -> list[Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in third normal forms
    '''
    pass

def boyce_codd_normal_form(table: Table) -> list[Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in boyce codd normal forms
    '''
    pass

def forth_normal_form(table: Table) -> list[Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in fourth normal forms
    '''
    pass

def fifth_normal_form(table: Table) -> list[Table]:
    '''
    Takes in a table and returns a list of tables
    These tables store an equivalent amount of data as the inputed table
    The tables returned will be in fifth normal forms
    '''
    pass