from django_assets import Bundle, register

js = Bundle(
    'lib/jquery/jquery.min.js',
    'lib/bootstrap/bootstrap.min.js'
)
register('js', js)

css = Bundle(
    'lib/bootstrap/bootstrap.min.css',
    'css/index.css',
    'css/bootstrap.css'
)
register('css', css)
