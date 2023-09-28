class Table:
    
    def __init__(self, columns: list[str], primary_key: list[str], functional_dependencies: dict[str, str]):
        self.columns: list[str] = columns
        self.check_for_invalid_columns(primary_key)
        self.primary_key: list[str] = primary_key
        for lhs, rhs in functional_dependencies:
            self.check_for_invalid_columns([lhs, rhs])
        self.functional_dependencies: dict[str, str] = functional_dependencies
    
    def check_for_invalid_columns(self, cols: list[str]) -> None:
        for col in cols:
            if not (col in self.columns):
                raise RuntimeError(f"{col} is not in {self.columns}")
                