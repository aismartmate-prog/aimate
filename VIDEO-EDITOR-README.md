<div dir="rtl">

# AY Video Editor – תנו ל-Claude לערוך לכם את הסרטון

מערכת עריכת וידאו ל-[Claude Code](https://claude.com/product/claude-code), של [AY Digital Marketing](https://github.com/Amiryaco). מצלמים טייק אחד בטלפון, ו-Claude מתמלל כל מילה בעברית, חותך, מוסיף זומים, כתוביות, כרטיס מותג וסאונד – ומחזיר סרטון אנכי מוכן לרילס, טיקטוק ושורטס. בלי טיימליין ובלי תוכנת עריכה.

> ⭐ **אם המערכת עזרה לכם ליצור סרטונים טובים יותר, נשמח לכוכב (Star) במאגר.** זה עוזר לנו להמשיך לפתח ולשתף כלים חדשים.

## מה מקבלים

| Skill | מה הוא עושה |
|---|---|
| [`brand-reels`](.claude/skills/brand-reels/SKILL.md) | **מתחילים כאן.** סגנון הבית והתהליך המלא: חיתוך, זומים עדינים, גריידינג, כרטיס מותג שמתחלף על המילים, כתוביות, סאונד, בדיקה ומסירה. |
| [`video-edit`](.claude/skills/video-edit/SKILL.md) | מנוע העריכה: תמלול (עברית עם ivrit-ai, אנגלית), ניתוח שתיקות, פנים וטייקים חוזרים, חיתוך, זומים, מעברים, מוזיקה ועוצמה. |
| [`hebrew-captions`](.claude/skills/hebrew-captions/SKILL.md) | כתוביות צרובות מימין לשמאל, מילה אחר מילה, כולל מספרים ואנגלית בסדר הנכון, וקובץ ‎.srt. |
| [`motion-broll`](.claude/skills/motion-broll/SKILL.md) | גרפיקה בתנועה כ-HTML: צורה אחת שמשתנה על המילים, מרונדרת עם רקע שקוף. |

וגם: [`CLAUDE.md`](CLAUDE.md) (הוראות הפרויקט ל-Claude), [`examples/showcase`](examples/showcase) (תבנית לסרטון "העורך שמציית לקול"), ו-[`scripts/setup-env.sh`](scripts/setup-env.sh) (התקנה אוטומטית בענן).

## התקנה: מעתיקים, מדביקים, עורכים

**1. מעתיקים את הקישור:**

```
https://github.com/Amiryaco/ay-video-editor.git
```

**2. פותחים Claude Code בתיקייה ריקה** (באפליקציית Claude לדסקטופ או בטרמינל) **ומדביקים:**

```
שכפל לתיקייה הזו את https://github.com/Amiryaco/ay-video-editor.git עם git clone. קרא את README.md ואת CLAUDE.md והתקן כל מה שחסר לפי סעיף Requirements – ושאל אותי לפני כל התקנה. בסוף הרץ בדיקת תקינות, ותגיד לי איך להפעיל אותך מחדש מתוך התיקייה ay-video-editor כדי להשתמש ב-Skills.
```

**3. מפעילים את Claude Code מחדש מתוך התיקייה `ay-video-editor`**, מעלים סרטון וכותבים: *"תערוך ממותג, נקי וקריאייטיבי"*.

### בענן (בלי להתקין כלום)

ב-[claude.ai/code](https://claude.ai/code) בוחרים את המאגר `Amiryaco/ay-video-editor`. סקריפט ההתקנה רץ לבד בתחילת כל סשן. בהגדרות הסביבה (Network access ← Custom) מסמנים *Also include default list of common package managers* ומוסיפים:

```
huggingface.co
*.hf.co
drive.google.com
drive.usercontent.google.com
```

(השניים האחרונים רק אם מעבירים סרטונים דרך Google Drive.)

### ידנית

```bash
git clone https://github.com/Amiryaco/ay-video-editor.git
cd ay-video-editor
claude
```

## ה-Claude שלכם לומד לבד

- **כל עותק עומד בפני עצמו.** מה שתלמדו את Claude – סגנון הכתוביות, כמה זום, איך לאיית שמות, ה-CTA שלכם – הוא שומר אצלכם בקובץ `motion/my-notes.md`, ואת המותג ב-`motion/brands.json`. שום דבר לא חוזר למאגר הזה.
- **אין עדכונים אוטומטיים.** העותק שלכם נשאר כמו שהוא עד שתבקשו. רוצים את הגרסה החדשה? כתבו ל-Claude *"עדכן את מערכת העריכה"* – הוא ישמור קודם את השינויים שלכם.
- **בענן** כל סשן מתחיל מעותק נקי של המאגר, ולכן ההערות לא נשמרות בין סשנים. הדביקו את פרטי המותג וההעדפות שלכם בתחילת כל סשן, או עבדו במחשב – שם הלמידה נשמרת.

</div>

## Requirements

- **Claude Code** (Pro, Max, Team or Enterprise plan).
- **ffmpeg** with libass and `prores_ks`.
- **Python 3.10+** with `numpy`, `opencv-python-headless<5`, `uharfbuzz`, `fonttools`, `faster-whisper`.
- **Node.js 18+** with Playwright and Chromium in `motion/node_modules`.

**macOS** (Homebrew):

```bash
brew install ffmpeg python node git
python3 -m venv .venv && source .venv/bin/activate
pip install numpy "opencv-python-headless<5" uharfbuzz fonttools faster-whisper
bash .claude/skills/motion-broll/scripts/setup.sh ./motion
python3 .claude/skills/video-edit/scripts/make_sfx.py motion/inputs/sfx
```

**Windows:** Claude Code runs natively, but some scripts are Bash. Install [Git for Windows](https://git-scm.com/downloads/win) (Git Bash) or, more reliably, use **WSL 2 (Ubuntu)** with `sudo apt install ffmpeg python3-venv nodejs npm git` and the same steps as macOS.

**Cloud (claude.ai/code):** nothing to install; `scripts/setup-env.sh` runs on session start. Allow the network domains listed above.

## Layout

```
.claude/skills/        the four skills (SKILL.md, scripts, references, templates)
CLAUDE.md              project instructions Claude reads at the start of every session
motion/brands.json     brand kit per business (colours, name) – add your own
motion/clips/          your card sources
examples/showcase/     template for the "editor that obeys my voice" format
scripts/setup-env.sh   automatic setup for cloud sessions
```

Per-video work folders (`motion/v*/`), renders and video files are git-ignored.

## Credits and licences

- Built by **Amir Yacoby / AY Digital Marketing**. Code under the [MIT licence](LICENSE).
- `motion-broll` engine: © Barty-Bart, MIT ([LICENSE](.claude/skills/motion-broll/LICENSE)), with Hebrew/RTL additions.
- Hebrew transcription model: [ivrit-ai/whisper-large-v3-turbo-ct2](https://huggingface.co/ivrit-ai/whisper-large-v3-turbo-ct2) via [faster-whisper](https://github.com/SYSTRAN/faster-whisper).
- Fonts: Heebo, Rubik, Noto Sans Hebrew/Symbols, Geist (SIL OFL); licence texts sit next to the font files. Icons from [Lucide](https://lucide.dev) (ISC).
