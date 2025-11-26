package ca.jump.thegrid.signage;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.view.WindowManager;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.TextView;
import android.widget.ProgressBar;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

/**
 * MainActivity for The Grid Fire TV Signage App
 *
 * This activity manages the registration flow and content playback for
 * digital signage on Fire TV devices.
 *
 * Flow:
 * 1. Request registration code from API
 * 2. Display code to user for entry in admin panel
 * 3. Poll API until device is registered and has content assigned
 * 4. Transition to playback mode (WebView)
 * 5. If playlist, rotate through screens; if single screen, display it
 */
public class MainActivity extends Activity {

    // API Configuration
    private static final String API_BASE_URL = "https://the-grid-v2-bxfue0bhbkacffac.canadaeast-01.azurewebsites.net";
    private static final String REQUEST_CODE_ENDPOINT = "/digital-signage/api/devices/request-code/";
    private static final String CONFIG_ENDPOINT = "/digital-signage/api/devices/%s/config/";

    // Registration polling interval (check every 5 seconds)
    private static final long POLL_INTERVAL_MS = 5000;

    // Playlist rotation handler
    private Handler playlistHandler;
    private int currentPlaylistIndex = 0;
    private List<PlaylistItem> playlistItems;

    // HTTP client
    private OkHttpClient httpClient;

    // Device registration data
    private String deviceId;
    private String registrationCode;

    // UI Components
    private View registrationLayout;
    private TextView codeTextView;
    private TextView statusTextView;
    private ProgressBar progressBar;
    private WebView webView;

    // Handlers
    private Handler pollHandler;
    private Runnable pollRunnable;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Keep screen on
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        // Initialize HTTP client with timeouts
        httpClient = new OkHttpClient.Builder()
                .connectTimeout(10, TimeUnit.SECONDS)
                .readTimeout(10, TimeUnit.SECONDS)
                .writeTimeout(10, TimeUnit.SECONDS)
                .build();

        // Initialize UI components
        registrationLayout = findViewById(R.id.registration_layout);
        codeTextView = findViewById(R.id.code_text);
        statusTextView = findViewById(R.id.status_text);
        progressBar = findViewById(R.id.progress_bar);
        webView = findViewById(R.id.webview);

        // Configure WebView for full-screen signage
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setLoadWithOverviewMode(true);
        webSettings.setUseWideViewPort(true);
        webSettings.setCacheMode(WebSettings.LOAD_NO_CACHE);

        // WebView client to handle page loads
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                // Hide system UI for true full-screen
                hideSystemUI();
            }
        });

        // Initialize handlers
        pollHandler = new Handler(Looper.getMainLooper());
        playlistHandler = new Handler(Looper.getMainLooper());

        // Start registration flow
        requestRegistrationCode();
    }

    /**
     * Request a registration code from the API
     */
    private void requestRegistrationCode() {
        updateStatus("Requesting registration code...");

        String url = API_BASE_URL + REQUEST_CODE_ENDPOINT;
        JSONObject requestBody = new JSONObject();

        try {
            requestBody.put("device_name", "Fire TV Device");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        RequestBody body = RequestBody.create(
                requestBody.toString(),
                MediaType.parse("application/json")
        );

        Request request = new Request.Builder()
                .url(url)
                .post(body)
                .build();

        httpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                runOnUiThread(() -> {
                    updateStatus("Error connecting to server. Retrying...");
                    // Retry after 3 seconds
                    new Handler(Looper.getMainLooper()).postDelayed(
                            MainActivity.this::requestRegistrationCode,
                            3000
                    );
                });
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    try {
                        JSONObject json = new JSONObject(response.body().string());
                        if (json.getBoolean("success")) {
                            deviceId = json.getString("device_id");
                            registrationCode = json.getString("registration_code");

                            runOnUiThread(() -> {
                                displayRegistrationCode();
                                startPollingForConfig();
                            });
                        } else {
                            throw new Exception("API returned success=false");
                        }
                    } catch (Exception e) {
                        runOnUiThread(() -> {
                            updateStatus("Error parsing response. Retrying...");
                            new Handler(Looper.getMainLooper()).postDelayed(
                                    MainActivity.this::requestRegistrationCode,
                                    3000
                            );
                        });
                    }
                } else {
                    runOnUiThread(() -> {
                        updateStatus("Server error. Retrying...");
                        new Handler(Looper.getMainLooper()).postDelayed(
                                MainActivity.this::requestRegistrationCode,
                                3000
                        );
                    });
                }
            }
        });
    }

    /**
     * Display the registration code on screen
     */
    private void displayRegistrationCode() {
        codeTextView.setText(registrationCode);
        updateStatus("Enter this code in The Grid admin panel to assign content");
        progressBar.setVisibility(View.VISIBLE);
    }

    /**
     * Start polling the API for device configuration
     */
    private void startPollingForConfig() {
        pollRunnable = new Runnable() {
            @Override
            public void run() {
                checkDeviceConfig();
                pollHandler.postDelayed(this, POLL_INTERVAL_MS);
            }
        };
        pollHandler.post(pollRunnable);
    }

    /**
     * Check if device has been configured with content
     */
    private void checkDeviceConfig() {
        String url = API_BASE_URL + String.format(CONFIG_ENDPOINT, deviceId);

        Request request = new Request.Builder()
                .url(url)
                .get()
                .build();

        httpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                // Silently fail, will retry on next poll
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    try {
                        JSONObject json = new JSONObject(response.body().string());
                        if (json.getBoolean("success") && json.getBoolean("registered")) {
                            JSONObject config = json.getJSONObject("config");
                            String configType = config.getString("type");

                            if (!configType.equals("none")) {
                                // Stop polling
                                pollHandler.removeCallbacks(pollRunnable);

                                // Start playback
                                runOnUiThread(() -> startPlayback(config, configType));
                            }
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        });
    }

    /**
     * Start content playback based on configuration
     */
    private void startPlayback(JSONObject config, String configType) {
        try {
            if (configType.equals("playlist")) {
                // Playlist mode - load items and start rotation
                JSONArray items = config.getJSONArray("items");
                playlistItems = new ArrayList<>();

                for (int i = 0; i < items.length(); i++) {
                    JSONObject item = items.getJSONObject(i);
                    playlistItems.add(new PlaylistItem(
                            item.getString("player_url"),
                            item.getInt("duration_seconds")
                    ));
                }

                if (!playlistItems.isEmpty()) {
                    // Hide registration UI, show WebView
                    registrationLayout.setVisibility(View.GONE);
                    webView.setVisibility(View.VISIBLE);

                    // Start playlist rotation
                    currentPlaylistIndex = 0;
                    loadPlaylistItem(0);
                }

            } else if (configType.equals("screen")) {
                // Single screen mode - load and display
                String playerUrl = config.getString("player_url");

                // Hide registration UI, show WebView
                registrationLayout.setVisibility(View.GONE);
                webView.setVisibility(View.VISIBLE);

                // Load screen
                webView.loadUrl(playerUrl);
            }
        } catch (JSONException e) {
            e.printStackTrace();
            updateStatus("Error loading content configuration");
        }
    }

    /**
     * Load a specific playlist item
     */
    private void loadPlaylistItem(int index) {
        if (playlistItems == null || playlistItems.isEmpty()) {
            return;
        }

        PlaylistItem item = playlistItems.get(index);
        webView.loadUrl(item.url);

        // Schedule next item
        playlistHandler.postDelayed(() -> {
            currentPlaylistIndex = (currentPlaylistIndex + 1) % playlistItems.size();
            loadPlaylistItem(currentPlaylistIndex);
        }, item.durationSeconds * 1000L);
    }

    /**
     * Update status text
     */
    private void updateStatus(String message) {
        statusTextView.setText(message);
    }

    /**
     * Hide system UI for true full-screen mode
     */
    private void hideSystemUI() {
        View decorView = getWindow().getDecorView();
        decorView.setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                        | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                        | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_FULLSCREEN
        );
    }

    @Override
    protected void onResume() {
        super.onResume();
        hideSystemUI();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // Clean up handlers
        if (pollHandler != null && pollRunnable != null) {
            pollHandler.removeCallbacks(pollRunnable);
        }
        if (playlistHandler != null) {
            playlistHandler.removeCallbacksAndMessages(null);
        }
    }

    /**
     * Simple data class for playlist items
     */
    private static class PlaylistItem {
        String url;
        int durationSeconds;

        PlaylistItem(String url, int durationSeconds) {
            this.url = url;
            this.durationSeconds = durationSeconds;
        }
    }
}
