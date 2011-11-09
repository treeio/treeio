/* Copyright (c) 2009-2010, Benito Jorge Bastida :: For further information check COPYING */
var Dajax = {
    process: function(data)
    {
        if(data==Dajaxice.EXCEPTION){
            alert('Something went wrong, please reload the page.');
        }
        else{
            $.each(data, function(i,elem){
            switch(elem.cmd)
            {
                case 'alert':
                    alert(elem.val)
                break;
        
                case 'data':
                    eval( elem.fun+"(elem.val);" );
                break;
        
                case 'as':
                    jQuery.each($(elem.id),function(){ this[elem.prop] = elem.val; });
                break;
        
                case 'addcc':
                    jQuery.each(elem.val,function(){
                        $(elem.id).addClass(String(this));
                    });
                break;
            
                case 'remcc':
                    jQuery.each(elem.val,function(){
                        $(elem.id).removeClass(String(this));
                    });
                break;
            
                case 'ap':
                    jQuery.each($(elem.id),function(){ this[elem.prop] += elem.val; });
                break;
            
                case 'pp':
                    jQuery.each($(elem.id),function(){ this[elem.prop] = elem.val + this[elem.prop]; });
                break;
            
                case 'clr':
                    jQuery.each($(elem.id),function(){ this[elem.prop] = ""; });
                break;
            
                case 'red':
                    window.setTimeout('window.location="'+elem.url+'";',elem.delay);
                break;
            
                case 'js':
                    eval(elem.val);
                break;
            
                case 'rm':
                    $(elem.id).remove();
                break;
            
                default:
                    console.log('Dajaxice error!\n\n'+data);
                    return;
                break;
                }
            });
        }
    }
};