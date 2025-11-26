# Quick Start: Building and Deploying the Fire TV App

**Complete Beginner's Guide** - No Android experience required!

This guide will walk you through deploying The Grid Signage app to your Fire TV stick step-by-step.

## What You'll Need

1. **A computer** (Windows, Mac, or Linux)
2. **Your Fire TV Stick** (Gen 2 or later)
3. **WiFi network** (Fire TV and computer must be on the same network)
4. **About 1-2 hours** for first-time setup (faster next time)

---

## Part 1: Install Android Studio

Android Studio is the official tool for building Android apps. You only need to do this once.

### Windows Installation

1. **Download Android Studio**:
   - Go to: https://developer.android.com/studio
   - Click the big green **"Download Android Studio"** button
   - Accept the terms and conditions
   - Download will start (approximately 1GB file)

2. **Install Android Studio**:
   - Find the downloaded file (usually in your Downloads folder)
   - Double-click `android-studio-<version>.exe`
   - Click **Next** through the installer
   - Use all default settings (don't change anything)
   - Click **Install**
   - Wait 5-10 minutes for installation to complete
   - Click **Finish**

3. **First Launch**:
   - Android Studio will open automatically
   - You'll see "Import Android Studio Settings" - choose **"Do not import settings"**
   - Click **OK**
   - Wait for "Android Studio Setup Wizard"
   - Click **Next**
   - Choose **Standard** installation type
   - Click **Next** through the screens
   - Click **Finish** to download SDK components (this takes 10-20 minutes)
   - ☕ Grab a coffee - this is the longest wait

4. **Verify Installation**:
   - Once complete, you'll see the Android Studio welcome screen
   - ✅ You're ready to move on!

### Mac Installation

1. Download Android Studio from https://developer.android.com/studio
2. Open the downloaded `.dmg` file
3. Drag "Android Studio" to your Applications folder
4. Open Android Studio from Applications
5. Follow the same "First Launch" steps as Windows above

### Linux Installation

1. Download Android Studio from https://developer.android.com/studio
2. Extract the archive: `tar -xzf android-studio-*.tar.gz`
3. Navigate to `android-studio/bin/`
4. Run: `./studio.sh`
5. Follow the same "First Launch" steps as Windows above

---

## Part 2: Enable Developer Mode on Fire TV

This allows you to install apps that aren't from the Amazon Appstore.

### Step-by-Step Instructions

1. **Turn on your Fire TV** and navigate to the home screen

2. **Open Settings**:
   - Use your Fire TV remote
   - Scroll to the far right to **Settings** (gear icon)
   - Press the center button to select

3. **Navigate to My Fire TV**:
   - Scroll down to **My Fire TV** (or "Device & Software" on older versions)
   - Press center button

4. **Go to About**:
   - Select **About**
   - Press center button

5. **Unlock Developer Mode** (the secret trick!):
   - You'll see a screen with device information
   - Highlight the line that says your device name (top of the list)
   - **Press the center button 7 times rapidly** (like clicking)
   - After the 7th press, you'll see a message: **"You are now a developer!"**
   - 🎉 Success!

6. **Enable Developer Options**:
   - Press the **Back** button once (you're now back at "My Fire TV" menu)
   - You'll now see a new option: **Developer Options**
   - Select **Developer Options**

7. **Turn on ADB Debugging**:
   - Select **ADB debugging**
   - Toggle it to **ON**
   - If you see a warning, select **Turn On**

8. **Allow Unknown Sources**:
   - Select **Apps from Unknown Sources**
   - Toggle it to **ON**
   - If you see a warning, select **Turn On**

✅ Your Fire TV is now ready to receive apps!

---

## Part 3: Find Your Fire TV's IP Address

Your computer needs to know where your Fire TV is on the network.

1. **On Fire TV, go back to Settings** → **My Fire TV**
2. Select **About**
3. Select **Network**
4. You'll see "IP Address: **192.168.X.XXX**"
5. **Write this down!** You'll need it later
   - Example: `192.168.1.45`

---

## Part 4: Install ADB Tools

ADB (Android Debug Bridge) is how your computer talks to the Fire TV.

### Windows

1. **Download Platform Tools**:
   - Go to: https://developer.android.com/studio/releases/platform-tools
   - Click **"Download SDK Platform-Tools for Windows"**
   - Accept the terms
   - Download the ZIP file (about 10MB)

2. **Extract the Tools**:
   - Go to your Downloads folder
   - Right-click `platform-tools-latest-windows.zip`
   - Choose **"Extract All..."**
   - Extract to `C:\platform-tools\` (easy to remember location)

3. **Add to PATH** (makes ADB accessible from anywhere):
   - Press **Windows Key** and type "environment"
   - Click **"Edit the system environment variables"**
   - Click **"Environment Variables"** button
   - Under "System variables", find **Path**, click **Edit**
   - Click **New**
   - Type: `C:\platform-tools`
   - Click **OK** on all windows

4. **Verify Installation**:
   - Press **Windows Key + R**
   - Type `cmd` and press Enter
   - Type: `adb version`
   - You should see version information
   - ✅ ADB is installed!

### Mac

Open Terminal and run:
```bash
brew install android-platform-tools
```

If you don't have Homebrew, first install it from https://brew.sh

### Linux

```bash
sudo apt update
sudo apt install adb
```

---

## Part 5: Open the Fire TV App Project in Android Studio

Now we'll open the existing Fire TV app project.

1. **Launch Android Studio**:
   - Double-click the Android Studio icon
   - Wait for it to fully load (you'll see the welcome screen)

2. **Open the Project**:
   - On the welcome screen, click **Open**
   - If you're already in Android Studio, go to **File** → **Open**

3. **Navigate to the Project**:
   - Browse to where you have "The Grid 2.0" folder
   - Go inside: **The Grid 2.0** → **core** → **firetv_app**
   - Click the **firetv_app** folder (don't go inside)
   - Click **OK**

4. **Wait for Gradle Sync** (important!):
   - Android Studio will start loading the project
   - At the bottom of the screen, you'll see: "Gradle Build Running..."
   - **Wait for this to complete** (2-5 minutes first time)
   - You'll see "Gradle sync finished" when done
   - ✅ The project is now open!

5. **Verify Project Structure**:
   - On the left side, you should see a file tree
   - Expand **app** → **src** → **main** → **java** → **ca** → **jump** → **thegrid** → **signage**
   - You should see **MainActivity.java**
   - ✅ Everything looks good!

---

## Part 6: Build the APK

An APK is the Android app file that will run on your Fire TV. We'll build it now.

### Using Android Studio (Recommended for Beginners)

1. **Start the Build**:
   - At the top menu, click **Build**
   - You may see different menu options depending on your Android Studio version:
     - **Option A**: "Build Bundle(s) / APK(s)" → Click "Build APK(s)"
     - **Option B**: "Assemble 'app'" or "Assemble Module 'The_Grid_Signage.app'" → Click this
     - **Option C**: If you only see "Generate App Bundles / SDK's" → Skip this, use the command line method below
   - Any option with "assemble" or "APK" (but NOT "bundle") will work

2. **Wait for Build**:
   - At the bottom of the screen, you'll see "Building APK..."
   - This takes 1-3 minutes
   - You'll see a notification balloon when it's done: "APK(s) generated successfully"

3. **Locate Your APK**:
   - In the notification, click the **locate** link
   - This opens the folder with your APK
   - You'll see a file named `app-debug.apk`
   - **This is your app file!** 🎉

4. **Remember the Location** (you'll need it):
   - The full path is: `The Grid 2.0\core\firetv_app\app\build\outputs\apk\debug\app-debug.apk`
   - You can copy this file to your Desktop for easier access

### Alternative: Using Command Line (Advanced)

If you prefer using the command line:

**Windows**:
```bash
# Navigate to the project folder
cd "C:\Users\<YourName>\Desktop\The Grid 2.0\core\firetv_app"

# Build the APK
gradlew.bat assembleDebug
```

**Mac/Linux**:
```bash
# Navigate to the project folder
cd ~/Desktop/The\ Grid\ 2.0/core/firetv_app

# Build the APK
./gradlew assembleDebug
```

The APK will be at the same location: `app/build/outputs/apk/debug/app-debug.apk`

---

## Part 7: Connect to Your Fire TV with ADB

Now we'll wirelessly connect your computer to your Fire TV.

### Step-by-Step Connection

1. **Open Command Prompt (Windows) or Terminal (Mac/Linux)**:
   - **Windows**: Press **Windows Key + R**, type `cmd`, press Enter
   - **Mac**: Press **Cmd + Space**, type `terminal`, press Enter
   - **Linux**: Press **Ctrl + Alt + T**

2. **Connect to Your Fire TV**:
   - Remember that IP address you wrote down? Time to use it!
   - Type this command (replace `192.168.1.45` with YOUR Fire TV's IP):

   ```bash
   adb connect 192.168.1.45:5555
   ```

   - Press Enter
   - You should see: **"connected to 192.168.1.45:5555"**

3. **Authorize the Connection** (first time only):
   - **Look at your TV screen!**
   - You'll see a popup: "Allow USB debugging?"
   - Use your Fire TV remote to select **"Always allow from this computer"**
   - Press **OK**
   - ✅ You're connected!

4. **Verify Connection**:
   - Type: `adb devices`
   - Press Enter
   - You should see your Fire TV's IP address listed
   - Example output:
   ```
   List of devices attached
   192.168.1.45:5555    device
   ```
   - If it says "unauthorized", repeat step 3

---

## Part 8: Install the App on Your Fire TV

Almost there! Now we'll push the app to your Fire TV.

### Installation Steps

1. **Make Sure You're Connected**:
   - In the same command prompt/terminal window
   - Type: `adb devices`
   - Verify your Fire TV is listed

2. **Navigate to the APK Location**:
   - **Windows**:
   ```bash
   cd "C:\Users\<YourName>\Desktop\The Grid 2.0\core\firetv_app"
   ```
   - **Mac/Linux**:
   ```bash
   cd ~/Desktop/The\ Grid\ 2.0/core/firetv_app
   ```

3. **Install the APK**:
   - Type this command:
   ```bash
   adb install app\build\outputs\apk\debug\app-debug.apk
   ```
   - **Mac/Linux** (use forward slashes):
   ```bash
   adb install app/build/outputs/apk/debug/app-debug.apk
   ```

   - Press Enter
   - You'll see "Performing Streamed Install"
   - Wait 5-10 seconds
   - You should see: **"Success"**
   - 🎉 The app is installed!

4. **If You Get "App Already Installed" Error**:
   - This means you're reinstalling
   - Use the `-r` flag to replace it:
   ```bash
   adb install -r app\build\outputs\apk\debug\app-debug.apk
   ```

5. **If You Get "Permission Denied" Error**:
   - Make sure "Apps from Unknown Sources" is enabled (Part 2, Step 8)
   - Disconnect and reconnect ADB:
   ```bash
   adb disconnect
   adb connect <YOUR_IP>:5555
   ```

---

## Part 9: Launch the App and Register Your Device

The moment of truth! Let's see it in action.

### Launch the App

1. **On Your Fire TV**:
   - Use your remote to go to **Home**
   - Navigate to **Your Apps & Channels** (at the top)
   - Scroll down to find **"The Grid Signage"**
   - Click on it to launch

2. **What You'll See**:
   - The app will open with a black screen
   - After a few seconds, you'll see a large **6-character code** (like "ABC123")
   - This is your **registration code**
   - **Leave the app running!** Don't close it

### Register the Device (NEW EASY WAY!)

Now you'll connect this Fire TV to The Grid using the new UI we built.

1. **Open The Grid on Your Computer**:
   - Go to: https://the-grid-v2-bxfue0bhbkacffac.canadaeast-01.azurewebsites.net
   - Sign in with your Microsoft account

2. **Navigate to Digital Signage**:
   - In the top menu, click **"Apps"** dropdown
   - Click **"Digital Signage"**
   - You'll see the new tabbed interface

3. **Click "Add Device"**:
   - Look for the purple **"Add Device"** button (floating at bottom right)
   - Click it
   - A modal popup will appear

4. **Enter the Registration Code**:
   - Type the **6-character code** from your Fire TV screen
   - Example: `ABC123`
   - Click **"Register Device"**

5. **Name Your Device** (optional but recommended):
   - After registration, click on the device card
   - Click **"Edit Device"**
   - Fill in:
     - **Name**: e.g., "Store 1 Main Display"
     - **Location**: e.g., "Store 1, Front Counter"
   - Click **"Save"**

6. **Assign Content**:
   - On the device card, you'll see a dropdown: **"Assign Content"**
   - Click it
   - Choose either:
     - A **Playlist** (rotates through multiple screens)
     - A **Screen Design** (shows one screen continuously)
   - Click **"Assign"**

7. **Watch the Magic!** 🎉
   - Within 5 seconds, your Fire TV will automatically refresh
   - The registration code will disappear
   - Your assigned content will start playing!
   - The device card will show status: **"Online"** (green dot)

### What Happens Next

- **Playlist Mode**: If you assigned a playlist, the Fire TV will rotate through all screens based on the duration settings (default 30 seconds each)
- **Single Screen Mode**: If you assigned a single screen, it will display that screen continuously
- **Auto-Refresh**: The Fire TV polls The Grid every 5 seconds, so any changes you make to playlists or screens will appear automatically

### Check Device Status

Back in The Grid's Digital Signage app:
- Click the **"Devices"** tab
- You'll see your device card with:
  - Device name
  - Online/offline status (green/gray/red dot)
  - Last seen timestamp
  - Currently assigned content
  - Quick assign dropdown to change content

---

## Part 10: Create Your First Screen Design

Now that your device is connected, let's create some content for it to display!

### Create a Screen Design

1. **In The Grid Digital Signage App**:
   - Click the **"Designs"** tab

2. **Click "Create New Design"**:
   - Look for the purple button: **"Create New Design"**
   - Click it

3. **Fill in the Design Details**:
   - **Name**: e.g., "Welcome Screen"
   - **Description**: e.g., "Main welcome message for lobby"
   - **HTML Code**: Copy this example:
   ```html
   <div style="text-align: center; padding: 100px;">
     <h1>Welcome to Our Store!</h1>
     <p>Thank you for visiting us today</p>
   </div>
   ```
   - **CSS Code**: Copy this example:
   ```css
   body {
     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
     color: white;
     font-family: Arial, sans-serif;
   }
   h1 {
     font-size: 72px;
     margin-bottom: 20px;
   }
   p {
     font-size: 36px;
   }
   ```
   - **JS Code**: (leave blank for now)

4. **Preview Your Design**:
   - Click **"Preview"** button
   - A new tab will open showing your design
   - Adjust the HTML/CSS until you like it

5. **Save Your Design**:
   - Click **"Save"**
   - Your design is now available!

### Assign Your New Design to Your Device

1. **Go to the Devices Tab**
2. **Find Your Device Card**
3. **Click the "Assign Content" Dropdown**
4. **Select Your New "Welcome Screen" Design**
5. **Watch Your Fire TV Update!**
   - Within 5 seconds, the new design will appear on your Fire TV

---

## Part 11: Create a Playlist

Want to rotate through multiple screens? Create a playlist!

### Create a Playlist

1. **Click the "Playlists" Tab**
2. **Click "Create New Playlist"**
3. **Fill in Details**:
   - **Name**: e.g., "Lobby Rotation"
   - Click **"Add Screen"** for each screen you want
   - Set the **Duration** (how long each screen shows)
   - Use drag handles to reorder screens
4. **Save the Playlist**

### Assign the Playlist to Your Device

1. **Go to Devices Tab**
2. **Find Your Device**
3. **Assign Content** → Select Your Playlist
4. **Watch It Rotate!**

---

## Troubleshooting Common Issues

### Problem: Can't Connect to Fire TV with ADB

**Error Message**: "Unable to connect" or "Connection refused"

**Solutions**:
1. **Check the IP Address**:
   - Make sure you typed it correctly
   - Go back to Fire TV: Settings → My Fire TV → About → Network
   - Verify the IP hasn't changed

2. **Check WiFi Network**:
   - Your computer and Fire TV must be on the **same WiFi network**
   - Check your computer's WiFi connection
   - Check Fire TV's network (Settings → Network)

3. **Restart ADB**:
   - Disconnect: `adb disconnect`
   - Try connecting again: `adb connect <IP>:5555`

4. **Restart Fire TV**:
   - Hold the **Select** and **Play/Pause** buttons for 5 seconds
   - Or: Settings → My Fire TV → Restart

5. **Re-enable ADB Debugging**:
   - Go to Settings → My Fire TV → Developer Options
   - Turn ADB Debugging OFF, then back ON

---

### Problem: "Device Unauthorized" Error

**What It Means**: Fire TV needs you to approve the connection.

**Solution**:
1. **Look at your TV screen!** (This is important!)
2. You should see a popup: "Allow USB debugging?"
3. Check "Always allow from this computer"
4. Click OK with your remote
5. Try the `adb devices` command again

---

### Problem: App Won't Install

**Error Message**: "App not installed" or "INSTALL_FAILED"

**Solutions**:

1. **Make Sure "Unknown Sources" is Enabled**:
   - Settings → My Fire TV → Developer Options
   - Turn on "Apps from Unknown Sources"

2. **Uninstall Old Version First**:
   ```bash
   adb uninstall ca.jump.thegrid.signage
   ```
   Then try installing again

3. **Check ADB Connection**:
   - Type: `adb devices`
   - Make sure your Fire TV is listed
   - It should say "device", not "unauthorized"

---

### Problem: Registration Code Not Showing

**What You See**: Black screen or app crashes when launched.

**Solutions**:

1. **Check Fire TV Internet Connection**:
   - Settings → Network
   - Try opening Amazon Appstore to verify internet works
   - Try browsing to confirm WiFi is working

2. **View Error Logs** (Advanced):
   ```bash
   adb logcat | grep GridSignage
   ```
   Look for error messages

3. **Reinstall the App**:
   ```bash
   adb uninstall ca.jump.thegrid.signage
   adb install app\build\outputs\apk\debug\app-debug.apk
   ```

4. **Check The Grid Server**:
   - Make sure https://the-grid-v2-bxfue0bhbkacffac.canadaeast-01.azurewebsites.net is accessible
   - Try opening it in your web browser

---

### Problem: Content Not Displaying After Registration

**What You See**: Registration code disappears, but screen stays black.

**Solutions**:

1. **Verify Content is Assigned**:
   - In The Grid Digital Signage app
   - Go to Devices tab
   - Check that your device has content assigned
   - Look for "Assigned: [Playlist/Screen Name]"

2. **Check Screen Design is Active**:
   - Go to Designs tab
   - Make sure the design is marked as "Active"
   - Edit the design and check the "Is Active" checkbox

3. **Wait 10 Seconds**:
   - The Fire TV polls every 5 seconds
   - Sometimes it takes two polling cycles

4. **Check WebView Errors** (Advanced):
   ```bash
   adb logcat | grep chromium
   ```

5. **Try Assigning Different Content**:
   - Unassign the content
   - Wait 5 seconds (screen should show registration code again)
   - Assign different content

---

### Problem: Fire TV Shows "Offline" in The Grid

**What It Means**: The Fire TV hasn't checked in recently.

**Solutions**:

1. **Make Sure App is Running**:
   - Open the app on Fire TV
   - It should be in the foreground

2. **Check Internet Connection**:
   - Fire TV needs internet to poll The Grid

3. **Restart the App**:
   - Press Home button on Fire TV remote
   - Navigate back to "The Grid Signage"
   - Launch it again

4. **Clear App Data** (Last Resort):
   ```bash
   adb shell pm clear ca.jump.thegrid.signage
   ```
   This will reset the app - you'll need to re-register with a new code

---

### Problem: Playlist Not Rotating

**What You See**: Only the first screen shows, others don't appear.

**Solutions**:

1. **Check Playlist Configuration**:
   - In The Grid, go to Playlists tab
   - Click your playlist
   - Make sure it has multiple screens
   - Each screen should have a duration (default: 30 seconds)

2. **Check JavaScript Errors** (Advanced):
   ```bash
   adb logcat | grep chromium
   ```

3. **Verify All Screens in Playlist are Active**:
   - Go to Designs tab
   - Each screen in your playlist should be marked "Active"

---

## Updating the App (When You Make Changes)

If you modify the Fire TV app code and want to update your Fire TV:

1. **Build the New APK**:
   - In Android Studio: Build → Build Bundle(s) / APK(s) → Build APK(s)

2. **Reinstall with -r Flag** (preserves data):
   ```bash
   adb install -r app\build\outputs\apk\debug\app-debug.apk
   ```

3. **Your Device Registration is Preserved**:
   - You won't need to re-enter the registration code
   - All assigned content stays the same

---

## Quick Reference: Useful Commands

Here are the most common commands you'll use:

### ADB Commands

```bash
# Connect to Fire TV
adb connect 192.168.1.45:5555

# Check connected devices
adb devices

# Install app
adb install app\build\outputs\apk\debug\app-debug.apk

# Reinstall app (keeps data)
adb install -r app\build\outputs\apk\debug\app-debug.apk

# Uninstall app
adb uninstall ca.jump.thegrid.signage

# Restart the app remotely
adb shell am start -n ca.jump.thegrid.signage/.MainActivity

# View app logs (useful for troubleshooting)
adb logcat | grep GridSignage

# Clear app data (forces re-registration)
adb shell pm clear ca.jump.thegrid.signage

# Disconnect from Fire TV
adb disconnect
```

### Building Commands

```bash
# Build APK (Windows)
gradlew.bat assembleDebug

# Build APK (Mac/Linux)
./gradlew assembleDebug
```

---

## Summary: What You've Accomplished! 🎉

Congratulations! You've successfully:

1. ✅ Installed Android Studio
2. ✅ Enabled Developer Mode on your Fire TV
3. ✅ Installed ADB tools
4. ✅ Built an Android APK from source
5. ✅ Sideloaded an app onto Fire TV
6. ✅ Registered a device with The Grid
7. ✅ Created custom screen designs
8. ✅ Deployed content to a physical device

### What You Can Do Now

- **Create Unlimited Screen Designs**: HTML/CSS/JS designs for any purpose
- **Build Playlists**: Rotate through multiple screens automatically
- **Manage Multiple Devices**: Deploy the app to as many Fire TVs as you want
- **Real-Time Updates**: Change content and see it update within 5 seconds
- **Monitor Device Status**: See which devices are online/offline in real-time

### Next Steps

1. **Experiment with Designs**:
   - Try adding animations with CSS
   - Use JavaScript for dynamic content
   - Fetch live data from APIs

2. **Deploy to More Fire TVs**:
   - Install the app on additional Fire TV sticks
   - Each gets a unique registration code
   - Assign different content to different locations

3. **Create Advanced Playlists**:
   - Mix different types of content
   - Adjust timing for different screens
   - Create location-specific rotations

4. **Monitor and Maintain**:
   - Check the Devices tab regularly
   - Watch for offline devices
   - Update content as needed

---

## Getting Help

### If Something Goes Wrong

1. **Check the Troubleshooting Section** (above)
   - Most common issues are covered

2. **Check the Logs**:
   ```bash
   adb logcat | grep GridSignage
   ```

3. **Start Fresh** (nuclear option):
   ```bash
   # Uninstall app
   adb uninstall ca.jump.thegrid.signage

   # Reinstall
   adb install app\build\outputs\apk\debug\app-debug.apk
   ```

### Additional Documentation

- **README.md** - Technical overview of the Fire TV app
- **Digital Signage Admin** - Manage devices, screens, and playlists via The Grid web interface

---

## Production Deployment (Advanced - Future)

For a production APK with code signing (for Amazon Appstore submission):

1. Generate a keystore (one-time):
   ```bash
   keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-alias
   ```

2. Configure signing in `app/build.gradle`

3. Build release APK:
   ```bash
   gradlew.bat assembleRelease
   ```

See Android documentation for full details on app signing.

## Final Checklist

Before you start, make sure you have:

- [ ] Android Studio installed
- [ ] Fire TV with Developer Mode enabled
- [ ] ADB tools installed
- [ ] Fire TV's IP address written down
- [ ] Computer and Fire TV on same WiFi network

**Estimated Time**: 1-2 hours for first-time setup (30 minutes after you've done it once)

---

**Good luck! You've got this!** 🚀

If you run into issues, check the Troubleshooting section above. Most problems have simple solutions.
