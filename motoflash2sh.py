import argparse
import sys
from os import path
from textwrap import indent
from xml.etree import ElementTree
from collections import OrderedDict as odict

def commentify(x, prefix='# '):
    return indent(ElementTree.tostring(x).strip().decode(), prefix)

p = argparse.ArgumentParser()
p.add_argument('FLASHFILE_XML')
p.add_argument('-o', '--output', metavar='FLASHFILE_SH', type=argparse.FileType('w'),
               help='Script to output (default is flashfile.sh in same directory)')
p.add_argument('-n', '--no-verify', dest='verify', default=True, action='store_false',
               help="Don't verify MD5/SHA1 sums")
p.add_argument('-v', '--verbose', action='store_true')
args = p.parse_args()

if args.output is None:
    args.output = open(path.join(path.dirname(args.FLASHFILE_XML), 'flashfile.sh'), 'w')

########################################

x = ElementTree.parse(args.FLASHFILE_XML)
assert x.getroot().tag == 'flashing'

args.output.write('#!/bin/sh -x\n\n')

header = x.find('header')
if header:
    args.output.write(commentify(header) + '\n\n')
else:
    args.output.write('# WARNING: no <header> tag found\n\n')

steps = x.find('steps')
if not steps:
    args.output.write('# WARNING: no <steps> found\n')
    sys.exit()

if args.verify:
    md5sums = odict()
    sha1sums = odict()
    for step in steps.iter('step'):
        if 'MD5' in step.keys() and 'filename' in step.keys():
            md5sums[step.get('filename')] = step.get('MD5')
        elif 'SHA1' in step.keys() and 'filename' in step.keys():
            sha1sums[step.get('filename')] = step.get('SHA1')

    if md5sums:
        args.output.write('md5sum --check <<EOF || exit 1\n' + ''.join('{1} *{0}\n'.format(*p) for p in md5sums.items()) + 'EOF\n\n')
    if sha1sums:
        args.output.write('sha1sum --check <<EOF || exit 1\n' + ''.join('{1} *{0}\n'.format(*p) for p in sha1sums.items()) + 'EOF\n\n')

for nn, step in enumerate(steps.iter('step')):
    op = step.get('operation')
    if op=='flash':
        vars = 'partition', 'filename',
    elif op=='erase':
        vars = 'partition',
    elif op in ('getvar','oem'):
        vars = 'operation',
    else:
        args.output.write('\n# %02d: unknown operation %r:\n%s\n\n' % (nn, op, commentify(step)))
        op = None

    if op:
        if args.verbose:
            args.output.write(commentify(step, '# %02d: ' % nn) + '\n')
        args.output.write('fastboot %s || exit 1\n' % ' '.join(step.get(v) for v in vars))
