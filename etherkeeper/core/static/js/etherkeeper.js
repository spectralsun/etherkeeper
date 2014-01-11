;var ek = (function() {
    var EtherKeeper = {
        setView: function(url) {
            search.addClass('top');
            iframe.attr('src', url);
            viewer.show();
        }
    }
    var search = $('#search');
    $('button', search).click(function() {
        search.addClass('top');
    });
    var viewer = $('#viewer'),
        iframe = $('iframe', viewer);

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
            }
        },'json').fail(function() {
            alertify.error('Failed to log in successfuly')
        });
    });

    $('#create button').click(function () {
        $.post('/etherpad/create', function (json) {
            if (json.success) {
                EtherKeeper.setView(json.pad)
            }
        }, 'json');
    });

    $(document).on('click', '.logout', function() {
        $.post('/logout', function(json) {
            if (json.success) {
                alertify.success('Logged out.');
                $('#navbar_user').html(json.navbar);
            }
        }, 'json')
    });

   
    $.ajaxSetup({
        crossDomain: false, 
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });


})()