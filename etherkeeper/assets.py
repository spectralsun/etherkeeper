from django_assets import Bundle, register

from etherkeeper.core import assets as core


js = Bundle(
    core.js
)
register('js', js)

css = Bundle(
    core.css
)
register('css', css)