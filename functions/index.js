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

  const nowdate = new Date()

  var isoDateStr = nowdate.toISOString()

  //var propertystring = JSON.stringify(content2.properties.temperature,null,4)
  var propertystringTest = JSON.stringify(content2.properties.temperature.values,null,4)

  var temparray = content2.properties.temperature.values
  var dateStr = temparray[8].validTime
  var tempStr = temparray[8].value
  var d = new Date(Date.parse(dateStr.split('/')[0]));
  var humantime = d.toLocaleTimeString('en-US', { timeZone: 'America/Denver' })
  var hourStr = d.getHours()
  var ftemp = "At " + humantime + "the hour is " + hourStr + "and the iso is " + isoDateStr + " the temperature in " + city + " is" + Math.round((1.8 * tempStr) + 32) + "degrees"

  const currd = new Date()
  currd.setTime(currd.getTime()-(currd.getTime() % 3600000))

  var textIntermediate = currd.toISOString()

  var textSearch = textIntermediate.split('Z')[0] + "+00:00/PT1H"

  //Find the object matching the date
  const obj = temparray.find(o => o.validTime === textSearch)

  //Get the value from the object
  //const currentTemp = obj.value;


  // Find the placeholder in our static asset
  return new HTMLRewriter().on('#weather', {
    // And act on the element
    element(element) {
      // https://developers.cloudflare.com/workers/runtime-apis/html-rewriter#methods
      element.setInnerContent(JSON.stringify(obj))
    }
  }).transform(response)
  } catch (thrown){
      return new Response(thrown);
  }
}
