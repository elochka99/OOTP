from viewSearch import SearchDialog
from pattern import singleton
import webbrowser


@singleton
class Search(object):

    def __init__(self):
        self.ui = SearchDialog()
        self.ui.trigger(self.search)

    def show(self):

        self.ui.show()

    def hide(self):
        self.ui.hide()

    def search(self):
        if self.ui.web_url != '':
            webbrowser.open('https://soundcloud.com/search/sounds?q={}'
                            .format(self.ui.web_url))
