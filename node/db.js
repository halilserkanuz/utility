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
            this.con.connect();
        }
        
    }

    async executeSql(query){
        var self = this;
        
        return new Promise(async (resolve, reject) => {
            /*
            await this.con.query(query, (err,res) => {
                if(err) {
                    throw err;
                }
                if (this.dbConfig.db_type =="mysql") {
                    resolve(res);
                } else if (this.dbConfig.db_type =="postgresql") {
                    //this.con.end();
                    resolve(res.rows);
                }
                
            });
            */
            if (this.dbConfig.db_type =="mysql") {
                await this.con.query(query, (err,res) => {
                    if(err) {
                        throw err;
                    }
                    resolve(res);
                });
           } else if (this.dbConfig.db_type =="postgresql") {
                await this.con.query(query)
                .then(res => {
                    resolve(res.rows);
                })
                .catch(e=>{
                    console.log(e.stack)
                })
           }
           
        });
    }
}

module.exports = DBHelper;