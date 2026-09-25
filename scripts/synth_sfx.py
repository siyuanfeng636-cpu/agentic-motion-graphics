#!/usr/bin/env python3
"""
synth_sfx.py - Procedural Sound Effects & Rhythmic Backing Track Synthesizer.
Generates deterministic, syncable audio cues (pops, clicks, whooshes, risers, pulses) via Python numpy.
"""

import math
import struct
import wave
import argparse
import numpy as np

SAMPLE_RATE = 44100

def write_wav(filename: str, samples: np.ndarray):
    """Normalize and write numpy float array to 16-bit WAV file"""
    samples = np.clip(samples, -1.0, 1.0)
    int_samples = (samples * 32767).astype(np.int16)
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(int_samples.tobytes())
    print(f"[✓] Synthesized audio saved to: {filename}")

def synth_pop(duration: float = 0.04) -> np.ndarray:
    """Button click / badge pop SFX"""
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_samples, False)
    freq = np.linspace(1400, 300, num_samples)
    signal = np.sin(2 * np.pi * freq * t) * np.exp(-t * 90)
    return signal

def synth_whoosh(duration: float = 0.35) -> np.ndarray:
    """Fast perspective zoom / pan transition whoosh"""
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_samples, False)
    noise = np.random.uniform(-1, 1, num_samples)
    envelope = (np.sin(np.pi * t / duration) ** 2) * 0.35
    # Low-pass smoothing via simple moving average
    kernel = np.ones(10) / 10
    filtered = np.convolve(noise * envelope, kernel, mode='same')
    return filtered

def synth_sub_pulse(duration: float = 0.6) -> np.ndarray:
    """Sub-bass 808 scene change impact"""
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_samples, False)
    freq = np.linspace(80, 40, num_samples)
    signal = np.sin(2 * np.pi * freq * t) * np.exp(-t * 5.5) * 0.7
    return signal

def synth_riser(duration: float = 2.0) -> np.ndarray:
    """Tension building upward pitch sweep before key reveal"""
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_samples, False)
    freq = np.linspace(150, 750, num_samples)
    sawtooth = 2 * (t * freq - np.floor(0.5 + t * freq))
    envelope = (t / duration) ** 1.8 * 0.3
    return sawtooth * envelope

def synth_backing_track(duration: float = 30.0, bpm: float = 120.0) -> np.ndarray:
    """
    Rhythmic minimal electronic backing track locked to a 120 BPM grid.
    Includes kick pulses on downbeats and subtle hi-hats on offbeats.
    """
    num_samples = int(SAMPLE_RATE * duration)
    track = np.zeros(num_samples)
    seconds_per_beat = 60.0 / bpm
    total_beats = int(duration / seconds_per_beat)

    pop_sample = synth_pop(0.02) * 0.25
    sub_sample = synth_sub_pulse(0.3) * 0.45

    for b in range(total_beats):
        beat_time = b * seconds_per_beat
        start_idx = int(beat_time * SAMPLE_RATE)

        # Kick / Sub on beats 1 and 3 of every measure
        if b % 2 == 0:
            end_idx = min(start_idx + len(sub_sample), num_samples)
            track[start_idx:end_idx] += sub_sample[:end_idx - start_idx]
        
        # Click / Hi-hat on every beat
        end_idx_pop = min(start_idx + len(pop_sample), num_samples)
        track[start_idx:end_idx_pop] += pop_sample[:end_idx_pop - start_idx]

    return track

def main():
    parser = argparse.ArgumentParser(description="Procedural SFX and Music Track Synthesizer")
    parser.add_argument("--type", choices=["track", "pop", "whoosh", "sub", "riser"], default="track")
    parser.add_argument("--bpm", type=float, default=120.0)
    parser.add_argument("--duration", type=float, default=30.0)
    parser.add_argument("--output", default="synth_audio.wav")

    args = parser.parse_args()

    if args.type == "track":
        audio = synth_backing_track(duration=args.duration, bpm=args.bpm)
    elif args.type == "pop":
        audio = synth_pop()
    elif args.type == "whoosh":
        audio = synth_whoosh()
    elif args.type == "sub":
        audio = synth_sub_pulse()
    elif args.type == "riser":
        audio = synth_riser(duration=args.duration)

    write_wav(args.output, audio)

if __name__ == "__main__":
    main()
