from AbstractApp import AbstractApp
from AbstractMatchApp import AbstractMatchApp
from AbstractResolveApp import AbstractResolveApp

class HostVerification(AbstractApp):
    def getVertexType(self):
        return "Accommodation"

    def setColumnInfo(self, column_map):
        if len(column_map) == 0:
            return column_map
        column_map["HostLimit"].editable = True
        column_map["HasKids"].editable = True
        column_map["Verified"].editable = True
        column_map["Verified"].boolean = True
        return column_map

class RefugeeAccommodationVerification(AbstractApp):
    def getVertexType(self):
      return "Accommodation"

    def setColumnInfo(self, column_map):
        if len(column_map) == 0:
            return column_map
        column_map["HostLimit"].editable = True
        column_map["HasKids"].editable = True
        column_map["Verified"].editable = True
        column_map["Verified"].boolean = True
        return column_map

class TicketDonators(AbstractApp):
    def getVertexType(self):
      return "TicketDonation"

    def setColumnInfo(self, column_map):
        #nothing is editable
        return column_map

class VolunteerVerification(AbstractApp):
    def getVertexType(self):
      return "Volunteering"

    def setColumnInfo(self, column_map):
        if len(column_map) == 0:
            return column_map
        column_map["Name"].editable = True
        column_map["Email"].editable = True
        column_map["Writing"].editable = True
        column_map["Writing"].boolean = True
        column_map["HostVerification"].editable = True
        column_map["HostVerification"].boolean = True
        column_map["Verified"].editable = True
        column_map["Verified"].boolean = True
        return column_map

#------

class MatchAccommodation(AbstractMatchApp):
    pass

class MatchSchool(AbstractMatchApp):
    pass

class MatchPaperwork(AbstractMatchApp):
    pass

#-----

class ResolvePerson(AbstractResolveApp):
    pass