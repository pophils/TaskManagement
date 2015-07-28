
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

        el: ".main-content",

        initialize: function(){

            if($('dashboard-summary-container').length > 0){
                this.checkIsAdmin();
            }
            this.compiledTemplate = yasana.utils.views.compileTemplate($('#dashboard').html());
        },

        checkIsAdmin: function () {

             if($('p.summary-count.users').length > 0){
                    this.is_admin =true;
                }
                else{
                    this.is_admin = false;
                }
        },

        isSummaryContainerLoaded: function(){
            if($('dashboard-summary-container').length > 0){
                return true;
            }
            return false;
        },

        compiledTemplate: undefined,

        render: function(){
           // Just fetch summary and update page
            if(this.isSummaryContainerLoaded() == false){
                this.$el.empty().append(this.compiledTemplate);
            }

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
            yasana.utils.Constants.view.nav_link_clicked = $('li#dashboard-link');
            yasana.utils.views.updateNavLinkActiveClass();
            $("#loading-div").hide();
        }
    });

    mod.ManageUserPage = Backbone.View.extend({

        model: models.User,

        el: ".main-content",

        collection: collections.UserCollections,

        events: {
            'click #new-user-btn' : 'loadNewUserForm'
        },

        initialize: function(){

            if(typeof localStorage.yasana_user_collection_partial_view == 'undefined'){
                yasana.utils.views.getHtmlFromUrl(yasana.utils.Constants.url.get_user_collection_partial_view,
                this.getHtmlFromUrlCallback);
            }
        },

        loadNewUserForm : function(){
            if(typeof localStorage.formPopup == "undefined"){
                toastr.info('Loading user form popup...');
                yasana.utils.views.getHtmlFromUrl(yasana.utils.Constants.url.get_add_user_partial_view,
                this.loadNewUserFormCallback);
            }
            else{
                 mod.ManageUserPage.prototype.showForm();
            }
        },

        loadNewUserFormCallback: function(template){
            var ss = jQuery("<div/>").append(template);
            localStorage.formPopup = $(ss).html();
            mod.ManageUserPage.prototype.showForm();
        },

        showForm: function(){
            $(".popup-wrap").empty().append(localStorage.formPopup).show();
            $('.popup-wrap').lightbox_me({ centered: true, lightboxSpeed: "fast" });
            yasana.utils.views.initClosePopupClickEvent();
        },

        getHtmlFromUrlCallback: function(html){
            localStorage.yasana_user_collection_partial_view = html;
        },

        compiledTemplate: undefined,

        render: function(){

            var self = this;

            self.timeoutInstance = setInterval(function(){

                if (typeof localStorage.yasana_user_collection_partial_view != "undefined"){
                    if(typeof self.compiledTemplate == 'undefined'){
                        self.$el.empty().append(localStorage.yasana_user_collection_partial_view);
                        self.compiledTemplate = yasana.utils.views.compileTemplate($('#manage-users').html());
                    }

                    self.$el.append(self.compiledTemplate);
                    yasana.utils.Constants.view.nav_link_clicked = $('li#manage-user-link');
                    yasana.utils.views.updateNavLinkActiveClass();
                    clearInterval(self.timeoutInstance);

                    self.collection.fetch({
                        success: function(e){
                            for(var k = 0; k < self.collection.length; k++){
                                var userRowView = new mod.UserRow({model:self.collection.at(k)});
                                userRowView.render();
                            }
                             yasana.utils.views.hideLoading();
                        },
                        error: function(e){
                            yasana.utils.views.hideLoading();
                            toastr.error(e + " error");
                        }
                    });
                }
            }, 3);
        },

        timeoutInstance: undefined

    });

    mod.ManageUserPage.prototype.showForm =function(){
        $(".popup-wrap").empty().append(localStorage.formPopup).show();
        $('.popup-wrap').lightbox_me({ centered: true, lightboxSpeed: "fast" });
        yasana.utils.views.initClosePopupClickEvent();
    }

    mod.UserRow = Backbone.View.extend({

        model: models.User,

        el: '#tbody',

        compiledTemplate: undefined,

        initialize: function(){
            this.compiledTemplate = yasana.utils.views.compileTemplate($('#user-row').html());
        },

        render: function(){
           this.$el.append(this.compiledTemplate({'user': this.model.toJSON()}));
        }
    });

})($, Backbone, _, yasana.collections, yasana.models, yasana.views);
