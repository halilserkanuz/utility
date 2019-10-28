var puppeteer = require('puppeteer');
var md5 = require('md5');
const fs = require("mz/fs");

function PuppeteerHelper () {
      console.log('[PuppeteerHelper]')
};

PuppeteerHelper.prototype.processSteps = function (page, steps, customs) {
    var self = this;
    return new Promise(async function(resolve, reject){
        var result = {};
        for (var j=0; j<steps.length; j++){
            var step = steps[j];
            try{
                switch(step["type"]){
                    case "waitForSelector":
                        console.log(step);
                        await page.waitFor(step["selector"]);
                        break;
                    case "click":
                        console.log(step);
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
                        console.log(step);
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
                        console.log(step);
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
                        console.log(step);
                        await page.waitFor(step["second"]);
                        break;
                    case "tap":
                            console.log(step);
                            await page.tap(step["selector"]);
                            break;
                    case "waitForSelector":
                        console.log(step);
                        await page.waitForSelector(step["selector"], {visible: true});
                        break;
                    
                    case "waitForNavigation":
                        console.log(step);
                        await page.waitForNavigation({ waitUntil: 'networkidle2' })
                        break;
                    case "hide":
                        console.log(step);
                        var selector = step["selector"];
                        var order = step["order"];
                        await page.evaluate((selector, order)=>{
                            document.querySelectorAll(selector)[order].style.visibility='hidden';
                        }, selector, order);
                        break;
                    case "ss_by_selector":
                        console.log(step);
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
                        
                        const scroll = await page.evaluate(() => {
                            var left = (((t = document.documentElement) || (t = document.body.parentNode)) && typeof t.scrollLeft == 'number' ? t : document.body).scrollLeft;
                            var top = (((t = document.documentElement) || (t = document.body.parentNode)) && typeof t.scrollTop == 'number' ? t : document.body).scrollTop;
                            return {left, top};
                        });

                        if(!scroll)
                            scroll = {left:0,top:0};

                        console.log(rect);
                        console.log(scroll);
                        result.filename = customs;
                        result.newTextHash = md5(rect.text);
                        result.ignoreTextHash = false;
                        var buffer = await page.screenshot({
                            clip: {
                                x: rect.left + scroll.left ,
                                y: rect.top + scroll.top,
                                width: rect.width,
                                height: rect.height
                            }
                        });
                        await fs.writeFileSync(path, buffer);
                        break;
                    case "ss_by_coordinates":
                        console.log(step)
                        var buffer = await page.screenshot({path: customs,
                            clip: {x: step["x"], y:step["y"], width: step["w"], height: step["h"]}
                        });
                        result.filename = customs;
                        result.ignoreTextHash = true;
                        break;
                    case "eval":
                        console.log(step);
                        var script = step["script"];
                        await page.evaluate((script)=>{
                            eval(script);
                        }, script);
                        break;

                    case "type":
                        console.log(step);
                        var typingText = customs.typingText;
                        var inputSelector = step.selector;
                        await page.type(inputSelector, typingText);
                        break;
                    
                    case "multipleResults":
                        console.log(step);
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
                await reject(err);
            }
        }
    await resolve(result);
    });
};

module.exports = PuppeteerHelper;