
/// <reference path="../underscore.js" />
/// <reference path="../backbone.js" />
/// <reference path="../jquery.js" />

window.yasana = window.yasana || {};

yasana.utils = yasana.utils || {};

(function($, Backbone, _, mod){

    mod.views = mod.views || {};

    $.extend(mod.views, {

        compileTemplate: function(html, dataContext, templateSetting){
            if(typeof html != 'undefined' && html.length > 0){
                var compiledTemplate = _.template(html);

            if(typeof dataContext != "undefined" && dataContext.length > 0){
                compiledTemplate(dataContext, templateSetting);
                return compiledTemplate
            }
                return compiledTemplate;
            }
        },

        getHtmlFromUrl :function(url, callback){

            if(typeof url == "string"){
                $.get(url, function (template) {
                    if(typeof callback == "function"){
                        callback(template);
                    }
                    else{
                        return template;
                    }
                });
            }
            else{
                throw TypeError("Url must be a string");
            }
        },

        getJsonFromUrl: function(url, data, callback){
            if(typeof url == "string"){
                if(url && url.length > 0){
                    $.getJSON(url, data, function (data) {
                        if (data != null) {
                            callback(data);
                        }
                    });
                }
            }
            else{
                throw TypeError("Url must be a string");
            }

        },

        unbindPopupViewEvent: function(view){
            if (typeof view != "undefined"){

                if(mod.Constants.view.popupView){
                    mod.Constants.view.popupView.$el.empty();//remove();
                    mod.Constants.view.popupView.undelegateEvents();
                    mod.Constants.view.popupView.unbind();
                    if(mod.Constants.view.popupView.close){
                        mod.Constants.view.popupView.close();
                    }
            }
            mod.Constants.view.popupView = view;

            }
        },

        updateNavLinkActiveClass: function(){
            $('#nav_link_ul').find('li.active').removeClass('active');
            $(mod.Constants.view.nav_link_clicked).addClass('active');
        },

        showLoading: function(){
            $("#loading-div").show();
        },

        hideLoading: function(){
            $("#loading-div").hide();
        },

        hideLoadMoreBtn: function(){
            $("#load-more-btn").hide();
        },

        displayNoItem: function(){
            $("div.grid-rows").append($('<div id="grid-rows-no-items">No items found</div>'));
        },

        initClosePopupClickEvent: function(){
            $(".popup-close").click(function(ev){
                 $(".popup-wrap").trigger('close');
            });
        },

        closePopup: function(){
           $(".popup-wrap").trigger('close');
        },

        ajaxCSRFSetUp: function(){
               $.ajaxSetup({
                   beforeSend: function(xhr, settings) {
                       function getCookie(name) {
                           var cookieValue = null;
                           if (document.cookie && document.cookie != '') {
                               var cookies = document.cookie.split(';');
                               for (var i = 0; i < cookies.length; i++) {
                                   var cookie = jQuery.trim(cookies[i]);
                                   // Does this cookie string begin with the name we want?
                                   if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                       break;
                                   }
                               }
                           }
                           return cookieValue;
                       }
                       if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                           // Only send the token to relative URLs i.e. locally.
                           xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                       }
                   }
               });
        }

    });


    mod.helpers = mod.helpers || {};

    $.extend(mod.helpers, {

        validateEmail: function(email){
            var emailRegex = /^[ ]*\w+([-+.']\w+)*@\w+([-.]\\w+)*\.\w+([-.]\w+)*[ ]*$/i;
            return emailRegex.test(email);
        },

        validatePhone: function(phone){
            var phoneRegex = /^[0-9+][ ]*[0-9][0-9\s+]+$/i;
            phone = $.trim(phone).replace(/\s+/g, '');
            return phoneRegex.test(phone);
        },

        validateGender: function(gender){

            return gender == 'm' || gender == 'f' || gender == 'p';
        },

        validateTaskPriority: function(priority){
            try{
                priority = parseInt(priority);
            }
            catch(ex){
                return false;
            }

            return priority >= 0 && priority < 4;
        },

        validateRequired: function(value){
            if(typeof value == "undefined"){
                return false;
            }
            else if(typeof value != "undefined" && value.length < 1){
                return false;
            }

            return true;
        },

        validateMaxLength: function(value, maximumLength){

            if (typeof value == 'string' && typeof maximumLength == 'number'){
                return value.length <= maximumLength;
            }
            return false;
        },

        validatePassword: function(password){
            if(typeof password == "undefined"){
                return false;
            }
            else if(typeof password != "undefined" && password.length < 1){
                return false;
            }

            return true;
        },

        validateConfirmPassword: function(confirmPassword){
            if(typeof confirmPassword == "undefined"){
                return false;
            }
            else if(typeof confirmPassword != "undefined" && confirmPassword.length < 1){
                return false;
            }

            return true;
        },

        validatePasswordMatch: function(password, confirmPassword){

            return confirmPassword == password;
        }

    });



    mod.Constants = mod.Constants || {};
    mod.Constants.url = mod.Constants.url || {};

     $.extend(mod.Constants.url, {
         get_user_collection_partial_view: "partials/user-collection/",
         get_add_user_partial_view: 'partials/add-user/',
         get_landing_task_summary: 'api/task-summary/',
         get_user_collection:"/api/users/?pg_no=",
         get_total_users:"/api/total-users/",
         get_total_pending_tasks:"/api/total-tasks/?status=0",
         get_pending_task_collection_partial_view: "partials/task-collection/?status=0",
         get_add_task_partial_view: 'partials/add-task/'
    });

    mod.Constants.view = mod.Constants.view || {};

    $.extend(mod.Constants.view, {
        nav_link_clicked: null,
        is_admin_login: false,
        get_users_page_no: 0,
        current_total_users: 0,
        current_user_collection: undefined,
        popupView : undefined,
        current_total_tasks: 0,
        get_task_page_no: 0,
        current_task_collection: undefined
    });

})($, Backbone, _,  yasana.utils);