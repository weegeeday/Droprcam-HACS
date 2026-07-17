# Droprcam Custom Integration

This custom integration provides Home Assistant support for Droprcam hardware running the lightweight HTTP API on port 8080. 

## Features
- **Camera:** Provides the `rtsp://<camera_ip>/stream1` video stream via the camera platform.
- **Switch:** Provides a toggle for Night Vision (flips IR cut filter and turns on IR LEDs).
- **Light:** Provides control over the front Status LED ring (Blue, Yellow, Red, White).

## Installation
Add this repository to your HACS custom repositories list.
Then install the "Droprcam" integration and restart Home Assistant.

## Configuration
Go to **Settings** -> **Devices & Services** and click **Add Integration**. Search for "Droprcam" and provide your camera's IP address.
