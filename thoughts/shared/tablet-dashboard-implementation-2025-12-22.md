# Tablet Dashboard Implementation - December 22, 2025

## Overview

Complete redesign and implementation of an information-dense tablet dashboard for Home Assistant, designed for wall-mounted tablets and guest access.

## Key Features Implemented

### 1. Home View - Command Center
- **Status Bar**: Date, inside/outside temperatures, front door status
- **Weather Forecast**: Full daily weather forecast with thermostat control
- **Movie Mode & Quick Actions**: Toggle movie mode, all lights off, goodnight scene
- **Room Status Grid**: Information-dense cards showing:
  - Large temperature display (24px bold)
  - Motion/occupancy indicator (green when occupied)
  - Light status indicator (yellow when on)
  - For Master Bedroom: bed occupancy status (0, 1, or 2 people)

### 2. Room Views (Living Room, Kitchen, Dining, Master, Office, Alpha, Beta, Master Bath)
Each room includes:
- **Header chips**: Room name, temperature, humidity (where available), live motion indicator
- **Environmental info bar**: Temperature, humidity, light level sensors
- **Light controls**: Mushroom light card with brightness slider
- **Light presets**: Quick buttons (100%, 75%, 50%, 25%, Off, plus room-specific scenes)
- **Media controls**: Apple TV and HomePod controls where applicable
- **Automation toggles**: Motion disable (and "Keep Lights On" for rooms that support it)

### 3. Master Bedroom Special Features
- **Sunbeam Bed Warmer Controls**:
  - Master power toggle
  - Left Side / Right Side toggles (renamed from Jay/Tracy for AirBnB guests)
  - Heat level selectors for each side
  - "Turn Off Bed Warmer" button
- **Bed occupancy indicator**: Shows who's in bed via weight sensors

### 4. Remote View (TV Control Center)
- Device selector for 4 Apple TVs (Living Room, Master Bedroom, Alpha, Beta)
- Dynamic media player card showing now playing for selected device
- Full D-Pad navigation (up, down, left, right, select)
- Playback controls (play/pause, volume up/down, mute)
- Navigation buttons (menu, home, skip forward/backward)

### 5. Music View - Audio Control
- **Now Playing**: Spotify with full controls
- **Music Sources**: Spotify, Apple Music, WiiM buttons
- **Output Rooms**: Grid of room media players with individual volume controls
- **Master Volume**: Quick presets (All Quiet, Low, Medium, Loud)

### 6. Settings View
- System status (inside/outside temp, HVAC state)
- Theme selection dropdown
- Background style selector (10 gradient options)
- Bedtime schedule settings
- Quick controls (All Lights Off, Reload Page)
- Navigation tips

### 7. Manual Mode Indicators (Added December 22, 2025)
Each room header chip bar shows:
- **Auto/Manual indicator**: Shows robot icon (green) when in auto mode, hand icon (orange) when in manual mode
- Rooms with indicators: Living Room, Master Bedroom, Office, Alpha, Beta
- Indicates when lighting is being controlled manually via Shelly/H2 switch inputs

## Motion Control Configuration

Different rooms have different levels of automation control:

| Room | Motion Disable | Keep Lights On | Notes |
|------|----------------|----------------|-------|
| Living Room | Yes | No | Only motion disable supported by Node-RED |
| Kitchen | Yes | No | Only motion disable supported |
| Dining Room | Yes | No | Only motion disable supported |
| Master Bedroom | Yes | Yes | Full override support |
| Office | Yes | Yes | Full override support |
| Alpha | Yes | Yes | Full override support |
| Beta | Yes | Yes | Full override support |

## Entity References

### Key Input Booleans Used
- `input_boolean.global_movie_mode` - Global movie mode flag
- `input_boolean.living_room_motion_disable` - Living room motion disable
- `input_boolean.kitchen_motion_disable` - Kitchen motion disable
- `input_boolean.dining_room_motion_disable` - Dining room motion disable
- `input_boolean.mbr_motion_disable` - Master bedroom motion disable
- `input_boolean.mbr_leave_lights_on` - Master bedroom keep lights on
- `input_boolean.office_motion_disable` - Office motion disable
- `input_boolean.leave_lights_on_office` - Office keep lights on
- `input_boolean.alpha_motion_disable` - Alpha motion disable
- `input_boolean.leave_lights_on_alpha` - Alpha keep lights on
- `input_boolean.beta_motion_disable` - Beta motion disable
- `input_boolean.leave_lights_on_beta` - Beta keep lights on

### Bed Warmer Entities
- `switch.sunbeam_bedding_dual_s2_power` - Master power
- `switch.sunbeam_bedding_dual_s2_side_a_power` - Right side power
- `switch.sunbeam_bedding_dual_s2_side_b_power` - Left side power
- `select.sunbeam_bedding_dual_s2_level_1` - Right side heat level
- `select.sunbeam_bedding_dual_s2_level_2` - Left side heat level

### Temperature Sensors (Updated December 22, 2025)
- `sensor.thermostat_indoor_temperature` - Living Room, Kitchen, Dining Room (no room-specific sensors)
- `sensor.underbed_motion_device_temperature` - Master Bedroom
- `sensor.office_cube_device_temperature` - Office
- `sensor.motion_presence_alpha_temperature` - Alpha Guest Room
- `sensor.motion_presence_beta_temperature` - Beta Guest Room
- `sensor.motion_shower_air_temperature` - Master Bathroom

### Humidity Sensors
- `sensor.aqara_presence_multisensor_fp300_humidity` - Master Bedroom
- `sensor.motion_presence_alpha_humidity` - Alpha Guest Room
- `sensor.motion_presence_beta_humidity` - Beta Guest Room

### Light Level Sensors
- `sensor.master_bedroom_mm_light_level` - Master Bedroom

### Occupancy Sensors (Updated December 22, 2025)
- `binary_sensor.living_room_occupancy` + `binary_sensor.fp_living_room_presence_sensor` - Living Room
- `binary_sensor.kitchen_occupancy` + `binary_sensor.kitchen_mm_presence_sensor` - Kitchen
- `binary_sensor.dining_room_occupancy` + `binary_sensor.dining_mm_presence_sensor` - Dining Room
- `binary_sensor.master_bedroom_occupancy` + `binary_sensor.master_bedroom_mm_occupancy` - Master Bedroom
- `binary_sensor.motion_office` + `binary_sensor.espresense_office` - Office
- `binary_sensor.motion_presence_alpha_presence` - Alpha Guest Room
- `binary_sensor.motion_presence_beta_presence` - Beta Guest Room
- `binary_sensor.master_bath_motion_door_motion` - Master Bathroom

### Manual Mode Indicators (Added December 22, 2025)
- `input_boolean.living_room_manual_mode` - Living Room
- `input_boolean.mbr_manual_mode` - Master Bedroom
- `input_boolean.office_manual_mode` - Office
- `input_boolean.alpha_manual_mode` - Alpha Guest Room
- `input_boolean.beta_manual_mode` - Beta Guest Room

### Media Players (Updated December 22, 2025)
- `media_player.living_room` - Living Room Apple TV
- `media_player.master_bedroom_2_2` - Master Bedroom Apple TV
- `media_player.alpha_2` - Alpha Apple TV
- `media_player.beta_2` - Beta Apple TV
- `media_player.kitchen_2` - Kitchen HomePod
- `media_player.office_2_2` - Office HomePod
- `media_player.master_bathroom_2` - Master Bathroom HomePod

### Bed Sensors
- `binary_sensor.jay_in_bed`
- `binary_sensor.tracy_in_bed`

## Files Modified

### Dashboard Files
- `/dashboards/tablet-modern.yaml` - Main dashboard (completely rebuilt)

### Configuration Files
- `/configuration.yaml` - Added lovelace dashboard registration, input helpers
- `/scripts.yaml` - Added `remote_send_dynamic` script for dynamic Apple TV control
- `/automations.yaml` - Movie mode automations
- `/scenes.yaml` - Movie mode scenes
- `/themes/tablet-modern/tablet-modern.yaml` - Theme variants

## Design Decisions

1. **Left/Right vs Jay/Tracy for bed warmer**: Changed to Left Side/Right Side for AirBnB guest-friendliness

2. **Motion controls per room**: Only rooms with Node-RED flow support for "Keep Lights On" have that toggle. Living room, kitchen, and dining room only have motion disable.

3. **No Restart HA button**: Removed from settings to prevent guests from accidentally restarting the system

4. **Information density**: Each room card shows temperature, motion status, and light status at a glance

5. **Swipe navigation**: Enabled for tablet swiping between views

6. **Manual mode indicators**: Added to room headers to show when lights are being controlled manually vs automatically. Uses input_boolean.*_manual_mode entities.

7. **Background customization**: Added input_select.dashboard_background with 10 modern gradient options:
   - Dark Slate, Midnight Blue, Deep Purple, Northern Lights, Cosmic Gradient
   - Neon Glow, Sunset Horizon, Ocean Depth, Forest Night, Minimalist Dark

8. **Temperature sensor validation**: Replaced non-existent sensors with working alternatives:
   - Living Room, Kitchen, Dining Room → thermostat_indoor_temperature
   - Master Bedroom → underbed_motion_device_temperature
   - Office → office_cube_device_temperature
   - Master Bathroom → motion_shower_air_temperature

9. **Bidirectional navigation arrows**: Added forward/back arrows in room headers for easy navigation:
   - Back arrow (chevron-left) on left side of header
   - Forward arrow (chevron-right) on right side of header
   - Navigation flow: Home → Living Room → Kitchen → Dining → Master Bedroom → Master Bath → Office → Alpha → Beta → Deck
   - Allows guests to navigate sequentially through all room tabs

10. **Navigation hints**: Added swipe hint at bottom of each room view for guest discoverability

11. **Kitchen appliance status**: Added oven status, stove burner indicator, and ice maker status cards

12. **Master bedroom accent lights**: Added hexagon wall light, underbed light, and master accent control group

13. **Apply & Reload button**: Added to settings for ensuring changes take effect

## Testing Notes

- Dashboard available at `/tablet-modern/`
- Swipe left/right to navigate between tabs
- All navigation paths use `/tablet-modern/` prefix
- Theme selector in settings allows changing dashboard appearance

## Future Improvements

- Add more WLED effect options on Deck view
- Consider adding vacuum control to home view
- Add security/camera view if Ring integration improved
- Consider adding energy monitoring dashboard
