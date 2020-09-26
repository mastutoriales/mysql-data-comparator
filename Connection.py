import json
import mysql.connector

class Connection:
  def __init__(self):
    file = open('connections.json','r')     
    connections = json.load(file)
    self.preview = connections['databases'][0]
    self.current = connections['databases'][1]
    file.close()

  def getPreview(self):
    """
    Return the preview database connection
    """
    return self.current

  def getCurrent(self):
    """
    Return the current database connection
    """
    return self.current

  def getPreviewCursor(self):
    self.previewDB = mysql.connector.connect(host=self.preview['host'],user=self.preview['user'],passwd=self.preview['password'],db=self.preview['database'])
    return self.previewDB.cursor()
  
  def getCurrentCursor(self):
    self.currentDB = mysql.connector.connect(host=self.current['host'],user=self.current['user'],passwd=self.current['password'],db=self.current['database'])
    return self.currentDB.cursor()

  def closeAll(self):
    self.previewDB.close()
    self.currentDB.close()

