from
def get_db():
    db = Save.query().order(Save.start_date).fetch()
    params = {
        "projects": db
    }
    return self.render_template("index.html", params)
