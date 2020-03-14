var azure = require('azure-storage');
const fs = require("mz/fs");
const config = require('../config.json');

const azureConfig = config.azure;

function AzureHelper (storageAccount) {

    this.blobSvc = azure.createBlobService(
        config[storageAccount].storage_account,
        config[storageAccount].storage_account_key
      );
    console.log('[Azure Helper] --- Successfully connected to BlobService ---');
};


AzureHelper.prototype.uploadFile = function (container, blobName, localPath) {
    
    self = this;
    return new Promise(function (resolve, reject) {
        console.log('promise created')
        self.blobSvc.createBlockBlobFromLocalFile(container, blobName, localPath, (err, result) => {
            console.log(container, blobName, localPath)
            if(err!==null){
                console.log('[Azure Helper] --- Failed to upload to BlobService:');
                reject(err, container, blobName, localPath);
            }
            
            
        });
        resolve('[Azure Helper] --- Successfully uploaded to BlobService');
    })

};




AzureHelper.prototype.downloadFile = function (container, blob, localPath) {
    self = this;
    return new Promise(async function (resolve, reject) {
        await self.blobSvc.doesBlobExist(container, blob, async function(err, result) {
            if (err) {console.log(err);resolve(null)}
            else {
                if (result.exists){
                    await self.blobSvc.getBlobToLocalFile(container, blob, localPath, function(err, result){
                        if(err) reject(err);
                        resolve(blob);  
                    });   
                } else {

                    resolve(null);
                }
            }
        }
    )}
)};


AzureHelper.prototype.deleteFile = function (container, blob) {
    self = this;
    return new Promise(async function (resolve, reject) {
        await self.blobSvc.doesBlobExist(container, blob, async function(err, result) {
            if (err) {console.log(err);reject(null);}
            else {
                if (result.exists){
                    await self.blobSvc.deleteBlob(container, blob, function(err, result){
                        if(err) reject(err);
                        resolve(blob);  
                    });   
                } else {

                    resolve(null);
                }
            }
        }
    )}
)};


module.exports = AzureHelper;
