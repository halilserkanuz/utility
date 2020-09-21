const mysql = require('mysql');
const { Client } = require('pg');

const config = require('../config.json');

class DBHelper {
   

    async executeSql(query){
        
        return new Promise(async (resolve, reject) => {
            let dbConfig = config["pricetracker_db"];
            if (dbConfig.db_type =="mysql") {
                let con = mysql.createConnection({
                    host: dbConfig.host,
                    user: dbConfig.user_name,
                    password: dbConfig.password,
                    database: dbConfig.db_name
                });
                await this.con.query(query, (err,res) => {
                    if(err) {
                        throw err;
                    }
                    resolve(res);
                });
            } else if (dbConfig.db_type =="postgresql") {
                let con = new Client({
                    host: dbConfig.host,
                    user: dbConfig.user_name,
                    password: dbConfig.password,
                    database: dbConfig.db_name,
                    port: dbConfig.port
                });
                await con.connect();
                await con.query(query)
                .then(res => {
                    con.end();
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