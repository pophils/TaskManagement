
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

    getTemplateFromUrl :function(url, callback){

        if(typeof url == "string"){
             $.get(url, function (template) {

                 if(typeof callback == "function"){
                     callback();
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
        }
    });

    mod.Constants = mod.Constants || {};
    mod.Constants.url = mod.Constants.url || {};

     $.extend(mod.Constants.url, {

        HomePage: "/d"

    });

})($, Backbone, _,  yasana.utils);