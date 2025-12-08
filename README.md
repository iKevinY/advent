# iKevinY/advent

This repository contains my solutions to [Advent of Code](https://adventofcode.com)
problems.

These are not intended to be the fastest possible solutions, nor are they
always the solution I came to while solving the problem on the night-of.
They are cleaned up versions of the code, made to be relatively concise.

In addition, these solutions often rely heavily on importing `utils`, which
is the `utils.py` file that can be found in each year's subdirectory. This
often comes up when dealing with grids, because writing the same utility
classes for operating on objects in 2D space gets very repetitive.

For some insight into what my solutions look like *while* I'm solving a problem,
see my YouTube playlists of solves from [2022](https://www.youtube.com/playlist?list=PLrQuqV9YO5hQ-WndrHMWFlYyG8OWTnHng),
[2023](https://www.youtube.com/playlist?list=PLrQuqV9YO5hSrdTtbumg5hemhq1ntjbNA),
and [2024](https://www.youtube.com/playlist?list=PLrQuqV9YO5hRIR4AV5EmP-DSkRaflM9Qf).


## Test Runner

Under the request of the Advent of Code team, puzzle inputs and outputs
are not being committed to this repo. However, I have written a small
test runner for the puzzles.

The runner assumes that the input for year `YYYY`, day `DD` is stored
in `YYYY/inputs/DD.txt`, and that the expected output is present in
`YYYY/outputs/DD.txt`. If both files are present, the file will be
tested against the input; it passes if all lines in the output file
are printed to stdout during the execution of the program.

## License

Code in the `2015`, `2016`, `2017`, and `2018` directories are licensed
under the [MIT License](LICENSE).
