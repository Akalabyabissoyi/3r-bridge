// Parity check: the single-file web app must agree with the Python package.
// Usage: python scripts/make_web_expectations.py > /tmp/exp.json && node scripts/verify_web.js /tmp/exp.json  (needs: npm i playwright)
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const ex = JSON.parse(fs.readFileSync(process.argv[2]));
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(()=>chromium.launch());
  const pg = await b.newPage(); const errs=[]; pg.on('pageerror',e=>errs.push(e.message)); pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  await pg.goto('file://' + require('path').resolve(__dirname, '../3r-bridge.html'));
  const out = await pg.evaluate(ex => {
    const {assess,lowest,robustness,S}=window.__3R; const bad=[];
    for (const [k,a,exp] of ex.stats){ const got = S[{two:'twoGroup',paired:'paired',anova:'anova',props:'props',events:'events'}[k]](...a); if(got!==exp) bad.push(['stat',k,a,got,exp]); }
    let nl=0; for (const [area,ns,res,pk,stab,label] of ex.ladder){ nl++;
      const r=assess(area,ns); const g=r.map(x=>[x.key,x.verdict,x.score]); if(JSON.stringify(g)!==JSON.stringify(res)) bad.push(['ladder',area,ns]);
      const p=lowest(r); if((p?p.key:null)!==pk) bad.push(['pick',area,ns]);
      const rb=robustness(area,ns); if(Math.abs(rb.stable-stab)>1e-5||rb.label!==label) bad.push(['rob',area,ns,rb.stable,stab]);
      if(bad.length>5) break; }
    return {bad, nl};
  }, ex);
  console.log(JSON.stringify(out), 'errors:', errs);
  await b.close();
})();
