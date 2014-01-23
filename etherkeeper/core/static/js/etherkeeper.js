(function() {
    var EtherKeeper = {

        // creates a new document 
        create_doc: function() {
            $.post('/api/etherpad/create', function (json) {
                if (json.success) {
                    EtherKeeper.open_doc(json)
                }
            }, 'json');
        },

        // callback to setup etherpad after getting session
        open_doc: function(json) {
            iframe.removeAttr('src').one('load', function() {
                loading.hide();
                iframe.fadeIn('slow');
            }).attr('src', json.pad);
            
            var title = json.title;
            if (title === '') {
                $('.title-holder').addClass('untitled');
                title = 'Untitled Document';
            }
            $('.title-holder').html(title);
        },

        // gets a session for an etherpad
        get_session: function(pad) {            
            loading.show();
            this.current_pad = pad;
            this.page('viewer');
            var onfail = EtherKeeper.onfail('open document', function() {
                loading.hide();
                EtherKeeper.set_route('/home');
            });
            $.post('/api/etherpad/open/', { id: pad }, function(json) {
                if (json.success) {
                    EtherKeeper.open_doc(json)
                } else {
                    onfail();
                }
            },'json').fail(onfail);
        },

        get_title: function() {
            var onfail = EtherKeeper.onfail('get title');
            $.post('/api/etherpad/title', { id: this.current_pad }, function(json) {
                if (json.success) {
                    $('.title-holder').html(json.title)
                } else {
                    onfail();
                }
            },'json').fail(onfail);  
        },

        // clears all body classes causing a revert to index
        index: function() {
            body.attr('class','');
        },
        
        // sets a page-class on the body tag for pagination
        page: function(page) {
            this.index();
            body.addClass(page + '-open');
            if (page !== 'viewer') {
                iframe.hide();
                iframe.removeAttr('src');
            }
            return this;
        },
        
        // sends a message to the etherpad instance
        send_message: function(data) {
            
            iframe_window.postMessage(JSON.stringify(data), 'http://localhost:9001');
        },

        // sets the current location to the path and fire a pushState event
        set_route: function(path) {
            Davis.location.assign(new Davis.Request({
                method: 'get',
                fullPath: path,
                title: ''
            }));
        },


        set_title: function(title) {
            var onfail = EtherKeeper.onfail('change document title');
            $.post('/api/etherpad/set_title', { 
                title: title, 
                id: this.current_pad
            }, function(json) {
                if (json.success) {
                    alertify.success('Document title changed.');
                } else {
                    onfail();
                }
            },'json').fail(onfail);
        },
        onmessage: function(e) {
            var event = e.originalEvent;
            if (event.origin !== 'http://localhost:9001')
                return;
            var data = JSON.parse(event.data);
            console.log(data)
            if (data.type === 'init') {
                EtherKeeper.send_message({ type: 'init' });
            } else if (data.type === 'title_update') {
                EtherKeeper.get_title()
            }
        },
        onfail: function(error, cb) {
            return function() { alertify.error('Failed to ' + error + '.'); if (cb) cb() }
        },
        onresize: function() {
            viewer.height($window.height() - 125);
        }
    }
    var body = $('body'),
        search = $('#search'),
        viewer = $('#viewer'),
        viewer_bar = $('#viewer_bar'),
        iframe = $('iframe', viewer),
        iframe_window = iframe[0].contentWindow,
        home = $('#home'),
        loading = $('#loading'),
        $window = $(window);
    $window.resize(EtherKeeper.onresize)
           .on('message', EtherKeeper.onmessage);

    EtherKeeper.onresize();   

    $('.title-holder').click(function() {
        var input = $(this).hide().siblings('input').show().val('');
        if (!$(this).hasClass('untitled'))
            input.val($(this).text());
    });

    $('.edit-title input').keydown(function(e) {
        if (e.keyCode == 13) {
            var val = $(this).val();
            if (val === '')
                val = $(this).attr('placeholder')
            $(this).hide().siblings().html(val).show();
            EtherKeeper.set_title(val)
        } else if (e.keyCode === 27) {
            $(this).hide().siblings().show();
        }
    });

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
                EtherKeeper.page('home');
            }
        },'json').fail(function() {
            alertify.error('Failed to log in successfuly')
        });
    });

    $('#create button').click(EtherKeeper.create_doc);


    $(document).on('click', '.logout', function() {
        $.post('/logout', function(json) {
            if (json.success) {
                alertify.success('Logged out.');
                $('#navbar_user').html(json.navbar);
                home.html('');
                body.attr('class','');
            }
        }, 'json');
    }).on('change', 'thead .cb input', function() {
        $(this).parents('thead').siblings().find('.cb input').prop('checked', $(this).prop('checked'));
    });

    var routing = Davis(function () {
        this.get('/', EtherKeeper.index);
        this.get('/search', EtherKeeper.index);
        this.get('/search/:search', function(req) {

        });
        this.get('/home', function() {
            EtherKeeper.page('home');
        });
        this.get('/etherpad/:pad', function (req) {
            EtherKeeper.get_session(req.params['pad'])
        });
      
    });

    routing.start();

    $.ajaxSetup({
        crossDomain: false, 
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });

    EtherKeeper.set_route(window.location.pathname)
    
    
})();