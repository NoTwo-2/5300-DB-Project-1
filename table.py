class Table:
    
    def __init__(self, columns: list[str], primary_key: list[str], funct_depends: dict[str, str], tuples: list[tuple]):
        self.columns: list[str] = columns
        self.check_for_invalid_columns(primary_key)
        self.primary_key: list[str] = primary_key
        for lhs, rhs in funct_depends:
            self.check_for_invalid_columns([lhs, rhs])
        self.funct_depends: dict[str, str] = funct_depends
        self.tuples = []
        for tuple in tuples:
            self.add_tuple(tuple)
    
    def check_for_invalid_columns(self, cols: list[str]) -> None:
        for col in cols:
            if not (col in self.columns):
                raise RuntimeError(f"{col} is not in {self.columns}")
    
    def add_tuple(self, tuple: tuple) -> None:
        if len(tuple) != len(self.columns):
            raise RuntimeError(f"{tuple} values dont line up with {self.columns}")
        self.tuples.append(tuple)
                