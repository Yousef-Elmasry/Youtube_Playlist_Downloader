#!/usr/bin/env python3
"""Download all videos from a YouTube playlist into a user-provided folder."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yt_dlp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download all videos from a YouTube playlist to a target directory."
    )
    parser.add_argument("playlist_url", help="YouTube playlist URL")
    parser.add_argument(
        "output_dir",
        help="Target folder where videos will be saved",
    )
    parser.add_argument(
        "--audio-only",
        action="store_true",
        help="Download audio only as MP3 instead of video",
    )
    parser.add_argument(
        "--max-quality",
        default="bestvideo+bestaudio/best",
        help=(
            "yt-dlp format selector. Default: bestvideo+bestaudio/best "
            "(ignored with --audio-only)"
        ),
    )
    return parser.parse_args()


def build_ydl_options(output_dir: Path, audio_only: bool, max_quality: str) -> dict:
    outtmpl = str(output_dir / "%(playlist_title)s" / "%(playlist_index)03d - %(title)s.%(ext)s")

    options: dict = {
        "outtmpl": outtmpl,
        "ignoreerrors": True,
        "noprogress": False,
        "continuedl": True,
        "concurrent_fragment_downloads": 4,
        "retries": 10,
        "fragment_retries": 10,
        "windowsfilenames": True,
    }

    if audio_only:
        options.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
        )
    else:
        options["format"] = max_quality

    return options


def main() -> int:
    args = parse_args()

    output_path = Path(args.output_dir).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    ydl_opts = build_ydl_options(output_path, args.audio_only, args.max_quality)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([args.playlist_url])
    except yt_dlp.utils.DownloadError as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        return 1

    print(f"Done. Files saved in: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
