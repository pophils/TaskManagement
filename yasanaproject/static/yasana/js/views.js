
/// <reference path="../vendor/jquery.js" />
/// <reference path="../vendor/backbone.js" />
/// <reference path="../core/utils.js" />
/// <reference path="../models.js" />
/// <reference path="../collections.js" />


window.yasana = window.yasana || {};
yasana.views = yasana.views || {};

(function($, Backbone, _, collections, models, mod){

    mod.HomePage = Backbone.View.extend({

        el: ".main-content",

        initialize: function(){
            if($('#is_admin_user').length > 0){
                this.checkIsAdmin(true);
            }
            this.compiledTemplate = yasana.utils.views.compileTemplate($('#dashboard').html());
        },

        checkIsAdmin: function (isAdmin) {

             if(isAdmin){
                    yasana.utils.Constants.view.is_admin_login =true;
                }
                else{
                    yasana.utils.Constants.view.is_admin_login = false;
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

            if(yasana.utils.Constants.view.is_admin_login){
                 yasana.utils.views.getJsonFromUrl(yasana.utils.Constants.url.get_landing_task_summary,
                     {is_admin:1}, this.renderCallback)
            }
            else{
                yasana.utils.views.getJsonFromUrl(yasana.utils.Constants.url.get_landing_task_summary,
                    {is_admin:0}, this.renderCallback)
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
            yasana.utils.views.hideLoading();
        }
    });

    mod.ManageUserPage = Backbone.View.extend({

        model: models.User,

        el: ".main-content",

        collection: collections.UserCollections,

        events: {
            'click #new-user-btn' : 'loadNewUserForm',
            'click #load-more-user-btn' : 'loadMoreUsers'
        },

        initialize: function(){

            yasana.utils.views.getJsonFromUrl(yasana.utils.Constants.url.get_total_users,
                this.getTotalUserCallback);

            if(typeof localStorage.yasana_user_collection_partial_view == 'undefined'){
                yasana.utils.views.getHtmlFromUrl(yasana.utils.Constants.url.get_user_collection_partial_view,
                this.getHtmlFromUrlCallback);
            }
            yasana.utils.Constants.view.get_users_page_no = 0;
        },

        loadNewUserForm : function(){
            if(typeof this.newUserViewForm == 'undefined'){
                this.newUserViewForm =  new mod.NewUserForm({model: new models.User()});
            }
            this.newUserViewForm.render();
        },

        newUserViewForm : undefined,

        getHtmlFromUrlCallback: function(html){
            localStorage.yasana_user_collection_partial_view = html;
        },

        getTotalUserCallback: function(jsonMessage){
            yasana.utils.Constants.view.current_total_users = parseInt(jsonMessage.num_of_users);
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
                            yasana.utils.Constants.view.get_users_page_no += self.collection.length;

                            if(yasana.utils.Constants.view.current_total_users <= self.collection.length){
                                yasana.utils.views.hideLoadMoreBtn();
                            }
                        },
                        error: function(e){
                            yasana.utils.views.hideLoading();
                            toastr.error(e + " error");
                        }
                    });
                }
            }, 3);
        },

        timeoutInstance: undefined,

        loadMoreUsers: function(){
             this.collection.url = yasana.utils.Constants.url.get_user_collection +
                 yasana.utils.Constants.view.get_users_page_no;

             var self = this;

             this.collection.fetch({
                        success: function(e){
                            for(var k = 0; k < self.collection.length; k++){
                                var userRowView = new mod.UserRow({model:self.collection.at(k)});
                                userRowView.render();
                            }

                            yasana.utils.Constants.view.get_users_page_no += self.collection.length;

                             if(self.collection.length == 0){
                                 toastr.info('No more user exist.');
                                 yasana.utils.views.hideLoadMoreBtn();
                            }
                        },
                        error: function(e){
                            toastr.error(e + " error");
                        }
                    });
        }

    });

    mod.UserRow = Backbone.View.extend({

        model: models.User,

        el: '#tbody',

        compiledTemplate: undefined,

        initialize: function(){
            this.compiledTemplate = yasana.utils.views.compileTemplate($('#user-row').html());
        },

        render: function(){
           this.$el.append(this.compiledTemplate({'user': this.model.toJSON()}));
        },

        renderFirst: function () {
            this.$el.prepend(this.compiledTemplate({'user': this.model.toJSON()}));
        }
    });

    mod.NewUserForm = Backbone.View.extend({

        model: models.User,

        el: '.popup-wrap',

        events: {
            'click #submit-user':'submitUserForm'
        },

        submitUserForm: function(ev){

            ev.preventDefault();
            var self = this;

            toastr.info('Saving form...');
            var data = $(".popup-wrap form").serialize();

            $.post("/api/new-user/", data, function (jsonMessage) {
                if (jsonMessage.save_status == true) {
                    toastr.success('User saved successfully.');

                    //update full name
                    var first_name = $(".popup-wrap #first_name").val();
                    var last_name = $(".popup-wrap #last_name").val();
                    var other_name = $(".popup-wrap #other_name").val();
                    var full_name = "";

                    if(last_name.length > 0){
                        full_name = last_name.substring(0, 1).toUpperCase() + last_name.substring(1) + ", ";
                    }

                    if(first_name.length > 0){
                        full_name += first_name.substring(0, 1).toUpperCase() + first_name.substring(1) + " ";
                    }

                    if(other_name.length > 0){
                        full_name += other_name.substring(0, 1).toUpperCase() + other_name.substring(1);
                    }

                    self.model.set('name', full_name);

                    new mod.UserRow({model:self.model}).renderFirst();
                    yasana.utils.Constants.view.get_users_page_no += 1;
                    yasana.utils.views.closePopup();
                }
                else {
                    toastr.error(jsonMessage.save_status);
                    console.log(jsonMessage.save_status);
                }
            });
        },

        initialize: function(){
             if(typeof localStorage.formPopup == "undefined"){
                yasana.utils.views.getHtmlFromUrl(yasana.utils.Constants.url.get_add_user_partial_view,
                this.loadNewUserFormCallback);
            }
        },

        loadNewUserFormCallback: function(template){
            var ss = jQuery("<div/>").append(template);
            localStorage.formPopup = $(ss).html();
        },

        bindings: {
            '#full_name' : 'name',
            '#email': 'email',
            '#department' : 'department',
            '#phone' : 'phone'
        },

        render: function(){

            var self = this;

            self.timeoutInstance = setInterval(function(){
                if (typeof localStorage.formPopup != "undefined"){
                    self.$el.empty().append(localStorage.formPopup).show();
                    self.$el.lightbox_me({ centered: true, lightboxSpeed: "fast" });
                    yasana.utils.views.initClosePopupClickEvent();
                    clearInterval(self.timeoutInstance);
                    self.stickit();
                }
            }, 3);
        },

        timeoutInstance: undefined
    });

})($, Backbone, _, yasana.collections, yasana.models, yasana.views);
