var cacheNames = 'oshp-4.0.0';
var filesToCache = [
  '/summary',
  '/about',
  '/siteinfo',
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
  '/static/font-awesome/fonts/fontawesome-webfont.woff2?v=4.6.3',
  '/static/images/owasp_defenders.png',
  '/static/images/owasp_builders.png'
];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(cacheNames).then(function(cache) {
      return cache.addAll(filesToCache);
    })
  );
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(cacheName) {}).map(
          function(cacheName) {
            return caches.delete(cacheName);
          })
        );
      })
    );
  });

self.addEventListener('fetch', function(e) {
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request);
    })
  );
});
