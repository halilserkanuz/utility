const redis = require('redis');
const config = require('../config.json');
const redisConfig = config.redis;

function RedisHelper () {
    this.client = redis.createClient(redisConfig);
    console.log("[RedisHelper] --- Client created ---");
};

RedisHelper.prototype.pop = function (queue, count=1) {
    var self = this;
    return new Promise(function (resolve, reject) {
        self.client.spop(key=queue, count=count, function(err, res){
            if(err) {
                console.log("[RedisHelper] --- Error Occured: ---"); //TODO: Logging operation gonna add.
                reject(err);
            }
            console.log("[RedisHelper] --- Object getting ---");
            if (res!==null) {
                resolve(res);
            } else {
                throw `[RedisHelper] --- No object within ${queue} ---`
            }
            
        });
    });

};

RedisHelper.prototype.add = function (queue, str) {
    var self = this;
    return new Promise(function (resolve, reject) {
        self.client.sadd(queue, str, function(err, res){
            if(err) {
                console.log("[RedisHelper] --- Error Occured: ---")
                reject(err);
            }
            console.log("[RedisHelper] --- Object adding ---");
            resolve(res);
        });
    });

};

RedisHelper.prototype.keys = function (pattern) {
    var self = this;
    return new Promise(function (resolve, reject) {
        self.client.keys(pattern, function(err, res){
            if(err) {
                console.log("[RedisHelper] --- Error Occured: ---"); //TODO: Logging operation gonna add.
                reject(err);
            }
            console.log("[RedisHelper] --- Object getting ---");
            if (res!==null) {
                resolve(res);
            } 
            
        });
    });

};


RedisHelper.prototype.order_queues_get_key = function(pattern) {
    var self = this;
    return new Promise(function(resolve, reject){
        all_keys = self.keys(pattern);
        all_keys.sort();
        var queue_name = all_keys[0];
        var key = self.pop(queue_name);
        resolve(key);
    });

}


module.exports = RedisHelper;

