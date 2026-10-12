#!/usr/bin/env node
// Run with an existing Playwright installation; no packages or browsers are installed.
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const root = path.resolve(__dirname, '..');
const output = path.resolve(process.argv[2] || path.join(root, 'dist/showcase-evidence'));
(async () => {
  fs.mkdirSync(output, {recursive:true});
  const browser = await chromium.launch({headless:true, ...(process.env.SHOWCASE_CHROME ? {executablePath:process.env.SHOWCASE_CHROME} : {})});
  const url = process.env.SHOWCASE_URL || pathToFileURL(path.join(root, 'docs/showcase/index.html')).href;
  const local = new URL(url).protocol === 'file:';
  const reports = [];
  async function open(options={}) {
    const page = await browser.newPage(options);
    const requests = [];
    await page.route('**/*', route => {
      const target = new URL(route.request().url());
      const allowed = local ? target.protocol === 'file:' : target.origin === new URL(url).origin;
      if (!allowed) { requests.push(target.href); return route.abort(); }
      return route.continue();
    });
    page.on('pageerror', error => { throw error; });
    await page.goto(url); return {page,requests};
  }
  try {
    for (const width of [1280,390]) {
      const {page,requests} = await open({viewport:{width,height:900}});
      for (const theme of ['light','dark']) {
        await page.selectOption('#theme', theme);
        for (const name of ['ownership','task-loop','installation']) {
          await page.click(`[data-view="${name}"]`);
          assert.equal(await page.locator('.diagram-panel:visible').count(),1);
          assert.equal(await page.locator(`#${name}`).isVisible(),true);
          assert.equal(new URL(page.url()).hash, '#' + name);
          assert.equal(await page.locator(`#${name} [data-download]`).getAttribute('href'),`diagrams/${name}-${theme}.svg`);
          const geometry=await page.evaluate(() => ({overflow:document.documentElement.scrollWidth>innerWidth}));
          assert.equal(geometry.overflow,false,'page must not scroll sideways');
          const overflow=await page.locator(`#${name} .theme-${theme} svg`).evaluate(svg=>[...svg.querySelectorAll('g[data-step]')].flatMap(g=>{const b=g.querySelector('rect').getBBox(); return [...g.querySelectorAll('text')].filter(t=>{const a=t.getBBox();return a.x<b.x||a.x+a.width>b.x+b.width||a.y<b.y||a.y+a.height>b.y+b.height}).map(t=>t.textContent)}));
          assert.deepEqual(overflow,[]);
          await page.screenshot({path:path.join(output,`${name}-${theme}-${width}.png`),fullPage:true});
        }
      }
      await page.evaluate(() => { location.hash = 'task-loop'; });
      await page.locator('#task-loop').waitFor({state:'visible'});
      await page.click('#reset');
      await page.focus('#step'); await page.keyboard.press('Enter');
      assert.match(await page.locator('#step-status').innerText(),/Step 1 of 6/);
      await page.click('#play'); await page.waitForTimeout(1050); await page.click('#play');
      const paused=await page.locator('#step-status').innerText(); await page.waitForTimeout(1000);
      assert.equal(await page.locator('#step-status').innerText(),paused);
      await page.click('#reset'); assert.equal(await page.locator('.active-step').count(),0);
      assert.equal(await page.locator('#play').innerText(),'Play');
      await page.click('#play'); await page.waitForFunction(() => document.querySelector('#step-status').textContent.startsWith('Step 6 of 6') && document.querySelector('#play').textContent === 'Play', null, {timeout:15000}); assert.match(await page.locator('#step-status').innerText(),/Step 6 of 6/); assert.equal(await page.locator('#play').innerText(),'Play'); await page.click('#play'); await page.click('[data-view="ownership"]'); assert.equal(await page.locator('#play').innerText(),'Play');
      assert.deepEqual(requests,[]); reports.push({width,checks:'themes, selection, downloads, layout, keyboard step, pause, reset, switch stops playback',externalRequests:0}); await page.close();
    }
    const reduced=await open({reducedMotion:'reduce'}); await reduced.page.click('[data-view="task-loop"]');
    assert.equal(await reduced.page.locator('#play').isDisabled(),true);await reduced.page.click('#step');assert.match(await reduced.page.locator('#step-status').innerText(),/Step 1/);await reduced.page.close();
    const staticPage=await open({javaScriptEnabled:false,viewport:{width:390,height:900}});
    assert.equal(await staticPage.page.locator('.diagram-panel:visible').count(),3);assert.equal(await staticPage.page.locator('.controls').isVisible(),false);
    assert.equal(await staticPage.page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
    await staticPage.page.screenshot({path:path.join(output,'no-javascript.png'),fullPage:true});assert.deepEqual(staticPage.requests,[]);await staticPage.page.close();
    // Render reproducible diagram thumbnails and a six-step illustrated animation.
    const capture=await open({viewport:{width:1024,height:850}});
    for (const theme of ['light','dark']) {
      await capture.page.selectOption('#theme',theme);
      for(const name of ['ownership','task-loop','installation']) {
        await capture.page.click(`[data-view="${name}"]`);
        await capture.page.locator(`#${name} .theme-${theme} svg`).screenshot({path:path.join(output,`${name}-${theme}.png`)});
      }
    }
    await capture.page.selectOption('#theme','dark');await capture.page.click('[data-view="task-loop"]');await capture.page.click('#reset');
    for(let i=0;i<6;i++){await capture.page.click('#step');await capture.page.locator('#task-loop .theme-dark svg').screenshot({path:path.join(output,`frame-${i}.png`)});}
    await capture.page.click('#reset');await capture.page.locator('#task-loop .theme-dark svg').screenshot({path:path.join(output,'frame-6.png')});
    await capture.page.close();
    fs.writeFileSync(path.join(output,'checks.json'),JSON.stringify({url,reports,reducedMotion:'passed',noJavaScript:'passed',screenReaderSession:'not exercised'},null,2));
    console.log('Showcase browser checks passed:',output);
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1});
