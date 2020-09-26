from Connection import Connection
import os
import shutil
import difflib
import sys
import functools
import glob
from prettytable import PrettyTable

class Extract:
  def compare(self):
    if os.path.exists("files"):
      shutil.rmtree("files")

    os.makedirs("files")

    connection = Connection()
    cursorPreview = connection.getPreviewCursor()

    cursorPreview.execute("show full tables where Table_Type = 'BASE TABLE'")

    results = cursorPreview.fetchall()
    previewTables = []

    for row in results:
      previewTables.append(row[0])

      cursorPreview.execute("describe "+row[0])
      headers = []
      
      for col in cursorPreview.fetchall():
        headers.append(col[0])
      
      prettytable = PrettyTable(headers)
      cursorPreview.execute("select * from "+row[0])
      
      for rowData in cursorPreview.fetchall():
        prettytable.add_row(rowData)

      with open('files/preview_'+row[0]+'.txt', 'w') as f:
        f.write(str(prettytable))
      f.close()

    cursorCurrent = connection.getCurrentCursor()
    cursorCurrent.execute("show full tables where Table_Type = 'BASE TABLE'")

    results = cursorCurrent.fetchall()
    currentTables = []

    for row in results:
      currentTables.append(row[0])

      cursorCurrent.execute("describe "+row[0])
      headers = []
      
      for col in cursorCurrent.fetchall():
        headers.append(col[0])
      
      prettytable = PrettyTable(headers)
      cursorCurrent.execute("select * from "+row[0])
      
      for rowData in cursorCurrent.fetchall():
        prettytable.add_row(rowData)

      with open('files/current_'+row[0]+'.txt', 'w') as f:
        f.write(str(prettytable))
      f.close()
    
    tables = previewTables + currentTables
    tables = list(set(tables))
    tables.sort()

    for table in tables:
      with open('files/preview_'+table+'.txt', 'r') as preview:
        with open('files/current_'+table+'.txt', 'r') as current:
          diff = difflib.unified_diff(
            preview.readlines(),
            current.readlines(),
            fromfile='preview_'+table,
            tofile='current_'+table,
          )
          lines = 0
          with open('files/diff_'+table+'.txt', 'w') as f:
            for line in diff:
              lines += 1
              f.write(line)
            f.close()
          if lines == 0:
            os.remove('files/diff_'+table+'.txt')
    connection.closeAll()

    fileList = glob.glob('files/preview_*.txt')
    fileList += glob.glob('files/current_*.txt')
    for filePath in fileList:
      os.remove(filePath)


if __name__ == "__main__":
    extract =  Extract()
    extract.compare()