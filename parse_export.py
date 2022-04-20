import pandas
from csv import DictReader
import tigerdb
import phonenumbers

FORM_NAME_INDEX = 2

def is_empty_cell(row, key):
  return key not in row or row[key] == None or len(row[key].strip()) == 0

def parse_int(row, key):
  if key not in row.keys():
    return -1
  value = row[key].strip()
  if len(value) == 0:
    return -1
  return int(float(value))

def parse_phone(row, key):
  val = row[key]
  if 'E+' in val:
    fl = float(val)
    fl = format(fl, '.0f')
    val = str(fl)
  try:
    val = phonenumbers.parse(val, None)
    return str(val.country_code) + str(val.national_number)
  except:
    return val

class Parser:
  def __init__(self, tigerDB):
    self.tiger = tigerDB
    self.service_counter = max(1000000, self.tiger.getMaxId())
    
  def get_person(self, form_row):
    #"your-name", "your-email", "phone", "gender", "location"
    print(form_row)
    person_id = int(float(form_row['\ufeffid']))
    if self.tiger.alreadyExists([person_id]):
      print('repeating id: ', person_id, self.tiger.getMaxPersonId)
      return -1
    attributes = {"Name": form_row["your-name"], "Phone": parse_phone(form_row,"phone"), "Email": form_row["your-email"]}
    self.tiger.addPerson(person_id, attributes)
    return person_id

  def get_canhelp_ticket(self, form_row, person_id):
    #"tickethelp"
    if form_row["tickethelp"] is None or len(form_row["tickethelp"]) == 0:
      return
    service_id = self.service_counter
    self.service_counter = self.service_counter + 1
    attributes = {}
    self.tiger.addService("TicketDonation", service_id, attributes, person_id, "CAN_PROVIDE")
    pass

  def getChildren(self, form_row):
    #"haskid-baby", "haskid-toddler", "haskid-preschool", "haskid-elementary", "haskid-middle", "haskid-highschool",
    kids = []
    if not is_empty_cell(form_row, 'haskid-baby'):
      kids.append("Baby")
    if not is_empty_cell(form_row, 'haskid-toddler'):
      kids.append("Toddler")
    if not is_empty_cell(form_row, 'haskid-preschool'):
      kids.append("Preschool")
    if not is_empty_cell(form_row, 'haskid-elementary'):
      kids.append("Elementary")
    if not is_empty_cell(form_row, 'haskid-middle'):
      kids.append("Middle")
    if not is_empty_cell(form_row, 'haskid-highschool'):
      kids.append("Highschool")
    return ' '.join(kids)

  def get_hosthelp_ticket(self, form_row, person_id):
    #"hosthelp", "room-pictures",  "your-message", "host-limit"
    if form_row["hosthelp"] is None or len(form_row["hosthelp"]) == 0:
      return
    service_id = self.service_counter
    self.service_counter = self.service_counter + 1
    attributes = {"RoomPhotos": form_row["room-pictures"],
                  "HasKids": self.getChildren(form_row),
                  "Message": form_row["your-message"],
                  "HostLimit": parse_int(form_row, "host-limit")}
    self.tiger.addService("Accommodation", service_id, attributes, person_id, "CAN_PROVIDE")
    pass

  def get_child_help(self, form_row, person_id):
    "childhelp"
    if form_row["childhelp"] is None or len(form_row["childhelp"]) == 0:
      return
    service_id = self.service_counter
    self.service_counter = self.service_counter + 1
    attributes = {}
    self.tiger.addService("School", service_id, attributes, person_id, "CAN_PROVIDE")
    pass

  def get_foodhelp_ticket(self, form_row, person_id):
    #"foodhelp"
    pass

  def get_jobhelp_ticket(self, form_row, person_id):
    #"jobhelp", "location"
    pass

  def get_englishhelp(self, form_row, person_id):
    #"englishhelp"
    if form_row["englishhelp"] is None or len(form_row["englishhelp"]) == 0:
      return
    service_id = self.service_counter
    self.service_counter = self.service_counter + 1
    attributes = {}
    self.tiger.addService("Paperwork", service_id, attributes, person_id, "CAN_PROVIDE")
    pass

  def get_volunteerhelp_ticket(self, form_row, person_id):
    #"volunteerhelp"
    pass

  def parse_angel(self, form_row):
    person_id = self.get_person(form_row)
    if person_id == -1:
      return
    self.get_canhelp_ticket(form_row, person_id)
    self.get_hosthelp_ticket(form_row, person_id)
    self.get_englishhelp(form_row, person_id)
    self.get_child_help(form_row, person_id)

  def parse_need_accommodation(self, form_row, person_id):
    print("my: ", form_row )
    if form_row["need-host"] is None or len(form_row["need-host"]) == 0:
      return
    print('nned_host')
    service_id = self.service_counter
    self.service_counter = self.service_counter + 1
    attributes = {"HasKids": self.getChildren(form_row),
                  "WhoLives":  form_row["who"],
                  "Message": form_row["your-message"],
                  "HostLimit": parse_int(form_row, "people-count")}
    self.tiger.addService("Accommodation", service_id, attributes, person_id, "NEEDS")

  def parse_refugee(self, form_row):
    person_id = self.get_person(form_row)
    if person_id == -1: return
    print('parse_refugee: ', person_id)
    self.parse_need_accommodation(form_row, person_id)
    kids = self.getChildren(form_row).split(' ')
    if len(kids) > 0:
      service_id = self.service_counter
      self.service_counter = self.service_counter + 1
      self.tiger.addService("School", service_id, {}, person_id, "NEEDS")
    service_id = self.service_counter
    self.service_counter = self.service_counter + 1
    self.tiger.addService("Paperwork", service_id, {}, person_id, "NEEDS")

  def parse_volunteer(self, form_row):
    person_id = self.get_person(form_row)
    if person_id == -1: return
    print('volunteer: ', person_id)
    attributes = {}
    if form_row['volunteer-host'] is not None and len(form_row['volunteer-host']) > 0:
      attributes["HostVerification"] = True
    if form_row['volunteer-write'] is not None and len(form_row['volunteer-write']) > 0:
      attributes["Writing"] = True
    service_id = self.service_counter
    self.service_counter = self.service_counter + 1
    self.tiger.addService("Volunteering", service_id, attributes, person_id, "VOLUNTEERS")

def read_submission(filepath, target_dir, tigerDB):
  data = pandas.read_csv(filepath, encoding='utf8')
  data = data.sort_values(by=['id'])
  
  refugees = data[data['form_name'] == 'БеженцыРус']
  angels = data[data['form_name'] == 'АнгелыРус']
  volunteers = data[data['form_name'] == 'Volunteer']
  
  refugees.to_csv(target_dir + '/' + 'refugees.csv', index=False, encoding='utf-8-sig')
  angels.to_csv(target_dir + '/' + 'angels.csv', index=False, encoding='utf-8-sig')
  volunteers.to_csv(target_dir + '/' + 'volunteers.csv', index=False, encoding='utf-8-sig')

  parser = Parser(tigerDB)
  with open(target_dir + '/angels.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    # iterate over each line as a ordered dictionary
    for row in csv_dict_reader:
      parser.parse_angel(row)

  with open(target_dir + '/refugees.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    # iterate over each line as a ordered dictionary
    for row in csv_dict_reader:
      parser.parse_refugee(row)

  with open(target_dir + '/volunteers.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    # iterate over each line as a ordered dictionary
    for row in csv_dict_reader:
      parser.parse_volunteer(row)

def main():
  from jproperties import Properties
  configs = Properties()
  with open('app-config.properties', 'rb') as config_file:
    configs.load(config_file)
  tiger = tigerdb.TigerDB(configs)

  read_submission("./data/demo_data.csv", "./tmp", tiger)
  
if __name__ == "__main__":
  main()
