
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

        destroyAllEvents: function(view){

            if(typeof view != "undefined"){
                view.undelegateEvent();
                view.unbind();
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
            if(url && url.length > 0){
                   $.getJSON(url, data, function (data) {
                   if (data != null) {
                       callback(data);
                    }
                });
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

        displayNoItem: function(){
            $("div.grid-rows").append($('<div id="grid-rows-no-items">No items found</div>'));
        },

        initClosePopupClickEvent: function(){
            $(".popup-close").click(function(ev){
                 $(".popup-wrap").trigger('close');
            });
        }
    });

    mod.Constants = mod.Constants || {};
    mod.Constants.url = mod.Constants.url || {};

     $.extend(mod.Constants.url, {
         get_user_collection_partial_view: "partials/user-collection/",
         get_add_user_partial_view: 'partials/add-user/'
    });

    mod.Constants.view = mod.Constants.view || {};

    $.extend(mod.Constants.view, {

        nav_link_clicked: null

    });

})($, Backbone, _,  yasana.utils);