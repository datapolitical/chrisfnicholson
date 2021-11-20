

export const onRequest = ({ request }) => {
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

    let endpoint = "https://api.waqi.info/feed/geo:"
    const token = "c531734b5df728158946e194a92d2477a713f44d"
    let html_style = `body{padding:6em; font-family: sans-serif;} h1{color:#f6821f}`

    let html_content = "<h1>Weather 🌦</h1>"

    latitude = request.cf.latitude
    longitude = request.cf.longitude
    endpoint+= `${latitude};${longitude}/?token=${token}`
    const init = {
      headers: {
        "content-type": "application/json;charset=UTF-8",
      },
    }

    const response = await fetch(endpoint,init)
    const content = await response.json()

    html_content += `<p>This is a demo using Workers geolocation data. </p>`
    html_content += `You are located at: ${latitude},${longitude}.</p>`
    html_content += `<p>Based off sensor data from <a href="${content.data.city.url}">${content.data.city.name}</a>:</p>`
    html_content += `<p>The AQI level is: ${content.data.aqi}.</p>`
    html_content += `<p>The N02 level is: ${content.data.iaqi.no2.v}.</p>`
    html_content += `<p>The O3 level is: ${content.data.iaqi.o3.v}.</p>`
    html_content += `<p>The temperature is: ${content.data.iaqi.t.v}°C.</p>`

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
  }catch (thrown){
    return new Response(thrown);
  }
}
