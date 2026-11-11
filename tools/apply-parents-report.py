#!/usr/bin/env python3
"""Copies the 2026 parents report (style + script) from tirgul.html into the kids home page.
The block wraps the existing renderParentsDashboard(), which is identical on both sites, so the
kids data and login logic are untouched. Idempotent.
Usage: python3 tools/apply-parents-report.py tirgul.html kids/index.html"""
import re, sys
src_path, dst_path = sys.argv[1], sys.argv[2]
src = open(src_path, encoding='utf-8').read()
a = src.index('<!-- דוח הורים: עיצוב חדש')
b = src.index('</script>', src.index('window.__prAnalyze=analyze;', a)) + len('</script>')
block = src[a:b]
# קידס: מקצועות היסודי בצבעים משלהם, וכתובת האתר של הקידס
old_colors = "var COLORS={'מתמטיקה':'#D3263A',"
assert old_colors in block
block = block.replace(old_colors, "var COLORS={'חשבון':'#D3263A','עברית':'#7A3FD1','תנ\"ך':'#0E7C93','טריוויה':'#C2185B','מתמטיקה':'#D3263A',", 1)
block = block.replace('</b> · tirgulim.co.il</span>', '</b> · kids.tirgulim.co.il</span>')
# הזום של דף הקידס שונה מזה של האתר הרגיל, לכן מפצים עליו לפי הערך בפועל במקום מספרים קבועים
n = 0
for rule in ['@media (min-width:851px){html body #parents-modal{zoom:1.5686}}',
             '@supports (-webkit-touch-callout:none){@media (min-width:1024px) and (max-width:1366px){html body #parents-modal{zoom:1.4706}}}']:
    if rule in block: block = block.replace(rule, '', 1); n += 1
assert n == 2, 'zoom rules not found'
zoom_js = '''<script id="parents-report-2026-zoom">
(function(){
  var m=document.getElementById('parents-modal');if(!m)return;
  function fit(){var z=parseFloat(getComputedStyle(document.body).zoom)||1;m.style.setProperty('zoom',String(Math.round(10000/z)/10000),'important');}
  fit();window.addEventListener('resize',fit);window.addEventListener('orientationchange',fit);
  new MutationObserver(fit).observe(m,{attributes:true,attributeFilter:['style','class']});
})();
</script>'''
block = '<!-- parents-report-kids:start -->\n' + block + '\n' + zoom_js + '\n<!-- parents-report-kids:end -->\n'
dst = open(dst_path, encoding='utf-8').read()
dst = re.sub(r'<!-- parents-report-kids:start -->.*?<!-- parents-report-kids:end -->\n', '', dst, flags=re.S)
assert 'parents-report-2026-js' not in dst, 'target already has its own report'
i = dst.rfind('</body>')
open(dst_path, 'w', encoding='utf-8').write(dst[:i] + block + dst[i:])
print('ok', dst_path, len(block))
