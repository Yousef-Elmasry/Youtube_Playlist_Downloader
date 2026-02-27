# YouTube Playlist Downloader

سكريبت بسيط ببايثون لتحميل كل فيديوهات أي YouTube Playlist في مسار تحدده.

## المتطلبات

- Python 3.9+
- FFmpeg (ضروري لتحويل الصوت عند استخدام `--audio-only`)

## التثبيت

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## الاستخدام

تحميل الفيديوهات (أفضل جودة متاحة):

```bash
python download_playlist.py "PLAYLIST_URL" "/path/to/output"
```

تحميل الصوت فقط بصيغة MP3:

```bash
python download_playlist.py "PLAYLIST_URL" "/path/to/output" --audio-only
```

تحديد صيغة/جودة مخصصة من yt-dlp:

```bash
python download_playlist.py "PLAYLIST_URL" "/path/to/output" --max-quality "best[height<=720]"
```

## ملاحظات

- الملفات بتتحفظ داخل فولدر باسم الـ playlist.
- ترتيب الملفات بيكون برقم الفيديو داخل الـ playlist.
- لو فيديو غير متاح، السكريبت بيتخطاه ويكمل باقي الفيديوهات.
