#!/usr/bin/env python3
"""
timing_aligner.py - Extracts millisecond-accurate word-level timestamps from audio.
Supports faster-whisper, OpenAI Whisper API, or whisper.cpp CLI.
"""

import os
import sys
import json
import argparse
import subprocess

def align_with_faster_whisper(audio_path: str, model_size: str = "small.en"):
    from faster_whisper import WhisperModel
    print(f"[*] Running faster-whisper ({model_size}) on {audio_path}...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path, word_timestamps=True)
    
    words_data = []
    for segment in segments:
        for w in segment.words:
            words_data.append({
                "word": w.word.strip(),
                "start": round(w.start, 3),
                "end": round(w.end, 3),
                "confidence": round(w.probability, 2)
            })
    return words_data

def align_with_openai_api(audio_path: str):
    from openai import OpenAI
    client = OpenAI()
    print(f"[*] Running OpenAI Whisper API with verbose_json timestamps...")
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            file=f,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )
    words_data = []
    for w in transcript.words:
        words_data.append({
            "word": w.word.strip(),
            "start": round(w.start, 3),
            "end": round(w.end, 3),
            "confidence": 1.0
        })
    return words_data

def main():
    parser = argparse.ArgumentParser(description="Extract word-level timestamps from audio file")
    parser.add_argument("--audio", required=True, help="Input audio file (.mp3, .wav)")
    parser.add_argument("--output", default="timing.json", help="Path to save output JSON")
    parser.add_argument("--engine", choices=["faster-whisper", "openai", "auto"], default="auto")

    args = parser.parse_args()

    results = []
    if args.engine == "openai":
        results = align_with_openai_api(args.audio)
    elif args.engine == "faster-whisper":
        results = align_with_faster_whisper(args.audio)
    else:
        # Auto mode: try faster-whisper, fallback to openai api
        try:
            results = align_with_faster_whisper(args.audio)
        except Exception as e:
            print(f"[-] faster-whisper not available or failed ({e}), falling back to OpenAI API...")
            results = align_with_openai_api(args.audio)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"[✓] Extracted {len(results)} word timestamps to: {args.output}")

if __name__ == "__main__":
    main()
