// ./functions/index.js

export const onRequestGet = async ({ request, next }) => {

try{
  // Get the static asset response
  const response = await next()

  const { latitude, longitude, city, timezone } = request.cf

    // const { latitude, longitude } = request.cf
    
  var timeZoneUpdated = "United States/" + timezone.split('/')[1]

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
  var dateStr = temparray[6].validTime
  var tempStr = temparray[6].value
  var d = new Date(Date.parse(dateStr.split('/')[0]));
  var humantime = d.toLocaleTimeString('en-US', { timeZone: timezone })
  var hourStr = d.getHours()
  var ftemp = "At " + humantime + "the hour is " + hourStr + "and the iso is " + isoDateStr + " the temperature in " + city + " is" + Math.round((1.8 * tempStr) + 32) + "degrees"

  const currd = new Date()
  currd.setTime(currd.getTime()-(currd.getTime() % 3600000))

  var textIntermediate = currd.toISOString()

  var textSearch = textIntermediate.split('.')[0] + "+00:00/PT1H"

  //Find the object matching the date
  //const obj = temparray.find(o => o.validTime === textSearch)

  //const pickedTime = obj.validTime

  //var pd = new Date(Date.parse(pickedTime.split('/')[0]));
  //var humanPickedTime = pd.toLocaleTimeString('en-US', { timeZone: timezone })

  //Get the value from the object
  //const currentTemp = Math.round((1.8 * obj.value) + 32)

  //const weatherString = "At " + humanPickedTime + " the temperature in " + city + " is " + currentTemp + " degrees"
  
  var errorReport = textSearch + "\n" + propertystringTest

  // Find the placeholder in our static asset
  return new HTMLRewriter().on('#weather', {
    // And act on the element
    element(element) {
      // https://developers.cloudflare.com/workers/runtime-apis/html-rewriter#methods
      element.setInnerContent(propertystringTest)
    }
  }).transform(response)
  } catch (thrown){
      return new Response(thrown + "\n" + errorReport);
  }
}
