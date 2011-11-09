/*
* jQuery Mobile Framework : "ajaxform" plugin
* Copyright (c) jQuery Project
* Dual licensed under the MIT (MIT-LICENSE.txt) and GPL (GPL-LICENSE.txt) licenses.
* Note: Code is in draft form and is subject to change 
*/  
(function($){

//ajax response callbacks
$.formhandlers = {
	'default' : function(data,type){
		return $(data).find('[data-role="content"]:eq(0)');
	}
};

function getBaseURL(){
    var newBaseURL = location.hash.replace(/#/,'').split('/');
	if(newBaseURL.length && /[.|&]/.test(newBaseURL[newBaseURL.length-1]) ){
		newBaseURL.pop();	
	}
	newBaseURL = newBaseURL.join('/');
	if(newBaseURL !== "" && newBaseURL.charAt(newBaseURL.length-1) !== '/'){  newBaseURL += '/'; }
	return newBaseURL;
}

$.fn.ajaxform = function(options){
	return $(this).each(function(){	
		$this = $(this);
	
		//extendable options
		var o = $.extend({
			submitEvents: '',
			method: $this.attr('method'),
			action: getBaseURL()+$this.attr('action'),
			injectResponse: true,//should be data-attr driven
			dataFilter: $.formhandlers['default'], //should be data-attr driven 
			theme: $this.data('theme') || 'b'
		}, options);
				
		$this.addClass('ui-autoform ui-bar-'+o.theme);
		
		$this.bind(o.submitEvents, function(){
			$(this).submit();
		});
		
		$this.submit(function(){
			$.pageLoading();
			$.ajax({
				url: o.action,
				type: o.method,
				data: $(this).serialize(),
				dataFilter: o.dataFilter,
				success: function(data,textStatus){
					$('.ui-page-active .ui-content').replaceWith( data );
					$('.ui-page-active [data-role="content"]').page();
					$.pageLoading(true);
				}
			});
			return false;
		});
	});
};




})(jQuery);
	
