class Table:
    
    def __init__(
        self, 
        columns: list[str], 
        tuples: list[tuple[str]] = []
    ):
        self.columns: list[str] = columns
        
        self.tuples = []
        for tuple in tuples:
            self.add_tuple(tuple)
        
        # These will be set in other functions
        self.primary_key: list[int] = []
        self.funct_depends: dict[int, int] = {}
        
    def set_primary_key(self, *attributes: str)-> None:
        '''
        This takes in one or more attributes and sets self.primary_key to the indexes of them in self.columns\n
        Returns a RuntimeError if any attribute is not found
        '''
        for attribute in attributes:
            self.check_attribute_if_valid(attribute)
            self.columns.append(self.columns.index(attribute))
    
    def set_functional_dependencies(self, *dependencies: tuple[str, str]):
        '''
        This takes in one or more functional dependencies in the form of tuples (a, b) where a -> b.\n 
        And sets self.funct_depends to these values\n
        For cases where a, b -> c, do two tuples (a, c) and (b, c)\n
        Returns a RuntimeError if any attribute is not found
        '''
        for dependency in dependencies:
            determinant = dependency[0]
            self.check_attribute_if_valid(determinant)
            dependant = dependency[1]
            self.check_attribute_if_valid(dependant)
            
            determ_index = self.columns.index(determinant)
            depend_index = self.columns.index(dependant)
            
            self.funct_depends[determ_index] = depend_index
    
    def check_attribute_if_valid(self, attr: str) -> None:
        if not (attr in self.columns):
            raise RuntimeError(f"{attr} is not in {self.columns}")
    
    def add_tuple(self, tuple: tuple) -> None:
        if len(tuple) != len(self.columns):
            raise RuntimeError(f"{tuple} values dont line up with {self.columns}")
        self.tuples.append(tuple)
    
    def remove_tuple(self, primary_key: tuple[str]):
        '''
        Takes in a tuple of the PK values of the specific tuple to remove.\n
        Make sure the order of these values match the order of the attributes you entered to set the PK\n
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
        if len(tuples_to_search) != 1:
            raise RuntimeError(f"PK {primary_key} does not uniquely describe tuple, returned {tuples_to_search}")
        self.tuples.remove(tuples_to_search[0])
    