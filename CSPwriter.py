import inlinehashes

google_analytics="'sha256-7S8HHslrpUKGbGUmT/L2MgqW/dfTrlhZaY5GN8XhFqA='"

headers = open("_headers", "w")

headers.write("/*" + "\n")
headers.write("Link: </assets/fonts/PublicSans_subset.woff2>; rel=preload; as=font" + "\n")
headers.write("Report-To: {'group':'default','max_age':31536000,'endpoints':[{'url':'https://chrisfnicholson.report-uri.com/a/d/g'}],'include_subdomains':true}" +"\n")
headers.write("Content-Security-Policy-Report-Only: default-src 'none'; report-uri https://chrisfnicholson.report-uri.com/r/d/csp/reportOnly; report-to default; connect-src 'self' cloudflareinsights.com https://www.google-analytics.com www.google-analytics.com; img-src 'self'; base-uri 'self'; form-action https://chrisfnicholson-staticman.herokuapp.com 'self'; child-src crosshare.org; manifest-src 'sha256-0edVDnyAgE6BNyBQYXswCWA3fk82xEhm5MrAEuxyhYA=' 'self'; worker-src 'self'; font-src 'self';")







content = open("gh-pages/index.html", "r")
inlines = inlinehashes.parse(content)
script_src = " script-src " + google_analytics
style_src = " style-src"
for hash in inlines:
    print("NEW HASH\n")
    print(hash)
    if hash.directive == "script-src":
        script_src += " '" + hash.sha256 + "'"
    if hash.directive == "style-src":
        style_src += " '" + hash.sha256 + "'"
script_src += " ajax.cloudflare.com static.cloudflareinsights.com 'self' 'report-sample';"
style_src += " 'self' 'report-sample';"
# print(headers)
headers.write(script_src)
headers.write(style_src)