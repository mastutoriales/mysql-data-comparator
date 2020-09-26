from Connection import Connection
import os
import shutil
import difflib
import sys
import functools
import glob

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
      cursorPreview.execute("select * from "+row[0])

      with open('files/preview_'+row[0]+'.txt', 'w') as f:
        for row in cursorPreview.fetchall():
          f.write("%s\n" % str(row))
        f.close()

    cursorCurrent = connection.getCurrentCursor()
    cursorCurrent.execute("show full tables where Table_Type = 'BASE TABLE'")

    results = cursorCurrent.fetchall()
    currentTables = []

    for row in results:
      currentTables.append(row[0])
      cursorCurrent.execute("select * from "+row[0])

      with open('files/current_'+row[0]+'.txt', 'w') as f:
        for row in cursorCurrent.fetchall():
          f.write("%s\n" % str(row))
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