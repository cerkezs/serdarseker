const CACHE_NAME = 'yurdunal-teklif-v2';
const urlsToCache = [
  './',
  './index.html',
  './style.css',
  './script.js',
  './html2pdf.bundle.min.js',
  './logo.jpeg',
  './kase.png',
  './simza.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response; // Önbellekten döndür
        }
        return fetch(event.request); // İnternetten al
      })
  );
});
