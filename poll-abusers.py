#!/usr/bin/python


# Parses output from
# 'varnishtop -i TxHeader -C -I \^X-Forwarded-For
# Adds offenders to specified file


import os, re, sys
from datetime import date, datetime, timedelta
from optparse import make_option

import subprocess

# BURST_CONNECTIONS_ALLOWED = 99   # allowed stat
# BURST_CONNECTOINS_TIME    = 120  # in seconds
# ABUSER_TIME_OUT           = 1800 # in seconds
# ABUSER_PERM_BAN           = 5    # bursts allowed before perm ban

def get_as_dict(to_run='varnishtop', options='-i TxHeader -C -I \^X-Forwarded-For', value1=0, value2=-1):
    try :
        p = subprocess.Popen(['cat','output-varnishtop-xff'],
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                stdin=subprocess.PIPE)
        # p = subprocess.Popen(['varnishtop','-i TxHeader -C -I \^X-Forwarded-For'],
        #                                         stdout=subprocess.PIPE,
        #                                         stderr=subprocess.PIPE,
        #                                         stdin=subprocess.PIPE)
        # p = subprocess.Popen([to_run,options],
        #                                         stdout=subprocess.PIPE,
        #                                         stderr=subprocess.PIPE,
        #                                         stdin=subprocess.PIPE)

        command_output, err = p.communicate()
        toplines = [[x.split('\n')[0].split()[value1], x.split('\n')[0].split()[value2]]
                for x in command_output.splitlines() if x ]
        return toplines

    except Exception as e:
        import traceback, os.path
        print e

def exceeds_thresholds(input, field, threshold):
    offender = []
    for k,v in input:
        if float(k) >= threshold:
            offender.append(v)
    return offender

def add_offenders(filename="temp", offender=[]):
    with open(filename, "a") as dirty_script_hippies:
        for each in offender:
            dirty_script_hippies.write(each + '\n')

if __name__ == '__main__':
    # print get_as_dict()
    # print exceeds_thresholds(get_as_dict(), 0, 15)
    add_offenders("temp", exceeds_thresholds(get_as_dict(), 0, 15))
