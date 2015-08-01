

 $(document).ready(function(){

  var router = new yasana.routers.yasanaRouter();
     Backbone.history.start();

  $('#nav_link_ul').find('li').click(function(ev){
      if(ev.preventDefault){
          ev.preventDefault();
      }
      else{
          ev.returnValue = false;
      }

      router.navigate($(this).attr('href'), {trigger:true});
      yasana.utils.views.showLoading();

     });

    yasana.utils.views.ajaxCSRFSetUp();
 });