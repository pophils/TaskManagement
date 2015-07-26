

/// <reference path="../vendor/jquery.js" />
/// <reference path="../vendor/backbone.js" />
/// <reference path="../models.js" />


window.yasana = window.yasana || {};
yasana.collections = yasana.collections || {};

(function($, Backbone, models, mod){

    mod.UserCollections = Backbone.Collection.extend({

        url:"/account/users/",

        model: models.User
    });

})($, Backbone, yasana.models, yasana.collections);

