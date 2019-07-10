#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# set operation for lines in two files
# eg: two ip list file, find different or common ips

import requests
import re
import argparse

def _parse_args():
     parser = argparse.ArgumentParser(description="find different in two file")
     parser.add_argument('left_file')
     parser.add_argument('right_file')
     parser.add_argument('-o', '--output', choices=['left_only', 'right_only', 'both', 'all'], required=False)
     return parser.parse_args()

def get_set_lines(filename):
    res = set()
    with open(filename, 'r') as f:
        for line in f:
            res.add(line.strip())
    return res

def left_only(left, right):
    diff = left["ip_set"].difference(right["ip_set"])
    print "Only in [{}]".format(left["name"])
    print "number: {}".format(len(diff))
    print "-------------------------------------"
    for i in sorted(diff):
        print i
    print ""
    return diff

def right_only(left, right):
    diff = right["ip_set"].difference(left["ip_set"])
    print "Only in [{}]".format(right["name"])
    print "number: {}".format(len(diff))
    print "-------------------------------------"
    for i in sorted(diff):
        print i
    print ""
    return diff

def both_left_and_right(left, right):
    intersection = left["ip_set"].intersection(right["ip_set"])
    print "both in [{}] and [{}]".format(left["name"], right["name"])
    print "number: {}".format(len(intersection))
    print "-------------------------------------"
    for i in sorted(intersection):
        print i
    print ""
    return intersection


def get_output(output_type, left, right):
    if output_type == "left_only":
        left_only(left, right)
    elif output_type == "right_only":
        right_only(left, right)
    elif output_type == "both":
        both_left_and_right(left, right)
    else:
        left_res = left_only(left, right)
        right_res = right_only(left, right)
        both_res = both_left_and_right(left, right)
        print """Summary:
        {}: Only in {}
        {}: Only in {}
        {}: Both in [{}] and [{}]""".format(len(left_res), left["name"],
                                            len(right_res), right["name"],
                                            len(both_res), left["name"], right["name"])


def main():
    args = _parse_args()

    # 初始化操作单元
    left = {}
    left["ip_set"] = set()
    left["name"] = args.left_file

    right = {}
    right["ip_set"] = set()
    right["name"] = args.right_file

    left["ip_set"] = get_set_lines(left["name"])
    right["ip_set"] = get_set_lines(right["name"])

    get_output(args.output, left, right)
    
if __name__ == '__main__':
    main()
