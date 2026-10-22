/* pwa.js: הופך כל עמוד באתר לאפליקציה כשמוסיפים אותו למסך הבית (iPhone / Android).
   מספיק לטעון אותו בכל עמוד: <script src="/pwa.js"></script>
   מוסיף לבד את תגיות האפליקציה (אם חסרות), רושם service worker,
   וכשהאפליקציה נפתחת מהאייקון פותח קודם את מסך הבית שלה. */
(function () {
  /* משתמשים באפליקציה הקיימת שלך (הלאנצ'ר): אותו manifest, אותו אייקון, אותו שם. לא מוסיפים שום דבר חדש. */
  var CFG = {
    manifest: '/manifest.json',          // הקובץ הקיים של הלאנצ'ר
    icon: '/icon-192.png',               // האייקון הקיים של הלאנצ'ר
    title: 'TIRGULIM',                   // אותו שם שמוגדר היום בלאנצ'ר
    theme: '#0b1d4d',
    home: '/launcher.html'               // מסך הבית של האפליקציה (הלאנצ'ר)
  };

  /* 1. תגיות האפליקציה בראש הדף (רק אם עוד לא קיימות) */
  try {
    var head = document.head || document.getElementsByTagName('head')[0];
    var add = function (tag, attrs, key) {
      if (head.querySelector(key)) return;
      var el = document.createElement(tag);
      for (var k in attrs) el.setAttribute(k, attrs[k]);
      head.appendChild(el);
    };
    add('link', { rel: 'manifest', href: CFG.manifest }, 'link[rel="manifest"]');
    add('link', { rel: 'apple-touch-icon', href: CFG.icon }, 'link[rel="apple-touch-icon"]');
    add('meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }, 'meta[name="apple-mobile-web-app-capable"]');
    add('meta', { name: 'mobile-web-app-capable', content: 'yes' }, 'meta[name="mobile-web-app-capable"]');
    add('meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' }, 'meta[name="apple-mobile-web-app-status-bar-style"]');
    add('meta', { name: 'apple-mobile-web-app-title', content: CFG.title }, 'meta[name="apple-mobile-web-app-title"]');
    add('meta', { name: 'theme-color', content: CFG.theme }, 'meta[name="theme-color"]');
    var vp = head.querySelector('meta[name="viewport"]');
    if (vp && !/viewport-fit/.test(vp.content)) vp.setAttribute('content', vp.content + ', viewport-fit=cover');
  } catch (e) {}

  /* 2. כשהאפליקציה נפתחת מהאייקון: פעם אחת בכל הפעלה, פותחים את מסך הבית שלה */
  var standalone = (window.navigator.standalone === true) || (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches);
  if (standalone) {
    try {
      if (!sessionStorage.getItem('pwa_started')) {
        sessionStorage.setItem('pwa_started', '1');
        /* לא מחזירים ללאנצ'ר כשהגענו אליו מבחירת מערכת (קידס / תרגולים), ולא על תת-הדומיין של הקידס - אחרת מסך הפתיחה נטען שוב */
        var skipHome = /^kids\./.test(location.hostname) || /[?&]nosplash=1(&|$)/.test(location.search);
        try { if (document.referrer && /(^|\.)tirgulim\.co\.il$/.test(new URL(document.referrer).hostname)) skipHome = true; } catch (e2) {}
        var p = location.pathname.replace(/index\.html$/, '');
        if (!skipHome && p !== CFG.home && !(CFG.home === '/' && p === '/')) { location.replace(CFG.home); return; }
      }
    } catch (e) {}
  }

  /* 3. service worker (נדרש להתקנה בדפדפנים אחרים) */
  if ('serviceWorker' in navigator) { try { navigator.serviceWorker.register('/sw.js').catch(function () {}); } catch (e) {} }
})();
