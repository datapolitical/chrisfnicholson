var branchurl = "https://www.chrisfnicholson.com";
process.cwd();
const Crittr = require("crittr");

Crittr({
  urls: [branchurl],
  css: './gh-pages/stylesheet.css',
  device: {
    width: 600,
    height: 1000,
  },
})
  .then(({ critical, rest }) => {
    console.log(critical);
    const fs = require("fs");
    fs.writeFile("gh-pages/assets/css/generated-critical.css", critical, (err) => {
      if (err) {
        console.error(err);
        return;
      }
    });
  })
  .catch((err) => {
    console.error(err);
  });
