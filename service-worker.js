// service-worker.js

// set names for both precache & runtime cache
workbox.core.setCacheNameDetails({
  prefix: "my-blog",
  suffix: "v1.0",
  precache: "precache",
  runtime: "runtime-cache",
});

// let Service Worker take control of pages ASAP
workbox.core.skipWaiting();
workbox.core.clientsClaim();

// let Workbox handle our precache list
workbox.precaching.precacheAndRoute(self.__precacheManifest);

// use `NetworkFirst` strategy for html
workbox.routing.registerRoute(/\.html$/, new workbox.strategies.NetworkFirst());

// use `NetworkFirst` strategy for css and js
workbox.routing.registerRoute(
  /\.(?:js|css)$/,
  new workbox.strategies.NetworkFirst()
);

// use `CacheFirst` strategy for images
workbox.routing.registerRoute(
  /assets\/(fontawesome|images)/,
  new workbox.strategies.CacheFirst()
);

// use `StaleWhileRevalidate` third party files
workbox.routing.registerRoute(
  /^https?:\/\/ajax\.cloudflare\.com/,
  new workbox.strategies.StaleWhileRevalidate()
);

workbox.routing.registerRoute(
  /^https?:\/\/cdnjs\.cloudflare\.com/,
  new workbox.strategies.StaleWhileRevalidate()
);

workbox.routing.registerRoute(
  /^https?:\/\/cdn\.jsdelivr\.net/,
  new workbox.strategies.StaleWhileRevalidate()
);
