from tableRenderer import ColumnInfo as ColumnInfo

def prepare_data_for_rendering(json):
    header = get_headers(json)
    body = get_body(header, json)
    data = [header] + body
    column_map = init_column_map(header)
    return data, column_map

def get_headers(json):
    keys = list()
    if len(json[0]['results']) == 0:
        return []
    keys.extend(json[0]['results'][0].keys())
    keys.remove("v_id")
    id_list = ['ID']
    name_list = []
    if 'Name' in keys:
        keys.remove('Name')
        name_list = ['Name']
    return id_list + name_list + keys

def get_body(header, json):
    result = []
    for row in json[0]['results']:
      res_row = []
      res_row.append(row['v_id'])
      for h in header[1:]:
          res_row.append(row[h])
      result.append(res_row)
    return result

def get_matches_map(json):
    result = {}
    for item in json[0]['@@matches']:
        if item['idNeeded'] not in result:
            result[item['idNeeded']] = []
        print("item['idNeeded']", item['idNeeded'])
        result[item['idNeeded']].append(item['idAvailable'])
    return result

def init_column_map(header):
  result = {}
  for h in header:
      result[h] = ColumnInfo()
  return result

