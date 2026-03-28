# IKEA Dirigera Smart Home Dashboard Specification

## 1. Project Overview

**Project Name:** HomeDashboard
**Type:** Single-page Web Application
**Core Functionality:** Control IKEA Dirigera smart home devices (lights, blinds, sensors) with real-time status updates
**Target Users:** Homeowners with IKEA smart home devices

---

## 2. UI/UX Specification

### Layout Structure

**Page Sections:**
- Header: App title, connection status indicator, last refresh timestamp
- Main Content: Room-based device grid
- No footer (full-screen dashboard)

**Grid Layout:**
- Desktop: CSS Grid with auto-fit columns, min 320px per card
- Mobile: Single column stack
- Cards organized by room

**Responsive Breakpoints:**
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

### Visual Design

**Color Palette:**
- Background Primary: `#0a0a0f` (deep midnight)
- Background Secondary: `#12121a` (card backgrounds)
- Background Tertiary: `#1a1a24` (hover states)
- Accent Primary: `#00d4aa` (teal/mint - active states)
- Accent Secondary: `#7c3aed` (purple - sliders)
- Accent Gradient: `linear-gradient(135deg, #00d4aa 0%, #0891b2 50%, #7c3aed 100%)`
- Text Primary: `#f0f0f5`
- Text Secondary: `#8888a0`
- Text Muted: `#555566`
- Success: `#22c55e`
- Warning: `#f59e0b`
- Error: `#ef4444`
- Glass Effect: `rgba(255, 255, 255, 0.05)` with `backdrop-filter: blur(12px)`

**Typography:**
- Font Family: `'Outfit', 'Segoe UI', system-ui, sans-serif`
- Headings: 700 weight
- Body: 400 weight
- H1 (Page Title): 2.5rem
- H2 (Room Title): 1.5rem
- H3 (Device Name): 1rem
- Body: 0.875rem
- Small: 0.75rem

**Spacing System:**
- Base unit: 8px
- Card padding: 24px
- Card gap: 20px
- Section gap: 32px
- Border radius (cards): 20px
- Border radius (buttons): 12px

**Visual Effects:**
- Card glassmorphism: `background: rgba(18, 18, 26, 0.8); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.08);`
- Glow effect on active devices: `box-shadow: 0 0 30px rgba(0, 212, 170, 0.3);`
- Smooth transitions: `transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);`
- Hover lift: `transform: translateY(-2px);`
- Subtle pulse animation for active indicators

### Components

**1. Header Component**
- App logo/title on left
- Connection status badge (green dot = connected, red = disconnected)
- Last updated timestamp
- Manual refresh button

**2. Room Card**
- Room name as header with room icon
- Device list inside
- Subtle gradient border accent per room

**3. Light Control**
- Device icon (bulb)
- Device name
- Toggle switch (on/off)
- Brightness indicator (percentage)
- States: on (glowing), off (dimmed)

**4. Blind/Shutter Control**
- Device icon (blind/window)
- Device name
- Vertical slider (0-100%)
- Position indicator
- Open/Close quick buttons

**5. Motion Sensor Status**
- Device icon (motion sensor)
- Device name
- Last triggered timestamp
- Battery level indicator
- Active/inactive status badge

**6. Toggle Switch Component**
- Width: 56px, Height: 28px
- Off: dark gray track
- On: gradient track with glow
- Smooth slide animation

**7. Slider Component**
- Vertical orientation for blinds
- Track: dark gray
- Fill: purple gradient
- Thumb: white with glow on drag

---

## 3. Functionality Specification

### Core Features

**1. Device Discovery & Display**
- Fetch all devices from Dirigera API on load
- Group devices by room/capability
- Display 35 lights across rooms: Salon, Dormitorio, Habitaciones, Baño, Entrada, Despacho, Desvan
- Display 2 blinds: Estor Izquierda, Estor Derecha
- Display motion sensors

**2. Light Control**
- Toggle on/off via API POST
- Display current on/off state
- Show brightness level (if available)

**3. Blind Control**
- Set position 0-100% via API
- Display current position
- Quick buttons: Open (0%), Close (100%), 50%

**4. Sensor Display**
- Show last motion detected time
- Show battery status
- Show connection status

**5. Auto-Refresh**
- Poll API every 5 seconds
- Update all device states
- Show last refresh timestamp

**6. Error Handling**
- Show connection error state
- Retry logic with exponential backoff
- Visual feedback on API failures

### API Integration

**Base URL:** `https://192.168.1.226:8443`

**Authentication:** Bearer token in Authorization header

**Endpoints:**
- GET `/api/v1/devices` - List all devices
- POST `/api/v1/devices/{id}/actions` - Control device

**API Token:**
```
eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBiOWQyMTZlODJmNzU4ZTlmMGEwNTE3ZDA4MzE2Y2I5MWM4OTlmMWMwZjE2MzFmODQ2YzE1Y2E4YTdhODJmZmMifQ.eyJpc3MiOiI2NTk1NDA4NS1kOGY4LTRjOTUtOTZiZi1mNGY0MDc4ODIyY2YiLCJ0eXBlIjoiYWNjZXNzIiwiYXVkIjoiaG9tZXNtYXJ0LmxvY2FsIiwic3ViIjoiOWMxNWNiNmMtNzRhNi00ZDJhLTk5MzAtMmFjMzY5Y2MzY2FjIiwiaWF0IjoxNzc0NzIzMjA2LCJleHAiOjIwOTAyOTkyMDZ9.mrFF36jF01Vs9LSMfcvAzUFZ1iNm0LeRH8NEEStLaBwGhzerUsPZQ2XPsfy74CStY1D20MYf1LGXJB4VTJCrlw
```

### User Interactions

1. **Toggle Light:** Click toggle switch → API call → Update state → Visual feedback
2. **Adjust Blinds:** Drag slider → Debounce 300ms → API call → Update position
3. **Refresh:** Click refresh button → Immediate API poll → Update all states

---

## 4. Acceptance Criteria

### Visual Checkpoints
- [ ] Dark theme with deep midnight background
- [ ] Glassmorphism cards with subtle borders
- [ ] Accent teal/purple gradient on interactive elements
- [ ] Smooth hover animations on cards
- [ ] Glowing effect on active lights
- [ ] Responsive layout works on mobile and desktop

### Functional Checkpoints
- [ ] Page loads and fetches device list from API
- [ ] Lights grouped by room with toggle controls
- [ ] Blinds have slider control
- [ ] Motion sensors show status
- [ ] Auto-refresh every 5 seconds
- [ ] Connection status indicator works
- [ ] Manual refresh button works

### Technical Checkpoints
- [ ] Single HTML file with embedded CSS/JS
- [ ] Vanilla JavaScript (no frameworks)
- [ ] Fetch API for HTTP requests
- [ ] No console errors on load
- [ ] Proper error handling for API failures

---

## 5. Room Layout

Based on user description (35 lights):

| Room | Estimated Lights |
|------|------------------|
| Salon | ~10 |
| Dormitorio | ~8 |
| Habitaciones | ~6 |
| Baño | ~3 |
| Entrada | ~3 |
| Despacho | ~3 |
| Desvan | ~2 |
| **Total** | **35** |

### Blinds
- Estor Izquierda (Left blind)
- Estor Derecha (Right blind)
