from random import randrange
from model.project import Project


def test_project_delete(app):
    user_config = app.config['webadmin']
    if not app.session.is_logged_in():
        app.session.login(user_config['username'], user_config['password'])
    app.project.ensure_project_created(Project(name="Test name"))
    old_projects = app.soap.get_user_projects(user_config['username'], user_config['password'])
    index = randrange(len(old_projects))
    project_id = old_projects[index][0]
    app.project.delete_project_by_id(project_id)
    new_projects = app.soap.get_user_projects(user_config['username'], user_config['password'])
    old_projects[index:index + 1] = []
    assert str(old_projects) == str(new_projects)
