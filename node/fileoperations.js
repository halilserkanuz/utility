const fs = require('fs');
const config = require('../config.json');

function FileOperationHelper () {
    console.log("[Helper] --- Helper created ---");
};

FileOperationHelper.prototype.read_file_to_json = function (file_name) {
    var self = this;
    return new Promise(function (resolve, reject) {
        try{
            var rawdata = fs.readFileSync(file_name);
            var jsondata = JSON.parse(rawdata);
            resolve(jsondata)
        } catch(err){
            reject(err);
        }
        
    });

};

FileOperationHelper.prototype.write_json_to_file = function (file_name, obj) {
    var self = this;
    return new Promise(function (resolve, reject) {
        try{
            var rawdata = JSON.stringify(obj);
            fs.writeFile(file_name, rawdata, (error)=>{
                console.log(error);
            });
            resolve(file_name)
        } catch(err){
            reject(err);
        }
        
    });

};

FileOperationHelper.prototype.append_text_to_file = function (file_name, text) {
    var self = this;
    return new Promise(function (resolve, reject) {
        try{
            console.log(text);
            fs.appendFileSync(file_name, text);
            resolve(file_name)
        } catch(err){
            reject(err);
        }
        
    });

};

FileOperationHelper.prototype.delete_file = function (file_name) {
    var self = this;
    return new Promise(function (resolve, reject) {
        try{
            
            fs.unlink(file_name, (error)=>{
                console.log(error);
            });
            resolve('removed file')
        } catch(err){
            reject(err);
        }
        
    });

};



module.exports = FileOperationHelper;