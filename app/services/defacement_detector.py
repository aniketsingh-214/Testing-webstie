"""
Defacement Detector - Detects changes from baseline
"""
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from bs4 import BeautifulSoup
import requests

from app.utils.hash_utils import calculate_string_hash, calculate_file_hash, normalize_html


class DefacementDetector:
    def __init__(self):
        pass
    
    def check_defacement(self, baseline: Dict, url: str, static_dir: str = "app/static") -> Dict:
        """Check for defacement by comparing current state with baseline"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "defacement_detected": False,
            "changes": [],
            "summary": "No changes detected"
        }
        
        # Fetch current HTML
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            html_content = response.text
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "defacement_detected": False,
                "error": f"Failed to fetch URL: {e}",
                "changes": [],
                "summary": "Error fetching page"
            }
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check zones
        for zone_id, zone_data in baseline.get('zones', {}).items():
            zone_element = soup.find(id=zone_id)
            if zone_element:
                zone_html = str(zone_element)
                normalized = normalize_html(zone_html)
                current_hash = calculate_string_hash(normalized)
                
                if current_hash != zone_data['hash']:
                    report['changes'].append({
                        'type': 'zone',
                        'zone': zone_id,
                        'expected_hash': zone_data['hash'],
                        'current_hash': current_hash,
                        'description': f'Zone "{zone_id}" content has been modified',
                        'current_preview': zone_element.get_text()[:100].strip()
                    })
                    report['defacement_detected'] = True
            else:
                report['changes'].append({
                    'type': 'zone',
                    'zone': zone_id,
                    'description': f'Zone "{zone_id}" is missing from page',
                    'severity': 'critical'
                })
                report['defacement_detected'] = True
        
        # Check images
        static_path = Path(static_dir)
        for img_id, img_data in baseline.get('images', {}).items():
            img_path = img_data['path'].replace('/static/', '')
            full_path = static_path / img_path
            
            if full_path.exists():
                current_hash = calculate_file_hash(full_path)
                current_size = full_path.stat().st_size
                
                if current_hash != img_data['hash']:
                    report['changes'].append({
                        'type': 'image',
                        'image': img_id,
                        'path': img_data['path'],
                        'expected_hash': img_data['hash'],
                        'current_hash': current_hash,
                        'expected_size': img_data['size'],
                        'current_size': current_size,
                        'description': f'Image "{img_id}" has been replaced or modified'
                    })
                    report['defacement_detected'] = True
            else:
                report['changes'].append({
                    'type': 'image',
                    'image': img_id,
                    'path': img_data['path'],
                    'description': f'Image "{img_id}" is missing',
                    'severity': 'critical'
                })
                report['defacement_detected'] = True
        
        # Update summary
        if report['defacement_detected']:
            num_changes = len(report['changes'])
            report['summary'] = f"{num_changes} change{'s' if num_changes != 1 else ''} detected"
        
        return report
