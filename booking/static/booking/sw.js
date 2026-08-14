const CACHE_NAME = 'date-planlegger-v1';

const URLS_TO_CACHE = [
  '/static/booking/icons/icon-192.png',
  '/static/booking/icons/icon-512.png',
];

// "install": kjøres én gang når service workeren først registreres.
// Her legger vi grunnleggende filer (ikoner) i cachen med en gang.
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(URLS_TO_CACHE))
  );
});

// "activate": kjøres når en ny versjon av service workeren tar over.
// Her rydder vi bort gamle cache-versjoner, slik at brukeren aldri
// sitter fast med utdatert innhold.
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((names) =>
      Promise.all(
        names
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      )
    )
  );
});

// "fetch": kjøres for HVER nettverksforespørsel siden gjør.
// Strategien her er "network-first": prøv nettverket først (siden
// dette er en app med live data - bookinger, status osv. - vil vi
// ALDRI vise utdatert innhold når man faktisk har nett).
// Faller tilbake til cache kun hvis nettverket feiler helt.
self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});
