#!/usr/bin/env python3
import argparse
import sys
from os import path
from textwrap import indent
from xml.etree import ElementTree

def commentify(x, prefix='# '):
    if isinstance(x, (ElementTree.ElementTree, ElementTree.Element)):
        x = ElementTree.tostring(x).strip().decode()
    return indent(x, prefix)

def parse_args(args=None):
    p = argparse.ArgumentParser(description="Converts Motorola's flashfile.xml format to a [ba]sh script of fastboot commands")
    p.add_argument('FLASHFILE_XML')
    p.add_argument('-o', '--output', metavar='FLASHFILE_SH', type=argparse.FileType('w'),
                   help='Script to output (default is flashfile.sh in same directory)')
    p.add_argument('-n', '--no-verify', dest='verify', default=True, action='store_false',
                   help="Don't verify MD5/SHA1 sums")
    p.add_argument('-v', '--verbose', action='store_true',
                   help="Include step-by-step comments in output script")
    args = p.parse_args()

    if args.output is None:
        args.output = open(path.join(path.dirname(args.FLASHFILE_XML), 'flashfile.sh'), 'w')
    return p, args

def main():
    p, args = parse_args()

    try:
        x = ElementTree.parse(args.FLASHFILE_XML)
    except ElementTree.ParseError as e:
        p.error('XML parse error: %s' % e.args)
    if x.getroot().tag != 'flashing':
        p.error('Input does not appear to be a Motorola flashfile.xml (root node is not <flashing>)')

    args.output.write('#!/bin/sh -x\n\n')
    if args.FLASHFILE_XML != sys.stdin:
        args.output.write('cd "%s"\n\n' % path.dirname(args.FLASHFILE_XML))

    header = x.find('header')
    if header:
        args.output.write(commentify(header) + '\n\n')
    else:
        args.output.write('# WARNING: no <header> tag found\n\n')

    steps = x.find('steps')
    if not steps:
        args.output.write('# WARNING: no <steps> found\n')
        steps = ()

    md5sums = {}
    sha1sums = {}
    for step in steps:
        assert step.tag == 'step'
        if 'MD5' in step.keys() and 'filename' in step.keys():
            md5sums[step.get('filename')] = step.get('MD5')
        elif 'SHA1' in step.keys() and 'filename' in step.keys():
            sha1sums[step.get('filename')] = step.get('SHA1')

    for checker, checksums in (('md5sum', md5sums), ('sha1sum', sha1sums)):
        if checksums:
            checksums = checker + ' --check <<EOF || exit 1\n' + ''.join('{1} *{0}\n'.format(*p) for p in checksums.items()) + 'EOF'
            args.output.write((checksums if args.verify else commentify(checksums)) + '\n\n')

    for nn, step in enumerate(steps):
        assert step.tag == 'step'
        op = step.get('operation')
        if op=='flash':
            vars = 'operation', 'partition', 'filename',
        elif op=='erase':
            vars = 'operation', 'partition',
        elif op in ('getvar','oem'):
            vars = 'operation', 'var'
        else:
            args.output.write('\n# %02d: skipping unknown operation %r:\n%s\n\n' % (nn, op, commentify(step)))
            op = None

        if op:
            if args.verbose:
                args.output.write(commentify(step, '# %02d: ' % nn) + '\n')
            args.output.write('fastboot %s || exit 1\n' % ' '.join(step.get(v) for v in vars))

    print("Wrote shell script with %d fastboot steps to %s" % (len(steps), args.output.name),
          file=sys.stderr)

if __name__=='__main__':
    sys.exit( main() )
