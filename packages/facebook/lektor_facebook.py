# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
import lektor.admin.modules.dash
from flask import abort
from flask import Blueprint
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

bp = Blueprint("facebook", __name__, url_prefix="/facebook")


@bp.route("/hello")
def facebook_endpoint(**kwargs):
    """This function is invoked by all dash endpoints."""
    return "Hello from facebook plugin"


class FacebookPlugin(Plugin):
    name = 'lektor-facebook'
    description = u'Add your description here.'

#    def __init__(self, env, id):
#        super().__init__(env, id)
#        lektor.admin.modules.dash.endpoints.append('/fuck', 'fuck')

    def on_setup_env(self, **extra):
        #self.env.jinja_env.globals['my_variable'] = 'my value'
        pass

    # def on_process_template_context(self, context, **extra):
    #    def test_function():
    #        return 'Value from plugin %s' % self.name
    #    context['test_function'] = test_function

    def get_blueprint(self):
        return bp
