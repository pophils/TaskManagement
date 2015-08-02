
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
            "imageSrc":"",
            "first_name": "",
            "other_name" : "",
            "website" : "",
            "gender": ""
        },

        idAttribute: "email"
    });

    mod.Task = Backbone.Model.extend({

        url:"/api/tasks/",

        defaults:{
            "title":"",
            "details":"",
            "status":"",
            "priority":"",
            "expected_end_date":"",
            "is_completed": "",
            "start_date" : "",
            "id": ""
        },

        idAttribute: "id"
    });

})($, Backbone, yasana.models);

