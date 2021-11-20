
export async function onRequest(context) {
  try {
    // Contents of context object
    const {
      request, // same as existing Worker API
      env, // same as existing Worker API
      params, // if filename includes [id] or [[path]]
      waitUntil, // same as ctx.waitUntil in existing Worker API
      next, // used for middleware or to fetch assets
      data, // arbitrary space for passing data between middlewares
    } = context;

  let endpoint = "https://api.weather.gov/points/"
  const token = "c531734b5df728158946e194a92d2477a713f44d" //Use a token from https://aqicn.org/api/
  let html_style = `body{padding:6em; font-family: sans-serif;} h1{color:#f6821f}`

  let html_content = "<h1>Weather 🌦</h1>"

  var mylatitude = context.request.cf.latitude
  var yourlongitude = context.request.cf.longitude
  endpoint+= `${mylatitude}:${yourlongitude}`
  const init = {
    headers: {
      "User-Agent" : "datapolitical@gmail.com",

    },
  }

  const response = await fetch(endpoint,init)
  const content = await response.json()
  var propertystring = JSON.stringify(content,null,4)

  html_content += `<p>This is a demo using Workers geolocation data. </p>`
  html_content += `You are located in: ${context.request.cf.city}.</p>`
  html_content += `<p>The forecast is: ${propertystring}.</p>`
  let html = `
<!DOCTYPE html>
<head>
  <title>Geolocation: Weather</title>
</head>
<body>
  <style>${html_style}</style>
  <div id="container">
  ${html_content}
  </div>
</body>`

    return new Response(html, {
      headers: {
        "content-type": "text/html;charset=UTF-8",
      },})
    } catch (thrown){
      return new Response(thrown);
  }
}
