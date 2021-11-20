// ./functions/index.js

export const onRequestGet = ({ request, next }) => {
  // Get the static asset response
  const response = await next()
  
  const { latitude, longitude } = request.cf




// var mylatitude = context.request.cf.latitude
  // var yourlongitude = context.request.cf.longitude
  endpoint+= `${latitude},${longitude}`
  const init = {
    headers: {
      "User-Agent" : "datapolitical@gmail.com",

    },
  }

  const response = await fetch(endpoint,init)
  const content = await response.json()
  
  const response2 = await fetch(content.properties.forecastGridData,init)
  const content2 = await response2.json()
  
  var propertystring = JSON.stringify(content2.properties.temperature,null,4)
  var temparray = content2.properties.temperature.values
  var dateStr = temparray[6].validTime
  var d = new Date(Date.parse(dateStr.split('/')[0]));
  var humantime = d.toLocaleString('en-US', { timeZone: 'America/Denver' })
  var ftemp = "The temperature is" + Math.round((1.8 * temparray[8].value) + 32) + "degrees"


  // Find the placeholder in our static asset
  return new HTMLRewriter().on('#weather', {
    // And act on the element
    element(element) {
      // https://developers.cloudflare.com/workers/runtime-apis/html-rewriter#methods
      element.setInnerContent(ftemp)
    }
  }).transform(response) 
}