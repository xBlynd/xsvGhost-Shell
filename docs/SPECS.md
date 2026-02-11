<!-- DOCUMENT IS INCOMPLETE!!!!!!!!!!!!!!!!!!!!!!  Just a skeleton to work off of..... -->


# ⚙️ Technical Specifications & Snippets

**Purpose:** Repository for code snippets, registry keys, and library requirements.

## 1. Network / BlackBox
* **Jitter Logging:**
    * Use `subprocess.Popen(['ping', target])`. Parse `time=XXms`.
    * Calculate Variance over 100 samples.
* **Incognito Search:**
    * Use `requests` with randomized `User-Agent`.
    * Tor Proxy (SOCKS5) if available on port 9050.

## 2. System / Root
* **Trace Wiping (Windows):**
    * Event Logs: `wevtutil cl "Windows-System"`, `wevtutil cl "Security"`
    * Prefetch: `Del C:\Windows\Prefetch\*` (Requires Admin)
* **Notifications:**
    * Linux: `subprocess.run(['notify-send', title, msg])` (Check `shutil.which('notify-send')`)
    * Windows: PowerShell BurntToast or `WScript.Shell` Balloon.

## 3. Security / Ghost
* **Encryption:**
    * Algo: AES-256 (Fernet).
    * Key Storage: RAM ONLY. Never write key to disk.
* **Timestomping:**
    * Use `os.utime(path, (access_time, mod_time))` to match System32 folder times.

## 4. Data / Vault
* **Journal Search:**
    * Recursive grep: `glob.glob('data/vault/**/*.md')`.
    * Return format: `[File] [Line#] Context`