"""
Hash utilities for defacement detection
"""
import hashlib
from pathlib import Path
from typing import Union


def calculate_string_hash(content: str) -> str:
    """Calculate SHA256 hash of string content"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def calculate_file_hash(file_path: Union[str, Path]) -> str:
    """Calculate SHA256 hash of file content"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        # Read file in chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    return sha256_hash.hexdigest()


def normalize_html(html: str) -> str:
    """Normalize HTML by removing extra whitespace"""
    # Remove extra whitespace and newlines
    normalized = ' '.join(html.split())
    return normalized.strip()
