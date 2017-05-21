'use strict';

app.controller('UserCtrl', ['$rootScope', '$scope', '$http', '$state', '$stateParams',
    function($rootScope, $scope, $http, $state, $stateParams) {
        var user_id = $stateParams['userid'];
        this.user = $rootScope.reg.db[user_id];
        var self = this;

        // the user may not be loaded from the RESTFul service yet!
        if (self.user === undefined) {
            // load the data from the RESTFul service
            $http.get('/api/users/' + user_id).then(function (response) {
                self.user = $rootScope.reg.db[user_id];
            });
        } else {
            // check if it is a PlaceHolder
            if (self.user.hasOwnProperty('$ref')){
                // please load the data
                self.user.load().then(function(){
                    // replace the current user from the registry again
                    self.user = $rootScope.reg.db[user_id];
                });
            }
        }
    }
]);

app.controller('LoggedInUserController', ['$rootScope', '$scope', '$http',
    function($rootScope, $scope, $http){
        this.user = $rootScope.logged_in_user;
        var self = this;
        // the user may not be loaded from the RESTFul service yet!
        if (self.user === undefined) {
            $http.get('/api/logged_in_user').then(function (response) {
                // update logged_in_user info in the $rootScope
                $rootScope.logged_in_user = response.data;
                self.user = $rootScope.logged_in_user;
            });
        } else {
            // so we have a user object
            // check if it is a PlaceHolder
            if ($scope.user.hasOwnProperty('$ref')){
                // please load the data
                var user_id = $scope.user.id;
                self.user.load().then(function(){
                    // replace the current user from the registry again
                    $rootScope.logged_in_user = $rootScope.reg.db[user_id];
                    self.user = $rootScope.logged_in_user;
                });
            }
        }
    }
]);