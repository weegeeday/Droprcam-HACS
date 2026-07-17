# Droprcam Custom Integration

This custom integration provides Home Assistant support for [Droprcam](https://github.com/weegeeday/Droprcam). 

## Features
- **Camera:** Provides the `rtsp://<camera_ip>/stream1` video stream via the camera platform.
- **Switch:** Provides a toggle for Night Vision (flips IR cut filter and turns on IR LEDs).
- **Light:** Provides control over the front Status LED ring (Blue, Yellow, Red, White).

## Installation

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=weegeeday&repository=Droprcam-HACS&category=integration)

Add this repository to your HACS custom repositories list.
Then install the "Droprcam" integration and restart Home Assistant.

## Configuration
Go to **Settings** -> **Devices & Services** and click **Add Integration**. Search for "Droprcam" and provide your camera's IP address.
