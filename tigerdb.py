import json
import pyTigerGraph as tg
import time

class TigerDB:
  def __init__(self, props):
    self.conn = tg.TigerGraphConnection(\
      host=props["host"].data, username = props["username"].data, password = props["password"].data, \
      graphname=props["graphname"].data, apiToken=props["apiToken"].data)
      #host='https://uawelcome.i.tgcloud.io', username='tigergraph', password='tigergraph',
    # graphname='uawelcome', apiToken='7ae4nkln7fk6u6ha4d2hqsfnv2idlct1') #fixme

  def addPerson(self, id, attributes):
    self.conn.upsertVertex("Person", id, attributes)

  def addService(self, service_type, service_id, attributes, person_id, edgeType):
    self.conn.upsertVertex(service_type, service_id, attributes)
    self.conn.upsertEdge("Person", person_id, edgeType, service_type, service_id, attributes={})

  def addLocation(self, location_id, service_type, service_id, attributes, edgeType):
    self.conn.upsertVertex(service_type, service_id, attributes)

  def match(self, need_id, available_id):
    self.conn.runInstalledQuery("finalizeMatch",\
                                params={'need_id': need_id, 'available_id': available_id, 'becameUnavailable': True})
    #fixme

  def deleteVertex(self, id):
    res = self.conn.runInstalledQuery("removeVertexById",\
                                      params={'id': int(id)})
    print(res)
    return res[0]['@@counter'] > 0

  def runQuery(self, query):
    self.conn.gsql("USE GRAPH uawelcome", options=None)
    return self.conn.gsql(query, options=None)

  def getMaxId(self):
    res = self.conn.runInstalledQuery("maxId")
    if len(res) == 0 or '@@maxId' not in res[0]: return -1
    return res[0]['@@maxId']

  def alreadyExists(self, ids):
    str_ids = ['ids=' + str(id) for id in ids]
    param_ids = '&'.join(str_ids)
    res = self.conn.runInstalledQuery("alreadyExists", param_ids)
    return len(res[0]['results']) > 0

  def getMaxPersonId(self):
    res = self.conn.runInstalledQuery("maxPersonId")
    if len(res) == 0 or '@@maxId' not in res[0]: return -1
    return res[0]['@@maxId']

  def runInstalledQuery(self, name, params=None, timeout=None, sizeLimit=None):
    return self.conn.runInstalledQuery(name, params, timeout, sizeLimit)

  def update(self, id, field, value, type="Person"):
    id = int(id)
    if id < 1000000:
      type = "Person" #TODO
      self.conn.upsertVertex(type, id, {field: value})
    else:
      if value == 'True' or value == 'False':
        value = bool(value)
        print(value)
      self.conn.upsertVertex(type, id, {field: value}) #FIXME

  def cleanUpDB(self):
    types = self.conn.getVertexTypes()
    for type in types :
      self.conn.delVertices(type)
  