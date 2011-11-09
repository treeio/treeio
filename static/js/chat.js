$.fx.speeds._default = 500;
$(function() {

    $("#open-chat").click(function() {
      var chatframe = $('#chat-frame');
      if (chatframe.css('display') == 'none') {
        $("#chat-frame").fadeIn(300);
        $('#chat-icon').attr('src', "/static/icons/chat.gif");
      } else {
        $('#chat-frame').fadeOut(300);
      }
      return false;
    });
    $('#chat-close').click(function() {
      $('#chat-frame').fadeOut(300);
    })
});

var chat = {
    /* json object to string */
    'stringify': function(obj) {
        var t = typeof (obj);
        if (t != "object" || obj === null) {
            // simple data type
            if (t == "string") obj = '"' + obj + '"';
            return String(obj);
        }
        else {
            // recurse array or object
            var n, v, json = [], arr = (obj && obj.constructor == Array);
            for (n in obj) {
                v = obj[n];
                t = typeof(v);
                if (t == "string") v = '"' + v + '"';
                else if (t == "object" && v !== null) v = JSON.stringify(v);
                json.push((arr ? "" : '"' + n + '":') + String(v));
            }
            return (arr ? "[" : "{") + String(json) + (arr ? "]" : "}");
        }
    },

    'linsearch': function(v, t) {
        k = false;
        for (var i = 0; i <= v.length-1; i++)
            if (v[i] == t) {
                k = true;
                break
            }
        return k
    },

    // checking new userslist, if userslist is updated then return False, if not updated then return True
    'check_userslist': function(old_userslist, new_userlist) {
        k = true;

        for (var i = 0; i <= new_userlist.length -1; i++) {
            if (chat.linsearch(old_userslist, new_userlist[i]) == false) {
                k = false;
                break
            }
        }
        for (var i = 0; i <= old_userslist.length -1; i++) {
            if (chat.linsearch(new_userlist, old_userslist[i]) == false) {
                k = false;
                break
            }
        }
        return k
    },

    // checking - if owner conference is closed him then chat.on_close_conference
    'check_conferenceslist': function(old_conferenceslist, new_conferenceslist) {

        for (var i = 0; i <= new_conferenceslist.length -1; i++) {
            if (chat.linsearch(old_conferenceslist, new_conferenceslist[i]) == false) {
                chat.ui.on_close_conference(new_conferenceslist[i]);
            }
        }
    },

    'parse_json_conference': function(json){
        chat.events.on_conferences_list(json.conferences);
        chat.events.on_users_list(json.users);
        chat.events.on_messages(json.new_data);
        if (json.notifications) {
          json.notifications.length = json.notifications.length || []
          if (json.notifications.length > 0){
              treeio.process_notifications(json.notifications);
          }          
        }
    },

    'get_location': function(){
        if (window.location.hash == ""){
            return "#";
        } else {
            return ""+window.location.hash;
        }
    },

    'sendJSON': function(json) {
        json["location"] = chat.get_location();
        data = chat.stringify(json);
        $.ajax({
            type: "POST",
            url: chat.option.url,
            typedata: "json",
            data: {"json":data},
            timeout: chat.option.timeout,
            success: function(data) {
                chat.parse_json_conference(data)
            }
        });
    },

    'connect' : function() {
        chat.sendJSON({"cmd":"Connect"});
        chat.events.on_connect();
    },

    'disconnect': function(){
        sendJSON({"cmd":"Disconnect"});
        chat.events.on_disconnect();
    },

    'send': function(id_conference, text) {
        json = {
            "cmd":"Message",
            "data":{
                "id":id_conference,
                "text":text
            }
        };
        chat.sendJSON(json);
    },

    'exit_from_conference': function(id_conference) {
        json = {
            "cmd":"Exit",
            "data":{
                "id":id_conference
            }
        };
        chat.sendJSON(json);
    },

    'get_new_messages': function() {
        json = {
            "cmd":"Get",
            "location": chat.get_location()
        };

        data = chat.stringify(json);
        $.ajax({
            type: "POST",
            url: chat.option.url,
            typedata: "json",
            data: {"json":data},
            timeout: chat.option.timeout,
            success: function(data) {
                chat.parse_json_conference(data)
            },
            complete: function() { //called when the request finishes
                setTimeout(chat.get_new_messages, chat.option.interval);
            }
        });
    },

    'delete_conference': function(id_conference) {
        json = {
            "cmd":"Delete",
            "data":{
                "id":id_conference
            }
        };
        chat.sendJSON(json);
    },

    'remove_users_in_conference': function(id_conference, users) {
        json = {
            "cmd":"Remove",
            "data":{
                "id": id_conference,
                "users":users
            }
        };
        chat.sendJSON(json);
    },

    'add_users_in_conference': function(id_conference, users) {
        json = {
            "cmd":"Add",
            "data":{
                "id":id_conference,
                "users": users
            }
        };
        chat.sendJSON(json);
    },

    'create_conference': function(title, users) {
        json = {
            "cmd":"Create",
            "data":{
                "title": title,
                "users": users
            }
        };
        chat.sendJSON(json);
    }
};

chat.events = {
    'on_connect': function() {
        chat.get_new_messages();
    },

    'on_disconnect': function() {
    },

    'on_messages': function(messages) {
    },

    'on_users_list': function(users) {
    },

    'on_conferences_list': function(conferences) {
    }
};

chat.option = {
    'interval': 25000,
    'url': "/chat",
    'timeout': 60000
};

chat.ui = {
    /* add nick in input */
    'add_nick_in_input': function(nick) {
        $("#chat-input-msg").val(($("#chat-input-msg").val() + nick + ": "));
        $("#chat-input-msg").focus();
    },

    /* return id_conference in active_tab */
    'get_id_active_conference': function() {
        activeTab = $("#chat-tabs").tabs("option", "selected");
        id_conference = $($(".ui-tabs-panel").get()[activeTab]).attr("id");
        return '' + id_conference;
    },

    'send_msg': function() {
        chat.send(chat.ui.get_id_active_conference(), $("#chat-input-msg").val());
        $("#chat-input-msg").val('');
    },
    /// return JSON user_list
    'get_json_userlist': function() {
        data = {};
        data["results"]=[];
        $.each($('.chat-users p'), function() {
            if ($(this).text() != '+') {
                data["results"].push({
                    "id": $(this).attr('user'),
                    "name": $(this).text()
                })
            }
        });
        return data
    },

    'on_close_conference': function(id) { // if owner conference is closed him
        $('li a[href=#'+id+']').prev('img').attr('src', '/static/icons/forest.png');
        delete chat.conferences_dic[id];
    }
};

chat.conferences_dic = {};
chat.userslist = {"results":[], 'users':[]};

chat.events.on_users_list = function(users) {

    users = users || [];

    function get_list_users() { // json userslist to list
        list = [];
        if (users) {
            for (var itr = 0; itr < users.length; itr++) {
                list.push(users[itr].name);
            };
        }
        return list;
    };
    users_list = get_list_users();

    $('#chat-title').text('Chat (' + users.length +')'); // displays the number of online users
    if (users.length > 0) {
        if (chat.check_userslist(chat.userslist.users, users_list) == false) {

            /* Update user list BEGIN*/
            $('.chat-users').html('');
            for (var i = 0; i < users.length; i++) {
                $('<div/>')
                .append($('<p/>', {
                    text: users[i]['profile'],
                    user: users[i]['name']
                    }).bind('dblclick', function(){chat.create_conference($(this).text().split(' ',1),[$(this).attr('user')])}))
                .append($('<span/>').addClass('chat-users-actions')
                  .append($('<a/>', {
                      text: '+',
                      user: users[i]['name']
                      }).addClass('chat-invite-user').bind('click', function(){chat.add_users_in_conference(chat.ui.get_id_active_conference(),[$(this).attr('user')]); $('a.chat-invite-user').hide(); $('div.chat-fb-div').hide(); }))
                  .append(' <a href="' + users[i]['location'] + '">#</a>'))
                .append($('<br/>')).appendTo('.chat-users');
            }
            if (users.length == 0) {
                $('.chat-users').html('<p>No users online</p>');
            }
            /* Update user list END*/

            /* Update combobox users BEGIN */
            chat.userslist.results = chat.ui.get_json_userlist()["results"];
            $('.chat-fb').html('');
            $('.chat-fb').flexbox(chat.ui.get_json_userlist(), {
                width:100,
                maxVisibleRows: 10,
                onSelect: function() {
                    chat.add_users_in_conference(chat.ui.get_id_active_conference(), [$(this).attr('hiddenvalue')]);
                }
            });
            /* Update combobox users END */
        } else {
            for (var i = 0; i < users.length; i++) {
                $("a[user='"+users[i]['name']+"'] + a").attr('href',users[i]['location'])
            }
        }
    } else {
        $('.chat-users').html('');
        $('.chat-users').append($('<p/>', {
            text: 'No users online'
        }));
    }
    chat.userslist.users = users_list;
};

chat.events.on_conferences_list = function(conferences) {

    conferences = conferences || [];

    my_list_conferences = [];
    list_conferences = get_list_conferences(conferences);
    for (var key in chat.conferences_dic) {
        my_list_conferences.push(key)
    }
    chat.check_conferenceslist(list_conferences, my_list_conferences); // check - if owner conference is closed him then chat.on_close_conference

    function get_list_users(list_json) { // json userslist to list
        list = [];
        list_json = list_json || [];
        if (list_json.length>0){
            for (var itr = 0; itr < list_json.length; itr++) {
                list.push(list_json[itr].username);
            }
        }
        return list;
    }

    function get_list_conferences(list_json) { // json userslist to list
        list = [];
        list_json = list_json || [];
        if (list_json.length>0){
            for (var itr = 0; itr < list_json.length; itr++) {
                list.push(list_json[itr].id);
            }
        }
        return list;
    }

    function update_users() {
        $('<p/>').text('Between you,').appendTo('#' + conference.id + ' .chat-with');

        for (var u = 0; u < conference.users.length; u++) {
            user = conference.users[u];
            $('<p/>').text(user.profile.split(' ',1)[0]).appendTo('#' + conference.id + ' .chat-with');
        }

        $('<p/>').append($('<a/>',{
            text:'Invite more people'
        }).attr('class','chat-invite').bind('click',function(){
            $('#'+chat.ui.get_id_active_conference()+' .chat-fb-div').toggle();
            $('a.chat-invite-user').toggle();
            $('#'+chat.ui.get_id_active_conference()+' .chat-fb #_input').focus();
        })).appendTo('#' + conference.id + ' .chat-with');

        if (conference.users.length == 2){
            $("a[href='#"+conference.id+"']").text(conference.users[0].profile.split(' ',1)[0]+' and '+conference.users[1].profile.split(' ',1)[0]);
        }

        if (conference.users.length > 2){
            $("a[href='#"+conference.id+"']").text(conference.users[0].profile.split(' ',1)[0]+', '+conference.users[1].profile.split(' ',1)[0]+', ...');
        }
    }

    if (conferences.length > 0) {
        for (var i = 0; i < conferences.length; i++) {
            conference = conferences[i];
            id = conference.id;
            list_users = get_list_users(conference.users);
            if (chat.conferences_dic[id]) {
                if (chat.check_userslist(chat.conferences_dic[conference.id]['users'], list_users) == false) { // if in userslist new data, then update
                    $('#' + conference.id + ' .chat-with').html('');
                    update_users();
                }
                chat.conferences_dic[conference.id]['users'] = get_list_users(conference.users);
            } else {

                $("#chat-tabs").tabs("add", '#' + conference.id, conference.title);
                chat.conferences_dic[id] = {};
                chat.conferences_dic[id].active = true;
                chat.conferences_dic[id].users = [];

                $('<div/>').attr('class','chat-with small').appendTo('#' + conference.id);

                $('<div/>').attr('class','chat-fb-div')
                .append($('<div/>').attr('class','chat-fb').flexbox(chat.userslist, {
                    width:100,
                    maxVisibleRows: 10,
                    onSelect: function() {
                        chat.add_users_in_conference(chat.ui.get_id_active_conference(), [$(this).attr('hiddenvalue')]);
                    }
                }))
                .append($('<div/>').attr('class','ui-icon ui-icon-close vertical').bind('click', function(){$(this).parent().hide(); $('a.chat-invite-user').hide();}))
                .appendTo('#' + conference.id);

                $('<div/>').attr('class','chat-body').appendTo('#' + conference.id);

                update_users();

                chat.conferences_dic[conference.id]['users'] = get_list_users(conference.users);
            }
        }
    }
};



chat.events.on_messages = function(data) {
    data = data || []
    if (data.length > 0) {
        for (var itr = 0; itr < data.length; itr++) {
            new_msg = data[itr];
            for (var key in new_msg) {
                msg = new_msg[key].messages;
                for (var i = 0; i < msg.length; i++) {
                    text = msg[i].text;
                    date = msg[i].date;
                    time = msg[i].time;
                    user = msg[i].user;
                    profile = msg[i].profile;
                    $('<div/>').attr('class','message')
                    .append($('<div/>', {
                        text: '[' + time + ']'
                    }).attr('class','time'))
                    .append($('<div/>', {
                        user: user,
                        text: '<' + profile + '> '
                    }).attr('class','nick').bind('click', function(){chat.ui.add_nick_in_input($(this).text().slice(1, -2))}))
                    .append($('<div/>', {
                        text: ' ' + text
                    }).attr('class','text'))
                    .appendTo('#' + key + ' .chat-body');
                }
                if (msg.length > 0) {
                    $('li a[href=#'+key+']').prev('img').fadeIn(100).fadeOut(100).fadeIn(100).fadeOut(100).fadeIn(100).fadeOut(100).fadeIn(100);
                }
                $('#' + key + " .chat-body").animate({ scrollTop: $('#' + key + " .chat-body").attr("scrollHeight") }, 1000);
            }
        }
        var chatframe = $('#chat-frame');
        if (chatframe.css('display') == 'none'){
            $('#chat-icon').attr('src', "/static/icons/chat-active.gif").fadeOut(100).fadeIn(100).fadeOut(100).fadeIn(100).fadeOut(100).fadeIn(100);
        }
    }
};

$(function() {
    $("#chat-tabs").tabs({
        tabTemplate: "<li><img src='/static/icons/forest-active.png' class='margin-bottom' style='float: left;'><a href='#{href}'>#{label}</a><span class='ui-icon ui-icon-close'>Remove Tab</span></li>"
    });
    $("#chat-tabs li span.ui-icon-close").live("click", function() {
        delete chat.conferences_dic[chat.ui.get_id_active_conference()];
        chat.exit_from_conference(chat.ui.get_id_active_conference());
        var index = $("li", $('#chat-tabs')).index($(this).parent());
        $('#chat-tabs').tabs("remove", index);
    });

    $("#chat-input-msg").keypress(function(e) {
        if (e.which == '13') {
            chat.ui.send_msg();
            return false;
        }
    });

    $("#chat-btn-send").click(chat.ui.send_msg);

    chat.connect();

    $('.chat-fb').flexbox(chat.ui.get_json_userlist(), {
        width:100,
        maxVisibleRows: 10,
        onSelect: function(){
            chat.add_users_in_conference(chat.ui.get_id_active_conference(), [$(this).attr('hiddenvalue')]);
        }
    });

});

$(function() {

    var $tab_title_input = $("#tab_title");

    var $dialog = $("#chat-dialog").dialog({
        autoOpen: false,
        modal: true,
        buttons: {
            Invite: function() {
                users = [];
                $.each($('.chat-dialog-users input:checked'), function(){
                    users.push($(this).attr('name'));
                });
                if (users.length > 0){
                    chat.add_users_in_conference(chat.ui.get_id_active_conference(), users);
                }

                $(this).dialog("close");
            },
            Cancel: function() {
                $(this).dialog("close");
            }
        },
        open: function() {
            $('.chat-dialog-users').html('');
            $.each($('.chat-users p'), function() {
                $('<input>', {
                    name: $(this).attr('user'),
                    type: 'CHECKBOX'
                }).appendTo($('.chat-dialog-users'));
                $('.chat-dialog-users')
                        .append($(this).text())
                        .append($('<br/>'));
            });
            $tab_title_input.focus();
        },
        close: function() {
            $form[ 0 ].reset();
        }
    });

    var $form = $("form", $dialog).submit(function() {
        $dialog.dialog("close");
        return false;
    });
});
