self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('garage-sale-v1').then(cache => {
      return cache.addAll([
        '/',
        '/index.html',
        '/src/css/styles.css',
        '/src/js/app.js',
        '/manifest.json'
      ]);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});