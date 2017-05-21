'use strict';

app.controller('ProjectCtrl', ['$rootScope', '$scope', '$stateParams', '$http',
    function($rootScope, $scope, $stateParams, $http){
        var project_id = $stateParams['projectid'];
        var self = this;
        self.project = $rootScope.reg.db[project_id];
        self.task_count_in_statuses = {};

        // $http.get('/api/status_lists?target_entity_type=Task').then(function(response){
        //     var task_status_list = response.data[0];
        //     console.debug('task_status_list:', task_status_list);
        //     // load the statuses
        //     var task_status_list_id = task_status_list.id;
        //     task_status_list.load().then(function(){
        //         task_status_list = $rootScope.reg.db[task_status_list_id];
        //         console.debug('task_status_list:', task_status_list);
        //         task_status_list.statuses.load().then(function(){
        //             // this is soo deep
        //             console.debug('task_status_list.statuses:', task_status_list.statuses);
        //             for (var i=0; i < task_status_list.statuses.length; i++){
        //                 var status = task_status_list.statuses[i];
        //                 console.debug('status:', status);
        //                 try{
        //                     status.load();
        //                 } catch(e){
        //                     console.debug(e);
        //                 }
        //             }
        //             console.debug($rootScope.reg.db);
        //         })
        //     });
        // });

        // the project may not be loaded from the RESTFul service yet!
        if (self.project === undefined){
            // so load it from the RESTFul service
            $http.get('/api/projects/' + project_id).then(function (response){
                self.project = response.data;
            });
        } else {
            // check if it is a PlaceHolder
            if (self.project.hasOwnProperty('$ref')){
                // please load the data
                self.project.load().then(function(){
                    // replace the current project from registry again
                    self.project = $rootScope.reg.db[project_id];
                });
            }
        }
    }
]);