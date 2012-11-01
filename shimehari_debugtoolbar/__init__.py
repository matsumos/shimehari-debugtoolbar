import os

from shimehari import request, shared as g
from shimehari.shared import _requestContextStack
from shimehari.helpers import sendFromDirectory as send_from_directory
from jinja2 import Environment, PackageLoader
from werkzeug.urls import url_quote_plus

from shimehari_debugtoolbar.toolbar import DebugToolbar


def replace_insensitive(string, target, replacement):
    """Similar to string.replace() but is case insensitive
    Code borrowed from: http://forums.devshed.com/python-programming-11/case-insensitive-string-replace-490921.html
    """
    no_case = string.lower()
    index = no_case.rfind(target.lower())
    if index >= 0:
        return string[:index] + replacement + string[index + len(target):]
    else: # no results so return the original string
        return string


def _printable(value):
    if isinstance(value, unicode):
        return value.encode('unicode_escape')
    elif isinstance(value, str):
        return value.encode('string_escape')
    else:
        return repr(value)


class DebugToolbarExtension(object):
    _static_dir = os.path.realpath(
        os.path.join(os.path.dirname(__file__), 'static'))

    _redirect_codes = [301, 302, 303, 304]

    def __init__(self, app):
        self.app = app
        self.debug_toolbars = {}
        self.hosts = ()

        if not app.config.get('DEBUG_TB_ENABLED', app.debug):
            return

        if not app.config.get('SECRET_KEY'):
            raise RuntimeError(
                "The Shimehari-DebugToolbar requires the 'SECRET_KEY' config "
                "var to be set")

        DebugToolbar.load_panels(app)

        self.hosts = app.config.get('DEBUG_TB_HOSTS', ())

        self.app.beforeRequest(self.process_request)
        self.app.afterRequest(self.process_response)
        # self.app.teardownRequest(self.teardown_request)

        # Monkey-patch the Shimehari.dispatchRequest method
        app.dispatchRequest = self.dispatch_request

        # Configure jinja for the internal templates and add url rules
        # for static data
        self.jinja_env = Environment(
            autoescape=True,
            extensions=['jinja2.ext.i18n', 'jinja2.ext.with_'],
            loader=PackageLoader(__name__, 'templates'))
        self.jinja_env.filters['urlencode'] = url_quote_plus
        self.jinja_env.filters['printable'] = _printable
        self.jinja_env.globals['csrfToken'] = app.templateEnv.globals['csrfToken']

        app.addRoute('/_debug_toolbar/static/<path:filename>',self.send_static_file)

    def dispatch_request(self):
        """Modified version of Shimehari.dispatchRequest to call process_view."""

        self.app.tryTriggerBeforeFirstRequest()
        try:
            rv = self.app.preprocessRequest()
            if rv is None:
                req = _requestContextStack.top.request
                if req.routingException is not None:
                    self.app.raiseRoutingException(req)
                rule = req.urlRule
        
                view_func = self.app.controllers[rule.endpoint]
                view_func = self.process_view(self.app, view_func, req.viewArgs)
                rv = view_func(**req.viewArgs)
        except Exception, e:
            rv = self.app.makeResponse(self.app.handleUserException(e))

        response = self.app.makeResponse(rv)
        response = self.app.processResponse(response)

        return response

    def _show_toolbar(self):
        """Return a boolean to indicate if we need to show the toolbar."""
        if request.path.startswith('/_debug_toolbar/'):
            return False

        if self.hosts and request.remote_addr not in self.hosts:
            return False

        return True

    def send_static_file(self, filename):
        """Send a static file from the shimehari-debugtoolbar static directory."""
        return send_from_directory(self._static_dir, filename)

    def process_request(self):
        g.debug_toolbar = self

        if not self._show_toolbar():
            return

        real_request = request._get_current_object()

        self.debug_toolbars[real_request] = DebugToolbar(real_request, self.jinja_env)
        for panel in self.debug_toolbars[real_request].panels:
            panel.process_request(real_request)

    def process_view(self, app, view_func, view_kwargs):
        """ This method is called just before the shimehari view is called.
        This is done by the dispatch_request method.
        """
        real_request = request._get_current_object()
        if real_request in self.debug_toolbars:
            for panel in self.debug_toolbars[real_request].panels:
                new_view = panel.process_view(real_request, view_func, view_kwargs)
                if new_view:
                    view_func = new_view
        return view_func

    def process_response(self, response):
        real_request = request._get_current_object()
        if real_request not in self.debug_toolbars:
            return response

        # Intercept http redirect codes and display an html page with a
        # link to the target.
        if self.debug_toolbars[real_request].config['DEBUG_TB_INTERCEPT_REDIRECTS']:
            if response.status_code in self._redirect_codes:
                redirect_to = response.location
                redirect_code = response.status_code
                if redirect_to:
                    content = self.render('redirect.html', {
                        'redirect_to': redirect_to,
                        'redirect_code': redirect_code
                    })
                    response.content_length = len(content)
                    response.location = None
                    response.response = [content]
                    response.status_code = 200

        # If the http response code is 200 then we process to add the
        # toolbar to the returned html response.
        if (response.status_code == 200
            and response.headers['content-type'].startswith('text/html')):
            for panel in self.debug_toolbars[real_request].panels:
                panel.process_response(real_request, response)

            if response.is_sequence:
                response_html = response.data.decode(response.charset)
                toolbar_html = self.debug_toolbars[real_request].render_toolbar()

                content = replace_insensitive(
                    response_html, '</body>', toolbar_html + '</body>')
                content = content.encode(response.charset)
                response.response = [content]
                response.content_length = len(content)

        return response

    def teardown_request(self, exc):
        self.debug_toolbars.pop(request._get_current_object(), None)

    def render(self, template_name, context):
        template = self.jinja_env.get_template(template_name)
        return template.render(**context)
