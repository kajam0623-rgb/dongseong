import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

const read = (relativePath) => fs.readFileSync(path.join(root, relativePath), 'utf8');
const write = (relativePath, contents) => fs.writeFileSync(path.join(root, relativePath), contents, 'utf8');

const shell = read('src/builder-shell.html');
const css = read('src/styles/builder.css');
const genNeuro = read('src/js/generators/gen-neuro.js').trimEnd();
const js = read('src/js/builder.js').replace('/* __SITEON_GENERATOR_NEURO__ */', () => genNeuro);

if (!shell.includes('<!-- SITEON_BUILDER_CSS -->') || !shell.includes('<!-- SITEON_BUILDER_JS -->')) {
  throw new Error('src/builder-shell.html is missing build placeholders.');
}

if (js.includes('__SITEON_GENERATOR_NEURO__')) {
  throw new Error('Generator injection failed: gen-neuro marker is still present.');
}

const html = shell
  .replace('<!-- SITEON_BUILDER_CSS -->', () => css)
  .replace('<!-- SITEON_BUILDER_JS -->', () => js);

write('사이트온-빌더.html', html);

console.log('Built 사이트온-빌더.html from src/.');
