const mysql = require('mysql');
const { Client } = require('pg');

const config = require('../config.json');

class DBHelper {
    constructor(db="default_db"){
        this.dbConfig = config[db];
        if (this.dbConfig.db_type =="mysql") {
            this.con = mysql.createConnection({
                host: this.dbConfig.host,
                user: this.dbConfig.user_name,
                password: this.dbConfig.password,
                database: this.dbConfig.db_name
              });
        } else if (this.dbConfig.db_type =="postgresql") {
            this.con = new Client({
                host: this.dbConfig.host,
                user: this.dbConfig.user_name,
                password: this.dbConfig.password,
                database: this.dbConfig.db_name,
                port: this.dbConfig.port
            });
            console.log(this.dbConfig);
            
        }
        
    }

    async executeSql(query){
        var self = this;
        this.con.connect();
        return new Promise(async (resolve, reject) => {
            await this.con.query(query, (err,res) => {
                if(err) {
                    this.con.end();
                    throw err;
                }
                if (this.dbConfig.db_type =="mysql") {
                    resolve(res);
                } else if (this.dbConfig.db_type =="postgresql") {
                    this.con.end();
                    resolve(res.rows);
                }
                
            });
        });
    }
}

module.exports = DBHelper;