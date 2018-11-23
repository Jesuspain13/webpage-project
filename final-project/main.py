#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import webapp2
import jinja2
from column_models import Save


current_path = os.path.dirname(__file__)
template_dir = os.path.join(current_path, "templates")

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):
    def render_template(self, template_filename, params=None):
        if params is None:
            params= {}

        template = jinja_env.get_template(template_filename)
        response = template.render(params)

        return self.response.write(response)


class MainHandler(BaseHandler):
    # con este get recibimos los proyectos de la DB y los mostramos en el INDEX.HTML
    def get(self):
        db = Save.query().order(Save.start_date).fetch()
        params = {
            "messages": db
        }
        return self.render_template("index.html", params)

    def post(self):
        # seleccionamos los valores que cogemos de los input
        expediente = self.request.get("expediente")
        start_date = self.request.get("start_date")
        code = self.request.get("code")
        name = self.request.get("name")
        place = self.request.get("place")
        status = self.request.get("status")
        comments = self.request.get("comments")
        saved = Save(expediente=expediente, code=code, name=name, place=place, status=status, comments=comments)
        saved.put()
        params = {"message": "El proyecto ha sido guardado"}
        return self.render_template("index.html", params)


class ProjectInfoHandler(BaseHandler):
    def get(self, message_id):
        project_selected = Save.get_by_id(int(message_id))
        params = {
            "id": project_selected
        }
        return self.render_template("try.html", params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/info/<message_id:\d+>', ProjectInfoHandler)], debug=True)

