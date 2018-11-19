#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import webapp2
import jinja2
from project_class import Project


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
    def get(self):
        params = {}
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
        project = Project(expediente, start_date, code, name, place, status, comments)
        print str(project)
        params = {"message" : "El proyecto ha sido guardado"}
        return self.render_template("index.html", params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler)], debug=True)

