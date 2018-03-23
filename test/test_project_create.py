from model.project import Project


def test_project_create(app, json_projects):
    if not app.session.is_logged_in():
        app.session.login("administrator", "root")
    old_projects = app.project.get_project_list()
    app.project.create(json_projects)
    new_projects = app.project.get_project_list()
    old_projects.append(json_projects)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
