#!/usr/bin/env node
// בונה את learn-catalog.js - "מפת השיעורים" של עמוד הלמידה (learn.html) - מתוך מאגר האתר עצמו.
// סורק את כל קבצי data/*.js, אוסף לכל קובץ את תתי-הנושאים ומספר התרגילים, ומצמיד לכל נושא
// את השם העברי שמוגדר בעמודי המקצוע (math.html, english.html ...).
//
// הרצה (מתיקיית האתר):   node tools/build-learn-catalog.js . learn-catalog.js
// להריץ מחדש בכל פעם שמוסיפים / משנים קבצי נתונים.
const fs = require('fs'), vm = require('vm'), path = require('path');
const site = path.resolve(process.argv[2] || '.'), outFile = process.argv[3] || path.join(site, 'learn-catalog.js');
const DB_NAMES = ['readingTextsDB', 'questionsDB', 'questionsDB_grammar', 'questionsDB_syntax', 'questionsDB_part2', 'questionsDB_advanced', 'questionsDB_part3'];

// ---------- 1. סריקת קבצי הנתונים ----------
function scanFile(file) {
    const ctx = { window: {}, document: {}, console: { log() {}, warn() {}, error() {} } };
    vm.createContext(ctx);
    try { vm.runInContext(fs.readFileSync(file, 'utf8') + ';\n' + DB_NAMES.map(n => `try{this.__${n}=${n}}catch(e){}`).join(';'), ctx, { timeout: 8000 }); }
    catch (e) { return null; }
    const subs = [], idx = {};
    let total = 0;
    for (const n of DB_NAMES) {
        const v = ctx['__' + n]; if (!Array.isArray(v)) continue;
        for (const it of v) {
            if (!it || typeof it !== 'object') continue;
            const s = String(it.subTopic || it.subtopic || '').trim();
            const c = Array.isArray(it.questions) ? it.questions.length : 1;
            total += c; if (!s) continue;
            if (idx[s] == null) { idx[s] = subs.length; subs.push({ name: s, n: 0 }); }
            subs[idx[s]].n += c;
        }
    }
    return total ? { subs, total } : null;
}

// ---------- 2. שמות הנושאים מתוך עמודי המקצוע ----------
function pageTopics(html) {          // כל אובייקט { key: { name, subs: [...] } } שמוגדר בעמוד
    const out = [];
    let src; try { src = fs.readFileSync(path.join(site, html), 'utf8'); } catch (e) { return out; }
    const re = /const\s+(\w+)\s*=\s*\{/g; let m;
    while ((m = re.exec(src))) {
        let i = m.index + m[0].length - 1, depth = 0, q = null, end = -1;
        for (; i < src.length; i++) {
            const ch = src[i];
            if (q) { if (ch === '\\') i++; else if (ch === q) q = null; continue; }
            if (ch === '"' || ch === "'" || ch === '`') q = ch;
            else if (ch === '{') depth++;
            else if (ch === '}' && --depth === 0) { end = i; break; }
        }
        if (end < 0) continue;
        const body = src.slice(m.index + m[0].length - 1, end + 1);
        if (!/name\s*:/.test(body) || !/subs\s*:/.test(body)) continue;
        let obj; try { obj = vm.runInNewContext('(' + body + ')', {}, { timeout: 2000 }); } catch (e) { continue; }
        (function walk(o) {
            if (!o || typeof o !== 'object') return;
            for (const k of Object.keys(o)) {
                const v = o[k];
                if (v && typeof v === 'object' && typeof v.name === 'string' && Array.isArray(v.subs)) out.push({ key: k, name: v.name, subs: v.subs.map(String) });
                else walk(v);
            }
        })(obj);
    }
    return out;
}
const PAGE = {};
['math', 'english', 'hebrew', 'arabic', 'science', 'finance'].forEach(s => { PAGE[s] = pageTopics(s + '.html'); });
function labelFor(subject, subs, fallback) {
    let best = null, score = 0;
    for (const t of PAGE[subject] || []) {
        const set = new Set(t.subs.map(x => x.trim()));
        const hit = subs.filter(s => set.has(s.name)).length;
        if (hit > score) { score = hit; best = t; }
    }
    return best && score >= Math.max(1, Math.ceil(subs.length * 0.34)) ? { name: best.name, score: score, key: best.key } : null;
}
// math.html ממפה מפתחות נושא (equationsZ) לשמות קבצים (equations) - משמש להכרעה בין קבצים כפולים
const KEYMAP = {};
try {
    const src = fs.readFileSync(path.join(site, 'math.html'), 'utf8'), re = /const\s+map[A-Z]\s*=\s*(\{[^}]*\})/g; let m;
    while ((m = re.exec(src))) Object.assign(KEYMAP, vm.runInNewContext('(' + m[1] + ')'));
} catch (e) { }
const KNOWN = { bagrut_prep: 'הכנה לבחינת הבגרות', bar_ilan: 'מצוינות · בר אילן', abc_basics: 'אנגלית מהבסיס (ABC)', 'יסודי_כללי': 'יסודות הלשון (יסודי)' };

// ---------- 3. מקצועות, קבוצות (כיתות / שאלונים) וקישורי הפרמטרים ----------
const SUBJECTS = [
    { id: 'math', name: 'מתמטיקה' }, { id: 'hebrew', name: 'לשון והבעה' }, { id: 'english', name: 'אנגלית' },
    { id: 'science', name: 'מדעים' }, { id: 'arabic', name: 'ערבית' }, { id: 'finance', name: 'חינוך פיננסי' }
];
const MATH_GROUPS = [
    ['5_6', 'כיתות ה׳-ו׳'], ['grade7', 'כיתה ז׳'], ['grade8', 'כיתה ח׳'], ['grade9', 'כיתה ט׳'],
    ['35172', '3 יח״ל · שאלון 172'], ['35371', '3 יח״ל · שאלון 371'], ['35372', '3 יח״ל · שאלון 372'],
    ['35471', '4 יח״ל · שאלון 471'], ['35472', '4 יח״ל · שאלון 472'], ['35571', '5 יח״ל · שאלון 571'], ['35572', '5 יח״ל · שאלון 572']
];
function pretty(s) { return s.replace(/_\d{3}$/, '').replace(/_/g, ' ').trim(); }
function classify(base) {            // שם קובץ ← מקצוע, קבוצה, ופרמטרים לכתובת
    let m;
    if (base === '5_6_bar_ilan') return { subject: 'math', group: '5_6', grade: 'bar_ilan', topic: 'bar_ilan', fallback: 'מצוינות · בר אילן' };
    if ((m = /^5_6_(.+)$/.exec(base))) return { subject: 'math', group: '5_6', grade: '5_6', topic: m[1], fallback: pretty(m[1]) };
    if ((m = /^(grade\d)_(.+)$/.exec(base))) return { subject: 'math', group: m[1], grade: m[1], topic: m[2], fallback: pretty(m[2]) };
    if ((m = /^(35\d{3})_(.+)$/.exec(base))) return { subject: 'math', group: m[1], grade: m[1], topic: m[2], fallback: m[2] === 'bagrut_prep' ? 'הכנה לבחינת הבגרות' : pretty(m[2]) };
    if ((m = /^(english|arabic|science|finance|hebrew)_(.+)$/.exec(base))) return { subject: m[1], group: m[1], grade: m[1], topic: m[2], fallback: m[2] === 'bagrut_prep' ? 'הכנה לבחינת הבגרות' : pretty(m[2]) };
    if (base === 'כללי_יסודי_כללי') return { subject: 'hebrew', group: 'hebrew', grade: 'hebrew', topic: 'יסודי_כללי', fallback: 'יסודות הלשון (יסודי)' };
    return null;
}

const groups = {};
const files = fs.readdirSync(path.join(site, 'data')).filter(f => f.endsWith('.js')).sort((a, b) => a.localeCompare(b, 'he'));
let nTopics = 0, nSubs = 0, nQ = 0; const skipped = [];
for (const f of files) {
    const c = classify(f.slice(0, -3)); if (!c) continue;
    const s = scanFile(path.join(site, 'data', f)); if (!s) continue;
    const key = c.subject + '|' + c.group;
    const lab = labelFor(c.subject, s.subs);
    if (!lab && !KNOWN[c.topic]) { skipped.push(f); continue; }          // קובץ שאף עמוד מקצוע לא מפנה אליו (טיוטה / גרסה ישנה)
    const exact = lab ? ((KEYMAP[lab.key] || lab.key) === c.topic || (KEYMAP[lab.key] || lab.key) === c.topic.replace(/_\d{3}$/, '')) : true;
    (groups[key] = groups[key] || []).push({ name: lab ? lab.name : KNOWN[c.topic], file: 'data/' + f, grade: c.grade, topic: c.topic, n: s.total, subs: s.subs, _rank: (exact ? 1000 : 0) + (lab ? lab.score : 0) });
}
for (const key of Object.keys(groups)) {                                  // שני קבצים לאותו נושא - משאירים את זה שהאתר מפנה אליו
    const best = {};
    for (const t of groups[key]) { if (!best[t.name] || t._rank > best[t.name]._rank) { if (best[t.name]) skipped.push(best[t.name].file); best[t.name] = t; } else skipped.push(t.file); }
    groups[key] = Object.keys(best).map(k => { const t = best[k]; delete t._rank; nTopics++; nSubs += t.subs.length; nQ += t.n; return t; });
}
const catalog = SUBJECTS.map(sj => ({
    id: sj.id, name: sj.name,
    groups: (sj.id === 'math' ? MATH_GROUPS : [[sj.id, sj.name]]).map(g => ({ id: g[0], name: g[1], topics: (groups[sj.id + '|' + g[0]] || []).sort((a, b) => a.name.localeCompare(b.name, 'he')) })).filter(g => g.topics.length)
})).filter(sj => sj.groups.length);

fs.writeFileSync(outFile, '// נוצר אוטומטית על ידי tools/build-learn-catalog.js - לא לערוך ידנית.\nwindow.LEARN_CATALOG = ' + JSON.stringify(catalog) + ';\n');
console.log('learn-catalog.js: ' + nTopics + ' נושאים, ' + nSubs + ' תתי-נושאים, ' + nQ + ' תרגילים');
if (skipped.length) console.log('לא נכללו (כפולים / לא מקושרים מהאתר): ' + skipped.join(', '));
