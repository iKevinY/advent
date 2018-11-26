#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import glob
import argparse
import resource
import subprocess

try:
    from halo import Halo
except ImportError:
    # Use a noop context manager if Halo isn't installed
    from contextlib import contextmanager

    @contextmanager
    def Halo(text):
        yield


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def clock():
    return resource.getrusage(resource.RUSAGE_CHILDREN)[0]


def color_time_str(str, timespan):
    if abs(timespan) >= 10:
        color = bcolors.FAIL
    elif abs(timespan) >= 1:
        color = bcolors.WARNING
    else:
        color = ''

    return '{}{}{}'.format(color, str, bcolors.ENDC)


def format_time(timespan, padding=None):
    """Formats the timespan in a human readable format"""
    if timespan >= 1.0:
        time_str = '{:.3g} s'.format(timespan)
    else:
        time_str = '{:.3g} ms'.format(timespan * 1e3)

    if padding is not None:
        time_str = time_str.rjust(padding)

    return color_time_str(time_str, timespan)


def check_solution(program, day, input_file, output_file, pypy=False):
    with Halo(text='Day {:02}'.format(day)):
        cmd = ['pypy' if pypy else 'python', program, input_file]
        start = clock()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        stdout = proc.communicate()[0]
        end = clock()
        cpu_usr = end - start

    valid = True

    with open(output_file) as f:
        for line in f:
            if line.strip() not in stdout:
                valid = False
                break

    return valid, stdout, cpu_usr


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Advent of Code puzzle runner.")
    parser.add_argument('year', type=int)
    parser.add_argument('puzzles', type=int, metavar='puzzle', nargs='*')
    parser.add_argument('--pypy', const=True, action='store_const',
        help="use PyPy instead of CPython")
    parser.add_argument('--benchmark', const=True, action='store_const',
        help="compare PyPy against CPython")

    args = parser.parse_args()

    year = args.year
    puzzles = args.puzzles
    pypy = args.pypy

    if puzzles:
        programs = []
        for p in puzzles:
            programs.extend(glob.glob('%s/day%02i.py' % (year, p)))
    else:
        programs = glob.glob('%s/day*.py' % year)

    to_run = []

    for program in programs:
        day = int(re.findall(r'(\d+).py', program)[0])
        input_file = '%s/inputs/%02i.txt' % (year, day)
        output_file = '%s/outputs/%02i.txt' % (year, day)

        if os.path.exists(output_file):
            to_run.append((program, day, input_file, output_file))

    if args.benchmark:
        print "Day   CPython      PyPy      Delta    Speedup"
        print '-' * 45

        for program, day, input_file, output_file in to_run:
            cpy_time = check_solution(program, day, input_file, output_file, pypy=False)[2]
            pypy_time = check_solution(program, day, input_file, output_file, pypy=True)[2]

            print "{:02}    {}    {}   {}    {:0.1f}".format(
                day,
                format_time(cpy_time, padding=7),
                format_time(pypy_time, padding=7),
                format_time(cpy_time - pypy_time, padding=9),
                cpy_time / pypy_time,
            )

        sys.exit(0)

    exit_code = 0
    runtimes = []

    for program, day, input_file, output_file in to_run:
        valid, stdout, cpu_usr = check_solution(program, day, input_file, output_file, pypy)
        runtimes.append(cpu_usr)

        print '{}{}{} Day {:02} ({})'.format(
            bcolors.OKGREEN if valid else bcolors.FAIL,
            '✓' if valid else '✗',
            bcolors.ENDC,
            day,
            format_time(cpu_usr),
        )
        print stdout

        if not valid:
            exit_code = 1

    if len(puzzles) != 1:
        print "Total runtime:", format_time(sum(runtimes))

        cutoffs = [
            0.025, 0.050, 0.075, 0.100, 0.125, 0.150,
            0.200, 0.250, 0.300, 0.400, 0.500, 0.750,
            1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5,
        ]

        cutoffs.extend(range(5, 10))
        cutoffs.extend(range(10, 20, 2))
        cutoffs.extend(range(20, 120, 3))

        for day, runtime in enumerate(runtimes, start=1):
            out = "Day {:02}: {}".format(day, format_time(runtime, padding=7))
            bar_len = next(i + 1 for i, cutoff in enumerate(cutoffs) if runtime < cutoff)
            print out, color_time_str('■' * bar_len, runtime)

    sys.exit(exit_code)
