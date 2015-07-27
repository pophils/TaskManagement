
/// <reference path="../vendor/jquery.js" />
/// <reference path="../vendor/backbone.js" />

window.yasana = window.yasana || {};
yasana.models = yasana.models || {};

(function($, Backbone, mod){

    mod.User = Backbone.Model.extend({
        url:"/api/users/",

        defaults:{
            "name":"",
            "email":"",
            "phone":"",
            "department":"",
            "imageSrc":""
        },

        idAttribute: "email"
    });

})($, Backbone, yasana.models);

