#!/usr/bin/env python3
"""
main.py - Copies entry.jpg byte-for-byte to output path /output/entry.png
(or MAKEFUN_OUTPUT_DIR if set). Standard library only, no network.
"""

from pathlib import Path
import os
import sys
import hashlib

def main():
    base_dir = Path(__file__).resolve().parent
    src_path = base_dir / "entry.jpg"
    
    if not src_path.is_file():
        print(f"Error: Source image not found at {src_path}", file=sys.stderr)
        sys.exit(1)
        
    out_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir_env:
        out_dir = Path(out_dir_env)
    else:
        out_dir = Path("/output")
        
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error: Failed to create output directory {out_dir}: {e}", file=sys.stderr)
        sys.exit(1)
        
    dest_path = out_dir / "entry.png"
    
    try:
        data = src_path.read_bytes()
    except Exception as e:
        print(f"Error: Failed to read source image {src_path}: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Guard: verify source is non-empty
    if len(data) == 0:
        print(f"Error: Source image {src_path} is empty", file=sys.stderr)
        sys.exit(1)
        
    # Guard: verify JPEG magic bytes (FF D8 FF)
    if not data.startswith(b'\xff\xd8\xff'):
        print(f"Error: Source image does not start with JPEG magic bytes", file=sys.stderr)
        sys.exit(1)
        
    # Guard: verify size limit (at most 1048576 bytes)
    if len(data) > 1048576:
        print(f"Error: Image size {len(data)} exceeds 1048576 bytes gate limit", file=sys.stderr)
        sys.exit(1)
        
    try:
        dest_path.write_bytes(data)
    except Exception as e:
        print(f"Error: Failed to write destination image {dest_path}: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Verify written bytes match exactly (determinism guard)
    written_data = dest_path.read_bytes()
    if written_data != data:
        print(f"Error: Written file contents do not match source bytes", file=sys.stderr)
        sys.exit(1)
        
    digest = hashlib.sha256(written_data).hexdigest()
    print(f"Successfully copied entry.jpg to {dest_path}")
    print(f"Size: {len(written_data)} bytes, SHA-256: {digest}")

if __name__ == "__main__":
    main()
