var puppeteer = require('puppeteer');
var md5 = require('md5');
const fs = require("mz/fs");
const md5File = require('md5-file');
const resemble = require('resemblejs')

function PuppeteerHelper () {
      console.log('[PuppeteerHelper]')
};

PuppeteerHelper.prototype.getFileHash = (filename)=> {
    return new Promise(function(resolve, reject) {
        md5File(filename, (err, hash) => {
            if (err) reject(err);
            resolve(hash);
        });
    })
};


PuppeteerHelper.prototype.compareImages = (newImage, oldImage) => {
    return new Promise(async function(resolve, reject){
        const options = {};
        await resemble.compare(newImage, oldImage, options, function(err, data) {
            if(err) reject(err)
            if (data.misMatchPercentage>0.05){
                fs.writeFile("diff_"+newImage, data.getBuffer());
                resolve("diff_"+newImage);
            }
        });
        
        resolve(null)
    });
}

PuppeteerHelper.prototype.processSteps = function (page, steps, customs) {
    var self = this;
    return new Promise(async function(resolve, reject){
        var result = {};
        for (var j=0; j<steps.length; j++){
            var step = steps[j];
            console.log(step);
            try{
                switch(step["type"]){
                    case "waitForSelector":
                        await page.waitForTimeout(step["selector"]);
                        
                        break;
                    case "click":
                        try {
                            var selector = step["selector"];
                            var optionOrder = step["order"];
                            await page.evaluate((selector, optionOrder)=>{
                            document.querySelectorAll(selector)[optionOrder].click()
                            }, selector, optionOrder);
                            break;

                        } catch (err) {
                            break;
                        }

                    case "optionSelect":
                        var selector = step["selector"];
                        var optionOrder = step["order"];
                        await page.evaluate((selector, optionOrder)=>{
                            const event = new Event('change');
                            event.simulated = true;
                            console.log(selector, optionOrder);
                            document.querySelectorAll(selector+' option')[optionOrder].selected=true;
                            document.querySelectorAll(selector+' option')[optionOrder].click();
                            document.querySelector(selector).dispatchEvent(event);
                        }, selector, optionOrder);
                        break;

                    case "select":
                        var selector = step["selector"];
                        var value = step["value"];
                        page.select(selector, value);
                        break;
                    case "setAttribute":
                        var selector = step["selector"];
                        var attribute = step["attribute"];
                        var value = step["value"];
                        var order = step["order"];
                        await page.evaluate((selector, order, attribute, value)=>{
                            var element = document.querySelectorAll(selector)[order];
                            element.setAttribute(attribute, value);
                        },selector, order, attribute, value);
                        break;
                    case "waitFor":
                        await page.waitForTimeout(step["second"]);
                        break;
                    case "tap":
                            await page.tap(step["selector"]);
                            break;
                    case "waitForSelector":
                        await page.waitForSelector(step["selector"], {visible: true});
                        break;
                    
                    case "waitForNavigation":
                        await page.waitForNavigation({ waitUntil: 'networkidle2' })
                        break;
                    case "hide":
                        var selector = step["selector"];
                        var order = step["order"];
                        await page.evaluate((selector, order)=>{
                            document.querySelectorAll(selector)[order].style.visibility='hidden';
                        }, selector, order);
                        break;
                    case "ss_by_selector":
                        var path = customs;
                        var selector = step["selector"];
                        var order = step["order"];
                        await page.focus(selector);
                        const rect = await page.evaluate((selector,order) => {
                            const element = document.querySelectorAll(selector)[order];
                            
                            if (!element)
                                return null;
                            const {x, y, width, height} = element.getBoundingClientRect();
                                return {left: x, top: y, width, height, id: element.id, text:element.innerText};
                        }, selector, order);
                        console.log(rect)
                        const scroll = await page.evaluate(() => {
                            var left = (((t = document.documentElement) || (t = document.body.parentNode)) && typeof t.scrollLeft == 'number' ? t : document.body).scrollLeft;
                            var top = (((t = document.documentElement) || (t = document.body.parentNode)) && typeof t.scrollTop == 'number' ? t : document.body).scrollTop;
                            return {left, top};
                        });

                        if(!scroll)
                            scroll = {left:0,top:0};

                        result.filename = customs;
                        result.newTextHash = md5(rect.text);
                        result.ignoreTextHash = false;
                        await page.screenshot({path: customs,
                            clip: {
                                x: rect.left + scroll.left ,
                                y: rect.top + scroll.top,
                                width: rect.width,
                                height: rect.height
                            }
                        });
                        break;
                    case "ss_by_coordinates":
                        await page.screenshot({path: customs,
                            clip: {x: step["x"], y:step["y"], width: step["w"], height: step["h"]}
                        });
                        result.filename = customs;
                        result.ignoreTextHash = true;
                        break;
                    case "eval":
                        var script = step["script"];
                        await page.evaluate((script)=>{
                            eval(script);
                        }, script);
                        break;

                    case "type":
                        var typingText = customs.typingText;
                        var inputSelector = step.selector;
                        await page.type(inputSelector, typingText);
                        break;
                    
                    case "multipleResults":
                        var products= []; 
                        var selector = step["selector"];

                        var productsArrayLength = await page.evaluate((selector) => {    
                            arrayLength = document.querySelectorAll(selector).length;
                        return arrayLength;   
                        }, selector);
                    
                        console.log(productsArrayLength);
                    
                    
                        for (var i=0; i<productsArrayLength; i++){
                    
                            var product = await page.evaluate((selector, i) => {
                                var product = document.querySelectorAll(selector)[i].href;
                            return product;
                            }, selector, i);
                    
                        products.push(product);

                        result.products = products;
                    
                        };
                }
            }catch(err){
                console.log(err);
            }
        }
    await resolve(result);
    });
};

module.exports = PuppeteerHelper;