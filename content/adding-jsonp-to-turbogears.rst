Adding JSONP to turbogears
##########################
:date: 2012-11-09 08:34
:author: Toumorokoshi
:category: General

.. raw:: html

   <p>

::

    from tg import json_encode, responsefrom tg.render import _get_tg_varsdef render_jsonp(template_name, template_vars, **kwargs):callback = template_name or kwargs.pop('callback', None) or 'callback'for key in _get_tg_vars():del template_vars[key]response.headers['Content-Type'] = 'text/javascript'return '%s(%s)' % (template_name, json_encode(template_vars))from myapp.config.app_cfg import base_configbase_config.render_functions['jsonp'] = render_jsonpbase_config.mimetype_lookup = {'.jsonp': 'text/javascript'}

.. raw:: html

   </p>

courtesy of Pederson:

https://github.com/TurboGears/tg2/issues/2
