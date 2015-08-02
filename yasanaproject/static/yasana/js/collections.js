

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

    mod.PendingTaskCollections = Backbone.Collection.extend({

        url:"/api/tasks/?status=0&pg_no=0",

        model: models.Task,

        page_no: 0
    });

})($, Backbone, yasana.models, yasana.collections);

