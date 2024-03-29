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

    let endpoint = "https://api.weather.gov/points/";
    const token = env.AQICN_TOKEN; //Use a token from https://aqicn.org/api/
    let html_style = `body{padding:6em; font-family: sans-serif;} h1{color:#f6821f}`;

    let html_content = "<h1>Weather 🌦</h1>";

    var mylatitude = context.request.cf.latitude;
    var yourlongitude = context.request.cf.longitude;
    endpoint += `${mylatitude},${yourlongitude}`;
    const init = {
      headers: {
        "User-Agent": env.EMAIL,
      },
    };

    const response = await fetch(endpoint, init);
    const content = await response.json();

    const response2 = await fetch(content.properties.forecastGridData, init);
    const content2 = await response2.json();

    var propertystring = JSON.stringify(
      content2.properties.temperature,
      null,
      4
    );
    var temparray = content2.properties.temperature.values;
    var dateStr = temparray[6].validTime;
    var d = new Date(Date.parse(dateStr.split("/")[0]));
    var humantime = d.toLocaleString("en-US", { timeZone: "America/Denver" });
    var ftemp = Math.round(1.8 * temparray[8].value + 32);

    html_content += `<p>This is a demo using Workers geolocation data. </p>`;
    html_content += `You are located in: ${context.request.cf.city}.</p>`;
    html_content += `<p>The temp at ${humantime} is: ${ftemp} degrees.</p>`;
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
</body>`;

    return new Response(html, {
      headers: {
        "content-type": "text/html;charset=UTF-8",
      },
    });
  } catch (thrown) {
    return new Response(thrown);
  }
}
