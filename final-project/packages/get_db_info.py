from column_models import Save


def get_db():
    db = Save.query().order(Save.start_date).fetch()
    params = {
        "projects": db
    }
    return params


def get_project_info(message_id):
    # seleccion a un proyecto por su id
    project_selected = Save.get_by_id(int(message_id))
    params = {
        "project": project_selected,
    }
    return params
