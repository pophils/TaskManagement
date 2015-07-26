
/// <reference path="../vendor/jquery.js" />
/// <reference path="../vendor/backbone.js" />
/// <reference path="../core/utils.js" />
/// <reference path="../models.js" />
/// <reference path="../collections.js" />


window.yasana = window.yasana || {};
yasana.views = yasana.views || {};

(function($, Backbone, _, collections, models, mod){

    mod.HomePage = Backbone.View.extend({

        is_admin: undefined,

        initialize: function(){
             if($('p.summary-count.users').length > 0){
                 this.is_admin =true;
             }
            else{
                 this.is_admin = false;
             }
        },

        render: function(){
           // Just fetch summary and update page
            if(this.is_admin){
                 yasana.utils.views.getJsonFromUrl('/landing-task-summary/', {is_admin:1}, this.renderCallback)
            }
            else{
                yasana.utils.views.getJsonFromUrl('/landing-task-summary/', {is_admin:0}, this.renderCallback)
            }
        },

        renderCallback: function(data){

            if($('p.summary-count.users').length > 0){
                $('p.summary-count.users').text(data.users);
            }
            $('p.summary-count.new').text(data.new);
            $('p.summary-count.pending').text(data.pending);
            $('p.summary-count.completed').text(data.completed);
        }
    });


    mod.ManageUserPage = Backbone.View.extend({

        model: models.User,

        collection: collections.UserCollections,

        initialize: function(){

        },

        render: function(){

        },

        renderCallback: function(data){

        }

    });

})($, Backbone, _, yasana.collections, yasana.models, yasana.views);

