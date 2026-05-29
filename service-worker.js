const CACHE_NAME = 'quest-station-v3';
const ASSETS = [
  '/',
  '/index.html',
  '/mj.html',
  '/regles.html',
  '/outils_rapides.html',
  '/capacites.js',
  '/sorts.js',
  '/monstres-srd.js',
  '/infos-contenu.js',
  '/icon.svg',
  '/manifest.json'
];

// Installation : mise en cache des ressources statiques
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(ASSETS);
    })
  );
  self.skipWaiting();
});

// Activation : nettoyage des anciens caches
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(function(key) { return key !== CACHE_NAME; })
            .map(function(key) { return caches.delete(key); })
      );
    })
  );
  self.clients.claim();
});

// Fetch : cache-first pour les ressources statiques, réseau pour Firebase
self.addEventListener('fetch', function(event) {
  var url = event.request.url;

  // Laisser passer les requêtes Firebase (Firestore, Auth, etc.)
  if (url.includes('firestore.googleapis.com') ||
      url.includes('firebase.googleapis.com') ||
      url.includes('googleapis.com') ||
      url.includes('gstatic.com')) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then(function(cached) {
      if (cached) return cached;
      return fetch(event.request).then(function(response) {
        // Mettre en cache les nouvelles ressources statiques (GET uniquement)
        if (event.request.method === 'GET' && response && response.status === 200) {
          var responseClone = response.clone();
          caches.open(CACHE_NAME).then(function(cache) {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      }).catch(function() {
        // Fallback offline : retourner index.html pour les navigations
        if (event.request.mode === 'navigate') {
          return caches.match('/index.html');
        }
      });
    })
  );
});
