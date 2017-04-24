class frameEntry:
  'A frame entry that references a page table'

  def __init__(self, pageTable, tableEntry, lastUsed):
    self.pageTable = pageTable
    self.tableEntry = tableEntry
    self.referenceBit = True
    self.lastUsed = lastUsed
