#!/usr/bin/env python
"""
A parser for the 2008 earmarks data (XLS format) from http://taxpayer.net/

This script depends on xls2list which will convert the excel file to a 2d array. 
It then does some trivial parsing of each field and outputs the data in a few ways.
"""
__author__ = ['Alex Gourley <acgourley@gmail.com>',
              'Aaron Swartz <me@aaronsw.com>']

EARMARK_FILE = '../data/crawl/taxpayer/bigkahuna.xls'

import sys, re
import web
import xls2list

fmt = (
  'id',
  'house_request', 'senate_request', 
  'prereduction_amt', 'final_amt', 'budget_request',
  'description', 'city', 'county', 'state',
  'bill', 'bill_section', 'bill_subsection', 'project_heading',
  'house_member', 'house_party', 'house_state', 'district',
  'senate_member', 'senate_party', 'senate_state',
  'presidential', 'undisclosed', 'intended_recipient',
  'notes'
)

def parse_row(row):
    out = web.storage()
    for n, item in enumerate(fmt):
        out[item] = row[n]
    out.house_member = (out.house_member or []) and [x.strip() for x in out.house_member.split(';')]
    out.senate_member = (out.senate_member or []) and [x.strip() for x in out.senate_member.split(';')]
    #out.state = (out.state or []) and [x.strip() for x in out.state.split(';')]
    return out

def parse_file(fn):
    """Break down the xls into a 2d data array, stripping off first rows which do not have data."""
    data = xls2list.xls2list(fn)
    for n, row in enumerate(data[3:]):
        r = parse_row(row)
        # All of the earmarks have a description, stop when we finish all
        # earmarks
        if not r.description: break 
        # The id's aren't remotely uniq, map to something that is
        r.id=n+1 # Lets start at 1 instead of 0
        yield r

if __name__ == "__main__":
    import tools
    tools.export(parse_file(EARMARK_FILE))
