from random import randrange
from model.project import Project


def test_project_delete(app):
    if not app.session.is_logged_in():
        app.session.login("administrator", "root")
    app.project.ensure_project_created(Project(name="Test name"))
    old_projects = app.project.get_project_list()
    index = randrange(len(old_projects))
    app.project.delete_project_by_index(index)
    new_projects = app.project.get_project_list()
    old_projects[index:index+1] = []
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
