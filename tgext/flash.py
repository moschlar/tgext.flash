import json
from urllib import quote, unquote
from logging import getLogger
from tg.flash import TGFlash
from webflash import html_escape
from tg import response, request

log = getLogger(__name__)


class Flash(TGFlash):

    use_js = False

    def __call__(self, message, status=None,
        response=None, request=None,
        **extra_payload):

        response = response or self.get_response()
        if response is None:
            raise ValueError(
                "Must provide a response object or configure a callable that "
                "provides one"
                )

        payload = []

#        log.debug("Getting payload from cookie")
#        payload = response.get_cookie(self.cookie_name)

        request = request or self.get_request()
        if request:
            try:
                payload = request.environ['webflash.payload']
                log.debug(payload)
                payload = json.loads(unquote(payload))
                log.debug(payload)
                log.debug("Got payload from environ %d", id(request.environ))
            except:
                pass

        if isinstance(payload, dict):
            log.debug('Upgrading old-style payload...')
            payload = [payload]

        payload.append(
            dict(
                message=message,
                status=status or self.default_status,
                **extra_payload
            ))

        payload = quote(json.dumps(payload))

#        request = request or self.get_request()
        if request is not None:
            # Save the payload in environ too in case JavaScript is not being
            # used and the message is being displayed in the same request.
            request.environ['webflash.payload'] = payload
            log.debug("Setting payload in environ %d", id(request.environ))
        log.debug("Setting payload in cookie")
        response.set_cookie(self.cookie_name, payload)

    def render(self, container_id, use_js=False, request=None, response=None, *args, **kwargs):
        payload = self.pop_payload(request, response)
        if not payload:
            return ''
        if isinstance(payload, dict):
            payload = [payload]
        for p in payload:
            p['message'] = html_escape(p.get('message', ''))
            p['container_id'] = container_id
        return '\n'.join(self.static_template % p for p in payload)



flash = Flash(
    get_response=lambda: response,
    get_request=lambda: request
    )
