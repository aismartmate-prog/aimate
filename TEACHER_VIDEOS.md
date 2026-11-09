# סרטוני לופ למורים (אופציונלי)

לכל מורה (yoni, maya, ido, noa) מניחים בתיקייה `images/teachers/` עד 4 קבצי mp4 קצרים (3-6 שניות, בלי סאונד):

| קובץ | מתי מוצג | מה צריך להיות בו |
|---|---|---|
| `yoni_idle.mp4` | מוכן / ברירת מחדל | נשימה, מצמוץ, תזוזה קטנה, פה סגור |
| `yoni_talk.mp4` | המורה מדבר | מדבר רגיל למצלמה, פה זז, תזוזות ראש וגבות |
| `yoni_listen.mp4` | התלמיד מדבר | הטיית ראש קלה, הנהון, חיוך, פה סגור |
| `yoni_think.mp4` | חושב לפני תשובה | מבט למעלה לצד, גבה מורמת, פה סגור |

חובה: `idle` ו-`talk`. אם `listen`/`think` חסרים - מוצג idle. אם הכול חסר - נשארת התמונה (`yoni.jpg`).

## פרומפט לכלי וידאו (תמונה -> וידאו), מעלים את תמונת המורה
- idle: `Photo-realistic portrait, same person, subtle breathing, occasional natural blink, tiny head movement, neutral friendly expression, mouth closed, static camera, seamless loop`
- talk: `Same person speaking naturally to the camera as a friendly teacher, mouth moving continuously like in conversation, slight head and eyebrow movements, static camera, seamless loop`
- listen: `Same person listening attentively, slight head tilt, small nods, gentle smile, blinking, mouth closed, static camera`
- think: `Same person thinking, eyes looking up and to the side, one eyebrow raised, slight head tilt, mouth closed, static camera`

## דחיסה ולופ חלק (ffmpeg)
```bash
# דחיסה קטנה בלי סאונד
ffmpeg -i in.mp4 -an -vf "scale=480:-2" -c:v libx264 -crf 28 -movflags +faststart yoni_talk.mp4
# לופ חלק: מנגן קדימה ואחורה
ffmpeg -i in.mp4 -an -filter_complex "[0:v]split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1[v]" -map "[v]" -c:v libx264 -crf 28 -movflags +faststart yoni_idle.mp4
```
