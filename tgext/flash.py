# -*- coding: utf-8 -*-
'''
You can override templates and variable defaults in the Flash class
if you need customization

TODO:
- Customization per config
- JS stuff
'''

import json

from tg import response, request
from tg.flash import TGFlash

from urllib import quote, unquote
from markupsafe import escape_silent as html_escape

log = __import__('logging').getLogger(__name__)


def copy_and_call(d, *args, **kw):
    r = dict()
    for k in d:
        if hasattr(d[k], '__call__'):
            r[k] = d[k](*args, **kw)
        else:
            r[k] = d[k]
    return r


class Flash(TGFlash):

    # Displaying the flash message via JS is not implemented ATM
    use_js = False

    # For future- and backwards-compatibility
    get_response = lambda: response
    get_request = lambda: request

    container_template = """
<div id="%(container_id)s" class="%(container_class)s">
  %(content)s
</div>
"""
    # Default dictionary of container_template variables
    # If any value is a callable, it will be called
    container_vars = dict(
        container_id="flash",
        container_class=""
        )

    message_template = """
<div id="%(content_id)s" class="%(content_class)s">
  %(message)s
</div>
"""
    # Default dictionary of message_template variables
    # If any value is a callable, it will be called
    # with the current message dict as parameter
    message_vars = dict(
        content_id=lambda m: m['i'],
        content_class=lambda m: m['status']
        )

    def __call__(self, message, status=None,
        overwrite=False,
        **extra_payload):

        if response is None:
            raise ValueError("Must provide a response object or "
                "configure a callable that provides one")

        payload = []

        if not overwrite and request:
            try:
                # Get payload, if already set before
                payload = request.environ['webflash.payload']
                payload = json.loads(unquote(payload))
                log.debug("Got payload from environ %d", id(request.environ))
                if isinstance(payload, dict):
                    log.debug('Upgrading old-style payload...')
                    payload = [payload]
            except:
                # No previous payload set before
                pass

        payload.append(
            dict(
                # Force the message to be unicode so lazystrings, etc... are coerced
                message=unicode(message),
                status=status or self.default_status,
                **extra_payload
            ))

        payload = quote(json.dumps(payload))

        if request:
            # Save the payload in environ too in case JavaScript is not being
            # used and the message is being displayed in the same request.
            request.environ['webflash.payload'] = payload
            log.debug("Setting payload in environ %d", id(request.environ))
        log.debug("Setting payload in cookie")
        response.set_cookie(self.cookie_name, payload)

        if len(response.headers['Set-Cookie']) > 4096:
            raise ValueError('Flash value is too long (cookie would be >4k)')

    def render(self, container_id, use_js=False, container_class='', *args, **kwargs):
        payload = self.pop_payload(request, response)
        if not payload:
            return ''
        if isinstance(payload, dict):
            payload = [payload]

        r = []
        for i, p in enumerate(payload):
            p['i'] = i
            if 'no_escape' in p:
                p['message'] = p.get('message', '')
            else:
                p['message'] = html_escape(p.get('message', ''))
            vars = copy_and_call(self.message_vars, p)
            vars.update(p)
            r.append(self.message_template % vars)
        return self.container_template % {
            'container_id': container_id,
            'container_class': container_class,
            'content': '\n'.join(r)}


flash = Flash()
