"""
Baseline Manager - Creates and manages defacement detection baselines
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import requests

from app.utils.hash_utils import calculate_string_hash, calculate_file_hash, normalize_html


class BaselineManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.baseline_file = self.data_dir / "baseline.json"
        
        # Setup Jinja2 for template rendering (localhost only)
        self.jinja_env = Environment(loader=FileSystemLoader('app/templates'))
    
    def is_production(self) -> bool:
        """Check if running on Vercel/production"""
        return os.getenv('VERCEL') == '1' or os.getenv('PRODUCTION') == 'true'
    
    def create_baseline(self, url: str, static_dir: str = "app/static") -> Dict:
        """Create a baseline snapshot of the website"""
        baseline = {
            "created_at": datetime.now().isoformat(),
            "url": url,
            "zones": {},
            "images": {}
        }
        
        # Get HTML content based on environment
        if self.is_production():
            # Production: Use HTTP request to fetch actual page
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                html_content = response.text
            except Exception as e:
                raise Exception(f"Failed to fetch URL: {e}")
        else:
            # Localhost: Render template directly (faster, no HTTP overhead)
            try:
                template = self.jinja_env.get_template('index.html')
                html_content = template.render(request={'url': '/'})
            except Exception as e:
                raise Exception(f"Failed to render template: {e}")
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract protected zones
        zones = ['header', 'sidebar', 'footer']
        for zone_id in zones:
            zone_element = soup.find(id=zone_id)
            if zone_element:
                zone_html = str(zone_element)
                normalized = normalize_html(zone_html)
                baseline['zones'][zone_id] = {
                    'hash': calculate_string_hash(normalized),
                    'content_preview': zone_element.get_text()[:100].strip()
                }
        
        # Hash protected images
        static_path = Path(static_dir)
        images = {
            'logo1': 'images/logo1.png',
            'image2': 'images/image2.png',
            'image1': 'images/image1.png',
            'image3': 'images/image3.png'
        }
        
        for img_id, img_path in images.items():
            full_path = static_path / img_path
            if full_path.exists():
                baseline['images'][img_id] = {
                    'path': f'/static/{img_path}',
                    'hash': calculate_file_hash(full_path),
                    'size': full_path.stat().st_size
                }
        
        # Save baseline
        with open(self.baseline_file, 'w') as f:
            json.dump(baseline, f, indent=2)
        
        return baseline
    
    def load_baseline(self) -> Optional[Dict]:
        """Load existing baseline"""
        if not self.baseline_file.exists():
            return None
        
        with open(self.baseline_file, 'r') as f:
            return json.load(f)
    
    def baseline_exists(self) -> bool:
        """Check if baseline exists"""
        return self.baseline_file.exists()
    
    def delete_baseline(self) -> bool:
        """Delete existing baseline"""
        if self.baseline_file.exists():
            self.baseline_file.unlink()
            return True
        return False
