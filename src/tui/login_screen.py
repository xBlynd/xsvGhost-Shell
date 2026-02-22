"""
Ghost Shell Login Screen — Textual TUI
======================================
Interactive login screen with system stats and menu.
"""

from datetime import datetime
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Label, ListItem, ListView
from textual.containers import Vertical, Horizontal, Center, Container
from textual import on


class StatBlock(Static):
    """A small block displaying a single system statistic."""
    def __init__(self, label: str, value: str, color: str = "white", **kwargs):
        super().__init__(**kwargs)
        self.label_text = label
        self.value_text = value
        self.color = color

    def render(self):
        return f"[b]{self.label_text}:[/b] [{self.color}]{self.value_text}[/]"


class GhostLoginApp(App[str]):
    """Ghost Shell Login Screen — powered by Textual."""

    CSS = """
    Screen {
        background: #0a0a0a;
        align: center middle;
    }

    #main-container {
        width: 80;
        height: 35;
        border: double #00ff00;
        background: #111111;
        padding: 1;
    }

    #banner {
        width: 100%;
        height: auto;
        content-align: center middle;
        margin-bottom: 1;
        color: #00ff00;
        text-style: bold;
    }

    #stats-grid {
        height: auto;
        border: solid #333333;
        margin-bottom: 1;
        padding: 1;
        background: #1a1a1a;
    }

    StatBlock {
        margin: 0 2;
    }

    #menu-label {
        width: 100%;
        content-align: center middle;
        margin-bottom: 1;
        color: #888888;
    }

    #menu {
        width: 40;
        height: auto;
        border: solid #00ff00;
        background: #000000;
    }

    ListItem {
        padding: 1;
    }

    ListItem:hover {
        background: #004400;
    }

    .selected {
        background: #00ff00;
        color: black;
    }

    Footer {
        background: #002200;
        color: #00ff00;
    }
    """

    TITLE = "Ghost Shell Phoenix Login"
    BINDINGS = [
        ("s", "select('shell')", "Enter Shell"),
        ("d", "select('dashboard')", "Dashboard"),
        ("q", "quit_system", "Shutdown"),
    ]

    def __init__(self, kernel, **kwargs):
        super().__init__(**kwargs)
        self.kernel = kernel
        self.result = "shell"  # Default result

    def compose(self) -> ComposeResult:
        interface = self.kernel.get_engine("interface")
        role = "GUEST"
        if self.kernel.engine_available("security"):
            role = self.kernel.engines["security"].current_role
        
        banner_text = interface.get_banner(role) if interface else "GHOST SHELL PHOENIX"

        # Gather stats
        core = self.kernel.get_engine("ghost_core")
        heartbeat = self.kernel.get_engine("heartbeat")
        vault = self.kernel.get_engine("vault")
        loader = self.kernel.get_engine("loader")

        node_id = core.node_id if core else "Unknown"
        uptime = f"{heartbeat.check_health()['uptime_seconds']}s" if heartbeat else "0s"
        
        todo_count = "0"
        if vault:
            todos = vault.todo_list().get("items", [])
            todo_count = str(len(todos))

        cmd_count = str(len(self.kernel.commands))

        yield Header()
        with Container(id="main-container"):
            yield Static(banner_text, id="banner")
            
            with Horizontal(id="stats-grid"):
                yield StatBlock("NODE", node_id, color="cyan")
                yield StatBlock("UPTIME", uptime, color="yellow")
                yield StatBlock("TODOS", todo_count, color="green")
                yield StatBlock("CMDS", cmd_count, color="magenta")

            yield Label("— SYSTEM READY —", id="menu-label")
            
            with Center():
                with ListView(id="menu"):
                    yield ListItem(Label("[S] ENTER GHOST SHELL"), id="shell")
                    yield ListItem(Label("[D] OPEN DASHBOARD"), id="dashboard")
                    yield ListItem(Label("[Q] SYSTEM SHUTDOWN"), id="shutdown")

        yield Footer()

    @on(ListView.Selected)
    def on_selected(self, event: ListView.Selected):
        self.result = event.item.id
        self.exit(self.result)

    def action_select(self, option: str):
        self.result = option
        self.exit(self.result)

    def action_quit_system(self):
        self.result = "shutdown"
        self.exit(self.result)
