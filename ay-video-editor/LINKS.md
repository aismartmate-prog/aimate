<div dir="rtl">

# AY Video Editor – קישורים להורדה

מערכת עריכת הסרטונים מהמדריך "תנו ל-Claude לערוך לכם את הסרטון" (AY Digital Marketing, עמיר יעקובי).
המקור: **https://github.com/Amiryaco/ay-video-editor** (רישיון MIT – חינם לשימוש ולהעתקה).

התיקייה הזו (`ay-video-editor/`) מחכה לקבצים. בחר אחת משלוש הדרכים:

## דרך 1 – הכי קלה: להוריד הכל בקובץ ZIP אחד ⭐

1. הורד: **https://github.com/Amiryaco/ay-video-editor/archive/refs/heads/main.zip**
2. חלץ את הקובץ.
3. העתק את **כל התוכן** של התיקייה `ay-video-editor-main` (כולל התיקייה הנסתרת `.claude`!) לתוך התיקייה הזו.
   - במק: ב-Finder לחץ `Cmd+Shift+.` כדי לראות קבצים נסתרים.
   - בווינדוס: בסייר הקבצים ← תצוגה ← הצג ← "פריטים מוסתרים".

## דרך 2 – Fork (גרסה קבועה בחשבון GitHub שלך)

1. היכנס ל-https://github.com/Amiryaco/ay-video-editor/fork ולחץ **Create fork**.
2. ב-[claude.ai/code](https://claude.ai/code) בחר את המאגר החדש שלך (`aismartmate-prog/ay-video-editor`).
3. בהגדרות הסביבה ← Network access ← Custom: סמן *Also include default list of common package managers* והוסף:
   ```
   huggingface.co
   *.hf.co
   drive.google.com
   drive.usercontent.google.com
   ```

## דרך 3 – בטרמינל

```bash
cd ay-video-editor
git clone https://github.com/Amiryaco/ay-video-editor.git tmp && cp -R tmp/. . && rm -rf tmp/.git tmp
```

## אחרי ההורדה

- פתח Claude Code **מתוך התיקייה `ay-video-editor`** (רק כך ה-Skills נטענים).
- הדבק: *"קרא את README.md ואת CLAUDE.md והתקן כל מה שחסר לפי סעיף Requirements – ושאל אותי לפני כל התקנה. בסוף הרץ בדיקת תקינות."*
- כלים שצריך במחשב: FFmpeg, Python 3, Node.js, Git (פירוט בעמוד 04 במדריך).

---

## כל הקבצים – אחד-אחד

חשוב: שמור כל קובץ **בדיוק בנתיב שמופיע** (כולל התיקיות), אחרת Claude לא ימצא אותו.
קבצי פונטים (`.ttf`, `.woff2`) – השתמש בקישור "הורד".

### קבצי בסיס (שורש התיקייה)

| קובץ | צפייה | הורדה ישירה |
|---|---|---|
| `CLAUDE.md` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/CLAUDE.md) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/CLAUDE.md) |
| `README.md` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/README.md) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/README.md) |
| `LICENSE` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/LICENSE) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/LICENSE) |
| `.gitignore` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.gitignore) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.gitignore) |
| `.claude/settings.json` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/settings.json) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/settings.json) |

### Skill 1: brand-reels (מתחילים כאן – סגנון הבית והתהליך המלא)

| קובץ | צפייה | הורדה ישירה |
|---|---|---|
| `.claude/skills/brand-reels/SKILL.md` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/SKILL.md) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/SKILL.md) |
| `.claude/skills/brand-reels/reference/card-patterns.md` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/reference/card-patterns.md) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/reference/card-patterns.md) |
| `.claude/skills/brand-reels/reference/lessons.md` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/reference/lessons.md) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/reference/lessons.md) |
| `.claude/skills/brand-reels/reference/showcase-effects.md` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/reference/showcase-effects.md) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/reference/showcase-effects.md) |
| `.claude/skills/brand-reels/scripts/auto_cut.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/scripts/auto_cut.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/scripts/auto_cut.py) |
| `.claude/skills/brand-reels/scripts/deliver.sh` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/scripts/deliver.sh) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/scripts/deliver.sh) |
| `.claude/skills/brand-reels/scripts/fetch_drive.sh` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/scripts/fetch_drive.sh) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/scripts/fetch_drive.sh) |
| `.claude/skills/brand-reels/scripts/grade.sh` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/scripts/grade.sh) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/scripts/grade.sh) |
| `.claude/skills/brand-reels/scripts/make_finish.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/scripts/make_finish.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/scripts/make_finish.py) |
| `.claude/skills/brand-reels/scripts/make_tips_card.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/scripts/make_tips_card.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/scripts/make_tips_card.py) |
| `.claude/skills/brand-reels/scripts/person_matte.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/scripts/person_matte.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/scripts/person_matte.py) |
| `.claude/skills/brand-reels/scripts/smooth_cut.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/scripts/smooth_cut.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/scripts/smooth_cut.py) |
| `.claude/skills/brand-reels/scripts/sprites.js` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/scripts/sprites.js) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/scripts/sprites.js) |
| `.claude/skills/brand-reels/scripts/stills.sh` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/scripts/stills.sh) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/scripts/stills.sh) |
| `.claude/skills/brand-reels/templates/ab-choice.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/templates/ab-choice.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/templates/ab-choice.html) |
| `.claude/skills/brand-reels/templates/late-message.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/templates/late-message.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/templates/late-message.html) |
| `.claude/skills/brand-reels/templates/signs-tracker-chips.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/templates/signs-tracker-chips.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/templates/signs-tracker-chips.html) |
| `.claude/skills/brand-reels/templates/story-calendar.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/templates/story-calendar.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/templates/story-calendar.html) |
| `.claude/skills/brand-reels/templates/story-list-quote-compare.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/templates/story-list-quote-compare.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/templates/story-list-quote-compare.html) |
| `.claude/skills/brand-reels/templates/tips-spec.example.json` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/templates/tips-spec.example.json) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/templates/tips-spec.example.json) |
| `.claude/skills/brand-reels/templates/zodiac-coin-3d.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/brand-reels/templates/zodiac-coin-3d.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/brand-reels/templates/zodiac-coin-3d.html) |

### Skill 2: video-edit (מנוע העריכה – תמלול, חיתוך, זומים, סאונד)

| קובץ | צפייה | הורדה ישירה |
|---|---|---|
| `.claude/skills/video-edit/SKILL.md` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/video-edit/SKILL.md) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/video-edit/SKILL.md) |
| `.claude/skills/video-edit/scripts/align_script.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/video-edit/scripts/align_script.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/video-edit/scripts/align_script.py) |
| `.claude/skills/video-edit/scripts/analyze.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/video-edit/scripts/analyze.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/video-edit/scripts/analyze.py) |
| `.claude/skills/video-edit/scripts/common.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/video-edit/scripts/common.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/video-edit/scripts/common.py) |
| `.claude/skills/video-edit/scripts/finish.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/video-edit/scripts/finish.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/video-edit/scripts/finish.py) |
| `.claude/skills/video-edit/scripts/make_callouts.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/video-edit/scripts/make_callouts.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/video-edit/scripts/make_callouts.py) |
| `.claude/skills/video-edit/scripts/make_sfx.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/video-edit/scripts/make_sfx.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/video-edit/scripts/make_sfx.py) |
| `.claude/skills/video-edit/scripts/render_cut.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/video-edit/scripts/render_cut.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/video-edit/scripts/render_cut.py) |
| `.claude/skills/video-edit/scripts/sheet.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/video-edit/scripts/sheet.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/video-edit/scripts/sheet.py) |
| `.claude/skills/video-edit/scripts/transcribe.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/video-edit/scripts/transcribe.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/video-edit/scripts/transcribe.py) |

### Skill 3: hebrew-captions (כתוביות עבריות מימין לשמאל)

| קובץ | צפייה | הורדה ישירה |
|---|---|---|
| `.claude/skills/hebrew-captions/SKILL.md` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/hebrew-captions/SKILL.md) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/hebrew-captions/SKILL.md) |
| `.claude/skills/hebrew-captions/fonts/Heebo-Black.ttf` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/hebrew-captions/fonts/Heebo-Black.ttf) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/hebrew-captions/fonts/Heebo-Black.ttf) |
| `.claude/skills/hebrew-captions/fonts/Heebo-Bold.ttf` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/hebrew-captions/fonts/Heebo-Bold.ttf) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/hebrew-captions/fonts/Heebo-Bold.ttf) |
| `.claude/skills/hebrew-captions/fonts/Heebo-Medium.ttf` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/hebrew-captions/fonts/Heebo-Medium.ttf) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/hebrew-captions/fonts/Heebo-Medium.ttf) |
| `.claude/skills/hebrew-captions/fonts/NotoSansHebrew-Black.ttf` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/hebrew-captions/fonts/NotoSansHebrew-Black.ttf) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/hebrew-captions/fonts/NotoSansHebrew-Black.ttf) |
| `.claude/skills/hebrew-captions/fonts/OFL-Heebo.txt` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/hebrew-captions/fonts/OFL-Heebo.txt) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/hebrew-captions/fonts/OFL-Heebo.txt) |
| `.claude/skills/hebrew-captions/fonts/OFL-NotoSansHebrew.txt` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/hebrew-captions/fonts/OFL-NotoSansHebrew.txt) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/hebrew-captions/fonts/OFL-NotoSansHebrew.txt) |
| `.claude/skills/hebrew-captions/fonts/OFL-Rubik.txt` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/hebrew-captions/fonts/OFL-Rubik.txt) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/hebrew-captions/fonts/OFL-Rubik.txt) |
| `.claude/skills/hebrew-captions/fonts/Rubik-Black.ttf` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/hebrew-captions/fonts/Rubik-Black.ttf) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/hebrew-captions/fonts/Rubik-Black.ttf) |
| `.claude/skills/hebrew-captions/fonts/Rubik-Bold.ttf` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/hebrew-captions/fonts/Rubik-Bold.ttf) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/hebrew-captions/fonts/Rubik-Bold.ttf) |
| `.claude/skills/hebrew-captions/fonts/Rubik-Medium.ttf` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/hebrew-captions/fonts/Rubik-Medium.ttf) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/hebrew-captions/fonts/Rubik-Medium.ttf) |
| `.claude/skills/hebrew-captions/scripts/make_captions.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/hebrew-captions/scripts/make_captions.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/hebrew-captions/scripts/make_captions.py) |

### Skill 4: motion-broll (כרטיסי מותג וגרפיקה בתנועה)

| קובץ | צפייה | הורדה ישירה |
|---|---|---|
| `.claude/skills/motion-broll/LICENSE` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/LICENSE) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/LICENSE) |
| `.claude/skills/motion-broll/SKILL.md` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/SKILL.md) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/SKILL.md) |
| `.claude/skills/motion-broll/engine/base.css` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/engine/base.css) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/engine/base.css) |
| `.claude/skills/motion-broll/engine/beats.js` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/engine/beats.js) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/engine/beats.js) |
| `.claude/skills/motion-broll/engine/build.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/engine/build.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/engine/build.py) |
| `.claude/skills/motion-broll/engine/fonts/Geist-Variable.woff2` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/engine/fonts/Geist-Variable.woff2) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/engine/fonts/Geist-Variable.woff2) |
| `.claude/skills/motion-broll/engine/fonts/GeistMono-Medium.woff2` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/engine/fonts/GeistMono-Medium.woff2) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/engine/fonts/GeistMono-Medium.woff2) |
| `.claude/skills/motion-broll/engine/fonts/Heebo-Hebrew-Variable.woff2` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/engine/fonts/Heebo-Hebrew-Variable.woff2) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/engine/fonts/Heebo-Hebrew-Variable.woff2) |
| `.claude/skills/motion-broll/engine/fonts/NotoSansSymbols-Zodiac.woff2` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/engine/fonts/NotoSansSymbols-Zodiac.woff2) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/engine/fonts/NotoSansSymbols-Zodiac.woff2) |
| `.claude/skills/motion-broll/engine/fonts/OFL-Geist.txt` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/engine/fonts/OFL-Geist.txt) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/engine/fonts/OFL-Geist.txt) |
| `.claude/skills/motion-broll/engine/fonts/OFL-Heebo.txt` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/engine/fonts/OFL-Heebo.txt) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/engine/fonts/OFL-Heebo.txt) |
| `.claude/skills/motion-broll/engine/fonts/OFL-NotoSansSymbols.txt` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/engine/fonts/OFL-NotoSansSymbols.txt) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/engine/fonts/OFL-NotoSansSymbols.txt) |
| `.claude/skills/motion-broll/engine/motion.js` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/engine/motion.js) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/engine/motion.js) |
| `.claude/skills/motion-broll/engine/render.js` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/engine/render.js) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/engine/render.js) |
| `.claude/skills/motion-broll/examples/opus-aoe2/01-opus-drop.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/examples/opus-aoe2/01-opus-drop.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/examples/opus-aoe2/01-opus-drop.html) |
| `.claude/skills/motion-broll/examples/opus-aoe2/02-pip-builds.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/examples/opus-aoe2/02-pip-builds.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/examples/opus-aoe2/02-pip-builds.html) |
| `.claude/skills/motion-broll/examples/opus-aoe2/03-effort-slider.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/examples/opus-aoe2/03-effort-slider.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/examples/opus-aoe2/03-effort-slider.html) |
| `.claude/skills/motion-broll/examples/opus-aoe2/04-master-prompt.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/examples/opus-aoe2/04-master-prompt.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/examples/opus-aoe2/04-master-prompt.html) |
| `.claude/skills/motion-broll/examples/opus-aoe2/05-low-vs-max.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/examples/opus-aoe2/05-low-vs-max.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/examples/opus-aoe2/05-low-vs-max.html) |
| `.claude/skills/motion-broll/examples/opus-aoe2/06-chapter.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/examples/opus-aoe2/06-chapter.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/examples/opus-aoe2/06-chapter.html) |
| `.claude/skills/motion-broll/examples/opus-aoe2/plan.json` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/examples/opus-aoe2/plan.json) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/examples/opus-aoe2/plan.json) |
| `.claude/skills/motion-broll/reference/engine-api.md` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/reference/engine-api.md) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/reference/engine-api.md) |
| `.claude/skills/motion-broll/scripts/composite.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/scripts/composite.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/scripts/composite.py) |
| `.claude/skills/motion-broll/scripts/inspect_video.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/scripts/inspect_video.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/scripts/inspect_video.py) |
| `.claude/skills/motion-broll/scripts/make_pages.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/scripts/make_pages.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/scripts/make_pages.py) |
| `.claude/skills/motion-broll/scripts/setup.sh` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/scripts/setup.sh) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/scripts/setup.sh) |
| `.claude/skills/motion-broll/scripts/words.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/scripts/words.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/scripts/words.py) |
| `.claude/skills/motion-broll/templates/compare.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/templates/compare.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/templates/compare.html) |
| `.claude/skills/motion-broll/templates/viewer.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/.claude/skills/motion-broll/templates/viewer.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/.claude/skills/motion-broll/templates/viewer.html) |

### תיקיית motion (המותג שלך)

| קובץ | צפייה | הורדה ישירה |
|---|---|---|
| `motion/brands.json` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/motion/brands.json) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/motion/brands.json) |

### סקריפט התקנה

| קובץ | צפייה | הורדה ישירה |
|---|---|---|
| `scripts/setup-env.sh` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/scripts/setup-env.sh) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/scripts/setup-env.sh) |

### דוגמה: examples/showcase

| קובץ | צפייה | הורדה ישירה |
|---|---|---|
| `examples/showcase/coin.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/examples/showcase/coin.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/examples/showcase/coin.html) |
| `examples/showcase/compose.py` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/examples/showcase/compose.py) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/examples/showcase/compose.py) |
| `examples/showcase/cut.json` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/examples/showcase/cut.json) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/examples/showcase/cut.json) |
| `examples/showcase/finish.json` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/examples/showcase/finish.json) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/examples/showcase/finish.json) |
| `examples/showcase/layout.sh` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/examples/showcase/layout.sh) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/examples/showcase/layout.sh) |
| `examples/showcase/layout_sprites.json` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/examples/showcase/layout_sprites.json) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/examples/showcase/layout_sprites.json) |
| `examples/showcase/reels.html` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/examples/showcase/reels.html) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/examples/showcase/reels.html) |
| `examples/showcase/script.txt` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/examples/showcase/script.txt) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/examples/showcase/script.txt) |
| `examples/showcase/sprites.json` | [פתח](https://github.com/Amiryaco/ay-video-editor/blob/main/examples/showcase/sprites.json) | [הורד](https://raw.githubusercontent.com/Amiryaco/ay-video-editor/main/examples/showcase/sprites.json) |

</div>
