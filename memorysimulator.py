#!/usr/bin/python
# memsim proglist comlist 2 lru d

import logging, sys, getopt, os

def usage():
  print 'Usage:'
  print os.path.basename(__file__) + ' programlist commandlist <page size> <algorithm> <d|p>'
  sys.exit(-1)


def main(argv):
  logmsg = 'Start of ' + os.path.basename(__file__) + '.'
  logging.info(logmsg)
  logmsg = 'Number of args is {0}.'.format(len(sys.argv))
  logging.debug(logmsg)
  logmsg = sys.argv[0:]
  logging.debug(logmsg)

  if len(sys.argv) != 6:
    usage()

  try:
    proglist = open(argv[0], "r")
  except IOError:
    logging.error('Could not open file ' + argv[0] + '.')
    usage()

  try:
    comlist = open(argv[1], "r")
  except IOError:
    logging.error('Could not open file ' + argv[1] + '.')
    usage()

  try:
    pagesize = int(argv[2])
    if pagesize < 0 or pagesize > 16:
      raise ValueError('Incorrect page size given')
    if pagesize != 1 and pagesize % 2 != 0:
      raise ValueError('Incorrect page size given')
  except ValueError:
    logging.error('<page size> must be one of 1, 2, 4, 8, or 16.')
    usage()

  if argv[3] != 'lru' and argv[3] != 'fifo' and argv[3] != '2lru':
    logging.error('<algorithm> must be one of lru, fifo, or 2lru')
    usage()

  if argv[4] != 'd' and argv[4] != 'p':
    logging.error('The final arguement must be "d" for demand paging or "p" for prepaging')
    usage()

if __name__ == "__main__":
  # Initialize logging facility for debugging
  logging.basicConfig(level=logging.DEBUG)
  main(sys.argv[1:])
