# Implementation Plan: Modern Tablet Dashboard Redesign

**Date**: 2025-12-22
**Author**: Claude
**Status**: Awaiting Approval

## Overview

Complete redesign of the Home Assistant tablet dashboard with modern aesthetics, room-based navigation, and optimized layouts for 8" and 10" landscape tablets.

## Requirements Summary

1. **Modern/Sleek/Intuitive Design** - Professional appearance with gradients and colors
2. **Room-Based Tabs** - Living Room, Kitchen, Dining Room, Master Bedroom, Master Bath, Office, Alpha, Beta, Deck, Settings
3. **Dedicated TV Remote Tab** - Universal remote with device selector for all TVs/Apple TVs
4. **Music Tab** - Music Assistant with room output selection and cover art
5. **Movie Mode** - Automatic lighting for open floor plan (LR→Dining→Kitchen)
6. **No Scrolling** - All content fits on screen
7. **Theme Switching** - Multiple visual styles
8. **Working Entities Only** - Verified functional entities
9. **Fixed Doorbell Popup** - Ring camera popup on doorbell press
10. **Subtle Animations** - Modern touch interactions
11. **Tablet Optimized** - 8" (1280x800) and 10" (1920x1200) landscape

## Device Inventory

### TVs and Apple TVs
| Room | Smart TV | Apple TV | HomePod |
|------|----------|----------|---------|
| Living Room | Samsung TV | Yes | No |
| Master Bedroom | - | Yes | 2x Regular HomePod |
| Alpha Guest | Smart TV | Yes | 1x Mini |
| Beta Guest | Smart TV | Yes | 1x Mini |
| Office | - | - | 2x Mini |
| Kitchen | - | - | 1x Mini |
| Master Bath | - | - | 1x Mini |

### Open Floor Plan
```
┌────────────────────────────────────────────────────────┐
│                      (No walls)                        │
│   LIVING ROOM  ←→  DINING ROOM  ←→  KITCHEN          │
│   (Samsung TV)      (No TV)          (No TV)          │
│   (Apple TV)                                           │
│                                                        │
│   Movie mode dims/turns off Kitchen & Dining lights   │
└────────────────────────────────────────────────────────┘
```

---

## Architecture Decision

### Single Responsive Dashboard vs Two Dashboards

**Recommendation: Single Dashboard with CSS Media Queries**

Rationale:
- Easier maintenance (one codebase)
- Card-mod supports responsive breakpoints
- Modern cards (Mushroom, Bubble) are inherently responsive
- Reduce duplication of entities and logic

### Card Framework Selection

**Primary Cards:**
| Card | Purpose | Why |
|------|---------|-----|
| **Bubble Card** | Pop-ups, navigation, buttons | Modern pop-up system, touch-friendly |
| **Mushroom Cards** | Entity controls, chips, templates | Clean minimalist design, full UI editor |
| **Button Card** | Custom buttons with animations | Advanced CSS/animations support |
| **Card-mod** | CSS styling | Required for theme customization |
| **Swipe Card** | Room navigation | Touch gestures between rooms |

### Theme Selection

**Primary Theme: Custom Gradient Theme** (inspired by Frosted Glass)
- Dark mode base with translucent cards
- Gradient accents (customizable)
- Glassmorphism effects (blur where performant)
- **Lite mode** for 8" tablets (no blur for performance)

---

## Dashboard Structure

### Navigation Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  [Time]           DASHBOARD TITLE              [Settings] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              MAIN CONTENT AREA                       │  │
│  │         (Room-specific controls)                     │  │
│  │                                                       │  │
│  │                                                       │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ [🏠] [🛋️] [🍳] [🍽️] [🛏️] [🚿] [💼] [👤] [👥] [🌳]        │
│ Home  LR  Kitchen Dining MBR  MBath Office Alpha Beta Deck │
└─────────────────────────────────────────────────────────────┘
```

### Bottom Navigation Bar (Bubble Card)

**Implementation:** Bubble Card horizontal-buttons-stack
- Fixed at bottom of screen
- 13 navigation items (scrollable or 2-row)
- Active state indicator
- Touch-optimized (48px minimum touch targets)

### Views/Tabs (13 Total)

| View | Path | Icon | Primary Controls |
|------|------|------|------------------|
| Home | `/home` | 🏠 | Status overview, weather, quick actions, Movie Mode |
| Living Room | `/living-room` | 🛋️ | Lights, quick remote, scenes |
| Kitchen | `/kitchen` | 🍳 | Lights, undercabinet |
| Dining Room | `/dining-room` | 🍽️ | Lights, scenes |
| Master Bedroom | `/master-bedroom` | 🛏️ | Lights, nightlight, sleep controls |
| Master Bath | `/master-bath` | 🚿 | Lights, shower, motion settings |
| Office | `/office` | 💼 | Lights, scene selection |
| Alpha | `/alpha` | 👤 | Guest room lights, TV |
| Beta | `/beta` | 👥 | Guest room lights, TV |
| Deck | `/deck` | 🌳 | WLED effects, outdoor lights |
| **Remote** | `/remote` | 📺 | Universal TV/Apple TV remote |
| **Music** | `/music` | 🎵 | Music Assistant, room outputs |
| Settings | `/settings` | ⚙️ | Theme, bedtime, system |

---

## Detailed View Designs

### 1. Home View (Landing Page)

**Layout:** 2-column grid

**Left Column:**
- Current time/date (large)
- Weather card (temperature, conditions)
- Thermostat quick control

**Right Column:**
- Quick status chips:
  - Lights on count
  - Motion status
  - Door lock status
- Quick scene buttons:
  - All Off
  - Movie Mode
  - Goodnight

**Bottom:**
- Ring doorbell status (shows last ring time, tap for live view)

### 2. Room Views (Living Room, Kitchen, Dining, etc.)

**Standard Room Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│  [← Back]        LIVING ROOM           [Motion: AUTO 🟢]   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐  ┌─────────────────────────────────┐  │
│  │   LIGHT         │  │     SCENES                      │  │
│  │   GROUP         │  │  [Evening] [Bright] [Movie] [Off]│  │
│  │   CONTROL       │  └─────────────────────────────────┘  │
│  │                 │                                        │
│  │  [Brightness]   │  ┌─────────────────────────────────┐  │
│  │  [Color Temp]   │  │     MEDIA CONTROLS              │  │
│  └─────────────────┘  │  [TV] [Apple TV] [Spotify]       │  │
│                        └─────────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  MOTION SETTINGS (expandable pop-up)                    ││
│  │  Leave On: [Toggle] Duration: [Slider]                  ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 3. Living Room View (Special - Apple TV Remote)

**Additional Components:**
- Apple TV Remote Grid (3x3)
- App launcher row (Netflix, Disney+, YouTube TV)
- Samsung TV power/input
- WLED entertainment center control

**Pop-up:** Full Apple TV Remote (tap remote icon)

### 4. Master Bedroom View (Special - Sleep Controls)

**Additional Components:**
- Under-bed light control
- Hexagon accent light
- Nightlight control
- "In Bed" status indicator
- Bedtime mode toggle

### 5. Deck View (WLED Control Center)

**Design Philosophy:** No ugly dropdowns! Visual, icon-based effect selection with live preview.

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  [← Back]            DECK                    [Weather: 72°] │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐   │
│  │  WLED LIVE PREVIEW (iframe or wled-ws-card)          │   │
│  │  [═══════════════ animated gradient ═══════════════] │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  QUICK EFFECTS (icon buttons, no dropdown!)            │ │
│  │  [🌈] [🔥] [❄️] [⚡] [🎉] [🌊] [🌅] [💜]              │ │
│  │  Rainbow Fire  Ice  Storm Party Ocean Sunset Purple    │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────────────────────┐  │
│  │ BRIGHTNESS      │  │  OTHER LIGHTS                   │  │
│  │ [══════════■══] │  │  [🏠 Porch] [🪜 Roof Stairs]    │  │
│  │ SPEED           │  │  [🚪 Back Door]                 │  │
│  │ [════■════════] │  │                                 │  │
│  │ INTENSITY       │  │                                 │  │
│  │ [══════■══════] │  │                                 │  │
│  └─────────────────┘  └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**WLED Components:**

1. **Live Preview Card** (top)
   - Use `custom:wled-ws-card` (HACS: wled_liveviewproxy) for real-time CSS gradient
   - OR iframe with `/liveview` endpoint from WLED device
   - Styled as wide banner with rounded corners

2. **Effect Grid** (icon buttons, NOT dropdown)
   ```yaml
   type: grid
   columns: 8
   square: true
   cards:
     - type: custom:button-card
       name: Rainbow
       icon: mdi:rainbow
       color: auto  # Changes based on effect
       tap_action:
         action: call-service
         service: select.select_option
         target:
           entity_id: select.wled_preset
         data:
           option: "Rainbow"
       styles:
         card:
           - background: linear-gradient(135deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #8b00ff)
           - border-radius: 12px
     # ... repeat for each effect with unique gradient backgrounds
   ```

3. **Slider Controls** (Mushroom or slider-entity-row)
   - Brightness: `light.wled` brightness attribute
   - Speed: `number.wled_speed`
   - Intensity: `number.wled_intensity`

4. **Curated Effect Presets** (8 best effects, icon + gradient background):
   | Effect | Icon | Gradient Background |
   |--------|------|---------------------|
   | Rainbow | `mdi:rainbow` | Multi-color gradient |
   | Fire | `mdi:fire` | Orange → Red |
   | Ice | `mdi:snowflake` | Cyan → Blue |
   | Storm | `mdi:lightning-bolt` | Purple → White flash |
   | Party | `mdi:party-popper` | Pink → Purple |
   | Ocean | `mdi:waves` | Blue → Teal |
   | Sunset | `mdi:weather-sunset` | Orange → Pink |
   | Purple | `mdi:circle` | Purple → Magenta |

**Deck Entities:**
| Entity | Type | Control |
|--------|------|---------|
| `light.wled` | WLED Strip | On/Off, Brightness, Color |
| `select.wled_preset` | Presets | Effect selection |
| `select.wled_color_palette` | Palettes | Color scheme |
| `number.wled_speed` | Speed | 0-255 slider |
| `number.wled_intensity` | Intensity | 0-255 slider |
| `switch.shelly_2_5_lrfanporchlight_relay_0` | Porch Light | On/Off |
| `light.dining_room_stairs` | Roof Stairs | On/Off, Brightness |
| `switch.back_door_light` | Back Door | On/Off |

**Additional WLED Controls (Bubble Pop-up):**
- Tap "More" for advanced controls pop-up:
  - Full palette selector
  - Segment control
  - Sync send/receive toggles
  - Nightlight mode
  - Restart button

### 6. Settings View (Dynamic Theme Control)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  [← Back]           SETTINGS                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  🎨 APPEARANCE                                         │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │ │
│  │  │ ████████│ │ ░░░░░░░░│ │ ████████│ │ ████████│      │ │
│  │  │ ████████│ │ ░░░░░░░░│ │ ████████│ │ ████████│      │ │
│  │  │  Dark   │ │  Light  │ │  Ocean  │ │  Sunset │      │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘      │ │
│  │                                                        │ │
│  │  Accent Color: [🔵] [🟣] [🟢] [🟠] [🔴] [Custom]       │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌──────────────────────┐  ┌───────────────────────────┐   │
│  │ 🌙 BEDTIME           │  │ ⚙️ SYSTEM                 │   │
│  │ Start: [10:00 PM]    │  │ [Reload Dashboard]        │   │
│  │ End:   [6:00 AM]     │  │ [Clear Browser Cache]     │   │
│  └──────────────────────┘  │ [Screen: Auto/On/Off]     │   │
│                            └───────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Dynamic Theme Implementation:**

1. **Create input_select for theme choice:**
   ```yaml
   # In configuration.yaml
   input_select:
     dashboard_theme:
       name: Dashboard Theme
       options:
         - Dark Gradient
         - Light Mode
         - Ocean Blue
         - Sunset Warm
         - High Contrast
       initial: Dark Gradient
       icon: mdi:palette

   input_select:
     dashboard_accent:
       name: Accent Color
       options:
         - Indigo
         - Purple
         - Teal
         - Orange
         - Red
         - Pink
       initial: Indigo
       icon: mdi:palette-swatch
   ```

2. **Theme Preview Cards:**
   ```yaml
   type: custom:button-card
   name: Dark
   icon: mdi:weather-night
   tap_action:
     action: call-service
     service: input_select.select_option
     target:
       entity_id: input_select.dashboard_theme
     data:
       option: "Dark Gradient"
   styles:
     card:
       - background: linear-gradient(135deg, #0f172a, #1e293b)
       - border: "[[[ return states['input_select.dashboard_theme'].state == 'Dark Gradient' ? '2px solid #6366f1' : '2px solid transparent' ]]]"
   ```

3. **Automation to Apply Theme:**
   ```yaml
   # In automations.yaml
   - alias: "Apply Dashboard Theme"
     trigger:
       - platform: state
         entity_id: input_select.dashboard_theme
     action:
       - service: frontend.set_theme
         data:
           name: "tablet-modern-{{ states('input_select.dashboard_theme') | slugify }}"
   ```

4. **Accent Color Chips:**
   - Use Mushroom chips card with color swatches
   - Each chip sets `input_select.dashboard_accent`
   - Theme CSS uses CSS variables that reference accent choice

**Bedtime Settings:**
- `input_datetime.bedtime_start` - Time picker
- `input_datetime.bedtime_end` - Time picker

**System Controls:**
- Reload Dashboard: `browser_mod.refresh`
- Clear Cache: Fully Kiosk command via `rest_command.kiosk_command`
- Screen Control: Fully Kiosk screen on/off/brightness

### 7. TV Remote View (Universal Remote)

**Design Philosophy:** Single remote tab that can control any TV in the house. Device selector at top, remote controls below. Smart TV controls available via slide-out panel.

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  [← Back]           REMOTE                                  │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────┐ │
│  │  SELECT DEVICE                                          │ │
│  │  [🛋️ Living Room] [🛏️ Master] [👤 Alpha] [👥 Beta]    │ │
│  │         ✓                                               │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────┐  ┌───────────────────────────┐  │
│  │    APPLE TV REMOTE    │  │    QUICK APPS             │  │
│  │  ┌───────────────┐    │  │  [Netflix] [Disney+]      │  │
│  │  │               │    │  │  [YouTube] [Prime]        │  │
│  │  │   TOUCHPAD    │    │  │  [Apple TV+] [HBO]        │  │
│  │  │   (swipe)     │    │  │                           │  │
│  │  └───────────────┘    │  │  ┌─────────────────────┐  │  │
│  │  [Menu] [TV] [Home]   │  │  │ 📺 Smart TV Panel   │  │  │
│  │  [⏪] [⏯️] [⏩]       │  │  │ (tap to expand)     │  │  │
│  │                        │  │  └─────────────────────┘  │  │
│  └───────────────────────┘  └───────────────────────────┘  │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  VOLUME: [━━━━━━━━━━━━━━━■━━━━━━━]  [🔇] [🔊]          │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Device Selector Implementation:**
```yaml
# Create input_select for active device
input_select:
  active_remote_device:
    name: Active Remote Device
    options:
      - Living Room
      - Master Bedroom
      - Alpha Guest
      - Beta Guest
    initial: Living Room
    icon: mdi:remote-tv
```

**Remote Card (Universal Remote Card):**
```yaml
type: custom:state-switch
entity: input_select.active_remote_device
states:
  Living Room:
    type: custom:universal-remote-card
    remote_id: remote.living_room_apple_tv
    media_player_id: media_player.living_room_apple_tv
    platform: Apple TV
    autofill_entity_id: true
    rows:
      - - power
        - menu
        - home
      - - touchpad
      - - skip_backward
        - play
        - pause
        - skip_forward
      - - volume_slider
    custom_actions:
      netflix:
        tap_action:
          action: perform-action
          perform_action: media_player.select_source
          target:
            entity_id: media_player.living_room_apple_tv
          data:
            source: Netflix
  Master Bedroom:
    type: custom:universal-remote-card
    remote_id: remote.master_bedroom_apple_tv
    # ... similar config
  Alpha Guest:
    type: custom:universal-remote-card
    remote_id: remote.alpha_apple_tv
    # ... similar config
  Beta Guest:
    type: custom:universal-remote-card
    remote_id: remote.beta_apple_tv
    # ... similar config
```

**Smart TV Slide-Out Panel (Bubble Card Popup):**
```yaml
type: custom:bubble-card
card_type: pop-up
name: Smart TV Controls
entity: media_player.samsung_tv_living_room
styles: |
  .bubble-pop-up {
    max-width: 400px;
  }
cards:
  - type: vertical-stack
    cards:
      - type: custom:mushroom-media-player-card
        entity: media_player.samsung_tv_living_room
        fill_container: true
        use_media_info: true
        show_volume_level: true
        media_controls:
          - play_pause_stop
          - previous
          - next
      - type: horizontal-stack
        cards:
          - type: custom:button-card
            name: Power
            icon: mdi:power
            tap_action:
              action: call-service
              service: media_player.toggle
              target:
                entity_id: media_player.samsung_tv_living_room
          - type: custom:button-card
            name: Source
            icon: mdi:import
            tap_action:
              action: more-info
              entity: media_player.samsung_tv_living_room
```

**Entities by Room:**
| Room | Apple TV Remote | Smart TV | Volume Control |
|------|-----------------|----------|----------------|
| Living Room | `remote.living_room_apple_tv` | `media_player.samsung_tv_living_room` | TV via Apple TV |
| Master Bedroom | `remote.master_bedroom_apple_tv` | - | HomePod stereo |
| Alpha | `remote.alpha_apple_tv` | `media_player.alpha_tv` (verify) | TV |
| Beta | `remote.beta_apple_tv` | `media_player.beta_tv` (verify) | TV |

### 8. Music View (Music Assistant)

**Design Philosophy:** Browse and play music, select output rooms. Show cover art and playback controls prominently. Multi-room selection with visual feedback.

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  [← Back]            MUSIC                    [🔀] [🔁]     │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────┐ │
│  │  NOW PLAYING                                           │ │
│  │  ┌──────────────┐                                      │ │
│  │  │              │  Song Title                          │ │
│  │  │  COVER ART   │  Artist Name                         │ │
│  │  │   (large)    │  Album Name                          │ │
│  │  │              │                                      │ │
│  │  └──────────────┘  ━━━━━━━━━●━━━━━━━  2:34 / 4:12     │ │
│  │                                                        │ │
│  │  [⏮️]    [⏪]    [  ▶️  ]    [⏩]    [⏭️]              │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  🔊 OUTPUT ROOMS (tap to toggle)                       │ │
│  │  [🛋️ Living]  [🛏️ Master]  [👤 Alpha]  [👥 Beta]      │ │
│  │       ✓            ✓                                    │ │
│  │  [💼 Office]  [🍳 Kitchen]  [🚿 Master Bath]           │ │
│  │                                                        │ │
│  │  Group: [All] [Downstairs] [Upstairs] [Custom]         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  BROWSE: [Playlists] [Artists] [Albums] [Radio]        │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Music Assistant Media Player Card:**
```yaml
type: vertical-stack
cards:
  # Now Playing with Cover Art
  - type: custom:mushroom-media-player-card
    entity: media_player.mass_music_assistant
    fill_container: true
    use_media_info: true
    show_volume_level: true
    volume_controls:
      - volume_mute
      - volume_set
      - volume_buttons
    media_controls:
      - on_off
      - shuffle
      - previous
      - play_pause_stop
      - next
      - repeat
    card_mod:
      style: |
        ha-card {
          background: linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.95));
          border-radius: 16px;
        }
        mushroom-media-player-media-control {
          --control-icon-size: 48px;
        }

  # Room Output Selection
  - type: custom:mushroom-chips-card
    chips:
      - type: template
        content: "🔊 Output:"
      - type: entity
        entity: media_player.living_room_homepod
        tap_action:
          action: call-service
          service: media_player.join
          target:
            entity_id: media_player.mass_music_assistant
          data:
            group_members:
              - media_player.living_room_homepod
      - type: entity
        entity: media_player.master_bedroom_homepod
        tap_action:
          action: call-service
          service: media_player.join
          # ... similar
```

**Multi-Room Selection (Custom Implementation):**
```yaml
# Input booleans for room selection
input_boolean:
  music_output_living_room:
    name: Music Output - Living Room
  music_output_master_bedroom:
    name: Music Output - Master Bedroom
  music_output_alpha:
    name: Music Output - Alpha
  music_output_beta:
    name: Music Output - Beta
  music_output_office:
    name: Music Output - Office
  music_output_kitchen:
    name: Music Output - Kitchen
  music_output_master_bath:
    name: Music Output - Master Bath
```

**Room Toggle Buttons:**
```yaml
type: grid
columns: 4
square: false
cards:
  - type: custom:button-card
    entity: input_boolean.music_output_living_room
    name: Living
    icon: mdi:sofa
    show_state: false
    tap_action:
      action: toggle
    styles:
      card:
        - background: "[[[ return entity.state === 'on' ? 'linear-gradient(135deg, #6366f1, #8b5cf6)' : 'rgba(30,41,59,0.7)' ]]]"
        - border-radius: 12px
      icon:
        - color: "[[[ return entity.state === 'on' ? '#fff' : '#94a3b8' ]]]"
  # Repeat for each room...
```

**HomePod Entity Mapping:**
| Room | HomePod Entity | Type |
|------|----------------|------|
| Master Bedroom | `media_player.master_bedroom_homepod` | 2x Regular (stereo pair) |
| Office | `media_player.office_homepod` | 2x Mini |
| Kitchen | `media_player.kitchen_homepod` | 1x Mini |
| Alpha | `media_player.alpha_homepod` | 1x Mini |
| Beta | `media_player.beta_homepod` | 1x Mini |
| Master Bath | `media_player.master_bath_homepod` | 1x Mini |

**Preset Groups (Automation-based):**
```yaml
script:
  music_group_all:
    alias: "Music - Play Everywhere"
    sequence:
      - service: media_player.join
        target:
          entity_id: media_player.mass_music_assistant
        data:
          group_members:
            - media_player.master_bedroom_homepod
            - media_player.office_homepod
            - media_player.kitchen_homepod
            - media_player.alpha_homepod
            - media_player.beta_homepod
            - media_player.master_bath_homepod

  music_group_downstairs:
    alias: "Music - Downstairs Only"
    sequence:
      - service: media_player.join
        target:
          entity_id: media_player.mass_music_assistant
        data:
          group_members:
            - media_player.kitchen_homepod
            # Add other downstairs HomePods
```

**Volume Control Design (Master + Individual):**

Updated layout with volume:
```
┌─────────────────────────────────────────────────────────────┐
│  🔊 VOLUME                                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Master: [━━━━━━━━━━━━━━━●━━━━━━━━]  65%  [🔇]         │ │
│  │                                                        │ │
│  │  Room Volumes (tap 🎚️ to expand):                      │ │
│  │  [🛏️ Master ●●●●●○] [💼 Office ●●●●○○] [🍳 Kitchen ●●●○○○]│
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Master Volume Implementation:**
```yaml
# Master volume slider - affects all active outputs
type: custom:mushroom-slider-card
entity: media_player.mass_music_assistant
attribute: volume_level
fill: true
card_mod:
  style: |
    ha-card {
      background: linear-gradient(90deg, rgba(99,102,241,0.3), rgba(139,92,246,0.3));
      border-radius: 12px;
    }
```

**Individual Room Volume (Compact Dots Display):**
```yaml
# Compact volume indicators - tap to adjust
type: horizontal-stack
cards:
  - type: custom:button-card
    entity: media_player.master_bedroom_homepod
    name: Master
    icon: mdi:bed
    show_state: false
    custom_fields:
      vol_dots: |
        [[[
          const vol = Math.round((entity.attributes.volume_level || 0) * 6);
          let dots = '';
          for(let i = 0; i < 6; i++) {
            dots += i < vol ? '●' : '○';
          }
          return dots;
        ]]]
    styles:
      card:
        - background: rgba(30,41,59,0.6)
        - padding: 8px
        - border-radius: 10px
      custom_fields:
        vol_dots:
          - font-size: 10px
          - color: '#6366f1'
          - letter-spacing: 2px
    tap_action:
      action: fire-dom-event
      browser_mod:
        service: browser_mod.popup
        data:
          title: Master Bedroom Volume
          content:
            type: custom:mushroom-slider-card
            entity: media_player.master_bedroom_homepod
            attribute: volume_level
  # Repeat for each room...
```

**Full Volume Popup (Accessible via 🎚️ button):**
```yaml
type: custom:bubble-card
card_type: pop-up
name: Room Volumes
icon: mdi:tune-vertical
styles: |
  .bubble-pop-up {
    max-width: 350px;
  }
cards:
  - type: vertical-stack
    cards:
      - type: markdown
        content: "### 🔊 Master Volume"
      - type: custom:mushroom-slider-card
        entity: media_player.mass_music_assistant
        attribute: volume_level
        fill: true

      - type: markdown
        content: "### 🎚️ Individual Rooms"

      - type: entities
        entities:
          - entity: media_player.master_bedroom_homepod
            type: custom:slider-entity-row
            name: Master Bedroom
            icon: mdi:bed
          - entity: media_player.office_homepod
            type: custom:slider-entity-row
            name: Office
            icon: mdi:desk
          - entity: media_player.kitchen_homepod
            type: custom:slider-entity-row
            name: Kitchen
            icon: mdi:stove
          - entity: media_player.alpha_homepod
            type: custom:slider-entity-row
            name: Alpha
            icon: mdi:account
          - entity: media_player.beta_homepod
            type: custom:slider-entity-row
            name: Beta
            icon: mdi:account-multiple
          - entity: media_player.master_bath_homepod
            type: custom:slider-entity-row
            name: Master Bath
            icon: mdi:shower
        card_mod:
          style: |
            ha-card {
              background: transparent;
            }
```

**Volume Sync Script (optional - sync all to master):**
```yaml
script:
  sync_all_volumes_to_master:
    alias: "Sync All Volumes to Master"
    sequence:
      - variables:
          master_vol: "{{ state_attr('media_player.mass_music_assistant', 'volume_level') }}"
      - service: media_player.volume_set
        target:
          entity_id:
            - media_player.master_bedroom_homepod
            - media_player.office_homepod
            - media_player.kitchen_homepod
            - media_player.alpha_homepod
            - media_player.beta_homepod
            - media_player.master_bath_homepod
        data:
          volume_level: "{{ master_vol }}"
```

---

## Movie Mode Implementation

### Overview

Movie mode automatically adjusts lighting when content plays on Apple TV in the open floor plan (Living Room → Dining Room → Kitchen). Uses scene snapshots for restoration and blocks motion-triggered lighting during playback.

### Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     MOVIE MODE FLOW                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Apple TV → Playing    ──►  Save current scene snapshot    │
│  (after sunset)             Activate movie_mode scene      │
│                             Block motion automations        │
│                             Set movie_mode_active = ON      │
│                                                             │
│  Apple TV → Paused     ──►  Raise lights to 50%            │
│  (10 sec delay)             (intermission mode)             │
│                                                             │
│  Apple TV → Resume     ──►  Dim back to movie levels       │
│                                                             │
│  Apple TV → Idle/Off   ──►  Restore saved scene snapshot   │
│  (30 sec delay)             Unblock motion automations      │
│                             Set movie_mode_active = OFF     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Required Input Helpers
```yaml
input_boolean:
  movie_mode_active:
    name: Movie Mode Active
    icon: mdi:movie-open

  block_motion_lighting_living_room:
    name: Block Motion - Living Room
  block_motion_lighting_dining_room:
    name: Block Motion - Dining Room
  block_motion_lighting_kitchen:
    name: Block Motion - Kitchen
```

### Movie Mode Scenes
```yaml
scene:
  - name: "Movie Mode - Living Room"
    entities:
      # Living Room - OFF for best picture
      light.living_room:
        state: off

      # Entertainment center bias lighting (if available)
      light.entertainment_center_2:
        state: on
        brightness: 30
        kelvin: 6500  # Industry standard for accurate colors

      # Dining Room - very dim for navigation
      light.dining_room:
        state: on
        brightness_pct: 15
        kelvin: 2700  # Warm, non-distracting

      # Kitchen - off to prevent glare
      light.kitchen:
        state: off

      # Kitchen undercabinet - dim for safety
      light.kitchen_undercabinet_light:
        state: on
        brightness_pct: 10

  - name: "Movie Mode - Pause"
    entities:
      light.living_room:
        state: on
        brightness_pct: 40
      light.dining_room:
        state: on
        brightness_pct: 50
      light.kitchen:
        state: on
        brightness_pct: 30
```

### Movie Mode Automations
```yaml
automation:
  # Start Movie Mode
  - id: movie_mode_start
    alias: "Movie Mode - Start"
    trigger:
      - platform: state
        entity_id: media_player.living_room_apple_tv
        to: 'playing'
    condition:
      - condition: sun
        after: sunset
      - condition: state
        entity_id: input_boolean.movie_mode_active
        state: 'off'
    action:
      # Save current state
      - service: scene.create
        data:
          scene_id: before_movie
          snapshot_entities:
            - light.living_room
            - light.dining_room
            - light.kitchen
            - light.kitchen_undercabinet_light
            - light.entertainment_center_2

      # Small delay to confirm not just scrolling
      - delay:
          seconds: 5

      # Verify still playing
      - condition: state
        entity_id: media_player.living_room_apple_tv
        state: 'playing'

      # Activate movie mode
      - service: scene.turn_on
        target:
          entity_id: scene.movie_mode_living_room
        data:
          transition: 3

      # Block motion automations
      - service: input_boolean.turn_on
        target:
          entity_id:
            - input_boolean.block_motion_lighting_living_room
            - input_boolean.block_motion_lighting_dining_room
            - input_boolean.block_motion_lighting_kitchen

      # Set flag
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.movie_mode_active

  # Pause - Intermission Lighting
  - id: movie_mode_pause
    alias: "Movie Mode - Pause (Intermission)"
    trigger:
      - platform: state
        entity_id: media_player.living_room_apple_tv
        to: 'paused'
        for:
          seconds: 10  # Prevents flicker from brief pauses
    condition:
      - condition: state
        entity_id: input_boolean.movie_mode_active
        state: 'on'
    action:
      - service: scene.turn_on
        target:
          entity_id: scene.movie_mode_pause
        data:
          transition: 2

  # Resume from Pause
  - id: movie_mode_resume
    alias: "Movie Mode - Resume"
    trigger:
      - platform: state
        entity_id: media_player.living_room_apple_tv
        from: 'paused'
        to: 'playing'
    condition:
      - condition: state
        entity_id: input_boolean.movie_mode_active
        state: 'on'
    action:
      - service: scene.turn_on
        target:
          entity_id: scene.movie_mode_living_room
        data:
          transition: 2

  # End Movie Mode
  - id: movie_mode_end
    alias: "Movie Mode - End"
    trigger:
      - platform: state
        entity_id: media_player.living_room_apple_tv
        to: 'idle'
        for:
          seconds: 30
      - platform: state
        entity_id: media_player.living_room_apple_tv
        to: 'standby'
        for:
          seconds: 30
    condition:
      - condition: state
        entity_id: input_boolean.movie_mode_active
        state: 'on'
    action:
      # Restore previous lighting
      - service: scene.turn_on
        target:
          entity_id: scene.before_movie
        data:
          transition: 3

      # Unblock motion automations
      - service: input_boolean.turn_off
        target:
          entity_id:
            - input_boolean.block_motion_lighting_living_room
            - input_boolean.block_motion_lighting_dining_room
            - input_boolean.block_motion_lighting_kitchen

      # Clear flag
      - service: input_boolean.turn_off
        target:
          entity_id: input_boolean.movie_mode_active
```

### Manual Movie Mode Toggle (Dashboard Button)
```yaml
type: custom:button-card
name: Movie Mode
icon: mdi:movie-open
entity: input_boolean.movie_mode_active
show_state: true
tap_action:
  action: call-service
  service: script.toggle_movie_mode
styles:
  card:
    - background: "[[[ return entity.state === 'on' ? 'linear-gradient(135deg, #7c3aed, #4f46e5)' : 'rgba(30,41,59,0.7)' ]]]"
    - border-radius: 16px
    - box-shadow: "[[[ return entity.state === 'on' ? '0 0 20px rgba(124,58,237,0.4)' : 'none' ]]]"
  icon:
    - color: "[[[ return entity.state === 'on' ? '#fbbf24' : '#94a3b8' ]]]"
    - animation: "[[[ return entity.state === 'on' ? 'pulse 2s infinite' : 'none' ]]]"
```

### Script for Manual Toggle
```yaml
script:
  toggle_movie_mode:
    alias: "Toggle Movie Mode"
    sequence:
      - choose:
          - conditions:
              - condition: state
                entity_id: input_boolean.movie_mode_active
                state: 'off'
            sequence:
              # Save current state
              - service: scene.create
                data:
                  scene_id: before_movie
                  snapshot_entities:
                    - light.living_room
                    - light.dining_room
                    - light.kitchen
                    - light.kitchen_undercabinet_light
              # Activate movie mode
              - service: scene.turn_on
                target:
                  entity_id: scene.movie_mode_living_room
                data:
                  transition: 2
              - service: input_boolean.turn_on
                target:
                  entity_id:
                    - input_boolean.movie_mode_active
                    - input_boolean.block_motion_lighting_living_room
                    - input_boolean.block_motion_lighting_dining_room
                    - input_boolean.block_motion_lighting_kitchen
        default:
          # Restore and deactivate
          - service: scene.turn_on
            target:
              entity_id: scene.before_movie
            data:
              transition: 2
          - service: input_boolean.turn_off
            target:
              entity_id:
                - input_boolean.movie_mode_active
                - input_boolean.block_motion_lighting_living_room
                - input_boolean.block_motion_lighting_dining_room
                - input_boolean.block_motion_lighting_kitchen
```

### Motion Automation Integration

**Add this condition to existing motion automations:**
```yaml
# In your existing motion-triggered lighting automations
condition:
  - condition: state
    entity_id: input_boolean.block_motion_lighting_living_room
    state: 'off'
```

---

## Ring Doorbell Popup Fix

### Current Issues Identified

1. **Binary sensor entities may not exist** - Need to verify actual Ring integration entities
2. **browser_mod registration** - Tablets need explicit registration
3. **Ring livestream add-on** - Must be running for stream to work

### Fix Implementation

**Step 1: Verify Ring Entities**
```bash
# Check what Ring entities actually exist
# In HA Developer Tools > States, search for "ring" and "ding"
```

**Step 2: Update Automation Trigger**
```yaml
# automations.yaml - Update to use correct entity
- id: ring_doorbell_show_camera
  alias: "Ring Doorbell - Show Camera"
  trigger:
    - platform: state
      entity_id: binary_sensor.front_door_ding  # Verify this entity
      to: "on"
  action:
    - service: script.show_ring_camera
```

**Step 3: Update Script with Browser Mod 2.0 Syntax**
```yaml
# scripts.yaml
show_ring_camera:
  sequence:
    # Use popup instead of navigate for overlay effect
    - service: browser_mod.popup
      data:
        content:
          type: picture-entity
          entity: camera.front_door  # Verify entity name
          camera_view: live
          show_state: false
          show_name: false
        title: "🔔 Someone at the door"
        size: wide
        right_button: Dismiss
        dismissable: true
        timeout: 180000  # 3 minutes
    # Still send mobile notification
    - service: notify.mobile_app_jay_iphone_14_pro_max
      data:
        title: "🔔 Doorbell"
        message: "Someone is at the front door"
        data:
          image: /api/camera_proxy/camera.front_door
```

**Step 4: Register Tablets in Browser Mod**
- Access HA on each tablet
- Go to Settings > Devices > Browser Mod
- Register each tablet with unique ID

---

## Custom Cards Installation (HACS)

### Required Cards (verify installed)

```yaml
# Already installed (from research):
- lovelace-mushroom
- button-card
- card-mod
- mini-media-player
- kiosk-mode
- swipe-navigation

# Need to install:
- Bubble Card (critical for popups/navigation)
- simple-swipe-card (for room swiping)
```

### Installation Steps

1. Open HACS in Home Assistant
2. Search for "Bubble Card" → Install
3. Search for "Simple Swipe Card" → Install
4. Restart Home Assistant
5. Clear browser cache on tablets

---

## Theme Implementation

### Custom Theme File

**File:** `themes/tablet-modern/tablet-modern.yaml`

```yaml
tablet-modern-dark:
  # Base colors
  primary-color: "#6366f1"  # Indigo accent
  accent-color: "#8b5cf6"   # Purple accent

  # Background
  primary-background-color: "#0f172a"  # Dark slate
  secondary-background-color: "#1e293b"
  card-background-color: "rgba(30, 41, 59, 0.8)"

  # Text
  primary-text-color: "#f1f5f9"
  secondary-text-color: "#94a3b8"

  # Cards
  ha-card-background: "rgba(30, 41, 59, 0.7)"
  ha-card-border-radius: "16px"
  ha-card-box-shadow: "0 4px 6px -1px rgba(0, 0, 0, 0.3)"

  # Glassmorphism (for 10" tablets)
  ha-card-backdrop-filter: "blur(10px)"

  # Navigation
  paper-tabs-selection-bar-color: "#6366f1"

  # Buttons
  mdc-button-outline-color: "#6366f1"

tablet-modern-light:
  primary-color: "#6366f1"
  accent-color: "#8b5cf6"
  primary-background-color: "#f8fafc"
  secondary-background-color: "#e2e8f0"
  card-background-color: "rgba(255, 255, 255, 0.9)"
  primary-text-color: "#1e293b"
  secondary-text-color: "#64748b"
  ha-card-background: "rgba(255, 255, 255, 0.8)"
  ha-card-border-radius: "16px"
  ha-card-box-shadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
```

---

## Animation Implementation

### Button Press Animations (Button Card)

```yaml
# Ripple effect on tap
styles:
  card:
    - transition: transform 0.2s ease, box-shadow 0.2s ease
  custom_fields:
    ripple:
      - position: absolute
      - border-radius: 50%
      - transform: scale(0)
      - animation: ripple 0.6s linear
      - background: rgba(255,255,255,0.3)

# Scale on press
tap_action:
  action: call-service
  haptic: light
state:
  - operator: template
    value: "[[[ return true ]]]"
    styles:
      card:
        - transform: scale(0.98)
```

### Light Toggle Animation

```yaml
# Glow effect when light is on
state:
  - value: 'on'
    styles:
      card:
        - box-shadow: 0 0 20px 5px rgba(255, 200, 100, 0.3)
        - transition: box-shadow 0.3s ease
      icon:
        - color: var(--paper-item-icon-active-color)
        - animation: glow 2s ease-in-out infinite
```

### Navigation Slide Animation (CSS)

```css
/* View transition */
hui-view {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
```

---

## Entity Mapping (Verified Working)

### Light Groups by Room

| Room | Entity | Lights |
|------|--------|--------|
| Living Room | `light.living_room` | 1 light |
| Kitchen | `light.kitchen` | 2 lights |
| Dining Room | `light.dining_room` | 2 lights |
| Master Bedroom | `light.master_bedroom` | 4 lights |
| Master Bathroom | `light.master_bathroom` | 9 lights |
| Master Shower | `light.master_shower` | 2 lights |
| Office | `light.office` | 3 lights |
| Alpha | `light.alpha` | 4 lights |
| Beta | `light.beta` | 3 lights |
| Hall | `light.hall` | 4 lights |
| Master Hall | `light.master_hall` | 2 lights |

### Special Lights

| Light | Entity | Notes |
|-------|--------|-------|
| Under-bed | `light.underbedlight_2` | RGB strip |
| Hexagon | `light.master_bedroom_hexagon` | Accent |
| Nightlight | `light.master_bedroom_nightlight` | Dim |
| Entertainment | `light.entertainment_center_2` | WLED 150+ effects |
| Undercabinet | `light.kitchen_undercabinet_light` | Accent |

### Motion Controls by Room

| Room | Motion Disable | Manual Mode | Leave On |
|------|---------------|-------------|----------|
| Living Room | `input_boolean.living_room_motion_disable` | `input_boolean.living_room_manual_mode` | `input_boolean.living_room_leave_lights_on` |
| Kitchen | `input_boolean.kitchen_motion_disable` | `input_boolean.kitchen_manual_mode` | `input_boolean.kitchen_leave_lights_on` |
| Dining Room | `input_boolean.dining_room_motion_disable` | `input_boolean.dining_room_manual_mode` | `input_boolean.dining_room_leave_lights_on` |
| Master Bedroom | `input_boolean.mbr_motion_disable` | `input_boolean.mbr_manual_mode` | `input_boolean.mbr_leave_lights_on` |
| Office | `input_boolean.office_motion_disable` | `input_boolean.office_manual_mode` | `input_boolean.office_leave_lights_on` |

### Media Players

| Device | Entity |
|--------|--------|
| Samsung TV | `media_player.samsung_tv_living_room` |
| Living Room Apple TV | `media_player.living_room_apple_tv` |
| Master Bedroom TV | `media_player.master_bedroom_tv` |
| Spotify | `media_player.spotify_jstuart0` |
| Home Audio | `media_player.home_audio` |

### Climate & Weather

| Entity | Purpose |
|--------|---------|
| `climate.thermostat` | Honeywell Lyric T5 |
| `weather.home` | Weather forecast |

### Vacuum

| Entity | Purpose |
|--------|---------|
| `vacuum.roborock_vacuum_a15` | Zone cleaning |

---

## Implementation Steps

**DEADLINE: December 24, 2025 (Guests arriving)**

### Phase 1: Foundation (Today - Dec 22)

1. [ ] Install required HACS cards (Bubble Card, Universal Remote Card, State-Switch, Slider-Entity-Row)
2. [ ] Create theme file `themes/tablet-modern/tablet-modern.yaml`
3. [ ] Add all input helpers to `configuration.yaml` (theme, remote selector, movie mode, music outputs)
4. [ ] Create movie mode scenes in `scenes.yaml`
5. [ ] Add movie mode automations to `automations.yaml`
6. [ ] Add movie mode toggle script to `scripts.yaml`
7. [ ] Push config to HA and restart

### Phase 2: Dashboard Structure (Today - Dec 22)

1. [ ] Create new dashboard `dashboards/tablet-modern.yaml`
2. [ ] Configure kiosk mode
3. [ ] Create Bubble Card bottom navigation (13 tabs)
4. [ ] Set up all 13 views (Home, 9 rooms, Remote, Music, Settings)

### Phase 3: Core Views (Dec 22-23)

1. [ ] Home view with status overview + Movie Mode button
2. [ ] Living Room view (lights + quick controls)
3. [ ] Kitchen view
4. [ ] Dining Room view
5. [ ] Master Bedroom with sleep controls
6. [ ] Master Bathroom view
7. [ ] Office view
8. [ ] Alpha/Beta guest room views
9. [ ] Deck view with WLED controls

### Phase 4: Special Views (Dec 23)

1. [ ] TV Remote view with device selector and touchpad
2. [ ] Music view with cover art and room outputs
3. [ ] Settings view with theme switcher

### Phase 5: Testing & Polish (Dec 23-24)

1. [ ] Test movie mode automation (play/pause/stop)
2. [ ] Test TV remote for all 4 rooms
3. [ ] Test music controls and multi-room output
4. [ ] Test Ring doorbell popup
5. [ ] Test on 8" and 10" tablets
6. [ ] Verify no scrolling on any view
7. [ ] Final theme adjustments

---

## Success Criteria

**Core Functionality:**
- [ ] Dashboard loads in < 2 seconds
- [ ] No scrolling required on any view
- [ ] All 13 tabs accessible and working
- [ ] Works on both 8" and 10" tablets

**Movie Mode:**
- [ ] Auto-activates when Apple TV plays (after sunset)
- [ ] Living room lights off, dining dim, kitchen off
- [ ] Pausing raises lights to intermission level
- [ ] Stopping restores previous lighting
- [ ] Manual toggle works from Home view
- [ ] Motion automations blocked during movie

**TV Remote:**
- [ ] Device selector switches between 4 rooms
- [ ] Touchpad navigation works
- [ ] App launcher buttons work (Netflix, Disney+, etc.)
- [ ] Volume control works
- [ ] Smart TV panel accessible for rooms with Smart TVs

**Music:**
- [ ] Cover art displays for now playing
- [ ] Playback controls work (play/pause/skip)
- [ ] Room output selection works (toggle individual rooms)
- [ ] Master volume slider works
- [ ] Individual room volume accessible via popup
- [ ] Preset groups work (All, Downstairs, etc.)

**Other:**
- [ ] Ring doorbell popup appears when doorbell pressed
- [ ] Theme can be switched from Settings
- [ ] All lights controllable from respective room tabs
- [ ] WLED effects controllable from Deck tab

---

## Rollback Plan

If issues arise:
1. Original tablet dashboard preserved at `dashboards/tablet-dashboard.yaml`
2. New dashboard will be created as `dashboards/tablet-modern.yaml`
3. Can switch back via HA dashboard settings
4. Theme changes isolated to new theme file

---

## Questions for User

1. **Deck entities:** What lights/devices should be on the Deck tab? (None found in current config)
2. **Ring entity verification:** Can you check Developer Tools > States and search for "ding" or "ring" to confirm the doorbell binary sensor name?
3. **Tablet browser app:** Are you using Fully Kiosk Browser or native browser? (Affects kiosk mode configuration)
4. **Color preference:** Any specific accent colors you prefer? (Currently proposing indigo/purple gradient)

---

## Appendix: Key File Locations

| Purpose | File Path |
|---------|-----------|
| New Dashboard | `dashboards/tablet-modern.yaml` |
| New Theme | `themes/tablet-modern/tablet-modern.yaml` |
| Scripts | `scripts.yaml` |
| Automations | `automations.yaml` |
| Original Dashboard | `dashboards/tablet-dashboard.yaml` |
| Configuration | `configuration.yaml` |
