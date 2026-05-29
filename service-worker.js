const CACHE_NAME = 'quest-station-v4';

// Fichiers HTML : network-first (toujours récupérer la version fraîche)
const HTML_FILES = ['/', '/index.html', '/mj.html', '/regles.html', '/outils_rapides.html'];

// Assets statiques : cache-first (changent peu, chargement rapide)
const STATIC_ASSETS = [
  '/capacites.js',
  '/sorts.js',
  '/monstres-srd.js',
  '/infos-contenu.js',
  '/icon.svg',
  '/manifest.json'
];

// Installation : pré-cache des assets statiques uniquement
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// Activation : nettoyage de TOUS les anciens caches
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

self.addEventListener('fetch', function(event) {
  var url = event.request.url;
  if (event.request.method !== 'GET') return;

  // Laisser passer Firebase
  if (url.includes('firestore.googleapis.com') ||
      url.includes('firebase.googleapis.com') ||
      url.includes('googleapis.com') ||
      url.includes('gstatic.com')) {
    return;
  }

  var isHtml = HTML_FILES.some(function(p) { return url.endsWith(p); })
               || event.request.mode === 'navigate';

  if (isHtml) {
    // Network-first pour les HTML : toujours essayer le réseau
    event.respondWith(
      fetch(event.request).then(function(response) {
        if (response && response.status === 200) {
          var clone = response.clone();
          caches.open(CACHE_NAME).then(function(cache) { cache.put(event.request, clone); });
        }
        return response;
      }).catch(function() {
        // Hors-ligne : retourner la version en cache si dispo
        return caches.match(event.request) || caches.match('/index.html');
      })
    );
  } else {
    // Cache-first pour les assets statiques
    event.respondWith(
      caches.match(event.request).then(function(cached) {
        if (cached) return cached;
        return fetch(event.request).then(function(response) {
          if (response && response.status === 200) {
            var clone = response.clone();
            caches.open(CACHE_NAME).then(function(cache) { cache.put(event.request, clone); });
          }
          return response;
        });
      })
    );
  }
});
