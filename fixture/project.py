from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    project_cache = None

    def open_project_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php")):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def create(self, project):
        wd = self.app.wd
        self.open_project_page()
        # init project creation
        wd.find_element_by_css_selector("input[value='Create New Project']").click()
        self.fill_project_form(project)
        # submit project creation
        wd.find_element_by_css_selector("input[value='Add Project']").click()
        wd.find_element_by_link_text("Proceed").click()
        self.project_cache = None

    def fill_project_form(self, project):
        self.change_field_value("name", project.name)
        self.change_select_option("status", project.status)
        self.change_checkbox_value("inherit_global", project.inherit_global)
        self.change_select_option("view_state", project.view_status)
        self.change_field_value("description", project.description)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def change_select_option(self, select_name, option):
        wd = self.app.wd
        if option is not None:
            select_xpath = "//select[@name='" + select_name + "']//option[text()='" + str(option) + "']"
            if not wd.find_element_by_xpath(select_xpath).is_selected():
                wd.find_element_by_xpath(select_xpath).click()

    def change_checkbox_value(self, checkbox_name, value):
        wd = self.app.wd
        if value == 'no':
            if wd.find_element_by_name(checkbox_name).is_selected():
                wd.find_element_by_name(checkbox_name).click()
        elif value == 'yes':
            if not wd.find_element_by_name(checkbox_name).is_selected():
                wd.find_element_by_name(checkbox_name).click()

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_project_page()
            self.project_cache = []
            target_xpath = "//tr[td/a[contains(@href, 'manage_proj_edit_page.php?project_id=')]]"
            for element in wd.find_elements_by_xpath(target_xpath):
                cells = element.find_elements_by_tag_name("td")
                link_with_id = cells[0].find_element_by_tag_name("a").get_attribute("href")
                id = link_with_id[link_with_id.find('id=')+3:]
                name = cells[0].text
                status = cells[1].text
                if cells[2].text == 'X':
                    enabled = 'yes'
                else:
                    enabled = 'no'
                view_status = cells[3].text
                description = cells[4].text
                self.project_cache.append(Project(id=id, name=name, status=status, enabled=enabled,
                                                  view_status=view_status, description=description))
        return list(self.project_cache)

    def count(self):
        wd = self.app.wd
        self.open_project_page()
        return len(wd.find_elements_by_xpath("//tr[td/a[contains(@href, 'manage_proj_edit_page.php?project_id=')]]"))

    def ensure_project_created(self, project):
        if self.count() == 0:
            self.create(project)

    def delete_project_by_index(self, index):
        wd = self.app.wd
        self.open_project_page()
        self.open_project_by_index(index)
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        self.open_project_page()
        self.project_cache = None

    def open_project_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_xpath("//a[contains(@href, 'manage_proj_edit_page.php?project_id=')]")[index].click()
