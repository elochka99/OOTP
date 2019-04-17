from view.viewSearch import SearchDialog
from core.pattern import singleton
import webbrowser


@singleton
class Search(object):
    """
    Controller search view
    """
    def __init__(self):
        """
        Initialize controller and trigger buttons
        """
        self.ui = SearchDialog()
        self.ui.trigger(self.search)

    def show(self):
        """
        show user interface
        """
        self.ui.show()

    def hide(self):
        """
        hide user interface
        """
        self.ui.hide()

    def search(self):
        """
        On submit button search
        """
        if self.ui.web_url != '':
            webbrowser.open('https://soundcloud.com/search/sounds?q={}'
                            .format(self.ui.web_url))
