import argparse
import math
import os
import sys
import time

import numpy as np
import pandas as pd
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def parse_args():
    parser = argparse.ArgumentParser(description='simple script to calculate your final grade')
    parser.add_argument('-f', dest='file_path', help='path to the grades file')
    return parser.parse_args()


def load_grades(file_path):
    try:
        return pd.read_csv(file_path, comment='#')
    except OSError:
        print('Could not find file using path \"{}\"'.format(file_path))
        sys.exit(1)


def calc_final_grade(grades):
    # calc product of grade and ects
    grades['grade_times_ects'] = grades.grade * grades.ects
    # group by group
    grouped = grades.groupby(by='group')
    ects_per_group = grouped.ects.sum()
    print("Calculations based on {} / 120 ECTS points".format(ects_per_group.sum()))
    # calculate group mean
    grade_per_group = grouped.grade_times_ects.sum() / ects_per_group
    # join a column with truncated decimals
    grade_per_group_trunc = trunc(grade_per_group)
    print_grade_per_group(grade_per_group, grade_per_group_trunc)
    # calc weighted total average
    total_average = (grade_per_group_trunc * ects_per_group).sum() / ects_per_group.sum()
    print_total_average(total_average)


def print_grade_per_group(grades, grades_trunc):
    # concat series
    x = pd.concat([grades, grades_trunc], axis=1, keys=['grade', 'grade_trunc'])
    print('Average per group:')
    for k, v in x.iterrows():
        print('\t{}: {:0.1f} (exact: {:0.5f})'.format(k, v.grade_trunc, v.grade))


def print_total_average(total_average):
    print('Total average: {:0.1f} (exact: {:0.5f})'.format(math.floor(total_average * 10) / 10, total_average))


def trunc(x, dec=1):
    d = np.power(10, dec)
    return np.floor(x * d) / d


class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        grades = load_grades(event.src_path)
        calc_final_grade(grades)
        pass

if __name__ == '__main__':
    args = parse_args()
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(args.file_path), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
