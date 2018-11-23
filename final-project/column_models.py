from google.appengine.ext import ndb


class Save(ndb.Model):
    expediente = ndb.StringProperty()
    start_date = ndb.DateTimeProperty(auto_now_add=True)
    code = ndb.StringProperty()
    name = ndb.StringProperty()
    # no se si debemos guardarlo como punto geografico o como string simplemente
    place = ndb.StringProperty()
    status = ndb.StringProperty()
    comments = ndb.TextProperty()
