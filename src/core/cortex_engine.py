"""
Engine 13: Cortex Engine - The Mind
======================================
AI integration layer. Eventually connects Ghost Shell to local AI models
(Ollama, LM Studio) or remote AI services.

STATUS: STUB - Architecture defined, not yet operational.

Architecture Overview:
┌─────────────────────────────────────────────────────┐
│                   CORTEX LAYER                       │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │              CORTEX ENGINE                    │   │
│  │                                               │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐      │   │
│  │  │ Provider │  │ Provider │  │ Provider │      │   │
│  │  │  LOCAL   │  │  REMOTE  │  │  LEGION  │      │   │
│  │  │ (Ollama) │  │  (API)   │  │(Hive AI) │      │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘      │   │
│  │       │              │              │             │   │
│  │       └──────────────┴──────────────┘             │   │
│  │                      │                            │   │
│  │              ┌───────▼────────┐                   │   │
│  │              │  AI ROUTER     │                   │   │
│  │              │ (picks best    │                   │   │
│  │              │  provider)     │                   │   │
│  │              └───────┬────────┘                   │   │
│  │                      │                            │   │
│  │              ┌───────▼────────┐                   │   │
│  │              │  CONTEXT MGR   │                   │   │
│  │              │ (memory, state │                   │   │
│  │              │  persona)      │                   │   │
│  │              └────────────────┘                   │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘

Provider Strategy:
1. LOCAL:   Ollama/LM Studio running on this machine or LAN
            HTTP POST to http://localhost:11434/api/generate
            Best for: privacy, speed on powerful hardware, no internet needed

2. REMOTE:  Cloud AI APIs (OpenAI, Anthropic, etc.)
            Requires API key stored in Vault (encrypted)
            Best for: complex tasks, when local isn't available

3. LEGION:  AI running on another node in the mesh (HIVE_MIND node)
            Routed through LegionEngine
            Best for: offloading to a powerful desktop from a phone/laptop

Context Manager:
- Maintains conversation history per session
- Can inject system context (current OS, loaded engines, user role)
- Future: persona system (Ghost Shell AI has a personality)
- Future: RAG over Vault data (AI knows your journal entries)

Commands:
  xsv ask "Write me a bash script to backup /home"
  xsv chat                           (interactive AI chat)
  xsv cortex status                  (show AI provider status)
  xsv cortex provider local          (switch to local AI)
"""

import os
import json
from datetime import datetime


class CortexEngine:
    """The Mind - AI integration layer."""

    ENGINE_NAME = "cortex"
    ENGINE_VERSION = "0.1.0-stub"
    OPERATIONAL = False  # Not yet functional

    # Provider configuration defaults
    DEFAULT_CONFIG = {
        "active_provider": None,  # None until configured
        "providers": {
            "local": {
                "type": "ollama",
                "url": "http://localhost:11434",
                "model": "mistral",
                "enabled": False,
            },
            "remote": {
                "type": "api",
                "url": None,
                "model": None,
                "api_key_ref": None,  # Reference to encrypted key in Vault
                "enabled": False,
            },
            "legion": {
                "type": "hive",
                "node_id": None,     # HIVE_MIND node in Legion mesh
                "enabled": False,
            },
        },
        "context": {
            "max_history": 20,       # Messages to retain in conversation
            "system_prompt": None,   # Custom system prompt
            "inject_context": True,  # Include OS/engine info in prompts
        },
        "persona": {
            "name": "Ghost",
            "personality": "A knowledgeable, efficient AI assistant integrated into Ghost Shell. Direct, technical, slightly sardonic.",
        },
    }

    def __init__(self, kernel):
        self.kernel = kernel
        self.root_dir = kernel.root_dir
        self.config_file = os.path.join(self.root_dir, "data", "config", "cortex.json")
        self.config = self._load_config()
        self.conversation_history = []

    def _load_config(self):
        """Load Cortex configuration."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return dict(self.DEFAULT_CONFIG)

    def _save_config(self):
        """Save Cortex configuration."""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    # =========================================================================
    # AI INTERFACE (Stubs)
    # =========================================================================

    def ask(self, prompt, context=None):
        """
        Send a prompt to the active AI provider.
        STUB: Returns placeholder until a provider is configured.
        """
        if not self.OPERATIONAL:
            return {
                "response": None,
                "error": "Cortex is not yet operational. Configure an AI provider first.",
                "hint": "Future: `xsv cortex setup` to configure Ollama or API access.",
            }

        # Future implementation:
        # 1. Build context (system prompt + conversation history + user prompt)
        # 2. Route to active provider
        # 3. Parse response
        # 4. Update conversation history
        # 5. Return response
        return {"response": None, "error": "Not implemented"}

    def chat_start(self):
        """Start an interactive chat session."""
        self.conversation_history = []
        return {"status": "Chat session started", "operational": self.OPERATIONAL}

    def chat_message(self, message):
        """Send a message in the current chat session."""
        self.conversation_history.append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat(),
        })
        return self.ask(message)

    # =========================================================================
    # CONTEXT MANAGEMENT
    # =========================================================================

    def build_system_context(self):
        """
        Build the system context that gets injected into AI prompts.
        This gives the AI awareness of the Ghost Shell environment.
        """
        context = {
            "system": "Ghost Shell Phoenix v6.0",
            "os": None,
            "role": None,
            "engines_loaded": [],
            "commands_available": [],
        }

        core = self.kernel.get_engine("ghost_core")
        if core:
            context["os"] = core.os_type
            context["hostname"] = core.hostname

        sec = self.kernel.get_engine("security")
        if sec:
            context["role"] = sec.current_role

        context["engines_loaded"] = [
            name for name, eng in self.kernel.engines.items()
            if eng is not None
        ]
        context["commands_available"] = list(self.kernel.commands.keys())

        return context

    # =========================================================================
    # PROVIDER MANAGEMENT
    # =========================================================================

    def set_provider(self, provider_name, **kwargs):
        """Configure an AI provider."""
        if provider_name not in self.config["providers"]:
            return {"error": f"Unknown provider: {provider_name}"}

        provider = self.config["providers"][provider_name]
        for key, value in kwargs.items():
            if key in provider:
                provider[key] = value

        provider["enabled"] = True
        self.config["active_provider"] = provider_name
        self._save_config()

        return {"status": f"Provider '{provider_name}' configured", "config": provider}

    # =========================================================================
    # STATUS
    # =========================================================================

    def get_status(self):
        """Return Cortex engine status."""
        return {
            "operational": self.OPERATIONAL,
            "active_provider": self.config.get("active_provider"),
            "providers": {
                name: {
                    "type": p.get("type"),
                    "enabled": p.get("enabled", False),
                }
                for name, p in self.config.get("providers", {}).items()
            },
            "conversation_length": len(self.conversation_history),
            "version": self.ENGINE_VERSION,
            "message": "Cortex is stubbed. Architecture ready for AI integration.",
        }
