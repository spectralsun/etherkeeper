from django_assets import Bundle, register

from etherkeeper.core import assets as core
from etherkeeper.etherpad import assets as etherpad


js = Bundle(
    core.js,
    etherpad.js
)
register('js', js)

css = Bundle(
    core.css,
    etherpad.css
)
register('css', css)