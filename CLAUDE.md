# AY Video Editor

A Claude Code workspace that turns a raw talking-head video into a finished, branded vertical reel. Built by AY Digital Marketing.

## Skills

- `.claude/skills/brand-reels/`: **start here for any "edit this branded / clean / creative" request.** The house style for short-form edits (Reels/TikTok/Shorts): video from an upload or Google Drive, tight cut, a few gentle zooms, warm grade, one brand card on the meaningful lines only (30-40% of the runtime) that changes on the spoken words (hook, list, numbered tips, quote, compare, checklist, calendar story, send/follow), soft captions under the face, sparse sound, -14 LUFS. It orchestrates the three below.
- `.claude/skills/video-edit/`: the editing engine. Raw footage → transcription (Hebrew via ivrit-ai, English), analysis (silences, face, retakes), cut with zooms and transitions, B-roll, captions, sound effects, music and loudness. Its full workflow: interview → transcribe and analyse → plan table and **wait for approval** → cut → B-roll → captions → finish → check stills and loudness → deliver.
- `.claude/skills/motion-broll/`: motion-graphic clips as HTML (one shape that morphs on springs, a cursor that drives every change), rendered frame-exact with alpha. Imported from [Barty-Bart/motion-graphics](https://github.com/Barty-Bart/motion-graphics) (MIT) with Hebrew/RTL additions. **Read its `SKILL.md` and `reference/engine-api.md` before writing clips.**
- `.claude/skills/hebrew-captions/`: burned-in captions (Hebrew RTL or English) laid out word by word with HarfBuzz, plus an `.srt`.

For "wow" showcase edits where the speaker commands effects on camera ("zoom on my hand", "split into layers", "hide me"), follow `brand-reels/reference/showcase-effects.md` and the template in `examples/showcase/`. For B-roll only use `/motion-broll`; for captions only use `/hebrew-captions`.

## Environment

- **Cloud sessions:** `scripts/setup-env.sh` runs on session start (hook in `.claude/settings.json`) and installs ffmpeg (with `prores_ks` and libass), numpy, OpenCV 4, HarfBuzz, fontTools, faster-whisper and Playwright into `motion/node_modules` (using the pre-installed Chromium), and generates the sound effects into `motion/inputs/sfx/`. Don't run `motion-broll/scripts/setup.sh` there (it downloads Chromium).
- **Local machine:** see VIDEO-EDITOR-README.md → Requirements. `motion-broll/scripts/setup.sh ./motion` installs Playwright + Chromium; run `python3 .claude/skills/video-edit/scripts/make_sfx.py motion/inputs/sfx` once for the sound effects.
- Run engine scripts from the repo root with `NODE_PATH=./motion/node_modules`.
- Working folders: `motion/inputs/` (brand assets, logos, sfx), `motion/clips/` (card sources), `motion/v*/`, `motion/work/`, `motion/dist/`, `motion/out/` (generated, git-ignored).
- Transcription downloads Whisper models from Hugging Face. A cloud environment's network access must allow `huggingface.co` **and** its file storage (`*.hf.co`, or: `cas-server.xethub.hf.co`, `cas-bridge.xethub.hf.co`, `transfer.xethub.hf.co`, `cdn-lfs.hf.co`, `cdn-lfs-us-1.hf.co`, `us.aws.cdn.hf.co`). Without them the model metadata loads but the weights fail (CAS/403 errors); ask the user for an SRT meanwhile, and tell them which domains to add. Google Drive intake needs `drive.google.com` and `drive.usercontent.google.com`.

## Brands

Each business or character has a brand kit in `motion/brands.json` (colours, niche, handle). **Read it before building cards and use those colours.** When the user gives a business name or colours, add or update its entry. If the user pasted a brand prompt at the start of the session, it overrides the file for that session. Put a name on the Follow/CTA card only in that brand's own videos; unknown brand → "Follow for more", no name.

## Working rules

- **Output format:** vertical **1080×1920** (9:16) for Reels/TikTok/Shorts unless the user asks for 16:9. Pass `--W 1080 --H 1920` to every script that takes a size. Match the source fps.
- **Never invent** numbers, quotes, results or names. Every word on screen is the speaker's own, shortened.
- **Cards/pop-ups on 30-40% of the runtime only**; 60-70% is the speaker with captions. See "Windows" in `brand-reels/reference/card-patterns.md`.
- **Zooms: gentle and few.** 2-4 emphasis lines (+6-10%), return to the base framing, at most one or two snap zooms per video.
- **Captions default:** `--style soft --below-face <rough.mp4>`; over a light background add `--strong-shadow`. Fix names and English terms first (`--fix`). Check stills: Hebrew must read right to left, including numbers and English words.
- **Hebrew in cards:** put `class="rtl"` on Hebrew text and mirror the layout (leading element on the right, bars filling right to left). See "Hebrew and RTL" in `motion-broll/reference/engine-api.md`.
- **Before delivering:** stills of every card state, loudness (I ≈ -14 LUFS, peak below -1 dBFS), resolution, caption sync, no word cut mid-way. Deliver `final.mp4` and `captions.srt`; the parts (`rough.mp4`, card clips) are available for anyone who wants to finish in their own editor.
- Video files are git-ignored; never put the user's videos in git.

## Local learning (each copy learns on its own)

This repository is the shared source published by AY Digital Marketing. Each user's copy adapts to that user, and nothing flows back to the source.

- **Never push to the source.** If `git remote get-url origin` points to `github.com/Amiryaco/ay-video-editor`, do not push, open pull requests, or change that remote. The user doesn't own it, and their videos, brand and notes stay on their side. Local commits are fine. Push only if the user explicitly asks and `origin` is a repository they own.
- **No automatic updates.** Don't run `git pull` or update the skills from the source unless the user explicitly asks for an update. Before an update they asked for, keep their local changes (commit or stash them first) and tell them what changed.
- **Remember what the user teaches you.** At the start of every session, read `motion/my-notes.md` if it exists. When the user corrects or confirms something that should hold for future videos (caption look, zoom amount, card style, pacing, words to spell a certain way, their CTA), add one short dated line to `motion/my-notes.md` (create it if missing). Keep brand colours and the business name in `motion/brands.json`. Their notes override the defaults in this file and in the skills.
- Improve the user's local copy of the skills only when they ask, and say which file changed.
