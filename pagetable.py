class PageTable:
  'A page table for keeping track of a programs pages in frames'

  def __init__(self, lastUsed):
    self.lastUsed = lastUsed
    self.inFrame = True
    self.referenceBit = True

  def checkInFrame(self, time):
    self.lastUsed = time
    self.referenceBit = False
    return inFrame

  def __cmp__(self, other):
    if self.referenceBit
      if !other.referenceBit
        return -1
    else if other.referenceBit
      if !self.referenceBit
        return 1
      
    return cmp(self.lastUsed, other.
