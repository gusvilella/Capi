# Capi em vetor (a partir do desenho oficial)

O desenho oficial da Capi está em `capi-referencia.jpg`. O app não usa a imagem: usa um vetor
tirado dela, separado em partes pra animar (objeto `CAPI` no `index.html`).

Pra regerar (precisa de Python com `opencv-python-headless`, `scipy`, `potracer` e Node):

```
cd ferramentas/capi-vetor
python3 trace.py      # separa cores e partes; espelha a metade esquerda (Capi simétrica) -> parts.npy, pal.json
python3 vec2.py       # traça cada parte com potrace (bordas lisas) -> layers.json
node gen3.js          # monta o trecho de JS (snippet3.js) com CAPI, capiCoin, capiFull e CAPI_BUST
```

Depois troque no `index.html` o bloco que começa em `// Capi: vetor tirado direto do desenho oficial`
até antes de `const AVATARS = {` pelo conteúdo de `snippet3.js`.

- Laranja e moeda são desenhadas à mão (`hand.js`, `coin.js`); folha e cabinho vêm do traçado.
- Não use `transform="rotate(...)"` nas peças: as animações usam `transform-box: fill-box` e deslocam.
- Coordenadas: 149x200 (= imagem / 10), eixo de simetria em x = 74,6, pés no chão em y = 192,7.
