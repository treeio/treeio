/* Tree.io Mobile JS */

$(document).bind("mobileinit", function () {
    $.extend($.mobile, { ajaxFormsEnabled: true });
});

$(function() {
  $(window).hashchange(function(event) {
    $('form').each(function() {
      var url = window.location.hash.replace('#', '');
      if (url == '') { url = window.location.pathname };
      if (url.indexOf('?') != -1) {
        url = url.substring(0, url.indexOf('?'));
      };
      $(this).attr('action', url);
    })
  })
  $(window).hashchange();
});
