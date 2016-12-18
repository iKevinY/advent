import fileinput


def is_safe(row, x):
    """Helper function to read out-of-bounds tiles as safe."""
    if x < 0 or x >= len(row):
        return True

    return row[x]


def predict_next_row(row):
    """Given a row, returns the predicted following row."""
    next_row = []

    for i in range(len(row)):
        a, b, c = (is_safe(row, x) for x in range(i-1, i+2))
        next_row.append(predict_safe(a, b, c))

    return tuple(next_row)


def predict_safe(a, b, c):
    if a and b and not c:
        return False
    elif not a and b and c:
        return False
    elif a and not b and not c:
        return False
    elif not a and not b and c:
        return False

    return True


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
