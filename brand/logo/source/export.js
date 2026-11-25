// node export.js outdir name.svg:width:outname.png ...
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [dir, ...jobs] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 1 });
  for (const j of jobs) {
    const [svg, w, out, bg] = j.split(':');
    const src = 'data:image/svg+xml;base64,' + fs.readFileSync(path.join(dir, svg)).toString('base64');
    await p.setContent(`<body style="margin:0;background:transparent"><img id="i" src="${src}" style="width:${w}px;display:block;${bg ? 'background:' + bg : ''}"></body>`);
    await p.waitForFunction(() => document.getElementById('i').complete);
    await (await p.$('#i')).screenshot({ path: path.join(dir, out), omitBackground: true });
  }
  await b.close();
})();
