"""
Ghost Shell Entry Screen — Multi-Tab TUI
=========================================
A professional, app-like entry point for Ghost Shell.
"""

from datetime import datetime
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button, Label, TabbedContent, TabPane
from textual.containers import Vertical, Horizontal, Center, Container
from textual import on, work
from rich.panel import Panel
from rich.text import Text

class FrozenHeader(Static):
    """The persistent top section showing Logo and Stats."""
    
    def __init__(self, kernel, **kwargs):
        super().__init__(**kwargs)
        self.kernel = kernel

    def on_mount(self):
        self.set_interval(1, self.refresh)

    def render(self):
        core = self.kernel.get_engine("ghost_core")
        heartbeat = self.kernel.get_engine("heartbeat")
        vault = self.kernel.get_engine("vault")
        
        node_id = core.node_id if core else "Unknown"
        uptime = f"{heartbeat.check_health()['uptime_seconds']}s" if heartbeat else "0s"
        todo_count = str(len(vault.todo_list().get("items", []))) if vault else "0"
        cmd_count = str(len(self.kernel.commands))

        # Use Hex Codes directly to avoid Style errors
        GHOST = "#00ff00"
        INFO = "#00ffff"

        logo_text = (
            "   ╔═══════════════════════════════════════════════════╗\n"
            "   ║        G H O S T   S H E L L   P H O E N I X      ║\n"
            "   ║                  v6.5 - Phoenix                   ║\n"
            "   ╚═══════════════════════════════════════════════════╝"
        )
        
        stats_line = (
            f" [bold {GHOST}]NODE:[/] [bold {INFO}]{node_id}[/]  |  "
            f"[bold {GHOST}]UPTIME:[/] [bold {INFO}]{uptime}[/]  |  "
            f"[bold {GHOST}]TODOS:[/] [bold {INFO}]{todo_count}[/]  |  "
            f"[bold {GHOST}]CMDS:[/] [bold {INFO}]{cmd_count}[/]"
        )
        
        full_text = f"[{GHOST}]{logo_text}[/]\n\n{stats_line}"
        
        return Panel(
            Text.from_markup(full_text),
            border_style=GHOST,
            padding=(1, 2),
            title=f"[bold {GHOST}] SYSTEM CORE READY [/]",
            title_align="center"
        )

class GhostEntryApp(App[str]):
    """The official 'Front Door' of Ghost Shell Phoenix."""

    CSS = """
    Screen {
        background: #0a0a0a;
    }

    FrozenHeader {
        height: 12;
        margin: 1 2;
    }

    #body-container {
        height: 1fr;
        margin: 0 4;
        border: solid #333333;
        background: #111111;
    }

    TabPane {
        padding: 2 4;
        align: center middle;
    }

    Input {
        width: 40;
        margin-bottom: 1;
        border: tall #00ff00;
    }

    Button {
        width: 40;
        margin-top: 1;
    }

    .tab-label {
        text-style: bold;
        color: #00ff00;
        margin-bottom: 1;
    }

    #shutdown-btn {
        background: #440000;
        color: white;
    }
    """

    TITLE = "Ghost Shell Phoenix Entry"
    BINDINGS = [
        ("q", "quit_app", "Quit"),
        ("tab", "next_tab", "Next Tab"),
    ]

    def __init__(self, kernel, **kwargs):
        super().__init__(**kwargs)
        self.kernel = kernel
        self.result = "exit"

    def compose(self) -> ComposeResult:
        yield FrozenHeader(self.kernel)
        with Container(id="body-container"):
            with TabbedContent():
                with TabPane("LOGIN", id="login-tab"):
                    yield Label("ENTER MASTERKEY", classes="tab-label")
                    yield Input(placeholder="Passphrase...", password=True, id="pass-input")
                    yield Button("AUTHENTICATE", variant="success", id="auth-btn")
                
                with TabPane("GUEST", id="guest-tab"):
                    yield Label("GUEST ACCESS MODE", classes="tab-label")
                    yield Label("[dim]Read-only access to system tools and network diagnostics.[/dim]\n")
                    yield Button("ENTER AS GUEST", variant="primary", id="guest-btn")
                
                with TabPane("SETTINGS", id="settings-tab"):
                    yield Label("SYSTEM PREFERENCES", classes="tab-label")
                    yield Label("UI Mode: [#00ff00]RICH (Textual)[/]")
                    yield Label("Log Level: [#00ffff]DEBUG[/]")
                    yield Label("\n[dim]Settings persist to data/config/settings.json[/dim]")
                
                with TabPane("SHUTDOWN", id="exit-tab"):
                    yield Label("TERMINATE SESSION", classes="tab-label")
                    yield Button("SHUTDOWN GHOST SHELL", id="shutdown-btn")
        
        yield Footer()

    @on(Button.Pressed, "#auth-btn")
    def handle_auth(self):
        password = self.query_one("#pass-input", Input).value
        security = self.kernel.get_engine("security")
        
        # Check against god.key
        import os, json
        god_key_path = os.path.join(self.kernel.root_dir, "data", "keys", "god.key")
        if os.path.exists(god_key_path):
            with open(god_key_path, 'r') as f:
                key_data = json.load(f)
            
            if security.validate_passphrase(password, key_data):
                self.result = "login_success"
                self.exit(self.result)
            else:
                self.notify("Access Denied: Incorrect Passphrase", severity="error")
        else:
            self.notify("Error: God Key not found", severity="error")

    @on(Button.Pressed, "#guest-btn")
    def handle_guest(self):
        self.result = "guest_success"
        self.exit(self.result)

    @on(Button.Pressed, "#shutdown-btn")
    def handle_shutdown(self):
        self.result = "shutdown"
        self.exit(self.result)

    def action_quit_app(self):
        self.exit("exit")

    def action_next_tab(self):
        """Cycle through tabs with the Tab key."""
        tc = self.query_one(TabbedContent)
        # Simple cycle logic
        pass
