var azure = require('azure-storage');
const fs = require("mz/fs");
const config = require('../config.json');

const azureConfig = config.azure;

function AzureHelper () {
    this.blobSvc = azure.createBlobService(
        azureConfig.storage_account,
        azureConfig.storage_account_key
      );
    console.log('[Azure Helper] --- Successfully connected to BlobService ---');
};


AzureHelper.prototype.uploadFile = function (container, blobName, localPath, del) {
    if (del === undefined) {
        del = false;
    }
    self = this;
    return new Promise(function (resolve, reject) {
        self.blobSvc.createBlockBlobFromLocalFile(container, blobName, localPath, (err, result) => {
            if(err!==null){
                console.log('[Azure Helper] --- Failed to upload to BlobService:');
                reject(err);
            }
            resolve('[Azure Helper] --- Successfully uploaded to BlobService');
            if (del == true) {
                fs.unlinkSync(localPath);
            } 

            
        });
    })

};




AzureHelper.prototype.downloadFile = function (container, blobName, localPath) {
    self = this;
    return new Promise(async function (resolve, reject) {
        await self.blobSvc.doesBlobExist(container, blobName, async function(err, result) {
            if (err) {console.log(err);resolve(null)}
            else {
                if (result.exists){
                    await self.blobSvc.getBlobToLocalFile(container, blobName, localPath, function(err, result){
                        if(err) reject(err);
                        resolve(blobName);  
                    });   
                } else {

                    resolve(null);
                }
            }
        }
    )}
)};


AzureHelper.prototype.deleteFile = function (container, blobName) {
    self = this;
    return new Promise(async function (resolve, reject) {
        await self.blobSvc.doesBlobExist(container, blobName, async function(err, result) {
            if (err) {console.log(err);resolve(null)}
            else {
                if (result.exists){
                    await self.blobSvc.delete_blob(container, blobName, function(err, result){
                        if(err) reject(err);
                        resolve(blobName);  
                    });   
                } else {

                    resolve(null);
                }
            }
        }
    )}
)};


module.exports = AzureHelper;
