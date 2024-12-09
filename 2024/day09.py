import copy
import fileinput


def read_disk(disk_map, part_2=False):
    """
    Takes a disk map as a string and returns a list of the form
    (block_id, length) and the maximium block ID. For free space,
    `block_id` is set to None.
    """
    # Pad the disk with free space at the end for part 1.
    disk_map += '0'

    disk = []
    for block_id, (file_length, free_length) in enumerate(zip(disk_map[::2], disk_map[1::2])):
        if part_2:
            disk.append((block_id, int(file_length)))
            disk.append((None, int(free_length)))
        else:
            for _ in range(int(file_length)):
                disk.append((block_id, 1))
            for _ in range(int(free_length)):
                disk.append((None, 1))

    return disk, block_id

def disk_checksum(disk):
    """Returns the checksum of a disk."""
    checksum = 0
    idx = 0
    for block_id, length in disk:
        if block_id == None:
            idx += length
        else:
            for _ in range(length):
                checksum += block_id * idx
                idx += 1

    return checksum


def compact_disk(disk, max_block_id, part_2=False):
    """Performs the compacting operation on the disk."""
    disk = copy.deepcopy(disk)

    # The current block we should try to shift (if in Part 2).
    block = max_block_id

    while True:
        # Search for the next block to compact.
        idx = len(disk) - 1

        # If part 2, it's when we find a block matching the expected ID.
        if part_2:
            while disk[idx][0] != block:
                idx -= 1
                if idx < 0:
                    break

        # Otherwise, it's whenever we find a non-empty block.
        else:
            while disk[idx][0] == None:
                idx -= 1
                if idx < 0:
                    break

        # Try to perform a shift with the left-most free space we find.
        block_id, block_length = disk[idx]
        for free in range(len(disk)):
            free_id, free_length = disk[free]

            # If the `free` pointer is to the right of the `idx` pointer,
            # we've moved too far to attempt to find a possible swap.
            if idx < free:
                break

            # We've found a valid block to move!
            if free_id == None and block_length <= free_length:
                # Delete the existing free and file blocks (order matters).
                del disk[idx]
                del disk[free]

                # Create new free and file blocks (order matters).
                disk.insert(free, (block_id, block_length))
                disk.insert(idx, (None, block_length))

                # If we're in part 2 and we moved the file into a free
                # spot with more room available, we need to create a
                # new free block with the remainder space.
                if block_length < free_length:
                    disk.insert(free + 1, (None, free_length - block_length))

                break

        # Termination conditions.
        if part_2:
            block -= 1
            if block == 0:
                break
        else:
            if idx < free:
                break

    return disk


# Read problem input.
DISK_MAP = fileinput.input()[0].strip()

disk = compact_disk(*read_disk(DISK_MAP))
print("Part 1:", disk_checksum(disk))

disk = compact_disk(*read_disk(DISK_MAP, part_2=True), part_2=True)
print("Part 2:", disk_checksum(disk))



