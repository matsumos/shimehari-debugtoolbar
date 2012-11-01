from shimehari import VERSION as shimehari_version
from shimehari_debugtoolbar.panels import DebugPanel

_ = lambda x: x

class VersionDebugPanel(DebugPanel):
    """
    Panel that displays the Shimehari version.
    """
    name = 'Version'
    has_content = False

    def nav_title(self):
        return _('Versions')

    def nav_subtitle(self):
        return 'Shimehari  %s' % shimehari_version

    def url(self):
        return ''

    def title(self):
        return _('Versions')

    def content(self):
        return None


