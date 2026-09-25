#!/usr/bin/env python3
"""
contact_sheet.py - Extracts a grid of keyframes (Contact Sheet) from a video.
Enables LLM agents to "watch" and visually inspect video pacing, framing, and aesthetics.
"""

import os
import sys
import argparse
import subprocess

def create_contact_sheet(video_path: str, output_image: str, grid_cols: int = 4, grid_rows: int = 4):
    """
    Uses ffmpeg to sample frames uniformly across video duration and tiles them into a single image.
    """
    total_tiles = grid_cols * grid_rows
    # ffmpeg select filter: samples 1 frame per N frames or uses tile filter
    filter_graph = f"fps=1/2,scale=480:-1,tile={grid_cols}x{grid_rows}"
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", filter_graph,
        "-frames:v", "1",
        output_image
    ]
    print(f"[*] Generating contact sheet ({grid_cols}x{grid_rows}) from {video_path}...")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[✓] Contact sheet saved to: {output_image}")

def main():
    parser = argparse.ArgumentParser(description="Generate video contact sheet grid for LLM inspection")
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--output", default="contact_sheet.jpg", help="Output contact sheet image")
    parser.add_argument("--cols", type=int, default=4)
    parser.add_argument("--rows", type=int, default=4)

    args = parser.parse_args()
    create_contact_sheet(args.video, args.output, args.cols, args.rows)

if __name__ == "__main__":
    main()
