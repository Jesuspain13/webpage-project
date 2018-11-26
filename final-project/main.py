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
            params = {}

        template = jinja_env.get_template(template_filename)
        response = template.render(params)

        return self.response.write(response)


class MainHandler(BaseHandler):
    # con este get recibimos los proyectos de la DB y los mostramos en el INDEX.HTML
    def get(self):
        db = Save.query().order(Save.start_date).fetch()
        params = {
            "projects": db
        }
        return self.render_template("index.html", params)

    def post(self):
        # seleccionamos los valores que cogemos de los input
        expediente = self.request.get("expediente")
        code = self.request.get("code")
        name = self.request.get("name")
        place = self.request.get("place")
        status = self.request.get("status")
        comments = self.request.get("comments")
        saved = Save(expediente=expediente, code=code, name=name, place=place, status=status, comments=comments)
        saved.put()

        # esto es para cuando introduzcas el nuevo proyecto se vuelva a mostrar
        db = Save.query().order(Save.start_date).fetch()
        params = {"message1": "El proyecto ha sido guardado",
                  "messages": db}
        return self.render_template("index.html", params)


class ProjectListHandler(BaseHandler):
    def get(self):
        db = Save.query().order(Save.start_date).fetch()
        params = {
            "projects": db
        }
        return self.render_template("project-list.html", params)


class ProjectInfoHandler(BaseHandler):
    def get(self, message_id):
        project_selected = Save.get_by_id(int(message_id))
        params = {
            "project": project_selected,
        }
        return self.render_template("try.html", params)


class ProjectChangerHandler(BaseHandler):
    def get(self, message_id):
        project_selected = Save.get_by_id(int(message_id))
        params = {
            "project": project_selected,
        }
        return self.render_template("change-info.html", params)

    def post(self, message_id):
        project_selected = Save.get_by_id(int(message_id))
        project_selected.expediente = self.request.get("expediente")
        project_selected.code = self.request.get("code")
        project_selected.place = self.request.get("place")
        project_selected.status = self.request.get("status")
        project_selected.comments = self.request.get("comments")
        project_selected.put()

        params = {
            "answer1": "The project: " + project_selected.name + " has been edited",
            "project": project_selected
        }
        return self.render_template("change-info.html", params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/info', ProjectListHandler),
    webapp2.Route('/info/<message_id:\d+>', ProjectInfoHandler),
    webapp2.Route('/changeproject/<message_id:\d+>/edit', ProjectChangerHandler)],
    debug=True)

