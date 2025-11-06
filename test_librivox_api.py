"""
Quick test to see what data LibriVox API returns
"""
import requests
import json

url = "https://librivox.org/api/feed/audiobooks"
params = {
    'format': 'json',
    'extended': '1',
    'limit': 2
}

response = requests.get(url, params=params, timeout=30)
data = response.json()

print("="*70)
print("LIBRIVOX API SAMPLE DATA")
print("="*70)
print(json.dumps(data['books'][0], indent=2))
