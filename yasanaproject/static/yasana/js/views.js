
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
            'click #load-more-btn' : 'loadMoreUsers',
            'click .btn.btn-primary' : 'editUser',
            'click .btn.btn-danger' : 'deleteUser'
        },

        editUser: function(ev){

            var email = $(ev.target).parent().parent().find('.stickit_email').text();
            var modelTobeEdited = yasana.utils.Constants.view.current_user_collection.get(email);
            var editUserView = new mod.EditUserForm({model: modelTobeEdited, btnTarget: ev.target});
            yasana.utils.views.unbindPopupViewEvent(editUserView);
            editUserView.render();
        },

        deleteUser: function(ev){
            var email = $(ev.target).parent().parent().find('.stickit_email').text();
            var modelTobeEdited = yasana.utils.Constants.view.current_user_collection.get(email);

             $.ajax({
                url:'/api/users/',
                type: 'DELETE',
                data: {email: email},
                success: function(jsonMessage){
                    if (jsonMessage.save_status == true) {
                        toastr.success('User deleted successfully.');

                        yasana.utils.Constants.view.get_users_page_no -= 1;
                        yasana.utils.Constants.view.current_user_collection.remove(modelTobeEdited);
                        modelTobeEdited = undefined;

                        $(ev.target).parent().parent().remove();
                    }
                    else {
                        toastr.error(jsonMessage.save_status);
                        console.log(jsonMessage.save_status);
                    }
                },
                error: function(){

                }

            });

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

        loadNewUserForm : function(event){

            if(event.preventDefault){
                event.preventDefault();
            }
            else{
                event.returnValue = false;
            }

            var newUserViewForm =  new mod.NewUserForm({model: new models.User()});
            yasana.utils.views.unbindPopupViewEvent(newUserViewForm);
            newUserViewForm.render();
        },

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
                            if(self.collection.length > 0){
                                for(var k = 0; k < self.collection.length; k++){
                                    var userRowView = new mod.UserRow({model:self.collection.at(k)});
                                    userRowView.render();
                                }
                                yasana.utils.Constants.view.get_users_page_no += self.collection.length;
                                if(yasana.utils.Constants.view.current_total_users <= self.collection.length){
                                    yasana.utils.views.hideLoadMoreBtn();
                                }
                                yasana.utils.Constants.view.current_user_collection = self.collection;
                            }
                            else{
                                yasana.utils.views.displayNoItem();
                                yasana.utils.views.hideLoadMoreBtn();
                            }

                            yasana.utils.views.hideLoading();
                        },
                        error: function(e){
                            yasana.utils.views.hideLoading();
                            yasana.utils.views.hideLoadMoreBtn();
                            yasana.utils.views.displayNoItem();
                            toastr.error(e + " error");
                        }
                    });
                }
            }, 3);
        },

        timeoutInstance: undefined,

        loadMoreUsers: function(){

             var new_coll = new collections.UserCollections();

            new_coll.url = yasana.utils.Constants.url.get_user_collection + yasana.utils.Constants.view.get_users_page_no;
            new_coll.fetch({
                        success: function(e){

                            for(var k = 0; k < new_coll.length; k++){
                                var userRowView = new mod.UserRow({model:new_coll.at(k)});
                                userRowView.render();
                                if(typeof yasana.utils.Constants.view.current_user_collection == "undefined"){
                                    yasana.utils.Constants.view.current_user_collection = new collections.UserCollections();
                                }

                                yasana.utils.Constants.view.current_user_collection.push(userRowView.model);
                            }

                            yasana.utils.Constants.view.get_users_page_no += new_coll.length;

                             if(new_coll.length == 0){
                                 toastr.info('No more user exist.');
                                 yasana.utils.views.hideLoadMoreBtn();
                            }
                            delete new_coll
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

            var first_name = this.model.get('first_name');
            if (yasana.utils.helpers.validateRequired(first_name) == false){

                toastr.error('Please enter the first name.');
                return;
            }

            if ( this.model.get('phone').length > 0 && yasana.utils.helpers.validatePhone(this.model.get('phone'))
                == false){
                toastr.error('Please enter a valid phone number');
                return;
            }

            self.model.set('gender', self.$el.find("#gender").val());

             if (yasana.utils.helpers.validateGender(this.model.get('gender')) == false){
                toastr.error('Please select a valid gender');
                return;
            }

             if (yasana.utils.helpers.validateEmail(this.model.get('email')) == false){
                toastr.error('Please enter a valid email');
                return;
            }

            var password = self.$el.find("#password").val();
            var confirmPassword = self.$el.find("#confirm_password").val();

             if (yasana.utils.helpers.validatePassword(password) == false){
                toastr.error('Password is required');
                return;
            }

             if (yasana.utils.helpers.validateConfirmPassword(confirmPassword) == false){
                toastr.error('Confirm Password is required');
                return;
            }

             if (yasana.utils.helpers.validatePasswordMatch(password, confirmPassword) == false){
                toastr.error('Password does not match');
                return;
            }

            toastr.info('Saving form...');
            var data = $(".popup-wrap form").serialize();

            $.post("/api/new-user/", data, function (jsonMessage) {
                if (jsonMessage.save_status == true) {
                    toastr.success('User saved successfully.');

                    //update full name
                        var last_name = self.model.get('last_name'); // $(".popup-wrap #last_name").val();
                        var other_name = self.model.get('other_name'); //$(".popup-wrap #other_name").val();
                        var department = self.model.get('department'); // $(".popup-wrap #department").val();
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

                        if(department.length > 0){
                            department = department.substring(0, 1).toUpperCase() + department.substring(1);
                        }

                        self.model.set('department', department);

                    self.model.set('name', full_name);

                    new mod.UserRow({model:self.model}).renderFirst();
                    yasana.utils.Constants.view.get_users_page_no += 1;
                    yasana.utils.views.closePopup();
                    if(typeof yasana.utils.Constants.view.current_user_collection == "undefined"){
                        yasana.utils.Constants.view.current_user_collection = new collections.UserCollections();
                    }
                    yasana.utils.Constants.view.current_user_collection.push(self.model);
                    // dereferencing the formPopup will allow a new form with a new csrf token to be fetched
                    delete localStorage.formPopup;

                }
                else {
                    errorMessages = '';
                    _.forEach(jsonMessage.save_status, function(error){
                        errorMessages += error +'/n';
                    });
                     toastr.error(errorMessages);
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
            '#email': 'email',
            '#department' : 'department',
            '#phone' : 'phone',
            '#first_name' : 'first_name',
            '#other_name' : 'other_name',
            '#last_name' : 'last_name',
            '#website': 'website'
        },

        render: function(){

            var self = this;

            self.timeoutInstance = setInterval(function(){
                if (typeof localStorage.formPopup != "undefined"){
                    self.$el.empty().append(localStorage.formPopup).show();
                    $('.popup-header-text').text('Add User');
                    self.$el.lightbox_me({ centered: true, lightboxSpeed: "fast" });
                    yasana.utils.views.initClosePopupClickEvent();
                    clearInterval(self.timeoutInstance);
                    self.stickit();
                }
            }, 3);
        },

        timeoutInstance: undefined
    });

    mod.EditUserForm = Backbone.View.extend({

        model: models.User,

        el: '.popup-wrap',

        events: {
            'click #submit-user':'submitUserForm'
        },

        submitUserForm: function(ev){
            ev.preventDefault();

            var self = this;

            var first_name = this.model.get('first_name');
            if (yasana.utils.helpers.validateRequired(first_name) == false){

                toastr.error('Please enter the first name.');
                return;
            }

            if ( this.model.get('phone').length > 0 && yasana.utils.helpers.validatePhone(this.model.get('phone'))
                == false){
                toastr.error('Please enter a valid phone number');
                return;
            }

            self.model.set('gender', self.$el.find("#gender").val());

             if (yasana.utils.helpers.validateGender(this.model.get('gender')) == false){
                toastr.error('Please select a valid gender');
                return;
            }

           toastr.info('Updating form...');

           var data = $(".popup-wrap form").serialize();
            $.ajax({
                url:'/api/users/',
                type: 'PUT',
                data: data,
                success: function(jsonMessage){
                    if (jsonMessage.save_status == true) {
                        toastr.success('User updated successfully.');

                        //update values on grid
                        var first_name = self.model.get('first_name');
                        var last_name = self.model.get('last_name');
                        var other_name = self.model.get('other_name');
                        var department = self.model.get('department');
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

                        if(department.length > 0){
                            department = department.substring(0, 1).toUpperCase() + department.substring(1);
                        }

                        self.model.set('name', full_name);
                        self.model.set('gender',$(".popup-wrap #gender").val());

                        $(self.btnTarget).parent().parent().find('.stickit_name').text(full_name);
                        $(self.btnTarget).parent().parent().find('.stickit_department').text(department);
                        $(self.btnTarget).parent().parent().find('.stickit_phone').text($(".popup-wrap #phone").val());

                        yasana.utils.views.closePopup();
                        delete localStorage.formPopup;
                    }
                    else {
                         errorMessages = '';
                    _.forEach(jsonMessage.save_status, function(error){
                        errorMessages += error +'/n';
                    });
                     toastr.error(errorMessages);
                    }
                },
                error: function(){

                }

            });

        },

        initialize: function(options){
            _.extend(this, _.pick(options, "btnTarget"));
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
            '#email': 'email',
            '#department' : 'department',
            '#phone' : 'phone',
            '#first_name' : 'first_name',
            '#other_name' : 'other_name',
            '#last_name' : 'last_name',
            '#website': 'website'
        },

        render: function(){

            var self = this;

            self.timeoutInstance = setInterval(function(){
                if (typeof localStorage.formPopup != "undefined"){
                    self.$el.empty().append(localStorage.formPopup).show();
                    self.$el.find('hr').remove();
                    self.$el.find('#password').remove();
                    self.$el.find('#confirm_password').remove();
                     $('.popup-header-text').text('Edit User');
                    self.$el.find('#email').hide();
                    self.$el.find("#gender").val(self.model.get('gender'));
                    self.$el.lightbox_me({ centered: true, lightboxSpeed: "fast" });
                    yasana.utils.views.initClosePopupClickEvent();
                    clearInterval(self.timeoutInstance);
                    self.stickit();
                }
            }, 3);
        },

        timeoutInstance: undefined
    });

    mod.PendingTaskPage = Backbone.View.extend({

        model: models.Task,

        el: ".main-content",

        collection: collections.PendingTaskCollections,

        events: {
            'click #new-task-btn' : 'loadNewTaskForm'
           // 'click #load-more-btn' : 'loadMoreUsers',
            //'click .btn.btn-primary' : 'editUser',
            //'click .btn.btn-danger' : 'deleteUser'
        },

        //editUser: function(ev){
        //
        //    var email = $(ev.target).parent().parent().find('.stickit_email').text();
        //    var modelTobeEdited = yasana.utils.Constants.view.current_user_collection.get(email);
        //    var editUserView = new mod.EditUserForm({model: modelTobeEdited, btnTarget: ev.target});
        //    yasana.utils.views.unbindPopupViewEvent(editUserView);
        //    editUserView.render();
        //},
        //
        //deleteUser: function(ev){
        //    var email = $(ev.target).parent().parent().find('.stickit_email').text();
        //    var modelTobeEdited = yasana.utils.Constants.view.current_user_collection.get(email);
        //
        //     $.ajax({
        //        url:'/api/users/',
        //        type: 'DELETE',
        //        data: {email: email},
        //        success: function(jsonMessage){
        //            if (jsonMessage.save_status == true) {
        //                toastr.success('User deleted successfully.');
        //
        //                yasana.utils.Constants.view.get_users_page_no -= 1;
        //                yasana.utils.Constants.view.current_user_collection.remove(modelTobeEdited);
        //                modelTobeEdited = undefined;
        //
        //                $(ev.target).parent().parent().remove();
        //            }
        //            else {
        //                toastr.error(jsonMessage.save_status);
        //                console.log(jsonMessage.save_status);
        //            }
        //        },
        //        error: function(){
        //
        //        }
        //
        //    });
        //
        //},

        initialize: function(){

            yasana.utils.views.getJsonFromUrl(yasana.utils.Constants.url.get_total_pending_tasks,
                this.getTotalTaskCallback);

            if(typeof localStorage.yasana_pending_task_collection_partial_view == 'undefined'){
                yasana.utils.views.getHtmlFromUrl(yasana.utils.Constants.url.get_pending_task_collection_partial_view,
                this.getHtmlFromUrlCallback);
            }
            yasana.utils.Constants.view.get_task_page_no = 0;
        },

        loadNewTaskForm : function(event){

            if(event.preventDefault){
                event.preventDefault();
            }
            else{
                event.returnValue = false;
            }

            var newTaskViewForm =  new mod.NewTaskForm({model: new models.Task()});
            yasana.utils.views.unbindPopupViewEvent(newTaskViewForm);
            newTaskViewForm.render();
        },

        getHtmlFromUrlCallback: function(html){
            localStorage.yasana_pending_task_collection_partial_view = html;
        },

        getTotalTaskCallback: function(jsonMessage){
            yasana.utils.Constants.view.current_total_tasks = parseInt(jsonMessage.num_of_tasks);
        },

        compiledTemplate: undefined,

        render: function(){

            var self = this;

            self.timeoutInstance = setInterval(function(){

                if (typeof localStorage.yasana_pending_task_collection_partial_view != "undefined"){
                    if(typeof self.compiledTemplate == 'undefined'){
                        self.$el.empty().append(localStorage.yasana_pending_task_collection_partial_view);
                        self.compiledTemplate = yasana.utils.views.compileTemplate($('#task-template').html());
                    }

                    self.$el.append(self.compiledTemplate);
                    yasana.utils.Constants.view.nav_link_clicked = $('li#pending-task-link');
                    yasana.utils.views.updateNavLinkActiveClass();
                    clearInterval(self.timeoutInstance);

                    self.collection.fetch({
                        success: function(e){

                            if(self.collection.length > 0){
                                for(var k = 0; k < self.collection.length; k++){
                                    var taskRowView = new mod.TaskRow({model:self.collection.at(k)});
                                    taskRowView.render();
                                }
                                yasana.utils.Constants.view.get_task_page_no += self.collection.length;
                                if(yasana.utils.Constants.view.current_total_tasks <= self.collection.length){
                                    yasana.utils.views.hideLoadMoreBtn();
                                }
                            yasana.utils.Constants.view.current_task_collection = self.collection;
                            }
                            else{
                                yasana.utils.views.displayNoItem();
                                yasana.utils.views.hideLoadMoreBtn();
                            }


                            yasana.utils.views.hideLoading();

                        },
                        error: function(e){
                            yasana.utils.views.hideLoading();
                            toastr.error(e + " error");
                            yasana.utils.views.displayNoItem();
                            yasana.utils.views.hideLoadMoreBtn();
                        }
                    });
                }
            }, 3);
        },

        timeoutInstance: undefined

        //loadMoreUsers: function(){
        //
        //     var new_coll = new collections.UserCollections();
        //
        //    new_coll.url = yasana.utils.Constants.url.get_user_collection + yasana.utils.Constants.view.get_users_page_no;
        //    new_coll.fetch({
        //                success: function(e){
        //
        //                    for(var k = 0; k < new_coll.length; k++){
        //                        var userRowView = new mod.UserRow({model:new_coll.at(k)});
        //                        userRowView.render();
        //                        if(typeof yasana.utils.Constants.view.current_user_collection == "undefined"){
        //                            yasana.utils.Constants.view.current_user_collection = new collections.UserCollections();
        //                        }
        //
        //                        yasana.utils.Constants.view.current_user_collection.push(userRowView.model);
        //                    }
        //
        //                    yasana.utils.Constants.view.get_users_page_no += new_coll.length;
        //
        //                     if(new_coll.length == 0){
        //                         toastr.info('No more user exist.');
        //                         yasana.utils.views.hideLoadMoreBtn();
        //                    }
        //                    delete new_coll
        //                },
        //                error: function(e){
        //                    toastr.error(e + " error");
        //                }
        //            });
        //}

    });

    mod.TaskRow = Backbone.View.extend({

        model: models.Task,

        el: '#tbody',

        compiledTemplate: undefined,

        initialize: function(){
            this.compiledTemplate = yasana.utils.views.compileTemplate($('#task-row').html());
        },

        render: function(){
           this.$el.append(this.compiledTemplate({'task': this.model.toJSON()}));
        },

        renderFirst: function () {
            this.$el.prepend(this.compiledTemplate({'task': this.model.toJSON()}));
        }
    });

    mod.NewTaskForm = Backbone.View.extend({

        model: models.Task,

        el: '.popup-wrap',

        events: {
            'click #submit-task':'submitTaskForm'
        },

        submitTaskForm: function(ev){

            ev.preventDefault();
            var self = this;

            if (yasana.utils.helpers.validateRequired(this.model.get('title')) == false){

                toastr.error('Please enter the title.');
                return;
            }

            if (yasana.utils.helpers.validateRequired(this.model.get('details')) == false){

                toastr.error('Please enter the details.');
                return;
            }

            this.model.set('priority', this.$el.find("#priority").val());
             if (yasana.utils.helpers.validateTaskPriority(this.model.get('priority')) == false){
                toastr.error('Please select a valid priority.');
                return;
            }

            toastr.info('Saving form...');
            var data = $(".popup-wrap form").serialize();

            $.post("/api/tasks/", data, function (jsonMessage) {
                if (jsonMessage.save_status == true) {
                    toastr.success('Task saved successfully.');
                    var title = self.model.get('title');
                    title = title.substring(0, 1).toUpperCase() + title.substring(1);

                    self.model.set('title', title);
                    self.model.set('id', jsonMessage.id);

                    new mod.TaskRow({model:self.model}).renderFirst();
                    yasana.utils.Constants.view.get_task_page_no += 1;
                    yasana.utils.views.closePopup();
                    if(typeof yasana.utils.Constants.view.current_task_collection == "undefined"){
                        yasana.utils.Constants.view.current_task_collection = new collections.PendingTaskCollections();
                    }
                    yasana.utils.Constants.view.current_task_collection.push(self.model);
                    // dereferencing the taskFormPopup will allow a new form with a new csrf token to be fetched
                    delete localStorage.taskFormPopup;

                }
                else {
                    errorMessages = '';
                    _.forEach(jsonMessage.save_status, function(error){
                        errorMessages += error +'/n';
                    });
                     toastr.error(errorMessages);
                }
            });
        },

        initialize: function(){
             if(typeof localStorage.taskFormPopup == "undefined"){
                yasana.utils.views.getHtmlFromUrl(yasana.utils.Constants.url.get_add_task_partial_view,
                this.loadNewTaskFormCallback);
            }
        },

        loadNewTaskFormCallback: function(template){
            var _template = jQuery("<div/>").append(template);
            localStorage.taskFormPopup = $(_template).html();
        },

        bindings: {
            '#title': 'title',
            '#details' : 'details',
            '#expected_end_date' : 'expected_end_date',
            '#start_date' : 'start_date'
        },

        render: function(){

            var self = this;

            self.timeoutInstance = setInterval(function(){
                if (typeof localStorage.taskFormPopup != "undefined"){
                    self.$el.empty().append(localStorage.taskFormPopup).show();
                    $('.popup-header-text').text('Add Task');
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
