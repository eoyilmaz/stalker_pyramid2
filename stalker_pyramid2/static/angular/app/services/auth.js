(function(window, angular, undefined) {

'use strict';

angular.module('app')
.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.interceptors.push(
        function ($q, $rootScope) {
            return {
                'responseError': function error(response) {
                    if ((response.status == 403) ||
                        ((response.config.method === 'JSONP') && (response.status === 0))) {
                        var deferred = $q.defer();
                        $rootScope.failed_requests.push({
                            config: response.config,
                            deferred: deferred
                        });
                        $rootScope.$broadcast('event:loginRequired');
                        return deferred.promise;
                    } else {
                        return response;
                    }
                }
            }
        }
    );
}])
.run(['$rootScope', '$compile', '$http', '$modal', '$q',
    function ($rootScope, $compile, $http, $modal, $q) {
        $rootScope.failed_requests = [];

        // to prevent showing multiple modal dialogs
        $rootScope.currently_logging_in = false;

        var m; // slot for modal

        $rootScope.$on('event:loginRequired', function () {
            // prevent showing multiple modal dialogs
            if(!$rootScope.currently_logging_in){
                console.debug('currently not logging in');
                m = $modal.open({
                    backdrop: false,
                    keyboard: false,
                    templateUrl: 'templates/angular/auth/login.html',
                    controller: function (){
                        $rootScope.currently_logging_in = true;
                        var scope = this;
                        this.user_id = '';
                        this.password = '';
                        this.errorMessage = '';
                        this.login = function () {
                            var params = {
                                login: scope.user_id,
                                password: scope.password
                            };
                            $http({method: 'POST', url: '/api/login', params: params})
                            .then(function successCallback(response) {
                                // window.console.debug('data', data);
                                // window.console.debug('config', config);
                                var data = response.data;
                                if (data.id !== undefined) {
                                    $rootScope.logged_in_user = data;
                                    $rootScope.$broadcast('event:loginSuccess');
                                } else {
                                    scope.errorMessage = 'Invalid login or password';
                                }
                            }, function errorCallback() {
                                scope.errorMessage = 'Backend problem login in. Contact IT.';
                                $rootScope.$broadcast('event:loginRequired');
                            });
                        };
                    },
                    controllerAs: 'loginCtrl'
                });
            }
        });

        $rootScope.$on('event:loginSuccess', function () {
            m.close();
            $rootScope.currently_logging_in = false;
            for (var i = 0; i < $rootScope.failed_requests.length; i++) {
                var request = $rootScope.failed_requests[i];
                $http(request.config).then(function (response) {
                    request.deferred.resolve(response);
                });
            }
            $rootScope.failed_requests = [];
        });
    }
]);

})(window, window.angular);