;var ek = (function() {
    var EtherKeeper = {
        open: function(page) {
            body.removeClass('viewer-open home-open')
            body.addClass(page + '-open');
            return this;
        },
        open_doc: function(url) {
            iframe.attr('src', url);
            this.open('viewer');
        }
    }
    var body = $('body');
    var search = $('#search');
    $('button', search).click(function() {
        search.addClass('top');
    });
    var viewer = $('#viewer'),
        viewer_bar = $('#viewer_bar'),
        iframe = $('iframe', viewer);
    var home = $('#home');
    var $window = $(window), onresize;
    $window.resize(onresize = function() {
        viewer.height($window.height() - 125);
    });
    onresize();

    var login = $('#login_modal');
    $('.submit', login).click(function () {
        $.post('/login',{
            username: $('[name=username]').val(),
            password: $('[name=password]').val()
        }, function(json) {
            if (json.success) {
                login.modal('hide');
                alertify.success('Logged in.');
                $('#navbar_user').html(json.navbar);
                home.html(json.home);
                EtherKeeper.open('home');
            }
        },'json').fail(function() {
            alertify.error('Failed to log in successfuly')
        });
    });

    $('#create button').click(function () {
        $.post('/api/etherpad/create', function (json) {
            if (json.success) {
                EtherKeeper.open_doc(json.pad)
            }
        }, 'json');
    });


    $(document).on('click', '.logout', function() {
        $.post('/logout', function(json) {
            if (json.success) {
                alertify.success('Logged out.');
                $('#navbar_user').html(json.navbar);
                home.html('');
                body.attr('class','');
            }
        }, 'json')
    }).on('change', 'thead .cb input', function() {
        $(this).parents('thead').siblings().find('.cb input').prop('checked', $(this).prop('checked'));
    });

    var routing = Davis(function () {
        function index() {
            body.attr('class','');
        }
        this.get('/', index);
        this.get('/search', index);
        this.get('/search/:search', function(req) {

        });
        this.get('/home', function() {
            EtherKeeper.open('home');
        });
        this.get('/etherpad/:pad', function (req) {
            $.post('/api/etherpad/open/', { id: req.params['pad'] }, function(json) {
                EtherKeeper.open_doc(json.pad)
            },'json');
        });
      

    })

    routing.start()
   
    EtherKeeper.routing = routing;
    $.ajaxSetup({
        crossDomain: false, 
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });

    return EtherKeeper;
})();