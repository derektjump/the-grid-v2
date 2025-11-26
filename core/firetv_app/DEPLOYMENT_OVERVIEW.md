# Fire TV App Deployment - Quick Overview

**For Complete Beginners** - A visual guide to deploying The Grid Signage to your Fire TV stick.

---

## The Big Picture: How This Works

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Your Computer │      │    The Grid      │      │  Fire TV Stick  │
│                 │      │   (Azure Cloud)  │      │                 │
│  1. Build APK   │─────▶│                  │◀─────│  3. Shows Code  │
│  using Android  │      │  2. Generates    │      │     ABC123      │
│     Studio      │      │  Registration    │      │                 │
│                 │      │      Code        │      │                 │
└─────────────────┘      └──────────────────┘      └─────────────────┘
         │                        │                         │
         │                        │                         │
         └────────────────────────┼─────────────────────────┘
                                  │
                    4. You enter code "ABC123"
                       in The Grid web UI
                                  │
                    5. Assign content to device
                                  │
                    6. Fire TV displays content!
```

---

## The Flow: From Start to Finish

### Phase 1: Setup (One Time)
1. **Install Android Studio** → Build Android apps
2. **Enable Developer Mode on Fire TV** → Press device name 7 times
3. **Install ADB Tools** → Connect computer to Fire TV wirelessly
4. **Open Fire TV App Project** → Load existing code

### Phase 2: Build & Deploy (Every Time)
5. **Build APK** → Create the app file (app-debug.apk)
6. **Connect to Fire TV** → `adb connect 192.168.1.45:5555`
7. **Install APK** → `adb install app-debug.apk`

### Phase 3: Register & Use
8. **Launch App on Fire TV** → Shows registration code
9. **Enter Code in The Grid** → Digital Signage → Add Device → Enter code
10. **Assign Content** → Choose playlist or screen design
11. **Watch It Display!** → Content appears within 5 seconds

---

## What You're Building

The Fire TV app is a **simple full-screen WebView** that:
- Requests a registration code when first launched
- Displays the code in large text on the TV
- Polls The Grid API every 5 seconds
- When content is assigned, loads the content URL in a WebView
- For playlists, rotates through screens automatically

---

## File Structure

```
The Grid 2.0/
└── core/
    └── firetv_app/                    ← Open THIS folder in Android Studio
        ├── app/
        │   ├── src/
        │   │   └── main/
        │   │       ├── AndroidManifest.xml     (App configuration)
        │   │       ├── java/ca/jump/thegrid/signage/
        │   │       │   └── MainActivity.java   (Main app logic)
        │   │       └── res/
        │   │           └── layout/
        │   │               └── activity_main.xml (UI layout)
        │   └── build.gradle                     (App build config)
        ├── build.gradle                         (Project build config)
        ├── QUICK_START.md                       (Detailed setup guide)
        └── README.md                            (Technical documentation)
```

---

## Key Concepts for Beginners

### What is an APK?
- APK = Android Package
- It's like a `.exe` for Windows, but for Android
- Contains all the app code, resources, and configuration
- You build it with Android Studio

### What is ADB?
- ADB = Android Debug Bridge
- Command-line tool to talk to Android devices
- Lets you install apps, view logs, and debug
- Connects over WiFi (no USB cable needed for Fire TV!)

### What is Sideloading?
- Installing an app without using an app store
- Fire TV allows this if you enable "Apps from Unknown Sources"
- Common for testing and internal apps

### What is a Registration Code?
- 6-character code (like "ABC123")
- Fire TV app generates it automatically
- You enter it in The Grid web interface
- Links the physical device to your account

---

## Timeline Expectations

| Task | First Time | After You've Done It Once |
|------|-----------|---------------------------|
| Install Android Studio | 30-45 min | N/A (already installed) |
| Setup Fire TV | 5-10 min | 2 min (if you disable dev mode) |
| Install ADB | 10-15 min | N/A (already installed) |
| Open Project | 5 min | 1 min |
| Build APK | 3-5 min | 1-2 min |
| Connect & Install | 5 min | 1 min |
| Register & Test | 2 min | 1 min |
| **TOTAL** | **60-90 min** | **5-10 min** |

---

## Common Mistakes to Avoid

❌ **Forgetting to enable "Apps from Unknown Sources"** on Fire TV
   → Install will fail

❌ **Computer and Fire TV on different WiFi networks**
   → ADB won't connect

❌ **Not looking at TV screen for authorization prompt**
   → ADB will show "unauthorized"

❌ **Opening the wrong folder in Android Studio**
   → Open `firetv_app`, not `The Grid 2.0` or `app`

❌ **Trying to install while app is running on Fire TV**
   → Close the app first

❌ **Not waiting for Gradle sync to finish**
   → Build will fail

---

## The Registration Flow (Step-by-Step)

```
Fire TV Screen                     The Grid Web Interface
─────────────────                  ──────────────────────

1. App launches
   ┌──────────────┐
   │              │
   │   ABC123     │  ────────▶  2. You see this code
   │              │
   │ Registering  │
   └──────────────┘
                                  3. Click "Add Device"
                                     ┌─────────────────┐
                                     │ Enter Code:     │
                                     │ [ABC123____]    │
                                     │ [Register]      │
                                     └─────────────────┘

                                  4. Device appears!
                                     ┌─────────────────┐
                                     │ Device ABC123   │
                                     │ Status: Online  │
                                     │ Assign: [▼]     │
                                     └─────────────────┘

                                  5. Select content
                                     Assign: [Welcome Screen ▼]
                                            │
                                            ├─ Welcome Screen
                                            ├─ Sales Dashboard
                                            └─ Lobby Playlist

6. Content loads!
   ┌──────────────┐
   │              │
   │ Welcome to   │
   │ Our Store!   │
   │              │
   └──────────────┘
```

---

## What to Do After Successful Deployment

### Short Term
- [ ] Create 2-3 simple screen designs
- [ ] Test different HTML/CSS styles
- [ ] Create a playlist with multiple screens
- [ ] Test playlist rotation timing
- [ ] Try updating content and watch it auto-refresh

### Long Term
- [ ] Deploy to additional Fire TV sticks in other locations
- [ ] Create location-specific playlists
- [ ] Add JavaScript for dynamic content
- [ ] Integrate with external APIs for live data
- [ ] Monitor device uptime and status

---

## Resources

- **Full Guide**: [QUICK_START.md](QUICK_START.md) - Complete step-by-step instructions
- **Technical Docs**: [README.md](README.md) - Developer documentation
- **The Grid URL**: https://the-grid-v2-bxfue0bhbkacffac.canadaeast-01.azurewebsites.net
- **Android Studio**: https://developer.android.com/studio
- **Platform Tools (ADB)**: https://developer.android.com/studio/releases/platform-tools

---

## Need Help?

1. **Read [QUICK_START.md](QUICK_START.md)** - Comprehensive troubleshooting section
2. **Check logs**: `adb logcat | grep GridSignage`
3. **Start fresh**: Uninstall and reinstall the app
4. **Verify basics**: Same WiFi network, developer mode enabled, correct IP address

---

**You've got this!** The hardest part is the first time. After that, it's quick and easy. 🚀
