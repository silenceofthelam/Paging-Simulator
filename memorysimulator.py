#!/usr/bin/python
# memsim proglist comlist 2 lru d

import logging, sys, getopt, os, frameEntry

framelist = []
pages = []
globalCounter = 0
queuePointer = 0
totalFrames = 0

def usage():
  print 'Usage:'
  print os.path.basename(__file__) + ' programlist commandlist <page size> <algorithm> <d|p>'
  sys.exit(-1)

def lru(page, entry):
  global framelist
  global pages
  global globalCounter
  global queuePointer

  lastUsed = framelist[0].lastUsed
  leastUsed = 0
  for i, frame in enumerate(framelist):
    if frame.lastUsed < lastUsed:
      lastUsed = frame.lastUsed
      leastUsed = i

  frame = framelist[leastUsed]
  pages[frame.pageTable][frame.tableEntry] = -1
  framelist[leastUsed].pageTable = page
  framelist[leastUsed].tableEntry = entry
  pages[page][entry] = leastUsed

    

def fifo(page, entry):
  global framelist
  global pages
  global queuePointer
  global totalFrames
  frame = framelist[queuePointer]
  pages[frame.pageTable][frame.tableEntry] = -1
  framelist[queuePointer].pageTable = page
  framelist[queuePointer].tableEntry = entry
  pages[page][entry] = queuePointer
  if queuePointer == (totalFrames - 1):
    queuePointer = 0
  else:
    queuePointer += 1

def sclru(page, entry):
  global framelist
  global pages
  global queuePointer
  global totalFrames
  while True:
    if framelist[queuePointer].referenceBit:
      framelist[queuePointer].referenceBit = False
    else:
      frame = framelist[queuePointer]
      pages[frame.pageTable][frame.tableEntry] = -1
      framelist[queuePointer].pageTable = page
      framelist[queuePointer].tableEntry = entry
      pages[page][entry] = queuePointer
      if queuePointer == (totalFrames - 1):
        queuePointer = 0
      else:
        queuePointer += 1
      break

    if queuePointer == (totalFrames - 1):
      queuePointer = 0
    else:
      queuePointer += 1

def main(argv):

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

  global totalFrames
  totalFrames = 512 / pagesize
  if argv[3] == 'lru':
    swapalgo = lru
  elif argv[3] == 'fifo':
    swapalgo = fifo
  elif argv[3] == 'sclru':
    swapalgo = sclru
  else:
    logging.error('<algorithm> must be one of lru, fifo, or 2lru')
    usage()

  if argv[4] != 'd' and argv[4] != 'p':
    logging.error('The final arguement must be "d" for demand paging or "p" for prepaging')
    usage()

  pagingstyle = argv[4]

  global framelist
  global pages

  for line in proglist:
    try:
      memspace = line.split(' ')[1]
    except IndexError:
      logging.debug("End of file")
      continue
    pages.append([-1 for x in range(int(memspace) / pagesize + 1)])

  global globalCounter
  global queuePointer
  frameListFull = False
  totalSwaps = 0

  for line in comlist:
    entry = line.split(' ')
    pagetable = int(entry[0])
    pageentry = int(entry[1]) / pagesize
    globalCounter += 1

    if pages[pagetable][pageentry] == -1:
      totalSwaps += 1
      if frameListFull:
        swapalgo(pagetable, pageentry)
      else:
        pages[pagetable][pageentry] = queuePointer
        framelist.append(frameEntry.frameEntry(pagetable, pageentry, globalCounter))
        queuePointer += 1
        if queuePointer == totalFrames:
          queuePointer = 0
          frameListFull = True

    framelist[pages[pagetable][pageentry]].referenceBit = True
    framelist[pages[pagetable][pageentry]].lastUsed = globalCounter

    if pagingstyle == 'p':
      if pageentry == len(pages[pagetable]) - 1:
        frameIndex = pages[pagetable][pageentry]
        if frameIndex == totalFrames - 1:
          frameIndex = 0
        framelist[frameIndex].lastUsed = 0
        framelist[frameIndex].referenceBit = False
        queuePointer += 1
        if queuePointer == totalFrames:
          queuePointer = 0
        continue
      pageentry += 1
      if pages[pagetable][pageentry] == -1:
        if frameListFull:
          swapalgo(pagetable, pageentry)
        else:
          pages[pagetable][pageentry] = queuePointer
          framelist.append(frameEntry.frameEntry(pagetable, pageentry, globalCounter))
          queuePointer += 1
          if queuePointer == totalFrames:
            queuePointer = 0
            frameListFull = True

      framelist[pages[pagetable][pageentry]].referenceBit = True
      framelist[pages[pagetable][pageentry]].lastUsed = globalCounter
      

      

  print 'Total Swaps: '
  print totalSwaps
      

if __name__ == "__main__":
  # Initialize logging facility for debugging
  logging.basicConfig(level=logging.DEBUG)
  main(sys.argv[1:])
