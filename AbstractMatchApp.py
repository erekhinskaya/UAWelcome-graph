from DataUtil import *
import pandas as pd
import re

class AbstractMatchApp:
    def getQueryName(self):
        return self.__class__.__name__.replace("Match", "match")

    def getVertextType(self):
        return self.__class__.__name__.replace("Match", "")

    def getTitle(self):
        classname = self.__class__.__name__
        return ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', classname))

    def getData(self, tiger, ids):
        str_ids = ['ids='+str(id) for id in ids]
        param_ids = '&'.join(str_ids)
        json = tiger.runInstalledQuery(self.getQueryName().replace('match', 'print'), param_ids)
        print('json', json)
        data, column_map = prepare_data_for_rendering(json)
        return data, column_map

    def setColumnInfoNeed(self, column_map):
        return column_map

    def getTables(self, tiger, tableRenderer):
        json = tiger.runInstalledQuery(self.getQueryName())
        match_map = get_matches_map(json)
        print('match_map', match_map)
        if len(match_map) == 0:
            return "", "<br>"
        for (k, v) in match_map.items():
          dataNeeded, column_map_needed = self.getData(tiger, [k])
          column_map_needed = self.setColumnInfoNeed(column_map_needed)
          tableNeeded = tableRenderer.render_table(dataNeeded, column_map_needed, self.getVertextType())
          dataOptions, column_map_options = self.getData(tiger, v)
          dataOptions, column_map_options = self.expandOptionTable(dataOptions, column_map_options)
          column_map_options = self.setColumnInfoOption(column_map_options)
          tableOptions = tableRenderer.render_table(dataOptions, column_map_options, self.getVertextType(), k)

          return tableNeeded, tableOptions

    def setColumnInfoOption(self, column_map):
        if len(column_map) > 0:
          column_map["Select"].selector = True
        return column_map

    def expandOptionTable(self, dataOptions, column_map_options):
        dataOptions[0].append("Select")
        for r in range(1, len(dataOptions)):
            dataOptions[r].append("")
        column_map_options["Select"] = ColumnInfo()
        column_map_options["Select"].selector = True
        column_map_options["Select"].editable = True
        return dataOptions, column_map_options