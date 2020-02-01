#!/usr/bin/python3

import argparse
import os
import random
import sys


def fail(msg):
  sys.stderr.write('E: {}\n'.format(msg))
  sys.exit(1)


def ensureFile(f):
  if not os.path.exists(f):
    fail('does not exist: {}'.format(f))
  if not os.path.isfile(f):
    fail('not a file: {}'.format(f))


# Parse command-line arguments
parser = argparse.ArgumentParser( description=( 'Split text into multiple '
                                              + 'pages to be printed on  '
                                              + 'overhead sheets'
                                              )
                                )
parser.add_argument( '-i'
                   , '--input'
                   , metavar='FILE'
                   , required=True
                   , help='File with the text and name data'
                   )
parser.add_argument( '-l'
                   , '--latex'
                   , metavar='FILE'
                   , required=True
                   , help='File with the LaTeX code'
                   )
parser.add_argument( '-o'
                   , '--output'
                   , metavar='FILE'
                   , required=True
                   , help='File to output the result'
                   )
args = parser.parse_args();

# Sanity check
ensureFile(args.input)
ensureFile(args.latex)

# Initialize randomizer
random.seed()

# Read text and name data
texts = []
with open(args.input, 'r') as f:
  names = []
  text_lines = []
  first_text = True
  follows_empty = False
  for l in f.readlines():
    l = l.strip()
    if l.startswith('#'):
      # This line is a comment
      continue
    elif l.startswith('=='):
      # Line contains names; indicates start of a text
      if not first_text:
        if len(names) == 0:
          fail('invalid input format: no names given')
        if len(text_lines) == 0:
          fail('invalid input format: no text given')
        texts.append((names, text_lines))
      first_text = False
      text_lines = []
      names = [ n.strip()
                for n in l[2:].split(',')
                if len(n.strip()) > 0
              ]
      if len(names) == 0:
        fail('invalid input format: no names given')
    else:
      if len(l) == 0:
        if follows_empty: continue
        follows_empty = True
      else:
        if len(names) == 0:
          fail('invalid input format: text before names')
        follows_empty = False
      text_lines.append(l)
  if len(names) == 0:
    fail('invalid input format: no names given')
  if len(text_lines) == 0:
    fail('invalid input format: no text given')
  texts.append((names, text_lines))

# Split each line into words and randomly assign a name index
old_texts = texts
texts = []
for (names, lines) in old_texts:
  lines = [ [ (w, random.randint(0, len(names)-1))
              for w in l.split(' ')
            ] if len(l) > 0 else []
            for l in lines
          ]
  texts.append((names, lines))

# Generate latex page content
pages = []
for (names, text_data) in texts:
  for i in range(0, len(names)):
    lines = [ ' '.join([ w if i == n else '\\phantom{{{}}}'.format(w)
                         for (w, n) in l
                       ])
              if len(l) > 0 else '\\vspace{\\baselineskip}'
              for l in text_data
            ]
    p = ( '\chead[{0}]{{{0}}}\n'.format(names[i])
        + '\\par\n'.join(lines)
        )
    pages.append(p)
content = '\n\n\\newpage'.join(pages)

# Read latex
with open(args.latex, 'r') as f:
  latex = f.read()
latex = latex.replace('%-[INSERT HERE]-%', content)

# Write output
with open(args.output, 'w') as f:
  f.write(latex)
