const mysql = require('mysql');

const config = require('../config.json');

class MySQLHelper {
    constructor(db="default_db"){
        this.mySQLConfig = config[db];
        this.con = mysql.createConnection({
            host: this.mySQLConfig.host,
            user: this.mySQLConfig.user_name,
            password: this.mySQLConfig.password,
            database: this.mySQLConfig.db_name
          });
    }

    async executeSql(query){
        var self = this;
        return new Promise(async (resolve, reject) => {
            await this.con.query(query, (err,rows) => {
                if(err) throw err;
                resolve(rows);
            });
        });
    }
}

module.exports = MySQLHelper;