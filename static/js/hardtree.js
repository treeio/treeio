/* Tree.io JS
 * Copyright 2010-2011 Giteso Limited. All rights reserved. 
 */

var hardtree = {
  'put_mce': function(doc) {
      var obj;
      if (doc) {
        obj = $('textarea', doc);
      } else {
        obj = $('textarea');
      }
      obj.each(function() {
        if (!$(this).hasClass('no-editor')) {
            $(this).attr('id', doc.attr('id') + "-" + $(this).attr('id'));
            if ($(this).hasClass('full-editor')) {
                $(this).tinymce({
                  script_url : '/static/js/tinymce/jscripts/tiny_mce/tiny_mce.js',
                  theme : "advanced",
                  skin : "cirkuit",
                  relative_urls: false,
                  plugins : "safari,table,advhr,inlinepopups,insertdatetime,preview,searchreplace,contextmenu,paste,fullscreen,nonbreaking,visualchars,xhtmlxtras",
                  theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,fontselect,fontsizeselect,|,cut,copy,paste,pastetext,pasteword,|,search,replace",
                  theme_advanced_buttons2 : "bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,image,cleanup,code,|,insertdate,inserttime,preview,|,forecolor,backcolor,|,cite,abbr,acronym,del,ins",
                  theme_advanced_buttons3 : "tablecontrols,|,hr,removeformat,|,sub,sup,|,visualchars,nonbreaking,charmap,advhr,|,fullscreen",
                    theme_advanced_disable : 'help,styleselect,anchor,newdocument',
                  theme_advanced_toolbar_location : "top",
                  theme_advanced_toolbar_align : "left",
                  theme_advanced_statusbar_location : "bottom",
                  theme_advanced_resizing : true,
                    theme_advanced_resize_horizontal : true, 
                    theme_advanced_resizing_use_cookie : true,
                    theme_advanced_path : false, 
                      width: "70%"
                });
            } else {
                $(this).tinymce({
                  script_url : '/static/js/tinymce/jscripts/tiny_mce/tiny_mce.js',
                  theme : 'advanced',
                    skin : "cirkuit",
                    relative_urls: false,
                    plugins : "safari,table,advhr,inlinepopups,insertdatetime,preview,searchreplace,contextmenu,paste,fullscreen,nonbreaking,visualchars,xhtmlxtras",
                  theme_advanced_statusbar_location : 'bottom',
                  theme_advanced_toolbar_location : 'top',
                  theme_advanced_toolbar_align : 'left',
                  theme_advanced_path : false, 
                  theme_advanced_resizing : true, 
                  theme_advanced_resize_horizontal : true, 
                  theme_advanced_resizing_use_cookie : true,
                  theme_advanced_disable : 'justifyleft,justifycenter,justifyright,justifyfull,outdent,indent,image,help,hr,removeformat,formatselect,fontselect,fontsizeselect,styleselect,sub,sup,forecolor,backcolor,forecolorpicker,backcolorpicker,charmap,visualaid,anchor,newdocument,blockquote',
                  theme_advanced_buttons1 : 'bold,italic,underline,strikethrough,|,undo,redo,|,cut,copy,paste,link,unlink,cleanup,|,bullist,numlist,|,code',
                  theme_advanced_buttons2 : '',
                  theme_advanced_buttons3 : '',
                    width: "70%"
                });
            }
        }
    });
  },
    
    'remove_mce': function(doc) {
        var obj;
    if (doc) {
      obj = $('textarea', doc);
    } else {
      obj = $('textarea');
    }
        obj.each(function() {
            tinyMCE.execCommand('mceRemoveControl',false,$(this).attr('id'));
        })
    },
    
    'do_ajax': function(){
        // Process request on hashchange
        var url = window.location.hash.replace(/#/gi, "");
        if (!url) {
          url = window.location.pathname;
        }
        var menu = $(".menu-item a[href=\"\#" + url + "\"]");
        if (menu.length) {
            if (!menu.hasClass('active')) {
                block = $('#module-' + menu.attr('id').substring(5));
                if (block.length) {
                    $('.module-block').each(function() {
                      if ($(this).attr('id') != block.attr('id')) {
                        $(this).css('display', 'none');
                        $(this).data('active', false);
                      } else {
                        block.css('display', 'block');
                        block.data('active', true);
                      }
                    });
                    document.title = block.data('title');
                    $(".menu-item a").each(function(){
                        $(this).removeClass('active')
                    });
                    menu.addClass('active')
                    url = '';
                }
            }
        }
        if (url) {
            url = hardtree.prepare_url(url);
            $("#loading-status").css('display', 'block');
            $("#loading-status-text").html('Loading...');
            $.ajax({
                'url': url,
                'dataType': 'json',
                'success': hardtree.process_ajax,
                'complete': hardtree.process_html,
                'error': hardtree.show_error
            })
        }
    },
    
    'show_error': function() {
        $("#loading-status-text").html('Something went wrong...');
    },
    
    'process_userblock': function(data) {
        if (data.response.messages) {
            $('#userblock-messages').each(function() {
                $(this).html(data.response.messages);
            });
        }
    },

   'process_ajax': function(data, status, xhr) {
        if (!data) {
          return;
        }
        if (data.popup) {
            hardtree.process_popup_data(data);
            return;
        }
        if (data.redirect) {
            if (window.location.hash == "#" + data.redirect) {
                hardtree.do_ajax();
            } else {
                window.location.hash = data.redirect;
            }
            return;
        } else if (data.redirect_out) {
            window.location = data.redirect_out;
            return;
        }
        if (data.response.url) {
            var urljs = data.response.url.replace('.ajax', '');
            var urlcurr = window.location.hash.replace('#', '');
            if (urljs != urlcurr) {
                if (urljs.indexOf(urlcurr) == -1 && urlcurr.indexOf(urljs) == -1) {
                  $("#loading-status").css('display', 'none');
                  return;
                }
            }
        }
        document.title = data.response.content.title;
        var content = data.response.content.module_content;
        var module = data.response.modules.active;
          var sidebardisplay = 'none';
        if ($("#module-" + module).length == 0) {
            $("#content").append("<div class=\"module-block\" id=\"module-" + module + "\"></div>");
        } else {
            var sidebar = $("td.module-sidebar-right", $("#module-" + module));
            if (sidebar) {
                sidebardisplay = sidebar.css('display');
            }
          }
        var block = $("#module-" + module);
        $('.module-block').each(function() {
          if ($(this).attr('id') != block.attr('id')) {
            $(this).css('display', 'none');
            $(this).data('active', false);
          } else {
            block.css('display', 'block');
            block.data('active', true);
          }
          });
          hardtree.remove_mce($("#module-" + module + " form"));
        $("#module-" + module).html(content);
        if ($("#module-" + module + " form").length) {
          hardtree.prepare_forms(block);
          hardtree.prepare_comments(block)
          if ($("#module-" + module + " textarea").length) {
            hardtree.put_mce(block);
          }
        }
          hardtree.prepare_tags(block);
          hardtree.prepare_list_actions(block);
		  hardtree.prepare_content_top(block);
          hardtree.prepare_attachments(block);
          hardtree.prepare_invites(block);
          hardtree.prepare_popups(block);
          hardtree.convert_links(block);
          hardtree.prepare_ajax_links(block);
          hardtree.prepare_slider_sidebar(block, sidebardisplay);
          hardtree.showhidejs(block);
          hardtree.prepare_module_stuff(module);
          hardtree.process_notifications(data.response.notifications);
        $(".menu-item a").each(function(){
            $(this).removeClass('active')
        });
          hardtree.process_userblock(data);
        $("#menu-" + module).addClass('active')
        $(block).data('title', data.response.content.title);
        if ($('#loading-splash').css('display') != 'none') {
        	$('#loading-splash').fadeOut();
        }
        $("#loading-status").css('display', 'none');
  },
  
  'process_notifications': function(msgs) {
      for (var i in msgs) {
          var msg = {'title': ' ',
                     'text': msgs[i].message,
                     'image': '/static/notifications/'+msgs[i].tags+'.png'};
          if (msgs[i].title) {
            msg['title'] = msgs[i].title;
          }
          if (msgs[i].image) {
            msg['image'] = msgs[i].image;
          }
          $.gritter.add(msg);
      }
  },

  'process_html': function(xhr, status) {
      if (status == 'parsererror') {
          window.document.write(xhr.responseText);
      }
  },
    
  'prepare_module_stuff': function(module_name) {
      try
      {
          hardtree.modules[module_name].init();
      }
      catch(err){}
      
  },
  
  'prepare_url': function(url) {
        if ((url.indexOf("!") != -1) || (url.indexOf("?") != -1)) {
            url = url.replace("!", "?");
            if (url.indexOf(".ajax") == -1) {
                url = url.replace("?", ".ajax?");
            }
        }
        if (url.indexOf(".ajax") == -1) {
            url += ".ajax?";
        }
    return url;
  },
  
  'showhidejs': function(doc) {
      if (doc) {
          var showjs = $('div.showjs', doc);
          var hidejs = $('div.hidejs', doc);
      } else {
          var showjs = $('div.showjs');
          var hidejs = $('div.hidejs');
      }
      showjs.each(function() {
        $(this).css('display', 'block');
      })
      hidejs.each(function() {
        $(this).css('display', 'none');
      })
  },
    
  'convert_links': function(doc) {
      if (doc) {
          var links = $('a', doc);
      } else {
          var links = $('a');
      }
      links.each(function() {
          if ($(this).attr('href') && !$(this).hasClass('ajax-link-out') &&  
		   !$(this).hasClass('ajax-link') && !$(this).attr('target') &&
           !($(this).attr('href').substring(0,3) == 'www') &&
           !($(this).attr('href').substring(0,5) == 'http:') &&
           !($(this).attr('href').substring(0,6) == 'https:') &&
           !($(this).attr('href').substring(0,4) == 'ftp:') &&
           !($(this).attr('href').substring(0,7) == 'mailto:') &&
           ($(this).attr('href').indexOf('#') == -1)) {
            $(this).attr("href", ("#" + $(this).attr("href").replace("?", "!")));
              if ($.browser.msie && $.browser.version.substr(0,1)<7) {
                  var prefix = window.location.href.replace(window.location.hash, '');
                  $(this).attr("href", $(this).attr("href").replace(prefix, ""));
              }
          }
      })
  },
  
  'add_data': function(newdata) {
	  var target = $(newdata.target);
	  if (newdata.inner) {
	  	target.html(newdata.content);
	  } else if (newdata.append) {
	  	target.append(newdata.content);
	  } else {
	  	var newelem = $(newdata.content);
	  	target.replaceWith(newelem);
	  	target = newelem;
	  }
	  if ($("form", target).length) {
	      hardtree.prepare_forms(target);
	      hardtree.prepare_comments(target);
	      if ($("textarea", target).length) {
	        hardtree.put_mce(target);
	      }
	  }
      hardtree.prepare_tags(target);
      hardtree.prepare_list_actions(target);
	  hardtree.prepare_content_top(target);
      hardtree.prepare_attachments(target);
      hardtree.prepare_invites(target);
      hardtree.prepare_popups(target);
      hardtree.convert_links(target);
      hardtree.prepare_ajax_links(target);
      hardtree.showhidejs(target);
      $("#loading-status").css('display', 'none');
  },
  
  'prepare_ajax_links': function(doc) {
      if (doc) {
          var links = $('.ajax-link', doc);
      } else {
          var links = $('.ajax-link');
      }
      links.each(function() {
    	  $(this).click(function() {
    		  var target = $(this).parents($(this).attr('target'));
	    	  var targetid = hardtree.utils.generate_id();
	    	  target.attr('id', targetid);
	    	  $(this).attr('target', '#'+targetid);
    		  var callback = eval($(this).attr('callback'));
    		  var cargs = eval('('+$(this).attr('args')+')');
    		  if (cargs) {
    			  var args = $.extend({'target': '#'+targetid}, cargs);
    		  } else {
    			  var args = {'target': '#'+targetid};
    		  }
              $("#loading-status").css('display', 'block');
              $("#loading-status-text").html('Loading...');
    		  callback(Dajax.process, args);
    		  return false;
    	  })
      })
  },
  
  'prepare_slider_sidebar': function(doc, display) {
      if (!doc) {
          var doc = $('.module-block');
      }
      var sliderbtn = $('<div></div>').addClass('sidebar-slider');
      $('td.module-content-inner', doc).prepend(sliderbtn);
      sliderbtn.data('sidebar', $('td.module-sidebar-right', doc));
      sliderbtn.click(function(){
          var sidebar = $(this).data('sidebar');
          if (sidebar) {
              if (sidebar.css('display') == 'none') {
                  sidebar.fadeIn()
                  //$(this).html("&gt;");
              } else {
                  sidebar.fadeOut();
                  //$(this).html("&lt;");
              }
          }
      })
      
      var sidebar = $('td.module-sidebar-right', doc);
      
      // The following adds appropriate icons to the slider button to show
      // what's inside the sidebar
      
      // Add Quick Status icon
      if ($('a.projects-action', sidebar).length != 0 || $('a.services-action', sidebar).length != 0) {
        sliderbtn.append('<img src="/static/icons/sidebar/status.gif"/><br />');
      }      
      // Add Filter icon
      if ($('form.content-filter-form', sidebar).length != 0) {
        sliderbtn.append('<img src="/static/icons/sidebar/filter.gif"/><br />');
      }
      // Add Permissions icon
      if ($('div.permission-links', sidebar).length != 0) {
        sliderbtn.append('<img src="/static/icons/sidebar/permission.gif"/><br />'); 
      }
      // Add Linking icon
      if ($('div.object-links', sidebar).length != 0) {
        sliderbtn.append('<img src="/static/icons/sidebar/link.gif"/><br />'); 
      }
      // Add Subscription icon
      if ($('div.subscription-users', sidebar).length != 0) {
        sliderbtn.append('<img src="/static/icons/sidebar/subscribe.gif"/><br />'); 
      }
      // Add Export icon
      if ($('a.pdf-block-link', sidebar).length != 0) {
        sliderbtn.append('<img src="/static/icons/sidebar/export.gif"/><br />');
      }

      if (display) {
          sidebar.css('display', display);
      } else {
          sidebar.css('display', 'none');
          sliderbtn.css({
                  visibility: 'hidden'
              }) /* if module-sidebar-right is null then sidebar-slider hidden */
      }
  },
  
  'prepare_list_actions': function(doc) {
      $(".content-list-item", doc).each(function() {
          $("span.content-list-item-actions", $(this)).css('visibility', 'hidden');
          $(this).mouseover( function() {
              $("span.content-list-item-actions", $(this)).css('visibility', 'visible');
          }).mouseout( function() {
              $("span.content-list-item-actions", $(this)).css('visibility', 'hidden');
          })
          $("span.content-list-item-actions a", $(this)).addClass("popup-link");
      })
  },
  
  'prepare_content_top': function(doc) {

    var msie6 = $.browser == 'msie' && $.browser.version < 7;
    if (!msie6) {
        var top = $('.content-top', doc).offset().top - 20;
        $(window).scroll(function(event) {
            var y = $(this).scrollTop();
            if (y >= top) {
                $('.content-top').css({
                        position: 'fixed',
                        top: 32,
						opacity: 0.9,
                    });
            } else {
                $('.content-top').css({
                        position: 'relative',
                        top: 0,
						opacity: 1,
                    });
            }
        });
    }
  },
    
  'put_datepicker': function(doc) {
        $('input.datepicker', doc).each(function() {
            var options = {};
            var initial = $(this).attr('initial');
            if (initial) {
              initial = parseInt(initial) * 1000;
              var dinit = new Date(initial);
              options['defaultDate'] = dinit;
            }
            $(this).datepicker(options);
        })
        $('input.datetimepicker', doc).each(function() {
            var options = {stepMinute: 5, hour: 12, minute: 00, firstDay: 1};
            var initial = $(this).attr('initial');
            if (initial) {
              initial = parseInt(initial) * 1000;
              var dinit = new Date(initial);
              options['defaultDate'] = dinit;
              options['hour'] = dinit.getHours();
              options['minute'] = dinit.getMinutes();
              options['second'] = dinit.getSeconds();
            }
            $(this).datetimepicker(options);
        })
  },
    
    'prepare_mass_form': function(doc) {
        $('input[type=checkbox].group-control', doc).each(function() {
          $(this).data('form', $('ul.mass-form', doc));
          $(this).click(function() {
            $('input[type=checkbox].group-'+$(this).attr('name')).attr('checked', $(this).attr('checked'));
            $(this).data('form').fadeTo("fast", 1);
          });
        });
        
        $('ul.mass-form input[type=submit]', doc).remove();
        $('ul.mass-form', doc).each(function(){
          $(this).css('opacity', 0.6);
        });
    
        $('.content-list-item input[type=checkbox], #sales_table, #reports_table', doc).each(function() {
          $(this).data('form', $('ul.mass-form', doc));
          $(this).click(function() {
            $(this).data('form').fadeTo("fast", 1);
          });
        });
    
        $(".mass-form select", doc).each(function() {
          $(this).css('opacity', 0);
          $(this).change(function(ui, event) {
            var massvalue = $('span.wrap-value', $(this).parent());
            var selected = $(this).children('option:selected');
            if (!selected.val() == "") {
              massvalue.text(selected.text());
              if (selected.val() == "delete" || selected.val() == "delete_all") {
                if (confirm('Really delete?\n\n(This cannot be undone)')) {
                  $(this).parent().submit();
                }
              } else {
                $(this).parent().submit();
              }
            }
          });
        });
        $('.mass-form label', doc).each(function(doc){
          $(this).next('select').andSelf().wrapAll('<div class="wrap-class" />');
          $(this).replaceWith('<span class="wrap-label">' + $(this).text() + '&nbsp;<span class="wrap-value"></span></span>');
        });
		$('.mass-form button', doc).each(function(doc){
			$(this).andSelf().wrapAll('<div class="wrap-class" />');
		});
    },
  
    // submit filter form onChange
    'prepare_filter_form': function(doc) {
        $('form.content-filter-form input', doc).live('change',function(){ $(this).parents('form.content-filter-form').submit(); })
        $('form.content-filter-form select', doc).live('change',function(){ $(this).parents('form.content-filter-form').submit(); })
    
      	$('form.content-filter-form :submit').hide();
    },
    
    'prepare_popup_content': function(popupdata) {
        var popupid = popupdata.popup_id;
        if ($('#'+popupid).length) {
            var popup = $('#'+popupid);
            $("a", popup).each(function(){
                  if ($(this).attr('href') && !$(this).hasClass('popup-link') && !$(this).hasClass('ajax-link-out') && !$(this).attr('target') &&
                      !($(this).attr('href').substring(0,3) == 'www') && !($(this).attr('href').substring(0,5) == 'http:') &&
                      !($(this).attr('href').substring(0,6) == 'https:') && !($(this).attr('href').substring(0,4) == 'ftp:') &&
                      !($(this).attr('href').substring(0,7) == 'mailto:')) {
                          if ($(this).attr('href').indexOf(popupid) == -1 ) {
                            $(this).data("href", "/user/popup/" + popupid + "/url=" + $(this).attr("href"));
                          } else {
                            $(this).data("href", $(this).attr("href"));
                          }
                          if ($.browser.msie && $.browser.version.substr(0, 1) < 7) {
                              var prefix = window.location.href.replace(window.location.hash, '');
                              $(this).data("href", $(this).data("href").replace(prefix, "/"));
                          }
                          $(this).click(function(){
                              $("#loading-status").css('display', 'block');
                              url = $(this).data("href");
                              $.ajax({
                                  url: url,
                                  dataType: 'json',
                                  success: hardtree.process_popup_data
                              });
                              return false;
                          })
                  }
            });
            hardtree.prepare_popups(popup);
            $("form", popup).each(function() {
                url = $(this).attr('action');
                if (url) {
                  if (url.indexOf('/user/popup/') == -1) {
                    url = '/user/popup/' + popupdata.popup_id + '/url=' + url;
                  }
                } else {
                    url = popupdata.url;
                }
                $(this).attr('action', url);
                var options = {
                    'beforeSubmit': function(data) {
                    $("#loading-status").css('display', 'block');  
                    },
                  'url': url,
                  'dataType': 'json',
                  'success': hardtree.process_ajax
                }
                $(this).ajaxForm(options);
            })
            hardtree.showhidejs(popup);
            hardtree.prepare_ajax_links(popup);
            hardtree.prepare_comments(popup);
            hardtree.prepare_attachments(popup);
            hardtree.prepare_invites(popup);
            hardtree.prepare_tags(popup);
            hardtree.prepare_autocomplete(popup);
            hardtree.prepare_search_duplicates(popup);
            hardtree.put_datepicker(popup);
            hardtree.prepare_mass_form(popup);
            hardtree.put_mce(popup);
        }        
    },
    
    'process_popup_data': function(data) {
         if (data.popup) {
             var popup = $('#' + data.popup.popup_id);
             if (data.popup.object) {
                 // Object created, close popup
                 if (popup.data('field')) {
                     var doc = $('#' + popup.data('module'));
                     var field = $('#' + popup.data('field'), doc);
                     if (field.hasClass('autocomplete')) {
                         field.val(data.popup.object.name);
                         var idfield = $('#' + field.attr('id').replace('autocomplete_', ''), doc);
                         idfield.each(function() {
                            $(this).val(data.popup.object.id); 
                         });
                     } else if (field.hasClass('duplicates')) {
                         field.val(data.popup.object.name);
                         var idfield = $('#' + field.attr('id').replace('duplicates_', ''), doc);
                         idfield.each(function() {
                            $(this).val(data.popup.object.id); 
                         });
                     } else {
                         field.append('<option value="' + data.popup.object.id + '" selected="selected">' + data.popup.object.name + '</option>');                         
                     }
                 } else {
                     var url = location.hash.substring(1);
                     url = hardtree.prepare_url(url);
                     var popupparents = popup.parents('div.popup-block-inner');
                     $("#loading-status").css('display', 'block');
                     if (popupparents.length > 0) {
                       $(popupparents).first().each(function() {
                         url = '/user/popup/' + $(this).attr('id') + '/url=' + $(this).parent().data('link').replace('#','');
                       });
                     }
                     $.ajax({
                        'url': url,
                        'dataType': 'json',
                        'success': hardtree.process_ajax,
                        'complete': hardtree.process_html
                     });
                 }
                 popup.parent().remove();
             } else if (data.popup.redirect) {
                 var url = location.hash.substring(1);
                 url = hardtree.prepare_url(url);
                 var popupparents = popup.parents('div.popup-block-inner');
                 $("#loading-status").css('display', 'block');
                 if (popupparents.length > 0) {
                   $(popupparents).first().each(function() {
                     url = '/user/popup/' + $(this).attr('id') + '/url=' + $(this).parent().data('link').replace('#','');
                   });
                 }
                 $.ajax({
                    'url': url,
                    'dataType': 'json',
                    'success': hardtree.process_ajax,
                    'complete': hardtree.process_html
                 });
                 popup.parent().remove();
             } else {
                 var popuptitleblock = popup.parent().children('div.popup-title-block');
                 popuptitleblock.children('span.popup-title').html(data.popup.title);
                 popuptitleblock.children('span.popup-subtitle').html(data.popup.subtitle);
                 popup.html(data.popup.content);
                 hardtree.prepare_popup_content(data.popup);
                 //popup.parent().css('display', 'block');
                 popup.parent().fadeIn(300);
                 $("input:text:visible:first", popup).focus();
             }
         }
         $("#loading-status").css('display', 'none');
    },
    
    'prepare_popups': function(doc) {
        $('a.popup-link', doc).each(function() {
          if (!$(this).hasClass('popup-link-out')) {
            $(this).click(function() {
                var popupid = doc.attr('id') + '-popup-' + $(this).attr('id') + "-" + Date.now();
                if ($('#'+popupid).length) {
                    return false;
                }
                $("#loading-status").css('display', 'block');
                var popup = $('<div></div>').addClass('popup-block').css('display', 'none').css('visibility', 'visible');
                popup.data('link', $(this).attr('href'));
                var popuptitleblock = $('<div></div>').addClass('popup-title-block');
                popuptitleblock.append($('<span></span>').addClass('popup-title'));
                popuptitleblock.append($('<span></span>').addClass('popup-subtitle'));
                var popuplinkopen = $('<div></div>').addClass('popup-link-open');
                popuplinkopen.click(function() {
                    var url = $(this).parent().data('link');
                    if (url) {
                        url = url.replace('#', '');
                        window.location.hash = url;
                        $(this).parent().remove();
                    }
                })
                var popupclose = $('<div></div>').addClass('popup-close');
                popupclose.click(function() {
                    if ($('#'+popupid).length) {
                        $('#'+popupid).parent().remove();
                    }
                });
                var popupinner = $('<div></div>').addClass('popup-block-inner')
                popupinner.attr('id', popupid);
                if ($(this).attr('field')) {
                    popupinner.data('field', $(this).attr('field'));
                    popupinner.data('module', doc.attr('id'));
                }
                popup.append(popupclose);
                popup.append(popuplinkopen);
                popup.append(popuptitleblock);
                popup.append(popupinner);
                doc.append(popup);
                var popupparents = popup.parents('div.popup-block-inner');
                if (popupparents.length > 0) {
                  var parentoffset = popupparents.first().offset();
                  popup.position({
                     my: "center top",
                     at: "center top",
                     of: $(this),
                     collision: "flip",
                     offset: "-" + parentoffset.left + " -" + parentoffset.top + ""
                  });
                } else {
                  popup.position({
                     my: "left top",
                     at: "left top",
                     of: $(this),
                     collision: "fit",
                     offset: "-30 -5"
                  }); 
                }
                popup.draggable({handle: 'div.popup-title-block',
                                 opacity: 0.5,
                                 addClasses: false});
                url = '/user/popup/' + popupid + "/url=" + $(this).attr('href').replace('#', '');
                if ($.browser.msie && $.browser.version.substr(0,1)<7) {
                    url = '/user/popup/' + popupid + "/url=/" + $(this).attr('href').replace('#', '');
                    var prefix = window.location.href.replace(window.location.hash, '');
                    url = url.replace(prefix, "");
                }
                url = url.replace('//', '/');
                $.ajax({
                 url: url,
                 dataType: 'json',
                 success: hardtree.process_popup_data
                });
                return false;
            })
          }  
        })
    },
    
    'prepare_autocomplete': function(doc) {
        $('input.autocomplete', doc).each(function() {
            $(this).data('hidden_field', $("#id_" + $(this).attr('name').replace("autocomplete_", ""), doc));
            $(this).autocomplete({
                'source': $(this).attr('callback') + ".json",
                'focus': function(event, ui) {
                        $(this).val(ui.item.label);
                        $(this).data('hidden_field').val(ui.item.value);
                        return false;
                    },
                'select': function(event, ui) {
                        $(this).val(ui.item.label);
                        $(this).data('hidden_field').val(ui.item.value);
                        return false;
                    }
            });
            $(this).change(function(event) {
              if ($(this).val() == "") {
                $(this).data('hidden_field').val("");
              }
            });
        });
        
        $('input.multicomplete', doc).each(function() {
          $(this).data('hidden_fields', $("#" + $(this).attr('name').replace("multicomplete_", "multi_"), doc));
          // don't navigate away from the field on tab when selecting an item
          $(this).bind( "keydown", function( event ) {
            if ( event.keyCode === $.ui.keyCode.TAB &&
                $( this ).data( "autocomplete" ).menu.active ) {
              event.preventDefault();
            }
          });
          $(this).bind( "keyup", function( event ) {
            if (event.keyCode === $.ui.keyCode.BACKSPACE ||
                       event.keyCode === $.ui.keyCode.DELETE) {
              var terms = hardtree.utils.split( this.value );
              var fields = $('input',$(this).data('hidden_fields'));
              for (var i=0; i<fields.length; i++)
              {
                var label = $(fields[i]).attr('label');
                if ($.inArray(label, terms) == -1) {
                  $(fields[i]).remove();
                }
              }
            }
          })
          var callback = $(this).attr('callback') + ".json"
          $(this).autocomplete({
            source: function( request, response ) {
              $.getJSON(callback, {
                term: hardtree.utils.extractLast( request.term )
              }, response );
            },
            search: function() {
              // custom minLength
              var term = hardtree.utils.extractLast( this.value );
              if ( term.length < 2 ) {
                return false;
              }
            },
            focus: function() {
              // prevent value inserted on focus
              return false;
            },
            select: function( event, ui ) {
              var terms = hardtree.utils.split( this.value );
              terms.pop();
              terms.push( ui.item.label );
              terms.push( "" );
              var fields = $(this).data('hidden_fields');
              var hidden = $('<input>');
              hidden.attr('type', 'hidden').attr('name', $(this).attr('name').replace("multicomplete_", ""))
              .attr('id', 'id_' + hidden.attr('name')).attr('value', ui.item.value).attr('label', ui.item.label);
              this.value = terms.join( ", " );
              fields.append(hidden);
        
              var terms = hardtree.utils.split( this.value );
              var fields = $('input',$(this).data('hidden_fields'));
              for (var i=0; i<fields.length; i++)
              {
                var label = $(fields[i]).attr('label');
                if ($.inArray(label, terms) == -1) {
                  $(fields[i]).remove();
                }
              }
              return false;
            }
          });
        });
    },
  
    'prepare_search_duplicates': function(doc) {
        $('input.duplicates', doc).each(function() {
            $(this).data('hidden_field', $("#id_" + $(this).attr('name').replace("duplicates_", ""), doc));
            $(this).autocomplete({
                'source': $(this).attr('callback') + ".json",
                'focus': function(event, ui) {
                        $(this).val(ui.item.label);
                        return false;
                    },
                'select': function(event, ui) {
                        $(this).val(ui.item.label);
                        return false;
                    }
            });
        })
    },

    'prepare_attachments': function(doc) {

        $('.delete-attachment', doc).each(function() {
           $(this).click(function() {
               Dajaxice.hardtree.account.attachment_delete(Dajax.process, {'attachment_id': $(this).attr('attachment')});
               return false;
           });
        });

        $('.attachment-uploader', doc).each(function() {
            auploader = $(this);
            var file_uploader = new qq.FileUploader({
                action: $(this).attr('action'),
                element: this,
                multiple: true,
                onComplete: function(id, fileName, responseJSON) {
                    Dajaxice.hardtree.account.attachment(Dajax.process, {'object_id': responseJSON.object_id, 'update_id': responseJSON.update_id});
                },
                params: {
                    'csrf_token': $(this).attr('csrf'),
                    'csrf_name': 'csrfmiddlewaretoken',
                    'csrf_xname': 'X-CSRFToken'
                },
                text: hardtree_attachment_text
            });
           auploader.parent().append(auploader.find('.qq-upload-list').remove());
        });
		
        $('.attachment-record-uploader', doc).each(function() {
            var file_uploader = new qq.FileUploader({
                action: $(this).attr('action'),
                element: this,
                multiple: false,
                onComplete: function(id, fileName, responseJSON) {
                    Dajaxice.hardtree.account.attachment(Dajax.process, {'object_id': responseJSON.object_id, 'update_id': responseJSON.update_id})
                },
                onAllComplete: function(uploads) {
                    // uploads is an array of maps
                    // the maps look like this: { file: FileObject, response: JSONServerResponse }
                    //alert( "All complete!" ) ;
                },
                params: {
                    'csrf_token': $(this).attr('csrf'),
                    'csrf_name': 'csrfmiddlewaretoken',
                    'csrf_xname': 'X-CSRFToken'
                },
                text: hardtree_attachment_record_text
            });
        });
    },


    'prepare_invites': function(doc) {
          $('.easy-invite', doc).each(function() {
           $(this).click(function() {
               Dajaxice.hardtree.account.easy_invite(Dajax.process, {'emails': $(this).attr('emails')});
               return false;
             });
           });
    },


    'prepare_comments': function(doc) {
    $('a.like-button', doc).each(function() {
      $(this).click(function() {
        $(this).parent().submit();
        return false;
      });
    });
    $('a.comment-button', doc).each(function() {
      $(this).click(function() {
        var commentslikes = $('div.comments-likes-box-'+$(this).attr('object'));
        commentslikes.toggle();
        if (commentslikes.css('display') != 'none') {
          $('textarea:visible:first', commentslikes).focus();
        }
        return false;
      })
    });
    $('span.comments-likes-toggle', doc).each(function() {
      $(this).click(function() {
        var commentslikes = $('div.comments-likes-box-'+$(this).attr('object'));
        commentslikes.toggle();
        if (commentslikes.css('display') != 'none') {
          $('textarea:visible:first', commentslikes).focus();
        }
        return false;
      })
    });
    $('form.like-form', doc).each(function() {
    	var targetid = 'comments-likes-box-' + $(this).attr('object');
    	var target = $('#'+targetid);
    	$(this).attr('target', targetid);
    	$(this).submit(function() {
    	  	var targetid = $(this).attr('target');
    	  	var target = $(this).parents('#'+targetid);
    	  	targetid = hardtree.utils.generate_id(targetid);
    	  	target.attr('id', targetid);
    		var args = {
    			'target': '#'+targetid,
    			'form': $(this).serializeObject(),
    			'expand': true
    		}; 
			Dajaxice.hardtree.account.comments_likes(Dajax.process, args);
    		return false;
    	});
    });
  },
  
  'prepare_tags': function(doc) {
    $('input#id_multicomplete_tags', doc).each(function() {
	    $(this).focus();
	    $(this).focusout(function() {
	      $(this).parent('form').submit();
	    });
	    $(this).parent('form').submit(function() {
    	  	var targetid = $(this).attr('target');
    	  	var target = $(this).parents(targetid);
    	  	targetid = hardtree.utils.generate_id();
    	  	target.attr('id', targetid);
    		var args = {
    			'target': '#'+targetid,
    			'object_id': $(this).attr('object'),
    			'edit': true,
    			'formdata': $(this).serializeObject()
    		};
			Dajaxice.hardtree.account.tags(Dajax.process, args);
    		return false;
	    });
    });
    $('span.tags-box').each(function(){
    	$('span.tags-box-link', $(this)).css('visibility', 'hidden');
    	$(this).hover(function() {
    		$('span.tags-box-link', $(this)).css('visibility', 'visible');
    	}, function() {
    		$('span.tags-box-link', $(this)).css('visibility', 'hidden');
    	})
    })
  },
  
  'prepare_forms': function(doc) {
    $('form', doc).each(function() {
      if (!$(this).hasClass('like-form') && !$(this).hasClass('tags-form')) {
	      url = $(this).attr('action');
	      if (!url) {
	        url = location.hash.substring(1);
	      }
	      if ($(this).attr('method')=='get') {
	        $(this).attr('action', url);
	        var options = {
	          'beforeSubmit': function(data, form) {
	            var url = form.attr('action');
	            if (url.indexOf('!') != -1) {
	              url = url.substring(0, url.indexOf('!'));
	            }
	            url += '!' + form.formSerialize();
	            window.location.hash = '#' + url;
	            return false;
	           }
	        }
	        $(this).ajaxForm(options);
	      } else {
	        url = hardtree.prepare_url(url);
	        var options = {
	          'beforeSubmit': function(data) {
	              $("#loading-status").css('display', 'block');
	           },
	          'url': url,
	          'dataType': 'json',
	          'success': hardtree.process_ajax
	        }
	        $(this).ajaxForm(options);
	      }
      }
    })
    hardtree.prepare_mass_form(doc);
    hardtree.prepare_filter_form(doc);
    hardtree.prepare_autocomplete(doc);
    hardtree.prepare_search_duplicates(doc);
    hardtree.put_datepicker(doc);
  },
  
  'prepare_dropdown_menus': function() {
    $("a.menu-dropdown-link").each(function() {
        $(this).click(function() {
          var dropmenu = $('#'+$(this).attr('dropdown'));
          $(this).addClass('menu-dropdown-link-active');
          dropmenu.slideDown('fast').show();
        });
        $(this).hover(function() {
          var dropmenu = $('#'+$(this).attr('dropdown'));
          $(this).addClass('menu-dropdown-link-active');
          dropmenu.slideDown('fast').show();
        })
        $(this).parent().hover(function() {}, function() {
          var droplink = $(this).children("a.menu-dropdown-link");
          var dropmenu = $(this).children('#'+droplink.attr('dropdown'));
          dropmenu.slideUp('fast');
          droplink.removeClass('menu-dropdown-link-active');
        });
    });  
  },

  'prepare_mega_menus': function() {

    //add megemenu body to dropdown divs.

      
      $("div.menu-item").each(function(){
        $(this).hover(function(){
            $(this).addClass('hover');
        }),function(){
            $(this).removeClass('hover');
        };});


    $("div.mwrapper").each(function() {

        var p = $(this).parent();
        var a = p.find('a')
        console.log(a);
        p.mouseenter(function() {

              Dajaxice.hardtree.account.mega_menu(Dajax.process, {'menu_id': $('.megamenu', this).attr('class')});
              return false;
          });
         p.mouseleave(function() {

             console.log('Im out of that menu item');

          });
        
          $(this).hover(function(){
             console.log('hi');
             p.find('a').addClass('hover');
          },
          function(){
              console.log(p.find('.megamenu'));
              p.find('a').removeClass('hover');
          });
          var mega = $(this);
          $(this).children().each(function() {
              $(this).hover(function(){
                                 console.log('hi');
             mega.parent().find('a').addClass('hover');
          },
          function(){
              console.log(p.find('.megamenu'));
              console.log('bye');
              mega.parent().find('a').removeClass('hover');
          });
          })
      });

      $("div.megamenu").each(function() {

      });
  },

  'prepare_toolbar': function() {
    
    //hide toolbar and make visible the 'up' arrow
    $("span.hide_toolbar").click(function() {
      $("#toolbar").slideToggle("fast", function() {
        $("#toolbar_action").fadeIn("slow");    
      });
      
    });
    
    //show toolbar and hide the 'up' arrow
    $("span.show_toolbar").click(function() {
      $("#toolbar_action").fadeOut("fast", function() {
        $("#toolbar").slideToggle("fast");
      });
      
    });
  }

}

hardtree.utils = {
  'split': function( val ) {
      return val.split( /,\s*/ );
  },
  
  'extractLast': function( term ) {
      return hardtree.utils.split( term ).pop();
  },
  
  'generate_id': function( prefix ) {
	  var uniqid = prefix;
	  if (!uniqid) {
		  uniqid = 'ajax';
	  }
	  uniqid = uniqid + '-' + Date.now();
	  var i = 0;
	  while ($('#'+uniqid).length > 0) {
		  uniqid = uniqid + '-' + i;
		  i++;
	  }
	  return uniqid;
  }
}

/*
 * Hardtree modules JS library
 * 
 * Needs to be loaded after hardtree.js
 */

hardtree.modules = {
    'hardtree-home': {
        'init': function() {
            var sortparams = { opacity: 0.6,
                               handle: 'div.widget-title',
                               connectWith: '#widget-panel-right',
                               items: 'div.widget-block',
                               cursor: 'move',
                               update: function() {
                                   var url = $(this).attr('callback') + "?" + $(this).sortable("serialize");
                                   $.ajax({url: url});
                               },
                               start: function(event, ui) {
                                   $('#widget-panel-left').addClass('widget-panel-active');
                                   $('#widget-panel-right').addClass('widget-panel-active');
                                   ui.item.addClass('widget-block-moving');
                               },
                               beforeStop: function(event, ui) {
                                   ui.item.removeClass('widget-block-moving');
                               },
                               stop: function() {
                                   $('#widget-panel-left').removeClass('widget-panel-active');
                                   $('#widget-panel-right').removeClass('widget-panel-active');
                               }
            }
            $('#widget-panel-left').sortable(sortparams);
            sortparams.connectWith = '#widget-panel-left';
            $('#widget-panel-right').sortable(sortparams);
        }
    },
    'hardtree-core': {
        'init': function() {
            var setupbox = $('div.setup-module-box');
            if (setupbox.length > 0) {
                $('div.setup-module-box').each(function() {
                    $(this).click(function() {
                        $(this).toggleClass('setup-module-box-active');
                        $('input', $(this)).each(function() {
                            $(this).attr('checked', !$(this).attr('checked'));
                        }) 
                    });
                });
            }
        }
    },
    'hardtree-projects': {
        'timer': function() {
            var timeslots = $('.projects-timeslot');
            if (timeslots) {
                timeslots.each(function() {
                    var start = $(this).data('start');
                    var now = Date.now();
                    if (start == null) {
                        var elapsed = parseInt($(this).attr('diff'));
                        start = now - elapsed * 1000;
                        $(this).data('start', start);
                    }
                    var diff = (now - start) / 1000;
                    var tim = Math.floor(diff / 3600)
                    var min = Math.floor((diff / 3600 - tim) * 60)
                    var sec = Math.round((((diff / 3600 - tim) * 60) - min) * 60)
                    var string = tim + ":"
                    if (min >= 10) {
                        string += min + ":"
                    }
                    else {
                        string += "0" + min + ":"
                    }
                    if (sec >= 10) {
                        string += sec
                    }
                    else {
                        string += "0" + sec
                    }
                    $(this).html(string);
                });
                window.setTimeout(hardtree.modules['hardtree-projects'].timer, 1000);
            }
            
        },
        'init': function() {
            var timeslots = $('.projects-timeslot');
            if (timeslots) {
                this.timer();
            }
            var ganttChart = $('div.ganttChart');
            if (ganttChart) {
            	this.gantt(ganttChart);
            }
        },
        'gantt': function(block) {
            block.each(function() {
            	if (ganttData) {
		            	$(this).ganttView({ 
		                data: ganttData,
		                behavior: {
		                    onClick: function (data) { 
		                                      
		                    },                    
		                    onResize: function (data) { 
		                        Dajaxice.hardtree.projects.gantt(callback_function, {'task':data.id, 'start':data.start.toString("yyyy-M-d"), 'end':data.end.toString("yyyy-M-d")});
		                    },  
		                    onDrag: function (data) { 
		                        Dajaxice.hardtree.projects.gantt(callback_function, {'task':data.id, 'start':data.start.toString("yyyy-M-d"), 'end':data.end.toString("yyyy-M-d")});
		                    }
		                }
	            	});
	            	var projects_block = $('#module-hardtree-projects');
	            	$(this).ganttView("setSlideWidth", $('td.module-content', projects_block).width() - 60);
	            	hardtree.prepare_popups($(this));
	            	$(window).resize(function() {
	            		$('div.ganttChart', projects_block).each(function() {
	            			var projects_block = $('#module-hardtree-projects');
	            			$(this).ganttView("setSlideWidth", $('td.module-content', projects_block).width() - 60);
	            		});
	            	})
            	}
            });            
        }
    },
  'hardtree-reports': {
        'init': function() {
          /*//LIVE CHARTS
             $('div.chart').each(function(){
               var divid = $.uuid('chart-');
               $(this).attr('id', divid);
               var settings = {
                 url: '/reports/chart/'+$(this).attr('chart')+'/options/'+divid,
                 dataType: 'json',
                 success: function(data) {
                   var options = data;
                   chart1 = new Highcharts.Chart(options);
               }
               }
               $.ajax(settings);
        });*/
       }
  }
}

/* Hardtree Nuvius library */
hardtree.nuvius = {
  
  'profile': null,
  'access_popup': false,
  'reload_on_profile': true,
  
  'fetch_profile': function() {
      $("#loading-status").css('display', 'block');
      $("#loading-status-text").html('Loading...');
      $.ajax({
          'url': nuvius_profile_url,
          'dataType': 'jsonp',
          'success': hardtree.nuvius.load_profile,
          'error': hardtree.show_error
      })
  },
  
  'check_profile': function(data) {
      if (data) {
        if (data.key_valid) {
          if (data.username) {
            $('#nuvius-username').html(data.username);
          } else {
            $('#nuvius-username').html("Anonymous User");
          }
          if (hardtree.nuvius.reload_on_profile) {
            hardtree.do_ajax();
          }
        }
      } else {
        if (hardtree.nuvius.profile) {
          var url = nuvius_profile_check_url;
          url += "?nuvius_id=" + hardtree.nuvius.profile.id + "&profile_key=" + hardtree.nuvius.profile.key;
          $.ajax({
            'url': url,
            'dataType': 'json',
            'success': hardtree.nuvius.check_profile,
            'error': hardtree.show_error
          })
        }
      }
  },
  
  'load_profile': function(data) {
      $("#loading-status").css('display', 'none');
      if (data.profile) {
        if (!data.profile.access_granted && hardtree.nuvius.access_popup) {
          $.colorbox({
            href: data.profile.access_url,
            width:"80%",
            height:"80%",
            iframe: true,
            overlayClose: false,
            onClosed: hardtree.nuvius.fetch_profile
          });
          hardtree.nuvius.access_popup = false;
        } else {
          hardtree.nuvius.profile = data.profile;
          hardtree.nuvius.check_profile();
        }
     }
  },
  
  'fetch_access': function() {
      hardtree.nuvius.access_popup = true;
      hardtree.nuvius.fetch_profile();
  },
  
  'close_iframe': function() {
      $.colorbox.close();
  }
}

/* Init */

$(function() {
  
  // Bind the event.
  $(window).hashchange(hardtree.do_ajax);

  // Trigger the event (first thing on page load).
  $(window).hashchange();
  hardtree.prepare_dropdown_menus();
  hardtree.prepare_toolbar();
  hardtree.convert_links();
  hardtree.prepare_ajax_links();
  $(".menu-item a").each(function(){
      $(this).click(function() {
        if ($(this).hasClass('active') && $(this).attr('href') == window.location.hash) {
              $(window).hashchange();
      }
      });
  });
  // Prepare perspective switcher
  $('#perspective_switch').each(function() {
      url = $(this).attr('action');
      if (!url) {
        url = location.hash.substring(1);
      }
      url = hardtree.prepare_url(url);
      var options = {
        'beforeSubmit': function(data) {
            $("#loading-status").css('display', 'block');
         },
        'url': url,
        'dataType': 'json',
        'success': hardtree.process_ajax
      }
      $(this).ajaxForm(options);
      $(this).children('select').change(function() {
        $('#perspective_switch').submit();
      })
  });
  // Prepare search form
  $('form#search_form').each(function() {
      url = $(this).attr('action');
      if (!url) {
          url = location.hash.substring(1);
      }
      $(this).attr('action', url);
      var options = {
        'beforeSubmit': function(data, form) {
          var url = form.attr('action');
          url += '!' + form.formSerialize();
          window.location.hash = '#' + url;
          return false;
         }
      }
      $(this).ajaxForm(options);
  })
  // Prepare modules
  $(".module-block").data('title', document.title);
  $(".module-block").each(function() {
      doc = $(this)
      if ($("form").length) {
        hardtree.prepare_forms(doc);
        hardtree.prepare_comments(doc);
        if ($("textarea").length) {
          hardtree.put_mce(doc);
        }
        hardtree.put_datepicker(doc)
        hardtree.prepare_forms(doc);
      }
      hardtree.prepare_tags();
      hardtree.prepare_slider_sidebar(doc);
      hardtree.prepare_list_actions(doc);
	  hardtree.prepare_content_top(doc);
      hardtree.prepare_attachments(doc);
      hardtree.prepare_mega_menus(doc);
      hardtree.prepare_invites(doc);
      hardtree.prepare_popups(doc);
      hardtree.showhidejs(doc);
      module_name = $(this).attr('id').substring(7);
      hardtree.prepare_module_stuff(module_name);
  });

});