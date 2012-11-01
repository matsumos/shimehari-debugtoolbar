(function($) {
    $.cookie = function(name, value, options) { if (typeof value != 'undefined') { options = options || {}; if (value === null) { value = ''; options.expires = -1; } var expires = ''; if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) { var date; if (typeof options.expires == 'number') { date = new Date(); date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000)); } else { date = options.expires; } expires = '; expires=' + date.toUTCString(); } var path = options.path ? '; path=' + (options.path) : ''; var domain = options.domain ? '; domain=' + (options.domain) : ''; var secure = options.secure ? '; secure' : ''; document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join(''); } else { var cookieValue = null; if (document.cookie && document.cookie != '') { var cookies = document.cookie.split(';'); for (var i = 0; i < cookies.length; i++) { var cookie = $.trim(cookies[i]); if (cookie.substring(0, name.length + 1) == (name + '=')) { cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); break; } } } return cookieValue; } };
    $('head').append('<link rel="stylesheet" href="'+DEBUG_TOOLBAR_STATIC_PATH+'css/toolbar.css?'+ Math.random() +'" type="text/css" />');
    var COOKIE_NAME = 'sdt';
    var COOKIE_NAME_ACTIVE = COOKIE_NAME +'_active';
    var sdt = {
        init: function() {
            $('#sDebug').show();
            var current = null;
            $('#sDebugPanelList li a').click(function() {
                if (!this.className) {
                    return false;
                }
                current = $('#sDebug #' + this.className + '-content');
                if (current.is(':visible')) {
                    $(document).trigger('close.sDebug');
                    $(this).parent().removeClass('active');
                } else {
                    $('.panelContent').hide(); // Hide any that are already open
                    current.show();
                    $('#debugToolbar li').removeClass('active');
                    $(this).parent().addClass('active');
                }
                return false;
            });
            $('#sDebugPanelList li .switch').click(function() {
                var $panel = $(this).parent();
                var $this = $(this);
                var dom_id = $panel.attr('id');

                // Turn cookie content into an array of active panels
                var active_str = $.cookie(COOKIE_NAME_ACTIVE);
                var active = (active_str) ? active_str.split(';') : [];
                active = $.grep(active, function(n,i) { return n != dom_id; });

                if ($this.hasClass('active')) {
                    $this.removeClass('active');
                    $this.addClass('inactive');
                }
                else {
                    active.push(dom_id);
                    $this.removeClass('inactive');
                    $this.addClass('active');
                }

                if (active.length > 0) {
                    $.cookie(COOKIE_NAME_ACTIVE, active.join(';'), {
                        path: '/', expires: 10
                    });
                }
                else {
                    $.cookie(COOKIE_NAME_ACTIVE, null, {
                        path: '/', expires: -1
                    });
                }
            });
            $('#sDebug a.sDebugClose').click(function() {
                $(document).trigger('close.sDebug');
                $('#debugToolbar li').removeClass('active');
                return false;
            });
            $('#sDebug a.remoteCall').click(function() {
                post_param = {};
                if($('meta[name=_cstfToken]').get(0)){
                    post_param = {_csrfToken: $('meta[name=_cstfToken]').attr('content')};
                }
                else if($('meta[name=csrf-token]').get(0)){
                    post_param = {_csrfToken: $('meta[name=csrf-token]').attr('content')};
                }
                $('#sDebugWindow').load(this.href, post_param, function() {
                    $('#sDebugWindow a.sDebugBack').click(function() {
                        $(this).parent().parent().hide();
                        return false;
                    });
                });
                $('#sDebugWindow').show();
                return false;
            });
            $('#sDebugTemplatePanel a.sTemplateShowContext').click(function() {
                sdt.toggle_arrow($(this).children('.toggleArrow'));
                sdt.toggle_content($(this).parent().next());
                return false;
            });
            $('#sDebugSQLPanel a.flSQLShowStacktrace').click(function() {
                sdt.toggle_content($('.sSQLHideStacktraceDiv', $(this).parents('tr')));
                return false;
            });
            $('#sHideToolBarButton').click(function() {
                sdt.hide_toolbar(true);
                return false;
            });
            $('#sShowToolBarButton').click(function() {
                sdt.show_toolbar();
                return false;
            });
            $(document).bind('close.sDebug', function() {
                // If a sub-panel is open, close that
                if ($('#sDebugWindow').is(':visible')) {
                    $('#sDebugWindow').hide();
                    return;
                }
                // If a panel is open, close that
                if ($('.panelContent').is(':visible')) {
                    $('.panelContent').hide();
                    return;
                }
                // Otherwise, just minimize the toolbar
                if ($('#debugToolbar').is(':visible')) {
                    sdt.hide_toolbar(true);
                    return;
                }
            });
            if ($.cookie(COOKIE_NAME)) {
                sdt.hide_toolbar(false);
            } else {
                sdt.show_toolbar(false);
            }
            $('#sDebug table.tablesorter')
                .tablesorter()
                .bind('sortStart', function() {
                    $(this).find('tbody tr')
                        .removeClass('sDebugEven')
                        .removeClass('sDebugOdd');
                })
                .bind('sortEnd', function() {
                    $(this).find('tbody tr').each(function(idx, elem) {
                        var even = idx % 2 == 0;
                        $(elem)
                            .toggleClass('sDebugEven', even)
                            .toggleClass('sDebugOdd', !even);
                    });
                });
        },
        toggle_content: function(elem) {
            if (elem.is(':visible')) {
                elem.hide();
            } else {
                elem.show();
            }
        },
        close: function() {
            $(document).trigger('close.sDebug');
            return false;
        },
        hide_toolbar: function(setCookie) {
            // close any sub panels
            $('#sDebugWindow').hide();
            // close all panels
            $('.panelContent').hide();
            $('#debugToolbar li').removeClass('active');
            // finally close toolbar
            $('#debugToolbar').hide('fast');
            $('#debugToolbarHandle').show();
            // Unbind keydown
            $(document).unbind('keydown.sDebug');
            if (setCookie) {
                $.cookie(COOKIE_NAME, 'hide', {
                    path: '/',
                    expires: 10
                });
            }
        },
        show_toolbar: function(animate) {
            // Set up keybindings
            $(document).bind('keydown.sDebug', function(e) {
                if (e.keyCode == 27) {
                    sdt.close();
                }
            });
            $('#debugToolbarHandle').hide();
            if (animate) {
                $('#debugToolbar').show('fast');
            } else {
                $('#debugToolbar').show();
            }
            $.cookie(COOKIE_NAME, null, {
                path: '/',
                expires: -1
            });
        },
        toggle_arrow: function(elem) {
            var uarr = String.fromCharCode(0x25b6);
            var darr = String.fromCharCode(0x25bc);
            elem.html(elem.html() == uarr ? darr : uarr);
        },
        load_href: function(href) {
          $.get(href, function(data, status, xhr) {
            document.open();
            document.write(xhr.responseText);
            document.close();
          });
          return false;
        }
    };
    $(document).ready(function() {
        sdt.init();
    });
    window.sdt = sdt;

})(jQuery.noConflict(true));
