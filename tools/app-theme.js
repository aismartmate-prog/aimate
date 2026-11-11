/* classroom-theme-2026: אחרי הגשת המבחן - חוזרים לראש העמוד, כדי שהסיכום ייראה מההתחלה */
(function () {
    var r = document.getElementById('review-screen'); if (!r || !window.MutationObserver) return;
    var shown = false;
    new MutationObserver(function () {
        var on = r.style.display && r.style.display !== 'none';
        if (on && !shown) { shown = true; [60, 450].forEach(function (ms) { setTimeout(function () { window.scrollTo(0, 0); document.documentElement.scrollTop = 0; document.body.scrollTop = 0; }, ms); }); }
        if (!on) shown = false;
    }).observe(r, { attributes: true, attributeFilter: ['style'] });
})();

/* ===== המחברת הדיגיטלית 2026: כרטיס תרגיל, הגדרות מחברת, מסך מלא, שמירה עם הדף =====
   שכבה מעל המנוע המקורי: משתמשת ב-setPadBg / resizePadCanvas / nbUpdatePageUI כמו שהם,
   ומוסיפה סוגי דפים ואפשרויות. ההעדפות נשמרות במכשיר (localStorage). */
(function () {
    var win = document.getElementById('notebook-window'), ov = document.getElementById('notebook-overlay');
    var area = document.getElementById('nb-canvas-area'), qc = document.getElementById('notebook-question-container');
    if (!win || !ov || !area || !qc) return;
    var tb = win.querySelector('.nb-toolbar');
    var hasPages = typeof nbPages !== 'undefined' && typeof curPage === 'function';
    var KEY = 'nb26prefs', P = { type: null, paper: '#fffdf6', cell: 26, margin: false, spiral: true, qmin: false, qsize: 1.12 };
    try { var sv = JSON.parse(localStorage.getItem(KEY) || '{}'); for (var k in sv) P[k] = sv[k]; } catch (e) {}
    function save() { try { localStorage.setItem(KEY, JSON.stringify(P)); } catch (e) {} }
    var TYPES = [['grid', 'משבצות'], ['lines', 'שורות'], ['blank', 'חלק'], ['dots', 'נקודות'], ['graph', 'מילימטרי'], ['axes', 'מערכת צירים'], ['iso', 'איזומטרי'], ['hand', 'כתב יד']];
    var PAPERS = [['#ffffff', 'לבן'], ['#fffdf6', 'שמנת'], ['#f3faf3', 'ירוק עדין'], ['#f1f6ff', 'תכלת'], ['#fff8e1', 'צהוב רך']];
    var CELLS = [[20, 'צפוף'], [26, 'רגיל'], [34, 'מרווח']];
    var examType = null;
    function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
    function isOpen() { return ov.style.display && ov.style.display !== 'none'; }
    function relayout() { if (isOpen() && typeof resizePadCanvas === 'function') requestAnimationFrame(function () { resizePadCanvas(); }); }

    function getType() {
        if (hasPages) { var p = curPage(); return p.nb26 || p.bg || 'grid'; }
        if (examType) return examType;
        return area.classList.contains('bg-grid') ? 'grid' : area.classList.contains('bg-lines') ? 'lines' : 'blank';
    }
    function paint() {
        var t = getType();
        TYPES.forEach(function (x) { area.classList.remove('nb26-t-' + x[0]); });
        if (t !== 'grid' && t !== 'lines' && t !== 'blank') area.classList.add('nb26-t-' + t);
        if (btnSw) btnSw.className = 'nb26-sw nb26-t-' + t;
        if (btnTxt) TYPES.forEach(function (x) { if (x[0] === t) btnTxt.textContent = x[1]; });
        sheet.querySelectorAll('.nb26-type').forEach(function (b) { b.classList.toggle('on', b.dataset.t === t); });
    }
    function applyType(t) {
        if (typeof setPadBg === 'function') setPadBg(t === 'grid' || t === 'lines' ? t : 'blank');
        if (hasPages) { curPage().nb26 = t; curPage().nb26set = true; } else examType = t;
        paint();
    }
    function applyLook() {
        win.style.setProperty('--nb-paper', P.paper);
        win.style.setProperty('--nb-cell', P.cell + 'px');
        win.style.setProperty('--nb-qsize', P.qsize + 'rem');
        win.classList.toggle('nb26-margin', !!P.margin);
        win.classList.toggle('nb26-nospiral', !P.spiral);
        win.classList.toggle('nb26-qmin', !!P.qmin);
        qToggle.innerHTML = P.qmin ? '<i class="fa-solid fa-chevron-down"></i><span>הצגת התרגיל</span>' : '<i class="fa-solid fa-chevron-up"></i><span>הסתרה</span>';
        sheet.querySelectorAll('.nb26-paper').forEach(function (b) { b.classList.toggle('on', b.dataset.c === P.paper); });
        sheet.querySelectorAll('.nb26-seg button').forEach(function (b) { b.classList.toggle('on', +b.dataset.v === P.cell); });
        sheet.querySelectorAll('.nb26-switch').forEach(function (b) { b.classList.toggle('on', !!P[b.dataset.k]); });
    }

    /* --- כרטיס התרגיל: כל השאלה גלויה, אפשר לגלול, להסתיר ולהגדיל כתב --- */
    var qcard = el('div', 'nb26-qcard'), qhead = el('div', 'nb26-qhead');
    qhead.appendChild(el('span', 'nb26-qlabel', '<i class="fa-solid fa-circle-question"></i>התרגיל'));
    var qpeek = el('span', 'nb26-qpeek'); qhead.appendChild(qpeek);
    qhead.appendChild(el('span', 'nb26-grow'));
    var qMinus = el('button', 'nb26-qbtn nb26-qsize', 'א-'), qPlus = el('button', 'nb26-qbtn nb26-qsize', 'א+'), qToggle = el('button', 'nb26-qbtn');
    qMinus.type = qPlus.type = qToggle.type = 'button';
    qMinus.title = 'הקטנת הכתב'; qPlus.title = 'הגדלת הכתב';
    qhead.appendChild(qMinus); qhead.appendChild(qPlus); qhead.appendChild(qToggle);
    qc.parentNode.insertBefore(qcard, qc); qcard.appendChild(qhead); qcard.appendChild(qc);
    qMinus.onclick = function () { P.qsize = Math.max(.9, +(P.qsize - .14).toFixed(2)); save(); applyLook(); relayout(); };
    qPlus.onclick = function () { P.qsize = Math.min(1.8, +(P.qsize + .14).toFixed(2)); save(); applyLook(); relayout(); };
    qToggle.onclick = function () { P.qmin = !P.qmin; save(); applyLook(); relayout(); };
    qpeek.onclick = qToggle.onclick;

    /* --- כפתור "סוג מחברת" במקום שלושת כפתורי הרקע הישנים --- */
    var btn = el('button', 'nb26-paper-btn', '<span class="nb26-sw"></span><span class="nb26-btn-txt">משבצות</span><i class="fa-solid fa-chevron-down"></i>');
    btn.type = 'button'; btn.title = 'סוג המחברת וצבע הנייר'; btn.setAttribute('aria-expanded', 'false');
    var btnSw = btn.querySelector('.nb26-sw'), btnTxt = btn.querySelector('.nb26-btn-txt');
    var oldBg = win.querySelector('.nb-bg-btn');
    if (oldBg && oldBg.parentNode) {
        var grp = oldBg.parentNode; grp.classList.add('nb26-old-bg');
        var sep = grp.previousElementSibling; if (sep && sep.classList.contains('nb-sep')) sep.classList.add('nb26-old-bg');
        grp.parentNode.insertBefore(btn, grp);
        var sep2 = el('div', 'nb-sep'); grp.parentNode.insertBefore(sep2, btn);
    } else if (tb) tb.appendChild(btn);

    /* --- חלונית הגדרות המחברת --- */
    var sheet = el('div', 'nb26-sheet'); sheet.hidden = true; sheet.setAttribute('role', 'dialog'); sheet.setAttribute('aria-label', 'הגדרות המחברת');
    var h = '<div class="nb26-sheet-head"><b>הגדרות המחברת</b><button type="button" class="nb26-x" aria-label="סגירה"><i class="fa-solid fa-xmark"></i></button></div>';
    h += '<div class="nb26-sec"><span>סוג הדף</span><div class="nb26-types">';
    TYPES.forEach(function (t) { h += '<button type="button" class="nb26-type" data-t="' + t[0] + '"><span class="nb26-sw nb26-t-' + t[0] + '"></span>' + t[1] + '</button>'; });
    h += '</div></div><div class="nb26-sec"><span>צבע הנייר</span><div class="nb26-row">';
    PAPERS.forEach(function (c) { h += '<button type="button" class="nb26-paper" data-c="' + c[0] + '" title="' + c[1] + '" aria-label="' + c[1] + '" style="background:' + c[0] + '"></button>'; });
    h += '</div></div><div class="nb26-sec"><span>מרווח בין השורות והמשבצות</span><div class="nb26-seg">';
    CELLS.forEach(function (c) { h += '<button type="button" data-v="' + c[0] + '">' + c[1] + '</button>'; });
    h += '</div></div><div class="nb26-sec"><span>תוספות</span>';
    h += '<div class="nb26-switch" data-k="margin" role="switch">קו שוליים אדום<i></i></div>';
    h += '<div class="nb26-switch" data-k="spiral" role="switch">ספירלה בראש הדף<i></i></div></div>';
    h += '<div class="nb26-hint">הבחירה נשמרת במכשיר הזה. "שמירה כתמונה" שומרת את הכתיבה יחד עם הדף שבחרתם.</div>';
    sheet.innerHTML = h; win.appendChild(sheet);
    function openSheet(on) { sheet.hidden = !on; btn.setAttribute('aria-expanded', on ? 'true' : 'false'); }
    btn.onclick = function (e) { e.stopPropagation(); openSheet(sheet.hidden); };
    sheet.querySelector('.nb26-x').onclick = function () { openSheet(false); };
    sheet.addEventListener('click', function (e) {
        e.stopPropagation();
        var t = e.target.closest('.nb26-type'); if (t) { P.type = t.dataset.t; save(); applyType(P.type); return; }
        var c = e.target.closest('.nb26-paper'); if (c) { P.paper = c.dataset.c; save(); applyLook(); return; }
        var s = e.target.closest('.nb26-seg button'); if (s) { P.cell = +s.dataset.v; save(); applyLook(); return; }
        var w = e.target.closest('.nb26-switch'); if (w) { P[w.dataset.k] = !P[w.dataset.k]; save(); applyLook(); }
    });
    document.addEventListener('pointerdown', function (e) { if (!sheet.hidden && !sheet.contains(e.target) && !btn.contains(e.target) && !setBtn.contains(e.target)) openSheet(false); });

    /* --- כותרת: מסך מלא + שמירה כתמונה עם הדף --- */
    var actions = win.querySelector('.nb-header-actions');
    var fullBtn = el('button', 'nb-hbtn nb26-full-btn', '<i class="fa-solid fa-expand"></i>'); fullBtn.type = 'button'; fullBtn.title = 'מסך מלא';
    fullBtn.onclick = function () { var on = ov.classList.toggle('nb26-full'); fullBtn.innerHTML = on ? '<i class="fa-solid fa-compress"></i>' : '<i class="fa-solid fa-expand"></i>'; fullBtn.title = on ? 'יציאה ממסך מלא' : 'מסך מלא'; relayout(); };
    var dl = actions && actions.querySelector('[onclick*="downloadPad"]');
    if (dl) { dl.removeAttribute('onclick'); dl.classList.add('nb26-hbtn-wide', 'nb26-hbtn-gold'); dl.innerHTML = '<i class="fa-solid fa-download"></i><span>שמירה כתמונה</span>'; dl.onclick = function () { nb26Download(); }; }
    var setBtn = el('button', 'nb-hbtn nb26-set-btn', '<i class="fa-solid fa-sliders"></i>'); setBtn.type = 'button'; setBtn.title = 'הגדרות המחברת';
    setBtn.onclick = function (e) { e.stopPropagation(); openSheet(sheet.hidden); };
    if (actions) { actions.insertBefore(fullBtn, actions.firstChild); actions.insertBefore(setBtn, actions.firstChild); }

    function drawPaper(x, w, h, t, k) {
        var c = P.cell * k, ink = 'rgba(59,130,246,.17)', inkS = 'rgba(59,130,246,.34)', i, y;
        function line(x1, y1, x2, y2, col, lw) { x.strokeStyle = col; x.lineWidth = lw || 1; x.beginPath(); x.moveTo(x1, y1); x.lineTo(x2, y2); x.stroke(); }
        function grid(step, col, ox, oy) { for (i = ox; i <= w; i += step) line(i + .5, 0, i + .5, h, col); for (i = oy; i <= h; i += step) line(0, i + .5, w, i + .5, col); }
        if (t === 'grid') grid(c, ink, 0, 0);
        else if (t === 'lines') for (y = c * 1.25 - 1; y <= h; y += c * 1.25) line(0, y + .5, w, y + .5, inkS);
        else if (t === 'dots') { x.fillStyle = 'rgba(51,65,85,.42)'; for (var a = c / 2; a < w; a += c) for (y = c / 2; y < h; y += c) { x.beginPath(); x.arc(a, y, 1.3, 0, 7); x.fill(); } }
        else if (t === 'graph') { grid(c * .4, 'rgba(234,88,12,.12)', 0, 0); grid(c * 2, 'rgba(234,88,12,.32)', 0, 0); }
        else if (t === 'axes') { grid(c, ink, (w / 2) % c, (h / 2) % c); line(w / 2, 0, w / 2, h, '#334155', 2); line(0, h / 2, w, h / 2, '#334155', 2); }
        else if (t === 'iso') {
            var d = Math.hypot(w, h);
            [30, 150].forEach(function (deg) { var r = deg * Math.PI / 180, nx = -Math.sin(r), ny = Math.cos(r), dx = Math.cos(r), dy = Math.sin(r);
                for (var o = -d; o <= d; o += c) { var px = nx * o, py = ny * o; line(px - dx * d, py - dy * d, px + dx * d, py + dy * d, inkS); } });
            for (i = 0; i <= w; i += c * 1.1547) line(i + .5, 0, i + .5, h, ink);
        }
        else if (t === 'hand') for (y = c * .8; y <= h; y += c * 3) { line(0, y + .5, w, y + .5, inkS); line(0, y + c + .5, w, y + c + .5, 'rgba(148,163,184,.4)'); line(0, y + 2 * c, w, y + 2 * c, 'rgba(239,68,68,.45)'); }
        if (P.margin) line(w - 55 * k, 0, w - 55 * k, h, 'rgba(239,68,68,.42)', 2 * k);
    }
    function nb26Download() {
        try {
            if (typeof resizePadCanvas === 'function') resizePadCanvas();
            var c = document.getElementById('scratchpad-canvas'), r = c.getBoundingClientRect();
            if (!c.width || !c.height || !r.width) throw new Error('not-ready');
            var s = c.width / r.width, k = r.width / (area.clientWidth || r.width); if (!(k > .3 && k < 3)) k = 1;
            var out = document.createElement('canvas'); out.width = c.width; out.height = c.height;
            var x = out.getContext('2d'); x.fillStyle = P.paper; x.fillRect(0, 0, out.width, out.height);
            x.save(); x.scale(s, s); drawPaper(x, r.width, r.height, getType(), k); x.restore();
            x.drawImage(c, 0, 0);
            var suffix = hasPages && nbPages.length > 1 ? '-דף-' + (nbCurrentPage + 1) : '';
            var a = document.createElement('a'); a.download = 'המחברת-שלי' + suffix + '.png'; a.href = out.toDataURL('image/png');
            document.body.appendChild(a); a.click(); a.remove();
        } catch (e) { if (typeof downloadPad === 'function') downloadPad(); }
    }

    /* --- חיבור למנוע: פתיחה, מעבר דפים, דף חדש --- */
    var origOpen = window.openNotebook;
    if (typeof origOpen === 'function') window.openNotebook = function () {
        var r = origOpen.apply(this, arguments);
        var cl = qc.cloneNode(true); cl.querySelectorAll('mjx-assistive-mml, script, style').forEach(function (n) { n.remove(); });
        var txt = (cl.textContent || '').replace(/\s+/g, ' ').trim();
        qpeek.textContent = txt; qcard.classList.toggle('nb26-empty', !txt);
        if (P.type && (hasPages ? !curPage().nb26set : true)) applyType(P.type); else paint();
        openSheet(false); relayout();
        return r;
    };
    if (hasPages && typeof window.nbUpdatePageUI === 'function') {
        var origUpd = window.nbUpdatePageUI; window.nbUpdatePageUI = function () { var r = origUpd.apply(this, arguments); paint(); return r; };
    }
    if (hasPages && typeof window.nbAddPage === 'function') {
        var origAdd = window.nbAddPage; window.nbAddPage = function () {
            var prev = curPage(), r;
            r = origAdd.apply(this, arguments);
            if (curPage() !== prev) { curPage().nb26 = prev.nb26 || prev.bg; curPage().nb26set = true; paint(); }
            return r;
        };
    }
    if (window.ResizeObserver) { var rq = 0; new ResizeObserver(function () { if (!isOpen()) return; cancelAnimationFrame(rq); rq = requestAnimationFrame(function () { resizePadCanvas(); }); }).observe(area); }
    applyLook(); paint();
})();

/* אורך השאלה ← גודל הכתב שלה (קצרה / בינונית / ארוכה), כך ששאלה ארוכה לא תתפוס מסך שלם אבל תמיד תישאר גדולה מהתשובות */
(function () {
    var q = document.getElementById('q-text'); if (!q || !window.MutationObserver) return;
    function mark() {
        var c = q.cloneNode(true); Array.prototype.forEach.call(c.querySelectorAll('mjx-container, svg, script, style'), function (n) { n.remove(); });
        var n = (c.textContent || '').replace(/\s+/g, ' ').trim().length, v = n > 320 ? 'l' : n > 170 ? 'm' : 's';
        if (q.getAttribute('data-qlen') !== v) q.setAttribute('data-qlen', v);
    }
    new MutationObserver(mark).observe(q, { childList: true, subtree: true, characterData: true }); mark();
})();
