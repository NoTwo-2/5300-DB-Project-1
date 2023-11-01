from tabulate import tabulate

class Table:
    
    def __init__(
        self, 
        columns: list[str], 
        tuples: 'list[tuple[str]]' = []
    ):
        self.columns: list[str] = columns
        
        self.tuples: 'list[tuple[str]]' = []
        for tuple in tuples:
            self.add_tuple(tuple)
        
        # These will be set in other functions
        self.primary_key: list[int] = []
        self.funct_depends: 'list[tuple[list[int], list[int]]]'= []
        
    def set_primary_key(self, attributes: list[str])-> None:
        '''
        This takes in one or more attributes and sets self.primary_key to the indexes of them in self.columns\n
        Returns a RuntimeError if any attribute is not found
        '''
        for attribute in attributes:
            self.check_attribute_if_valid(attribute)
        
        for attribute in attributes:
            self.primary_key.append(self.columns.index(attribute))
    
    def set_functional_dependencies(self, *dependencies: tuple[list[str], list[str]]) -> None:
        '''
        This takes in one or more functional dependencies in the form of tuples (a, b) where a -> b.\n 
        And sets self.funct_depends to these values\n
        Returns a RuntimeError if any attribute is not found
        '''
        for dependency in dependencies:
            determinant = dependency[0]
            determ_list: list[int] = []
            for attr in determinant:
                self.check_attribute_if_valid(attr)
            dependant = dependency[1]
            depend_list: list[int] = []
            for attr in dependant:
                self.check_attribute_if_valid(attr)
            
            for attr in determinant:
                index = self.columns.index(attr)
                determ_list.append(index)
            for attr in dependant:
                index = self.columns.index(attr)
                depend_list.append(index)
            
            self.funct_depends.append((determ_list, depend_list))
    
    def check_attribute_if_valid(self, attr: str) -> None:
        if not (attr in self.columns):
            raise RuntimeError(f"'{attr}' is not a valid attribute")
    
    def add_tuple(self, tuple: tuple[str]) -> None:
        if len(tuple) != len(self.columns):
            raise RuntimeError(f"{tuple} values dont line up with {self.columns}")
        self.tuples.append(tuple)
    
    def add_tuples(self, tuples: list[tuple[str]]) -> None:
        '''
        This takes in a list of tuples and adds them to the tuple list
        '''
        for tuple in tuples:
            self.add_tuple(tuple)
    
    def remove_tuple(self, primary_key: tuple) -> None:
        '''
        Takes in a tuple of the PK values of the specific tuple to remove.\n
        Make sure the order of these values match the order of the attributes you entered to set the PK\n
        Raises a runtime error if no tuple is found or if more than one tuple is found
        To keep it simple, enter these in the order they appear in the table <----!!!!
        '''
        tuples_to_search = self.tuples.copy()
        # TODO make sure that the PK values are entered in the order they appear in the column list (just sort them)
        if len(primary_key) != len(self.primary_key):
            raise RuntimeError(f"{primary_key} values dont line up with {self.primary_key}")
        # For each primary key value
        for i in range(len(primary_key)):
            matching_tuples = []
            pk_index = self.primary_key[i]
            # For each tuple in the list of tuples
            for tuple in tuples_to_search:
                if tuple[pk_index] == primary_key[i]: 
                    matching_tuples.append(tuple)
            tuples_to_search = matching_tuples.copy()
        if len(tuples_to_search) == 0:
            raise RuntimeError(f"No tuple found with PK {primary_key}")
        if len(tuples_to_search) != 1:
            raise RuntimeError(f"PK {primary_key} does not uniquely describe tuple, returned {tuples_to_search}")
        self.tuples.remove(tuples_to_search[0])
    
    def get_columns(self, indexes: list[int]) -> str:
        '''
        This takes in a list of indexes to specific columns\n
        And returns the names of those columns, formatted into a string, with a comma seperating them\n
        Mostly just a helper function so that I dont have to repeat code i wrote over and over
        '''
        string = ""
        
        first_elem = self.columns[indexes[0]]
        string += first_elem
        for i in indexes[1:]:
            string += f", {self.columns[i]}"
        
        return string
    
    def print_table(self) -> None:
        '''
        This will print the table data formatted with tabulate
        '''
        formatted_table = tabulate(self.tuples, headers=self.columns)
        print(formatted_table)
    
    def print_primary_key(self) -> None:
        '''
        This will print the primary key for the table
        '''
        pk_str = self.get_columns(self.primary_key)
        print(f"PK: {{ {pk_str} }}")

    def print_functional_dependencies(self) -> None:
        '''
        This will print a list of functional dependencies
        '''
        print("Functional Dependancies:")
        for dependancy in self.funct_depends:
            determinant = dependancy[0]
            determ_str = self.get_columns(determinant)
            
            depenant = dependancy[1]
            depend_str = self.get_columns(depenant)
            
            print(f"{determ_str} -> {depend_str}")
            