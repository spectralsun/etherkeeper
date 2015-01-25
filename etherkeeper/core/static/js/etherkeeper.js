(function() {
    var EtherKeeper = {

        // creates a new document 
        create_doc: function() {
            $.post('/etherpad/create', function (json) {
                if (json.success) {
                    EtherKeeper.set_route('/etherpad/' + json.id, 'state').open_doc(json);
                    EtherKeeper.set_page('viewer')
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
            this.set_page('viewer');
            var onfail = EtherKeeper.onfail('open document', function() {
                loading.hide();
                EtherKeeper.set_route('/home');
            });
            $.post('/etherpad/open/', { id: pad }, function(json) {
                if (json.success) {
                    EtherKeeper.open_doc(json)
                } else {
                    onfail();
                }
            },'json').fail(onfail);
        },

        // gets a pad's title
        get_title: function() {
            var onfail = EtherKeeper.onfail('get title');
            $.post('/etherpad/title', { id: this.current_pad }, function(json) {
                if (json.success) {
                    $('.title-holder').html(json.title)
                } else {
                    onfail();
                }
            },'json').fail(onfail);  
        },

        get_sharing: function() {
            var onfail = EtherKeeper.onfail('get sharing');
            $.post('/etherpad/sharing', { id: this.current_pad }, function(json) {
                if (json.success) {
                    $('.shares tbody').html(json.sharing);
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
        set_page: function(page) {
            this.index();
            body.addClass(page + '-open');
            if (page !== 'viewer') {
                iframe.hide();
                iframe.removeAttr('src');
            }
            return this;
        },

        set_treenav: function(page) {
            $('a[href="/' + page + '"]').parent().addClass('active').siblings().removeClass('active');
            return this;
        },
        
        // sends a message to the etherpad instance
        // TODO: replace the hostname with var
        send_message: function(data) {
            iframe_window.postMessage(JSON.stringify(data), etherpad_url);
        },

        // sets the current location to the path and fire a pushState event
        set_route: function(path, method) {
            if (method === undefined) 
                method = 'get'
            Davis.location.assign(new Davis.Request(path, {
                method: method,
                title: ''
            }));
            return this;
        },

        // sets a documents title
        set_title: function(title) {
            var onfail = EtherKeeper.onfail('change document title');
            $.post('/etherpad/set_title', { 
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

        // generates function for string error and callback
        onfail: function(error, cb) {
            return function(cb2) { 
                alertify.error('Failed to ' + error + '.'); 
                if (cb) cb() 
                if (cb2) cb2() 
            }
        },


        // on window message event received
        onmessage: function(e) {
            var event = e.originalEvent;
            if (event.origin !== 'http://localhost:9001')
                return;
            var data = JSON.parse(event.data);
    
            if (data.type === 'init') {
                EtherKeeper.send_message({ type: 'init' });
            } else if (data.type === 'title_update') {
                EtherKeeper.get_title()
            }
        },
       
        // on window resize
        onresize: function() {
            viewer.height($window.height() - 125);
        }, 

        // accept or deny an invite, effectively removing it
        respond_to_invite: function(accept, row) {
            var onfail = EtherKeeper.onfail(accept ? 'accept invite' : 'deny invite');
            $.post('/etherpad/respond', {
                accept: accept,
                id: row.data('id')
            }, function(json) {
                if (json.success) {
                    alertify.success('Successfully ' + (accept ? 'accepted' : 'denied') + ' invite.');
                    row.fadeOut();
                } else
                    onfail();
            }, 'json').fail(onfail);
        },

        // davis.js routes
        routes: function() {
            this.get('/', EtherKeeper.index);
            this.get('/search', EtherKeeper.index);
            this.get('/search/:search', function(req) {

            });
            this.get('/home', function() {
                EtherKeeper.set_page('home').set_treenav('home');
            });
            this.get('/invites', function() {
                EtherKeeper.set_page('invites').set_treenav('invites');
            });
            this.get('/etherpad/:pad', function (req) {
                EtherKeeper.get_session(req.params['pad'])
            });
        }
    }
    var body = $('body'),
        search = $('#search'),
        viewer = $('#viewer'),
        viewer_bar = $('#viewer_bar'),
        iframe = $('iframe', viewer),
        iframe_window = iframe[0].contentWindow,
        etherpad_url = iframe.data('etherpad-url'),
        home = $('#home'),
        share_modal = $('#share_modal'),
        loading = $('#loading'),
        $window = $(window);
    iframe.removeData('etherpad-url');
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
                EtherKeeper.set_page('home');
            }
        },'json').fail(function() {
            alertify.error('Failed to log in successfuly')
        });
    });

    $('#create button').click(EtherKeeper.create_doc);

    share_modal.on('show.bs.modal', function(e) {
        EtherKeeper.get_sharing();
    });

    $('#add_user', share_modal).tagsinput()

    $('#add_user').tagsinput('input').typeahead({
        remote: '/search/users?q=%QUERY'
    }).bind('typeahead:selected', $.proxy(function (obj, datum) {
        this.tagsinput('add', datum.value);
        this.tagsinput('input').typeahead('setQuery', '');
    }, $('#add_user')))

    $('#add_user').tagsinput('input').keyup(function(e) {
        if(e.keyCode == 13)
            $(this).typeahead('setQuery','')
    });

    $('#add_member button').click(function() {
        $.post('/etherpad/share', {
            id: EtherKeeper.current_pad,
            access: $('#share_role select').val(),
            members: $('#add_user').val()
        }, function(json) {
            if (json.success) {
                alertify.success('Invited users successfully.');
            }
        }, 'json');
    });

    $('#viewer_bar .pull-right a').tooltip();

    $('#inites tr button').tooltip();

    $('.ep-proxy').click(function() {
        EtherKeeper.send_message({ type: $(this).attr('id') });
    });

    $('#tag_dropdown').on('click', '.dropdown-menu', function(e) {
        e.preventDefault();
    })

    $('#tags').tagsinput();

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
    }).on('click', '#invites .btn-success', function() {
        EtherKeeper.respond_to_invite(true, $(this).parents('tr'));
    }).on('click', '#invites .btn-danger', function() {
        var row = $(this).parents('tr');
        alertify.confirm('Are you sure you wish to deny this invite?', function(resp) {
            if (resp) {
                EtherKeeper.respond_to_invite(false, row);
            }
        });
    });

    var routing = Davis(EtherKeeper.routes);

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
    
    this.ek = EtherKeeper;
})();