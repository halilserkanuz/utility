const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
const config = require('../config.json');

class MongoHelper {
    async insertDocuments(col, docs, callback){
            // Connection URL
        const url = config.mongo.connection_string;
        return new Promise(async (resolve, reject) => {
            const client = await MongoClient.connect(url, {useUnifiedTopology: true});
            const db = await client.db(config.mongo.db_name);
            const collection = await db.collection(col);
            await collection.insertMany(docs, function(err, result) {
                if(err) reject(err);
                console.log("document inserted into the collection");
                client.close();
                resolve(result)
            });
                
        });
    }  
}


module.exports = MongoHelper;