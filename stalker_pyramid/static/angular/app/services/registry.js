'use strict';

angular.module('app').service('registry', function(){
    /**
     * A PlaceHolder for remotely loaded data that is referencing yet to be
     * loaded data in the local registry.
     *
     * @constructor
     */
    function PlaceHolder(obj_in){
        this.references = [];
        this.$ref = null;
        this.$http = null;
        var self = this;

        this.owner = null;
        this.owner_attr = null;

        // extend it with the given object
        if (obj_in !== undefined){
            for (var i in obj_in){
                if(obj_in.hasOwnProperty(i)){
                    // copy properties
                    self[i] = obj_in[i];
                }
            }
        }

        this.load = function(params){
            if (self.$ref !== null && self.$ref !== undefined){
                // return the Promise object, so on the other side we can use it
                return self.$http({
                    url: self.$ref,
                    method: 'GET',
                    params: params
                }).then(function(response){
                    // for collections replace the list in the owner
                    if (self.owner !== null && self.owner_attr !== null){
                        // also inject a dummy load() function to prevent UI
                        // errors.
                        // response.data.load = function(){};
                        self.owner[self.owner_attr] = response.data;
                    }
                });
            }
        }
    }


    /**
     * Registry is a local database, that holds the partial data that's been
     * queried from the RESTFul service so far. So it is a merging point of
     * data.
     *
     * It's partial in terms of the total elements. That is the registry
     * doesn't have all the data in RESTFul service, unless it is all queried.
     *
     * The main idea is to store and interpret the data in one place, so all
     * the controllers will have a data that is all unique to all of the
     * controllers, allowing controllers to read and modify a unique set of
     * data.
     *
     * This is done mainly with $http interceptors. By intercepting the
     * Requests and Responses, the Registry will read and modify the JSON data
     * coming from the RESTFul service and re-unify them. So any data that is
     * related but come from different Requests will be stored and re-related
     * to each other, allowing to fully replicate the state of the RESTFul
     * service database.
     *
     * @constructor
     */
    function Registry(){
        this.db = {};
        this.$http = null;

        var self = this;
        /**
         * Appends a new object to the registry
         *
         * @param obj: This is a JSON object. The Registry magic will work only if the
         *   object has an ``id`` attribute, which should be unique to all of the data,
         *   which is how Stalker database is designed.
         */
        this.append = function(obj) {
            // console.debug('appending obj with id:', obj.id, obj);
            // Stage 1: Put the object to the Registry

            // if we do not own an object with this id in our local Registry,
            // store the object
            var local_obj;
            if (self.db[obj.id] === undefined){
                // store the initial object in the registry
                // console.debug('no object with id:', obj.id);

                // create a PlaceHolder object
                // if it has both an "id" and a "$ref" attributes
                if (obj.hasOwnProperty('$ref')){
                    obj = new PlaceHolder(obj);
                    obj.$http = self.$http;
                }
                self.db[obj.id] = obj;
            } else {
                // so we already have this object in the registry
                // check if it is a PlaceHolder
                local_obj = self.db[obj.id];
                // console.debug('found object with id:', obj.id, local_obj);
                if (local_obj instanceof PlaceHolder){
                    // console.debug('object is PlaceHolder:', obj.id);
                    // so it is a PlaceHolder
                    // replace any references to this PlaceHolder with the new object
                    var references = local_obj['references'];
                    // iterate over the ``references`` attribute
                    for (var i=0; i < references.length; i++){
                        // replace any references with this object
                        // TODO: this attribute can be a list referencing the obj, check if it is a list
                        references[i]['object'][references[i]['attribute']] = obj;
                    }

                    // check if the object has a $ref attribute
                    if (!obj.hasOwnProperty('$ref')){
                        // it is not a reference update db with this object
                        // now update the registry with this object
                        self.db[obj.id] = obj;
                    } else {
                        // the object has a $ref attribute
                        // so use the local_obj
                        obj = local_obj;
                    }
                } else {
                    // console.debug('object is not PlaceHolder');
                    // so we have it in the database already
                    // we should update the information with the one coming from the
                    // RESTFul service
                    // console.debug('obj is not a placeholder:', local_obj);
                    if (!local_obj.hasOwnProperty('$ref')){
                        // this is still a reference, hence the ``$ref`` attr
                        // so keep it instead of the obj
                        obj = local_obj;
                    }
                }
            }

            // Stage 2: iterate over incoming object attributes
            //
            // Replace any references to other objects with the local ones, or
            // create PlaceHolders to temporarily represent the referenced objects.
            // So we will be able to track the references to the real objects and
            // replace them later on when we have loaded that object from the
            // RESTFul service
            for (var attr_name in obj){
                // skip if this is an inherited attribute
                if (!obj.hasOwnProperty(attr_name)) continue;

                var attr_value = obj[attr_name];

                // skip strings, numbers and null objects
                if (typeof(attr_value) === 'object' && attr_value !== null){
                    // console.debug('append | iterating over attribute:', attr_name, attr_value);
                    // it could be an object or a list
                    // check if it has an id attribute
                    if (attr_value.hasOwnProperty('id')){
                        // then it is an object
                        obj[attr_name] = self.append_related(attr_value, obj, attr_name);
                    } else if(attr_value.hasOwnProperty('$ref')){
                        // it doesn't have an id attribute but has a $ref attribute
                        // then this is a reference to a lazy-load list

                        if (!(attr_value instanceof PlaceHolder)) {
                            attr_value = new PlaceHolder(attr_value);
                        }
                        attr_value.owner = obj;
                        attr_value.owner_attr = attr_name;
                        attr_value.$http = self.$http;
                        obj[attr_name] = attr_value;

                        // console.debug('attr_name:', attr_name);
                        // obj['_' + attr_name] = attr_value;
                        // // create a property
                        // Object.defineProperty(obj, attr_name, {
                        //     get: function() {
                        //         console.debug('this is a getter:', attr_name);
                        //         return obj['_' + attr_name];
                        //     },
                        //     set: function(value) { obj['_' + attr_name] = value;}
                        // });


                    }
                }
            }
            return obj;
        };

        /**
         * Appends a new object in relation with another.
         *
         * @param obj
         * @param referencer
         * @param referencer_attr
         */
        this.append_related = function(obj, referencer, referencer_attr){
            // console.debug('append_related | obj with id:', obj.id, obj);
            if (obj.hasOwnProperty('id') && obj.id !== null){
                // this is a valid object
                // try to get it from the Registry database
                var local_object = this.db[obj.id];

                if (local_object === undefined) {
                    // console.debug('append_related | no obj in database with id:', obj.id);
                    // we do not have the data so store it as a PlaceHolder
                    local_object = new PlaceHolder(obj);
                    local_object.$http = self.$http;
                    // console.debug('append_related | converted it to a PlaceHolder:', local_object);

                    // update the Registry with this PlaceHolder
                    this.db[obj.id] = local_object;
                }

                if (local_object instanceof PlaceHolder) {
                    // console.debug('append_related | local_obj is a PlaceHolder:', local_object);
                    // store the original object as a referencer of this
                    // PlaceHolder, so later when we load the real object
                    // we can replace it correctly
                    // console.debug('updating referencer.referencer_attr:', referencer_attr, referencer);
                    local_object.references.push({
                        object: referencer,
                        attribute: referencer_attr
                    });
                }

                // return the local object that is created or found in the
                // Registry
                return local_object;
            }
        };
    }

    return new Registry();
});