class Table:
    
    def __init__(
        self, 
        columns: list[str], 
        tuples: list[tuple] = []
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
        
    