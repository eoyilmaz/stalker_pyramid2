// Stalker Pyramid a Web Based Production Asset Management System
// Copyright (C) 2009-2017 Erkan Ozgur Yilmaz
//
// This file is part of Stalker Pyramid.
//
// Stalker Pyramid is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// any later version.
//
// Stalker Pyramid is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Stalker Pyramid.  If not, see <http://www.gnu.org/licenses/>.

'use strict';
var app = angular.module('app', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngTouch',
    'ngStorage',
    'ui.router',
    'ncy-angular-breadcrumb',
    'ui.bootstrap',
    'ui.utils',
    'oc.lazyLoad'
]);

app.controller('MainController', [function(){}]);

/**
 * create interceptors to interpret all incoming data and register them in the
 * main $rootScope.Registry.db
 */
app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.interceptors.push(
        function ($q, $rootScope) {
            return {
                'response': function(response) {
                    // store any data that is coming from the RESTFul Service
                    // which the url starts with '/api'
                    if (response.config.url.startsWith('/api') && response.status === 200){
                        console.debug('Incoming data from RESTFul service, updating local Registry!');
                        // console.debug('$httpProvider.interceptors.response:', response);
                        var data = response.data;

                        // update the local registry
                        var reg = $rootScope.reg;

                        if (data.length > 0){
                            for (var i=0; i < data.length; i++){
                                // relate any references to the ones in the local registry
                                // and replace the corresponding data in the Response
                                data[i] = reg.append(data[i]);
                            }
                        } else {
                            data = reg.append(data);
                        }
                        // replace the response.data
                        response.data = data;
                        console.debug(reg.db);
                    }
                    return response;
                }
            }
        }
    );
}]);

/**
 * create the main Registry
 */
app.run(['$rootScope', '$http', 'registry', function($rootScope, $http, registry){
    // Create the main registry
    console.debug('Creating main Registry!');
    var reg = registry;
    reg.$http = $http;
    $rootScope.reg = reg;
}]);
