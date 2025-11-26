# The Grid Fire TV Signage App

This is a simple Android app designed for Amazon Fire TV devices to display digital signage content from The Grid.

## Features

- Simple registration flow using a 6-character code
- Full-screen WebView playback of screen designs
- Playlist rotation support
- Automatic content refresh
- Minimal UI, designed for unattended operation

## How It Works

1. **Registration Flow**
   - App requests a registration code from the API
   - Displays the code on screen in large text
   - User enters the code in The Grid admin panel
   - User assigns a playlist or screen to the device
   - App polls the API until content is assigned
   - App transitions to playback mode

2. **Playback Mode**
   - For single screens: Loads the screen URL in a WebView
   - For playlists: Rotates through screens based on duration settings
   - Runs in full-screen kiosk mode
   - Refreshes content periodically

## Building and Sideloading

### Prerequisites

- Android Studio (latest version)
- Fire TV device with developer mode enabled
- ADB (Android Debug Bridge) installed

### Enable Developer Options on Fire TV

1. Go to **Settings** → **My Fire TV** → **About**
2. Click on the device name 7 times to enable Developer Options
3. Go back to **My Fire TV** → **Developer Options**
4. Enable **ADB debugging** and **Apps from Unknown Sources**

### Build the APK

1. Open the project in Android Studio
2. Select **Build** → **Build Bundle(s) / APK(s)** → **Build APK(s)**
3. The APK will be generated in `app/build/outputs/apk/debug/app-debug.apk`

### Install via ADB

1. Connect to your Fire TV via network:
   ```bash
   # Find your Fire TV's IP address (Settings → My Fire TV → About → Network)
   adb connect <fire-tv-ip-address>:5555
   ```

2. Install the APK:
   ```bash
   adb install app/build/outputs/apk/debug/app-debug.apk
   ```

3. Launch the app from the Fire TV home screen (Apps → Your Apps & Channels)

### Alternative: Install via File Transfer

1. Copy the APK to a USB drive
2. Plug the USB drive into your Fire TV
3. Use a file manager app (like ES File Explorer) to navigate to the APK
4. Click the APK to install

## Configuration

The app is pre-configured to connect to:
```
https://the-grid-v2-bxfue0bhbkacffac.canadaeast-01.azurewebsites.net
```

To change the server URL, edit the `API_BASE_URL` constant in `MainActivity.java`.

## API Endpoints Used

- `POST /digital-signage/api/devices/request-code/` - Request registration code
- `POST /digital-signage/api/devices/<uuid>/register/` - Mark device as registered
- `GET /digital-signage/api/devices/<uuid>/config/` - Fetch device configuration
- `GET /digital-signage/player/<slug>/` - Load screen content

## Troubleshooting

### App won't install
- Ensure "Apps from Unknown Sources" is enabled in Fire TV Developer Options
- Try uninstalling any previous version first

### App crashes on launch
- Check logcat output: `adb logcat | grep GridSignage`
- Ensure the API endpoint is reachable from the Fire TV
- Check that the device has internet access

### Registration code not showing
- Check network connectivity
- Verify API endpoint is correct in MainActivity.java
- Check logcat for error messages

### Content not displaying
- Ensure content is assigned in The Grid admin
- Check that the screen designs are marked as active
- Verify player URLs are publicly accessible (no authentication required)

## Development Notes

### Project Structure

```
firetv_app/
├── app/
│   ├── build.gradle (app-level config)
│   └── src/
│       └── main/
│           ├── AndroidManifest.xml
│           ├── java/ca/jump/thegrid/signage/
│           │   └── MainActivity.java
│           └── res/
│               ├── layout/
│               │   └── activity_main.xml
│               └── values/
│                   ├── strings.xml
│                   └── styles.xml
├── build.gradle (project-level config)
├── settings.gradle
└── README.md (this file)
```

### Key Components

- **MainActivity.java**: Main activity handling registration and playback
- **activity_main.xml**: Layout with registration UI and WebView
- **AndroidManifest.xml**: App configuration and permissions

### Technology Stack

- **Minimum SDK**: 22 (Android 5.1 - Fire TV Gen 2+)
- **Target SDK**: 33 (Android 13)
- **WebView**: For rendering screen designs
- **OkHttp**: For API communication (standard Android)

## License

Internal use only - Jump.ca
