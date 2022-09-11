var branchurl = "https://www.chrisfnicholson.com";
console.log("current directory");
console.log(__dirname);
const Crittr = require("crittr");
const hashstream = require('inline-csp-hash');
var CleanCSS = require('clean-css');
const crypto = require('crypto');
var output = "";

Crittr({
  urls: [branchurl],
  css: 'gh-pages/assets/css/stylesheet.css',
  device: {
    width: 600,
    height: 1000,
  },
})
  .then(({ critical, rest }) => {
    //console.log(critical);
    const fs = require("fs");
    var input = critical;
    var options = { /* options */ };
    output = new CleanCSS(options).minify(input);
    console.log(output.styles);
    var hash = 'sha256-' + crypto.createHash('sha256').update(output.styles).digest('base64');
    console.log(hash);
    fs.writeFile("_includes/critical.scss", output.styles, (err) => {
      if (err) {
        console.error(err);
        return;
      }
    });
  })
  .catch((err) => {
    console.error(err);
  });
