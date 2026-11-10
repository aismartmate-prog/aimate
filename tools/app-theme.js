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
