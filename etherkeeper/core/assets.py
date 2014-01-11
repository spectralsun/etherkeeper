from django_assets import Bundle, register


js = Bundle(
    'lib/jquery/jquery.min.js',
    'lib/jquery/jquery.cookie.js',
    'lib/alertify/alertify.min.js',
    'lib/bootstrap/bootstrap.min.js',
    'lib/lodash.min.js',
    'lib/davis.min.js',
    'js/etherkeeper.js'
)
register('js', js)

css = Bundle(
    'lib/bootstrap/bootstrap.min.css',
    'lib/alertify/alertify.core.css',
    'lib/alertify/alertify.default.css',
    'css/etherkeeper.css',
    'css/bootstrap.css',
)
register('css', css)
