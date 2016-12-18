import fileinput


def is_trap(row, i):
    """Helper function to read out-of-bounds tiles as safe."""
    if 0 <= i < len(row):
        return row[i]

    return False


def predict_next_row(row):
    """Given a row, returns the predicted following row."""
    return [is_trap(row, i-1) ^ is_trap(row, i+1) for i in range(len(row))]


if __name__ == '__main__':
    # Represent traps as True and safe tiles as False.
    # The number of safe tiles per row is len(row) - sum(row).
    row = [c == '^' for c in fileinput.input()[0].strip()]
    row_len = len(row)
    safe_tiles = row_len - sum(row)

    for _ in range(40 - 1):
        row = predict_next_row(row)
        safe_tiles += row_len - sum(row)

    print "Number of safe tiles in first 40 rows:", safe_tiles

    for _ in range(400000 - 40):
        row = predict_next_row(row)
        safe_tiles += row_len - sum(row)

    print "Number of safe tiles in all 400000 rows:", safe_tiles
