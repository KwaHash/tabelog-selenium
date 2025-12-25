# Tabelog Follower Post Liker

This tool automates the process of liking the last 10 posts for every follower you have on Tabelog, using Selenium and Chrome remote debugging.

---

## Setup

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### Recommended: Use your existing logged-in Chrome browser

#### 1. Start Chrome with remote debugging enabled

**On Windows**  
- Double-click `start_chrome_debug.bat`  
  *or*  
- Run in PowerShell:
    ```powershell
    & "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
    ```

**On Mac/Linux**
```bash
google-chrome --remote-debugging-port=9222
# Or:
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222
```

>If Chrome is already running, close all Chrome windows first, then run one of the commands above.

#### 2. Login to Tabelog

Use the Chrome window that opened with remote debugging enabled and log in to your Tabelog account.

#### 3. Run the script

```bash
python main.py
```

The script will automatically connect to your already-logged-in browser and start processing your followers.

---

### Command Line Arguments

- `--remote-port N`  
  Specify remote debugging port (default: 9222)

---

#### Additional Options (to be added in your implementation, see main.py):

*By default, the script will like the last 10 posts for all your followers. The following options can be added to main.py for more advanced usage by extending the argument parser:*

- `--max-followers N` : Process only the first N followers
- `--max-posts N` : Like only N posts per follower (default: 10)
- `--new-browser` : Start a new Chrome instance (will require a fresh login)
- `--headless` : Run browser in headless mode (only with `--new-browser`)

---

## How It Works

1. **Connects to an existing Chrome browser** launched with remote debugging enabled.
2. **Navigates to your Tabelog follower page** and collects the URLs of all followers.
3. **Visits each follower's profile**, up to the desired count.
4. **Finds and likes their latest posts** (the last 10 by default).
5. **Pauses between actions** to avoid triggering anti-bot measures on Tabelog.

---

## Notes & Troubleshooting

- If the script can't find certain elements, inspect Tabelog's page structure and update selectors in the code (see methods: `get_followers`, `click_like_button_for_follower` in `main.py`).
- You may need to adjust delays in the script if you hit rate limits or experience issues.
- Use responsibly and only if this is in accordance with Tabelog's Terms of Service.

---

## Build the executable with icon

### Console app

```bash
pyinstaller --onefile --icon=app.ico main.py
```

### GUI app (no console window)

```bash
pyinstaller --onefile --noconsole --icon=app.ico main.py
```

