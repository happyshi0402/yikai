#! /usr/bin/env python
# coding: utf-8
import sys

"""
------------------------配置文件修改------------------
"""
file_path = sys.argv[1]
old_con = sys.argv[2]
new_con = sys.argv[3]
print "reset_path parameter is:", file_path, old_con, new_con
with open(file_path, "r") as f:
    file_con = f.readlines()
    with open(file_path, "w") as f2:
        for line in file_con:
            f2.write(str(line).replace(old_con, new_con))
