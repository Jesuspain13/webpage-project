class Project(object):
    def __init__(self, expediente, start_date, code, name, place, status, comments):
        self.expediente = expediente
        self.start_date = start_date
        self.code = code
        self.name = name
        self.place = place
        self.status = status
        self.comments = comments

    def __str__(self):
        return self.name

    def modify_content(self):
        pass

# Ahora mismo esta clase no nos sirve. DIA 23/11
