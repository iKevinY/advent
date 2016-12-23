#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import glob
import resource
import subprocess


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def clock():
    return resource.getrusage(resource.RUSAGE_CHILDREN)[0]


def format_time(timespan):
    """Formats the timespan in a human readable format"""
    if timespan >= 1.0:
        return '{}{:.3g} s{}'.format(
            bcolors.FAIL if timespan >= 10 else bcolors.WARNING,
            timespan,
            bcolors.ENDC)
    else:
        return '{:.3g} ms'.format(timespan * 1e3)


def check_solution(program, input_file, output_file):
    cmd = ['python', program, input_file]
    start = clock()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout = proc.communicate()[0]
    end = clock()
    cpu_usr = end - start

    with open(output_file) as f:
        for line in f:
            if line.strip() not in stdout:
                return False, stdout, cpu_usr
        else:
            return True, stdout, cpu_usr


if __name__ == '__main__':
    exit_code = 0

    if len(sys.argv) == 1:
        print "Usage: ./test.py <year> [problem]"
        sys.exit()

    year = sys.argv[1]

    if len(sys.argv) > 2:
        programs = glob.glob('%s/day%02i.py' % (year, int(sys.argv[2])))
    else:
        programs = glob.glob('%s/day*.py' % year)

    for program in programs:
        day = int(re.findall(r'(\d+).py', program)[0])
        input_file = '%s/inputs/%02i.txt' % (year, day)
        output_file = '%s/outputs/%02i.txt' % (year, day)

        if os.path.exists(output_file):
            valid, stdout, cpu_usr = check_solution(program, input_file, output_file)
            print '{}{}{} {} Day {:02} ({})'.format(
                bcolors.OKGREEN if valid else bcolors.FAIL,
                '✓' if valid else '✗',
                bcolors.ENDC,
                year,
                day,
                format_time(cpu_usr),
            )
            print stdout

            if not valid:
                exit_code = 1

    sys.exit(exit_code)
