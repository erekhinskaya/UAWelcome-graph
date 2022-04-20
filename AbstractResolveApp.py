from AbstractMatchApp import AbstractMatchApp
from DataUtil import *

class AbstractResolveApp(AbstractMatchApp):
    def getQueryName(self):
        return self.__class__.__name__.replace("Resolve", "resolve")

    def getVertextType(self):
        return self.__class__.__name__.replace("Resolve", "")

    def setColumnInfoOption(self, column_map):
        for (h,v) in column_map.items():
            if h == "v_id" or h == "ID": continue
            v.editable = True
        print(column_map)
        return column_map

    def getData(self, tiger, ids):
        str_ids = ['ids='+str(id) for id in ids]
        param_ids = '&'.join(str_ids)
        json = tiger.runInstalledQuery(self.getQueryName().replace('resolve', 'print'), param_ids)
        print('json', json)
        data, column_map = prepare_data_for_rendering(json)
        return data, column_map

    def setColumnInfoNeed(self, column_map):
        print(column_map)
        for (h, v) in column_map.items():
            if h == "v_id" or h == "ID": continue
            print(h)
            print(v)
            v.editable = True
        print (column_map)
        return column_map

    def expandOptionTable(self, dataOptions, column_map_options):
        return dataOptions, column_map_options