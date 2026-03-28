#!/usr/bin/env python3
"""
Home Monitoring - IKEA Dirigera
Tracks light usage, room activity, and patterns
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from dirigera.hub.hub import Hub

# Config
HUB_IP = "192.168.1.226"
TOKEN = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBiOWQyMTZlODJmNzU4ZTlmMGEwNTE3ZDA4MzE2Y2I5MWM4OTlmMWMwZjE2MzFmODQ2YzE1Y2E4YTdhODJmZmMifQ.eyJpc3MiOiI2NTk1NDA4NS1kOGY4LTRjOTUtOTZiZi1mNGY0MDc4ODIyY2YiLCJ0eXBlIjoiYWNjZXNzIiwiYXVkIjoiaG9tZXNtYXJ0LmxvY2FsIiwic3ViIjoiOWMxNWNiNmMtNzRhNi00ZDJhLTk5MzAtMmFjMzY5Y2MzY2FjIiwiaWF0IjoxNzc0NzIzMjA2LCJleHAiOjIwOTAyOTkyMDZ9.mrFF36jF01Vs9LSMfcvAzUFZ1iNm0LeRH8NEEStLaBwGhzerUsPZQ2XPsfy74CStY1D20MYf1LGXJB4VTJCrlw"
DATA_FILE = "/Users/jmaudisio/Projects/HomeDashboard/monitoring_data.json"

def get_hub():
    return Hub(ip_address=HUB_IP, token=TOKEN)

def load_data():
    if Path(DATA_FILE).exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"events": [], "daily": {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_room(name):
    """Extract room from device name"""
    name_lower = name.lower()
    if 'salon' in name_lower or 'salón' in name_lower:
        return 'Salón'
    elif 'hab' in name_lower or 'dormitorio' in name_lower or 'habitacion' in name_lower:
        return 'Habitaciones'
    elif 'baño' in name_lower or 'bano' in name_lower:
        return 'Baño'
    elif 'entrada' in name_lower:
        return 'Entrada'
    elif 'despacho' in name_lower:
        return 'Despacho'
    elif 'desvan' in name_lower or 'desván' in name_lower:
        return 'Desván'
    else:
        return 'Otros'

def scan_and_record():
    """Scan all lights and record their state"""
    hub = get_hub()
    lights = hub.get_lights()
    
    data = load_data()
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    # Initialize today if not exists
    if today not in data["daily"]:
        data["daily"][today] = {
            "rooms": {},
            "total_on_minutes": 0,
            "devices_on": []
        }
    
    for light in lights:
        attrs = light.attributes
        name = attrs.custom_name
        room = get_room(name)
        is_on = attrs.is_on
        
        # Record event
        event = {
            "timestamp": now.isoformat(),
            "device": name,
            "room": room,
            "is_on": is_on,
            "brightness": getattr(attrs, 'light_level', None)
        }
        data["events"].append(event)
        
        # Update daily stats
        if room not in data["daily"][today]["rooms"]:
            data["daily"][today]["rooms"][room] = {
                "minutes_on": 0,
                "switch_count": 0,
                "last_state": None
            }
        
        room_stats = data["daily"][today]["rooms"][room]
        
        if is_on and name not in data["daily"][today]["devices_on"]:
            data["daily"][today]["devices_on"].append(name)
            room_stats["switch_count"] += 1
        
        if not is_on and name in data["daily"][today]["devices_on"]:
            data["daily"][today]["devices_on"].remove(name)
    
    # Keep only last 30 days of events
    cutoff = (now - timedelta(days=30)).isoformat()
    data["events"] = [e for e in data["events"] if e["timestamp"] > cutoff]
    
    # Clean old daily data
    old_days = [d for d in data["daily"] if d < (now - timedelta(days=90)).strftime("%Y-%m-%d")]
    for d in old_days:
        del data["daily"][d]
    
    save_data(data)
    return data

def get_stats(today_only=False):
    """Get usage statistics"""
    data = load_data()
    now = datetime.now()
    
    if today_only:
        today = now.strftime("%Y-%m-%d")
        stats = data["daily"].get(today, {})
    else:
        # Last 7 days
        stats = {"rooms": {}, "total_on_minutes": 0}
        for i in range(7):
            day = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            if day in data["daily"]:
                for room, room_data in data["daily"][day]["rooms"].items():
                    if room not in stats["rooms"]:
                        stats["rooms"][room] = {"minutes_on": 0, "switch_count": 0}
                    stats["rooms"][room]["minutes_on"] += room_data.get("minutes_on", 0)
                    stats["rooms"][room]["switch_count"] += room_data.get("switch_count", 0)
    
    return stats

def print_report():
    """Print monitoring report"""
    data = load_data()
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    print("=" * 50)
    print("🏠 HOME MONITORING REPORT")
    print("=" * 50)
    print(f"Date: {now.strftime('%Y-%m-%d %H:%M')}")
    print()
    
    if today in data["daily"]:
        today_data = data["daily"][today]
        print(f"📊 TODAY ({today})")
        print("-" * 30)
        
        # Active lights
        active = today_data.get("devices_on", [])
        print(f"💡 Currently ON: {len(active)} devices")
        for dev in active:
            print(f"   - {dev}")
        print()
        
        # Room stats
        print("📍 ROOM USAGE (switches today)")
        for room, stats in today_data.get("rooms", {}).items():
            switches = stats.get("switch_count", 0)
            bar = "█" * min(switches, 20)
            print(f"   {room:15} {bar} ({switches})")
        print()
    
    # Weekly stats
    print("📅 LAST 7 DAYS")
    print("-" * 30)
    weekly = get_stats()
    for room, stats in sorted(weekly.get("rooms", {}).items(), key=lambda x: x[1]["switch_count"], reverse=True):
        switches = stats.get("switch_count", 0)
        bar = "█" * min(switches, 20)
        print(f"   {room:15} {bar} ({switches} switches)")
    
    print()
    print("=" * 50)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        scan_and_record()
        print("✓ Scan recorded")
    elif len(sys.argv) > 1 and sys.argv[1] == "stats":
        print_report()
    else:
        # Run scan and show report
        scan_and_record()
        print_report()
