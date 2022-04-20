from DataUtil import *
import pandas as pd
import re

class AbstractApp:
    def getQueryName(self):
        return "app" + self.__class__.__name__

    def getVertexType(self):
        return "Accommodation"

    def getTitle(self):
        classname = self.__class__.__name__
        return ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', classname))

    def getData(self, tiger):
        json = tiger.runInstalledQuery(self.getQueryName())
        data, column_map = prepare_data_for_rendering(json)
        return data, column_map

    def setColumnInfo(self, column_map):
        return column_map

    def export(self, tiger):
        data, column_map = self.getData(tiger)
        dataFrame = pd.DataFrame(data=data[1:], columns=data[0])
        return dataFrame

    def view(self, tiger, tableRenderer):
        data, column_map = self.getData(tiger)
        column_map = self.setColumnInfo(column_map)
        print("vertex_type: " + self.getVertexType())
        table = tableRenderer.render_table(data, column_map, self.getVertexType())
        return table
