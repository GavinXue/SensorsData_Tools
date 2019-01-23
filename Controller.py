from Pages import Login, HomePage, ErrorDisplay, UpdateCname


class Controller:
    def __init__(self):
        self.sa = None
        self.event_design = None
        self.login = None
        self.homepage = None
        self.error_page = None
        self.update_cname_page = None

    def show_login(self):
        self.login = Login()
        self.login.login_success.connect(self.login_home)
        self.login.show()

    def login_home(self, sa):
        self.homepage = HomePage(sa)
        self.sa = sa
        self.login.close()
        self.homepage.show()
        self.homepage.upload_design_success.connect(self.upload_design)
        self.homepage.go_error_page.connect(self.show_error_page)
        self.homepage.go_update_cname_page.connect(self.show_update_cname_page)

    def upload_design(self, event_design=None):
        self.event_design = event_design

    def back_homepage(self, old_page):
        old_page.close()
        self.homepage.show()

    def show_error_page(self, error_str):
        self.error_page = ErrorDisplay(error_str)
        self.homepage.hide()
        self.error_page.show()
        self.error_page.back_homepage.connect(self.back_homepage)

    def show_update_cname_page(self, sa, upload_design):
        self.homepage.hide()
        self.update_cname_page = UpdateCname(sa, upload_design)
        self.update_cname_page.show()
        self.update_cname_page.back_homepage.connect(self.back_homepage)
