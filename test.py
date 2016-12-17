#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import glob
import resource
import subprocess


def clock():
    return resource.getrusage(resource.RUSAGE_CHILDREN)[0]


def format_time(timespan):
    """Formats the timespan in a human readable format"""
    if timespan >= 10.0:
        return '\033[91m%.3g s\033[0m' % timespan
    elif timespan >= 1.0:
        return '\033[93m%.3g s\033[0m' % timespan
    else:
        return '%.3g ms' % (timespan * 1e3)


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
                return False, cpu_usr
        else:
            return True, cpu_usr


def main():
    exit_code = 0

    if len(sys.argv) > 1:
        years = [sys.argv[1]]
    else:
        years = ['2015', '2016']

    for year in years:
        if len(sys.argv) > 2:
            programs = glob.glob('%s/day%02i.py' % (year, int(sys.argv[2])))
        else:
            programs = glob.glob('%s/day*.py' % year)

        for program in programs:
            day = int(re.findall(r'(\d+).py', program)[0])
            input_file = '%s/inputs/%02i.txt' % (year, day)
            output_file = '%s/outputs/%02i.txt' % (year, day)

            if os.path.exists(output_file):
                valid, cpu_usr = check_solution(program, input_file, output_file)
                print '{} {} Day {:02} ({})'.format('✓' if valid else '✗', year, day, format_time(cpu_usr))

                if not valid:
                    exit_code = 1

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
