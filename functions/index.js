// ./functions/index.js

export const onRequestGet = async ({ request, next }) => {

try{
  // Get the static asset response
  const response = await next()

  const { latitude, longitude, city, timezone } = request.cf

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
    
    
  var humanTime = currd.toLocaleTimeString('en-US', { timeZone: timezone })

  //Get the value from the object
  const currentTemp = content.main.temp
  const currentTempF = Math.round(((9/5)* (currentTemp - 273)) + 32)

  const weatherString = "At " + humanTime + " the temperature in " + city + " is " + currentTempF + " degrees"
  
  // var errorReport = timezone + "\n" + humanTime + "\n" + JSON.stringify(context)

  // Find the placeholder in our static asset
  return new HTMLRewriter().on('#weather', {
    // And act on the element
    element(element) {
      // https://developers.cloudflare.com/workers/runtime-apis/html-rewriter#methods
      element.setInnerContent(weatherString)
    }
  }).transform(response)
  } catch (thrown){
      return new Response(thrown);
  }
}
