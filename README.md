tgext.flash
===========

Advanced Flash Extension for TurboGears 2 that supports template customization and displaying multiple flash messages in one request.

Usage:
------

Install with `easy_install https://github.com/moschlar/tgext.flash/archive/master.tar.gz#egg=tgext.flash-0.1`

Use in your controller like
```python
from tg import TGController, expose, tmpl_context
from tgext.flash import flash

class BlaController(TGController):

    def _before(self, *args, **kw):
        tmpl_context.flash = flash

    @expose(...)
    def index(self):
        flash("First message", "ok")
        flash("<b>Second</b> message", "warning", no_escape=True)
        return dict(...)
```
and in your (Mako) template like:
```Mako
${c.flash() | n}
```

TODO:
-----

- Monkeypatching
- Maybe use `tgext.pluggable`
- Allow customization (templates) per app_config
- Allow *real* templates to be used
- Make JS stuff working
- Consider making the flash object a ToscaWidgets widget to have their rendering engine bindings
