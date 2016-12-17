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


def human_time(timespan):
    """Formats the timespan in a human readable format"""
    if timespan >= 1.0:
        return '%.*g s' % (3, timespan * 1.0)
    else:
        return '%.*g ms' % (3, timespan * 1e3)


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

    for program in glob.glob('2016/day*.py'):
        day = int(re.findall(r'(\d+).py', program)[0])
        input_file = '2016/inputs/%02i.txt' % day
        output_file = '2016/outputs/%02i.txt' % day

        if os.path.exists(output_file):
            valid, cpu_usr = check_solution(program, input_file, output_file)
            print '{} Day {:02} ({})'.format('✓' if valid else '✗', day, human_time(cpu_usr))

            if not valid:
                exit_code = 1

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
