var dataCacheName = 'oshp-v3.1.0'
var cacheName = 'oshp-3.1.0';
var filesToCache = [
  '/summary',
  '/static/dist/css/bootstrap.min.css',
  '/static/font-awesome/css/font-awesome.min.css',
  '/static/nprogress/nprogress.css',
  '/static/build/css/custom.min.css',
  '/static/images/owasp_icon.png',
  '/static/echarts/dist/echarts.min.js',
  '/static/jquery/dist/jquery.min.js',
  '/static/jquery/dist/jquery.dataTables.min.js',
  '/static/dist/js/bootstrap.min.js',
  '/static/fastclick/lib/fastclick.min.js',
  '/static/nprogress/nprogress.min.js',
  '/static/build/js/custom.min.js',
  '/static/build/js/datatable.js',
  '/static/font-awesome/fonts/fontawesome-webfont.woff2?v=4.6.3'
];

self.addEventListener('install', function(e) {
  console.log('[ServiceWorker] Install');
  e.waitUntil(
    caches.open(cacheName).then(function(cache) {
      console.log('[ServiceWorker] Caching app shell');
      return cache.addAll(filesToCache);
    })
  );
});

self.addEventListener('activate', function(e) {
  console.log('[ServiceWorker] Activate');
  e.waitUntil(
    caches.keys().then(function(keyList) {
      return Promise.all(keyList.map(function(key) {
        if (key !== cacheName && key !== dataCacheName) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  return self.clients.claim();
});

self.addEventListener('fetch', function(e) {
  console.log('[ServiceWorker] Fetch', e.request.url);
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request);
    })
  );
});

var supportsPassive = false;
try {
  var opts = Object.defineProperty({}, 'passive', {
    get: function() {
      supportsPassive = true;
    }
  });
  window.addEventListener("test", null, opts);
} catch (e) {}

self.addEventListener('touchstart', function(e) {
  console.log('[ServiceWorker] Passive Listener');
  document.addEventListener('touchstart', onTouchStart, { passive: true });
});
