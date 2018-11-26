#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import webapp2
import jinja2
from packages.column_models import Save
from packages.get_db_info import get_db, get_project_info


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
        return self.render_template("index.html", params=get_db())

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

        # esto es para cuando introduzcas el nuevo proyecto se vuelva a mostrar y ver que se ha guardado
        return self.redirect_to("project-list")


class ProjectListHandler(BaseHandler):
    # para mostrar la lista de proyectos y elegir uno cuando pulses en info y cambiarlo
    def get(self):
        return self.render_template("project-list.html", params=get_db())

    def post(self):
        # quiero que puedas buscar el nombre en la base de datos y te salga en la lista
        nombre = self.request.get("nombre")
        # con esto realizamos una busqueda en la DB con el valor introducido en el input antes
        selected = Save.query(Save.name == nombre)
        selected_key = selected.get()
        params = {
            "project": selected_key
        }
        return self.render_template("try.html", params)


class ProjectInfoHandler(BaseHandler):
    # mostrar la información detallada del proyecto seleccionado
    def get(self, message_id):
        return self.render_template("try.html", params=get_project_info(message_id))

    def post(self, message_id):
        # función borrar proyecto seleccionado
        project_selected = Save.get_by_id(int(message_id))
        project_selected.key.delete()

        return self.redirect_to("project-list")


class ProjectChangerHandler(BaseHandler):
    # mostrar la página con el proyecto seleccionado y los campos para introducir la nueva info
    def get(self, message_id):
        return self.render_template("change-info.html", params=get_project_info(message_id))

    def post(self, message_id):
        # coger el proyecto, coger la info de los input, sobrescribir atributos del proyecto y guardar en la DB.
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
    webapp2.Route('/', MainHandler, name="project-list"),
    webapp2.Route('/info', ProjectListHandler),
    webapp2.Route('/info/<message_id:\d+>', ProjectInfoHandler, name="project-info"),
    webapp2.Route('/changeproject/<message_id:\d+>/edit', ProjectChangerHandler)],
    debug=True)

