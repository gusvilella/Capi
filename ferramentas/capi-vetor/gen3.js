const L = require('./layers.json'), H = require('./hand'), C = require('./coin');
const coinSrc = C.coin.toString();
// partes do olho com classe pra piscada: some o brilho, o olho desce e vira um risquinho curvo
const SHUT = '<path class=\"shut\" d=\"M44.4 67.4q5.6 4.8 11.2 0M93.6 67.4q5.6 4.8 11.2 0\" fill=\"none\" stroke=\"#220e08\" stroke-width=\"2.9\" stroke-linecap=\"round\" opacity=\"0\"/>';
const eyesFix = s => s.replace(/<path d="([^"]*)" fill="#220e08"/g, '<path class="ep" d="$1" fill="#220e08"').replace(/<circle ([^>]*)fill="#fff"\/>/g, '<circle class="glint" $1fill="#fff"/>');
const q = s => "'" + s.replace(/\\/g, '\\\\').replace(/'/g, "\\'") + "'";
const out = `  // Capi: vetor tirado direto do desenho oficial (corpo inteiro de frente, 149x200, pés no chão em y=192.7).
  // Partes separadas pra animar: corpo (com orelhas, focinho e pés), olhos, bochechas, patinhas (esq./dir.), moeda e laranja.
  const capiCoin = ${coinSrc};
  const CAPI = {
    body: ${q(L.body)},
    eyes: ${q('<g class="eyes">' + eyesFix(L.eyes) + SHUT + '</g>')},   // .ep = olho aberto, .glint = brilho, .shut = olho fechado (risquinho) pra piscar
    happy: '<path d="M44.6 69.4q5.4-6.2 10.8 0M93.8 69.4q5.4-6.2 10.8 0" fill="none" stroke="#220e08" stroke-width="2.9" stroke-linecap="round"/>',
    blush: ${q('<g class="bl">' + L.blush + '</g>')},
    pl: ${q(L.pl)},
    pr: ${q(L.pr)},
    fruit: ${q('<g class="fruit">' + H.fruit + '</g>')},
    shadow: '<ellipse cx="74.6" cy="191.8" rx="56" ry="6.4" fill="#000" opacity=".1"/>',
  };
  // de frente, inteira (sombra e pés incluídos); o miolo fica num grupo .cb (pra amassar) e a laranja por fora (pra cair/pular)
  const capiFull = () => \`\${CAPI.shadow}<g class="cb">\${CAPI.body}<g class="mcoin">\${capiCoin()}</g><g class="paws">\${CAPI.pl}\${CAPI.pr}</g>\${CAPI.blush}\${CAPI.eyes}</g>\${CAPI.fruit}\`;
  // busto (cabeça, patinhas e moeda) encaixado no quadrado 64x64 dos avatares
  const CAPI_BUST = \`<g transform="matrix(.5289 0 0 .5289 -7.405 -11.636)"><g class="cb">\${CAPI.body}\${capiCoin()}\${CAPI.pl}\${CAPI.pr}\${CAPI.blush}\${CAPI.eyes}</g>\${CAPI.fruit}</g>\`;
`;
require('fs').writeFileSync('snippet3.js', out); console.log(out.length);
