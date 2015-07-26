

 $(document).ready(function(){

  var router = new yasana.routers.yasanaRouter();
     Backbone.history.start();


  $('#nav_link_ul').find('li').click(function(ev){
         ev.preventDefault();
         $('#nav_link_ul').find('li.active').removeClass('active');
         $(this).addClass('active');
         router.navigate($(this).attr('href'), {trigger:true});
     });
 });