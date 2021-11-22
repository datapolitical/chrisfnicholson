// ./functions/index.js

export const onRequestGet = async ({ request, next }) => {

try{
  // Get the static asset response
  const response = await next()

  const { latitude, longitude, city, country, timezone } = request.cf

    let endpoint = "https://api.openweathermap.org/data/2.5/weather?"

    endpoint += "lat=" + latitude + "&lon=" + longitude + "&appid=" + OPEN_WEATHER_KEY

    const init = {
    headers: {
    //  "User-Agent" : "datapolitical@gmail.com",

    },
  }

  const responseWeather = await fetch(endpoint,init)
  const content = await responseWeather.json()

  const currd = new Date()


  var humanTime = currd.toLocaleTimeString('en-US', { timeZone: timezone, hour: '2-digit', minute: '2-digit'})

  //Get the value from the object
  const currentTempK = content.main.temp
  const weatherDescription = content.weather[0].description
  const currentTempF = ((9/5)* (currentTempK - 273.15)) + 32
  const currentTempC = currentTempK - 273.15

  var currentTempLocal
  var degreesSymbol

  switch(country) {
    case "US":
    case "BS":
    case "KY":
    case "LR":
    case "PW":
    case "FM":
    case "MH":
      currentTempLocal = Math.round(currentTempF)
      degreesSymbol = "°F"
      break;
    default:
      currentTempLocal = Math.round(currentTempC)
      degreesSymbol = "°C"
      break;
  }

  var displayLocation
  if ( typeof city == 'undefined') {
    displayLocation = " where you are"
  }
  else {
    displayLocation = " in " + city
  }


  // US BS KY LR PW FM MH

  const weatherString = "At " + humanTime + displayLocation + " there's " + weatherDescription + " and the temperature is " + currentTempLocal + degreesSymbol + "."

  // var errorReport = timezone + "\n" + humanTime + "\n" + JSON.stringify(context)

  // Find the placeholder in our static asset
  return new HTMLRewriter().on('#weather', {
    // And act on the element
    element(element) {
      // https://developers.cloudflare.com/workers/runtime-apis/html-rewriter#methods
      element.setInnerContent(weatherString, { html: true })
    }
  }).transform(response)
  } catch (thrown){
      return new Response(thrown);
  }
}
