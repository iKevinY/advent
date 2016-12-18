import fileinput


def is_safe(row, i):
    """Helper function to read out-of-bounds tiles as safe."""
    if 0 <= i < len(row):
        return row[i]

    return True


def predict_next_row(row):
    """Given a row, returns the predicted following row."""
    return [not (is_safe(row, i-1) ^ is_safe(row, i+1)) for i in range(len(row))]


if __name__ == '__main__':
    # Represent safe tiles as True and traps as False
    raw_first_row = fileinput.input()[0].strip()
    row = tuple(True if c == '.' else False for c in raw_first_row)
    safe_tiles = sum(row)

    for _ in range(40 - 1):
        row = predict_next_row(row)
        safe_tiles += sum(row)

    print "Number of safe tiles in first 40 rows:", safe_tiles

    for _ in range(400000 - 40):
        row = predict_next_row(row)
        safe_tiles += sum(row)

    print "Number of safe tiles in all 400000 rows:", safe_tiles
