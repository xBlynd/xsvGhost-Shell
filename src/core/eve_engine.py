"""
Engine 13: Eve Engine - The Mind
===================================
Multi-tier AI integration with automatic tier detection.
Replaces the Cortex stub with a functional AI layer.

Tier System (from Gemini architecture discussion):
  MICRO:      Phi-3 (3.8B) - fits on USB stick, runs on laptop GPU (RTX 3050)
  PORTABLE:   Mistral 7B - local Ollama on current machine
  MOTHERSHIP: Mistral-Nemo (12B) - desktop powerhouse (i7-8700K + RTX 2070)
              Accessed remotely via Tailscale (100.x.y.z:11434)
  CLOUD:      API fallback (future - OpenAI/Anthropic/etc)

Shadow Loading (USB Portability):
  When running from USB, Eve copies model data to host temp dir
  so the USB isn't thrashed with constant read/write. Cleans up on exit.

Compartmentalization:
- Queries AI providers, returns structured data
- Does NOT format output (InterfaceEngine does that)
- Does NOT store conversation permanently (VaultEngine would do that)
- Uses stdlib only (urllib.request for HTTP, no requests library)
"""

import os
import json
import tempfile
from datetime import datetime


class EveEngine:
    """The Mind - Multi-tier AI integration."""

    ENGINE_NAME = "eve"
    ENGINE_VERSION = "1.0.0"
    OPERATIONAL = True

    # Tier configurations based on Gemini hardware discussion:
    # Desktop: i7-8700K + RTX 2070 (can handle 12B models)
    # Laptop: ASUS Vivobook + RTX 3050 (4-6GB VRAM, use 7B or smaller)
    # USB: Whatever machine you plug into
    TIER_CONFIGS = {
        "micro": {
            "model": "phi3",
            "size_gb": 2.3,
            "use": "USB stick / low-VRAM machines",
            "description": "Microsoft Phi-3 - small but capable",
        },
        "portable": {
            "model": "mistral",
            "size_gb": 4.1,
            "use": "Laptop with dedicated GPU",
            "description": "Mistral 7B - good balance of speed and smarts",
        },
        "mothership": {
            "model": "mistral-nemo",
            "size_gb": 7.0,
            "use": "Desktop powerhouse via Tailscale",
            "description": "Mistral-Nemo 12B - the heavy hitter",
        },
        "cloud": {
            "model": None,
            "size_gb": 0,
            "use": "API fallback when offline isn't an option",
            "description": "Remote API (future)",
        },
    }

    DEFAULT_CONFIG = {
        "active_tier": "auto",
        "ollama_url": "http://localhost:11434",
        "mothership_url": None,          # e.g. "http://100.x.y.z:11434" (Tailscale)
        "cloud_api_key_ref": None,       # Reference to encrypted key in Vault
        "shadow_loading": True,          # Copy model cache to host temp on USB
        "cleanup_on_exit": True,
        "conversation_max_history": 20,
        "system_prompt": None,           # Custom personality/context
        "inject_ghost_context": True,    # Give Eve awareness of Ghost Shell state
    }

    def __init__(self, kernel):
        self.kernel = kernel
        self.root_dir = kernel.root_dir
        self.config_file = os.path.join(self.root_dir, "data", "config", "eve.json")
        self.config = self._load_config()
        self.conversation_history = []
        self.shadow_path = None
        self.active_tier = None

        # Auto-detect best available tier
        self._detect_tier()

        # Shadow loading for USB portability
        core = kernel.get_engine("ghost_core")
        if core and core.is_portable and self.config.get("shadow_loading", True):
            self._init_shadow_loading()

        # Register cleanup on shutdown
        kernel.on("shutdown", lambda data: self._cleanup())

    # =========================================================================
    # CONFIGURATION
    # =========================================================================

    def _load_config(self):
        """Load Eve configuration, merging with defaults."""
        config = dict(self.DEFAULT_CONFIG)
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    config.update(loaded)
            except Exception:
                pass
        return config

    def _save_config(self):
        """Persist Eve configuration."""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    # =========================================================================
    # TIER DETECTION
    # =========================================================================

    def _detect_tier(self):
        """
        Auto-detect the best available AI tier.
        Priority: local Ollama > mothership via Tailscale > offline
        """
        if self.config.get("active_tier") != "auto":
            self.active_tier = self.config["active_tier"]
            return

        # 1. Check local Ollama
        if self._check_ollama(self.config["ollama_url"]):
            self.active_tier = "portable"
            return

        # 2. Check mothership (desktop via Tailscale)
        mothership = self.config.get("mothership_url")
        if mothership and self._check_ollama(mothership):
            self.active_tier = "mothership"
            return

        # 3. Check via Legion for any HIVE_MIND node
        legion = self.kernel.get_engine("legion")
        if legion:
            nodes = legion.list_nodes()
            for node in nodes:
                if node.get("node_type") == "HIVE_MIND" and node.get("address"):
                    url = f"http://{node['address']}:11434"
                    if self._check_ollama(url):
                        self.active_tier = "mothership"
                        self.config["mothership_url"] = url
                        return

        # 4. Fallback
        self.active_tier = "offline"

    def _check_ollama(self, base_url):
        """Check if an Ollama instance is reachable."""
        try:
            import urllib.request
            urllib.request.urlopen(base_url + "/api/tags", timeout=2)
            return True
        except Exception:
            return False

    # =========================================================================
    # SHADOW LOADING (USB Portability)
    # =========================================================================

    def _init_shadow_loading(self):
        """
        Shadow loading: when running from USB, use host temp storage
        for model cache to avoid thrashing the USB drive.
        """
        if os.name == 'nt':
            shadow_base = os.path.join(tempfile.gettempdir(), "ghost_eve_shadow")
        else:
            shadow_base = "/tmp/ghost_eve_shadow"

        self.shadow_path = shadow_base
        os.makedirs(shadow_base, exist_ok=True)

    def _cleanup(self):
        """Cleanup shadow cache on shutdown if configured."""
        if self.shadow_path and self.config.get("cleanup_on_exit", True):
            try:
                import shutil
                if os.path.exists(self.shadow_path):
                    shutil.rmtree(self.shadow_path)
            except Exception:
                pass

    # =========================================================================
    # AI INTERFACE
    # =========================================================================

    def ask(self, prompt, context=None):
        """
        Send a prompt to the best available AI provider.
        Returns structured data: {"response": str, "tier": str} or {"error": str}
        """
        if self.active_tier == "offline":
            return {
                "response": None,
                "error": "No AI provider available.",
                "hint": "Install Ollama (ollama.ai) and run: ollama pull mistral",
            }

        # Determine which URL to use
        if self.active_tier == "mothership" and self.config.get("mothership_url"):
            base_url = self.config["mothership_url"]
            model = self.TIER_CONFIGS["mothership"]["model"]
        else:
            base_url = self.config["ollama_url"]
            model = self.TIER_CONFIGS.get(self.active_tier, {}).get("model", "mistral")

        # Build the prompt with optional Ghost Shell context
        full_prompt = prompt
        if self.config.get("inject_ghost_context", True):
            ctx = self._build_ghost_context()
            if ctx:
                full_prompt = f"[System context: {ctx}]\n\n{prompt}"

        # Query
        try:
            response = self._query_ollama(base_url, model, full_prompt)

            # Track conversation
            self.conversation_history.append({
                "role": "user", "content": prompt,
                "timestamp": datetime.now().isoformat(),
            })
            self.conversation_history.append({
                "role": "assistant", "content": response,
                "timestamp": datetime.now().isoformat(),
            })

            # Trim history
            max_hist = self.config.get("conversation_max_history", 20)
            if len(self.conversation_history) > max_hist:
                self.conversation_history = self.conversation_history[-max_hist:]

            return {"response": response, "tier": self.active_tier, "model": model}

        except Exception as e:
            return {"response": None, "error": str(e)}

    def _query_ollama(self, base_url, model, prompt):
        """Query an Ollama API endpoint. Uses stdlib only."""
        import urllib.request

        url = base_url.rstrip("/") + "/api/generate"
        data = json.dumps({
            "model": model,
            "prompt": prompt,
            "stream": False,
        }).encode("utf-8")

        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"},
        )

        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "")

    def _build_ghost_context(self):
        """Build system context string so Eve knows about Ghost Shell state."""
        parts = []
        core = self.kernel.get_engine("ghost_core")
        if core:
            parts.append(f"OS={core.os_type}")
            parts.append(f"host={core.hostname}")

        sec = self.kernel.get_engine("security")
        if sec:
            parts.append(f"role={sec.current_role}")

        parts.append(f"engines={len(self.kernel.engines)}")
        parts.append(f"commands={len(self.kernel.commands)}")
        return ", ".join(parts) if parts else None

    # =========================================================================
    # CONFIGURATION COMMANDS
    # =========================================================================

    def set_mothership(self, url):
        """Set the mothership (desktop) Ollama URL."""
        self.config["mothership_url"] = url
        self._save_config()
        # Re-detect tier
        self._detect_tier()
        return {"status": "ok", "mothership_url": url, "active_tier": self.active_tier}

    def set_tier(self, tier):
        """Manually set the active tier."""
        valid = list(self.TIER_CONFIGS.keys()) + ["auto"]
        if tier not in valid:
            return {"error": f"Invalid tier. Choose from: {', '.join(valid)}"}
        self.config["active_tier"] = tier
        self._save_config()
        self._detect_tier()
        return {"status": "ok", "active_tier": self.active_tier}

    # =========================================================================
    # STATUS
    # =========================================================================

    def get_status(self):
        """Return Eve engine status."""
        ollama_local = self._check_ollama(self.config["ollama_url"])
        mothership_url = self.config.get("mothership_url")
        ollama_remote = self._check_ollama(mothership_url) if mothership_url else False

        return {
            "operational": self.OPERATIONAL,
            "active_tier": self.active_tier,
            "configured_tier": self.config.get("active_tier", "auto"),
            "ollama_local": ollama_local,
            "ollama_url": self.config["ollama_url"],
            "mothership_url": mothership_url,
            "mothership_available": ollama_remote,
            "shadow_loading": self.config.get("shadow_loading", False),
            "shadow_path": self.shadow_path,
            "conversation_length": len(self.conversation_history),
            "version": self.ENGINE_VERSION,
        }
