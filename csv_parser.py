def parse_csv(csv_file_location: str) -> tuple[list[str], list[tuple]]:
    with open(csv_file_location, "r") as csv:
        columns = csv.readline().split(",")
        # We strip leading and trailing whitespace
        columns = [str.strip(item) for item in columns]
        
        tuples = []
        while csv:
            # Check if line is empty, and stop the loop if it is
            line = csv.readline()
            print(line)
            if not line:
                break
            
            # We convert the line to a list, split by commas
            entry = line.split(",")
            # We strip leading and trailing whitespace and convert the list into a tuple
            entry = tuple([str.strip(item) for item in entry])
            # Check if the number of entries in the tuple is not equal with the number of columns
            if len(entry) != len(columns):
                raise RuntimeError(f"Items in {entry} not equal to number of columns ({len(columns)})")
            # Append the tuple to the list of tuples
            tuples.append(entry)
        
        return (columns, tuples)