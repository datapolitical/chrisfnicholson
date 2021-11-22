// ./functions/index.js

export const onRequestGet = async ({ request, next }) => {

try{
  // Get the static asset response
  const response = await next()

  const { latitude, longitude, city, country, timezone } = request.cf

    let endpoint = "https://api.openweathermap.org/data/2.5/weather?"

    endpoint += "lat=" + latitude + "&lon=" + longitude + "&appid=15e9a7ef375c125ec4d72783818f684b"

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
  const currentTempC = content.main.temp
  const weatherDescription = content.weather[0].description
  const currentTempF = Math.round(((9/5)* (currentTempC - 273)) + 32)

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
      currentTempLocal = currentTempF
      degreesSymbol = "°F"
      break;
    default:
      currentTempLocal = currentTempC
      degreesSymbol = "°C"
      break;
  }


  // US BS KY LR PW FM MH

  const weatherString = "At " + humanTime + " in " + city + " there's " + weatherDescription + " and the temperature is " + currentTempLocal + degreesSymbol + "."

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
