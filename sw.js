// Service worker: guarda o app no aparelho para abrir sem internet.
// Página: tenta a rede primeiro (pega atualizações) e cai no que está guardado se estiver offline.
const CACHE = 'orcamento-v19';
const FILES = ['./', './index.html', './manifest.webmanifest', './favicon.svg', './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  if (req.mode === 'navigate') {
    // Guarda só respostas boas (uma página de erro do servidor não pode virar a cópia offline)
    // Cada página guarda a própria cópia (o app e a prévia não se misturam); "/" e "/index.html" são a mesma
    const path = new URL(req.url).pathname, key = /\/(index\.html)?$/.test(path) ? './index.html' : path;
    const net = fetch(req).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(key, copy)); }
      return res;
    });
    e.waitUntil(net.catch(() => {}));   // mesmo se a cópia guardada abrir antes, termina de atualizar
    e.respondWith(new Promise(resolve => {
      let done = false;
      const finish = r => { if (!done && r) { done = true; resolve(r); } };
      const saved = () => caches.match(key);
      // Internet lenta: depois de 4 s abre a cópia guardada em vez de ficar esperando
      const timer = setTimeout(() => saved().then(finish), 4000);
      net.then(res => res.ok ? res : saved().then(hit => hit || res))
        .catch(() => saved().then(hit => hit || Response.error()))
        .then(r => { clearTimeout(timer); finish(r); });
    }));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req)));
});
