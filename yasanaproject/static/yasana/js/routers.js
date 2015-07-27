

/// <reference path="../vendor/jquery.js" />
/// <reference path="../vendor/backbone.js" />
/// <reference path="../models.js" />


window.yasana = window.yasana || {};
yasana.routers = yasana.routers || {};

(function($, Backbone, views, collections, models, mod){

    mod.yasanaRouter = Backbone.Router.extend({

        currentView: undefined,

        routes: {
             "": "home",
            "user-manager": "manageUsers"
        },

        home: function(){
            var view = new views.HomePage();
            this.render(view);
        },

        manageUsers: function(){
            var view = new views.ManageUserPage({collection: new collections.UserCollections()});
            this.render(view);
        },

        render: function(view){
            if(this.currentView){
                this.currentView.$el.empty();//remove();
                this.currentView.undelegateEvents();
                this.currentView.unbind();
                if(this.currentView.close){
                    this.currentView.close();
                }
            }
            this.currentView = view;
            view.render();
        }


    });

})($, Backbone, yasana.views, yasana.collections, yasana.models, yasana.routers);

