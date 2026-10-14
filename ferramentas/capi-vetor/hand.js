// laranja feita à mão nas medidas da imagem; cabinho e folha vêm do traçado
const O = '#4b1a0d';
const L = require('./layers.json');
const orange = `<circle cx="74.6" cy="41.3" r="10.85" fill="#f98724" stroke="${O}" stroke-width="3.9"/>`
 + `<path d="M80.63 34.76A8.9 8.9 0 1 1 67.27 46.34A8.9 8.9 0 0 0 80.63 34.76Z" fill="#ec6a1e"/>`
 + `<path d="M68.38 38.27A3.2 1.5 -38 1 0 73.42 34.33A3.2 1.5 -38 1 0 68.38 38.27Z" fill="#fbae6e" opacity=".9"/>`;
const fruit = L.stem + orange + L.leaf;
module.exports = { fruit, orange };
