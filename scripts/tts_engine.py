#!/usr/bin/env python3
"""
tts_engine.py - Agentic Voiceover Generator & Audio Cleaner
Generates speech via OpenAI or ElevenLabs, then trims silences and normalizes via ffmpeg.
"""

import os
import sys
import json
import argparse
import subprocess

def trim_and_clean_audio(input_file: str, output_file: str, tempo: float = 1.05):
    """
    Trims lead and tail silences and applies a slight tempo acceleration for commercial pacing.
    """
    af_filter = (
        f"silenceremove=start_periods=1:start_silence=0.05:start_threshold=-48dB,"
        f"areverse,"
        f"silenceremove=start_periods=1:start_silence=0.05:start_threshold=-48dB,"
        f"areverse,"
        f"atempo={tempo}"
    )
    cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-af", af_filter,
        "-b:a", "192k",
        output_file
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[✓] Cleaned audio saved to: {output_file}")

def generate_openai(text: str, raw_output: str, voice: str = "alloy"):
    from openai import OpenAI
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        input=text
    )
    response.stream_to_file(raw_output)
    print(f"[✓] OpenAI TTS generated: {raw_output}")

def generate_elevenlabs(text: str, raw_output: str, voice_id: str):
    import urllib.request
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is not set")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        with open(raw_output, "wb") as f:
            f.write(resp.read())
    print(f"[✓] ElevenLabs TTS generated: {raw_output}")

def main():
    parser = argparse.ArgumentParser(description="Voiceover generator with automated ffmpeg cleaning")
    parser.add_argument("--text", type=str, help="Text to speak")
    parser.add_argument("--script", type=str, help="Path to script.json (concatenates narration lines)")
    parser.add_argument("--provider", choices=["openai", "elevenlabs"], default="openai")
    parser.add_argument("--voice", type=str, default="alloy", help="OpenAI voice or ElevenLabs voice_id")
    parser.add_argument("--tempo", type=float, default=1.05, help="Playback speed multiplier")
    parser.add_argument("--output", type=str, default="voiceover_clean.mp3", help="Output audio file")

    args = parser.parse_args()

    speech_text = ""
    if args.script:
        with open(args.script, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                speech_text = " ".join([scene.get("narration", "") for scene in data])
            elif isinstance(data, dict):
                scenes = data.get("scenes", [])
                speech_text = " ".join([s.get("narration", "") for s in scenes])
    elif args.text:
        speech_text = args.text
    else:
        print("[!] Error: Specify either --text or --script")
        sys.exit(1)

    raw_temp = "/tmp/raw_voiceover_temp.mp3"
    if args.provider == "openai":
        generate_openai(speech_text, raw_temp, voice=args.voice)
    else:
        generate_elevenlabs(speech_text, raw_temp, voice_id=args.voice)

    trim_and_clean_audio(raw_temp, args.output, tempo=args.tempo)
    if os.path.exists(raw_temp):
        os.remove(raw_temp)

if __name__ == "__main__":
    main()
