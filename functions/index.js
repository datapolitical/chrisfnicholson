// ./functions/index.js

export const onRequestGet = async ({ request, next }) => {

try{
  // Get the static asset response
  const response = await next()

  const { latitude, longitude, city } = request.cf

    // const { latitude, longitude } = request.cf

  let endpoint = "https://api.weather.gov/points/"
  const token = "c531734b5df728158946e194a92d2477a713f44d" //Use a token from https://aqicn.org/api/

  // var mylatitude = context.request.cf.latitude
  // var yourlongitude = context.request.cf.longitude
  endpoint+= `${latitude},${longitude}`
  const init = {
    headers: {
      "User-Agent" : "datapolitical@gmail.com",

    },
  }

  const responseWeather = await fetch(endpoint,init)
  const content = await responseWeather.json()

  const response2 = await fetch(content.properties.forecastGridData,init)
  const content2 = await response2.json()

  //var propertystring = JSON.stringify(content2.properties.temperature,null,4)
  var propertystringTest = JSON.stringify(content2.properties.temperature.values,null,4)

  var temparray = content2.properties.temperature.values
  var dateStr = temparray[8].validTime
  var tempStr = temparray[8].value
  var d = new Date(Date.parse(dateStr.split('/')[0]));
  var humantime = d.toLocaleTimeString('en-US', { timeZone: 'America/Denver' })
  var ftemp = "At " + humantime + " the temperature in " + city + " is" + Math.round((1.8 * tempStr) + 32) + "degrees"

  // Find the placeholder in our static asset
  return new HTMLRewriter().on('#weather', {
    // And act on the element
    element(element) {
      // https://developers.cloudflare.com/workers/runtime-apis/html-rewriter#methods
      element.setInnerContent(ftemp)
    }
  }).transform(response)
  } catch (thrown){
      return new Response(thrown);
  }
}
