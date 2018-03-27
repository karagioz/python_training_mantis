def test_project_create(app, json_projects):
    user_config = app.config['webadmin']
    if not app.session.is_logged_in():
        app.session.login(user_config['username'], user_config['password'])
    old_projects = app.soap.get_user_projects(user_config['username'], user_config['password'])
    app.project.create(json_projects)
    new_projects = app.soap.get_user_projects(user_config['username'], user_config['password'])
    assert len(new_projects) == len(old_projects)+1
    assert is_equal(sorted(new_projects, key=pr_id)[-1], json_projects)


def is_equal(soap_project, json_project):
    return (soap_project['name'] == json_project.name
            and soap_project['status']['name'] == json_project.status
            and soap_project['view_state']['name'] == json_project.view_status
            and soap_project['description'] == json_project.description)


def pr_id(soap_project):
    return int(soap_project['id'])
