import pandas as pd
import numpy as np
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='simple script to calculate your final grade')
    parser.add_argument('-f', dest='file_path', help='path to the grades file')
    return parser.parse_args()


def load_grades(file_path):
    try:
        return pd.read_csv(file_path)
    except OSError:
        print('Could not find file using path \"{}\"'.format(file_path))
        sys.exit(1)


def calc_final_grade(grades):
    # calc product of grade and ects
    grades['grade_times_ects'] = grades.grade * grades.ects
    # group by group
    grouped = grades.groupby(by='group')
    ects_per_group = grouped.ects.sum()
    # calculate group mean
    grade_per_group = grouped.grade_times_ects.sum() / ects_per_group
    # cut off decimals
    grade_per_group = trunc(grade_per_group)
    print_grade_per_group(grade_per_group)
    # calc weighted total average
    total_average = (grade_per_group * ects_per_group).sum() / ects_per_group.sum()
    print_total_average(total_average)


def print_grade_per_group(grades):
    print('Average per group:')
    for group, grade in grades.iteritems():
        print('\t{}: {}'.format(group, grade))


def print_total_average(total_average):
    print('Total average: {0:0.1f} (exact: {0:0.5f})'.format(total_average, total_average))


def trunc(x, dec=1):
    d = np.power(10, dec)
    return np.floor(x * d) / d

if __name__ == '__main__':
    args = parse_args()
    grades = load_grades(args.file_path)
    calc_final_grade(grades)
