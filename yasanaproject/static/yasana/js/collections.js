

/// <reference path="../vendor/jquery.js" />
/// <reference path="../vendor/backbone.js" />
/// <reference path="../models.js" />


window.yasana = window.yasana || {};
yasana.collections = yasana.collections || {};

(function($, Backbone, models, mod){

    mod.UserCollections = Backbone.Collection.extend({

        url:"/api/users/?pg_no=0",

        model: models.User,

        page_no: 0
    });

})($, Backbone, yasana.models, yasana.collections);

