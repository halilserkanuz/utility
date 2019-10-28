const redis = require('redis');
const config = require('../config.json');
const useragents = config.useragents;

function Helper () {
    console.log("[Helper] --- Helper created ---");
};

Helper.prototype.getRandomUserAgent = function () {
    var self = this;
    return new Promise(function (resolve, reject) {
        try{
            var min = 0;
            var max = useragents.length;
            var index = Math.floor(Math.random() * (max - min + 1)) + min;
            resolve(useragents[index])
        } catch(err){
            reject(err);
        }
        
    });

};

module.exports = Helper;