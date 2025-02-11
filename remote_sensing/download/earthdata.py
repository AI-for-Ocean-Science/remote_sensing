import requests
import json
from typing import List, Dict, Optional

def get_earthdata_shortnames(
    page_size: int = 100,
    provider: Optional[str] = None,
    keyword: Optional[str] = None
) -> List[Dict]:
    """
    Retrieve collection short names from NASA's Common Metadata Repository (CMR).
    
    Args:
        page_size: Number of results per page (default 100, max 2000)
        provider: Filter by specific data provider (e.g., 'GHRC_DAAC')
        keyword: Filter collections by keyword
    
    Returns:
        List of dictionaries containing short_name and title for each collection
    """
    base_url = "https://cmr.earthdata.nasa.gov/search/collections.json"
    collections = []
    page = 1
    
    while True:
        params = {
            'page_size': page_size,
            'page_num': page,
            'sort_key': 'short_name'
        }
        
        if provider:
            params['provider'] = provider
        if keyword:
            params['keyword'] = keyword
            
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            entries = data.get('feed', {}).get('entry', [])
            
            if not entries:
                break
                
            for entry in entries:
                collections.append({
                    'short_name': entry.get('short_name'),
                    'title': entry.get('title'),
                    'provider': entry.get('provider_id')
                })
                
            page += 1
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            break
            
    return collections