const mysql = require('mysql');

const config = require('../config.json');



function MySQLHelper (db="default_db") {

    const mySQLConfig = config[db];
    this.con = mysql.createConnection({
        host: mySQLConfig.host,
        port: mySQLConfig.port,
        user: mySQLConfig.user,
        password: mySQLConfig.password,
        database: mySQLConfig.database
      });
      console.log('[MySQLHelper] ---  Succesfully created connection --- ')
};


MySQLHelper.prototype.get = function (query) {
    var self = this;
    return new Promise(function (resolve, reject) {
        self.con.connect(function(err) {
            if (err) return err;
            self.con.query(query, function (err, result, fields) {
                if (err) throw err;
                self.con.end();
                resolve(result);
            });
          });
    });
};

MySQLHelper.prototype.execute_sql = function (query) {
    var self = this;
    console.log(query);
    return new Promise(function (resolve, reject) {
        self.con.connect(function(err) {
            if (err) return err;
            console.log('connection established');
            self.con.query(query, function (err, result, fields) {
                if (err) throw err;
                self.con.end();
                console.log('query done');
                resolve(result);
            });
          });
    });
};

MySQLHelper.prototype.insert = function (query, data) {
    var self = this;
    return new Promise(function (resolve, reject) {
        self.con.connect(function(err) {
            if (err) return err;
            self.con.query(query, [data], function (err, result, fields) {
                if (err) throw err;
                self.con.end();
                resolve(result);
            });
          });
    });
};



module.exports = MySQLHelper;