"""
Engine 12: Legion Engine - The Hive
======================================
Multi-device mesh coordination. One Ghost Shell becomes many.

STATUS: STUB - Architecture defined, not yet operational.

Architecture Overview:
┌─────────────────────────────────────────────────┐
│                  LEGION MESH                     │
│                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  MASTER   │◄──►│LEGIONNAIRE│◄──►│LEGIONNAIRE│  │
│  │ (Your PC) │    │ (Laptop)  │    │(Grandma's)│  │
│  └──────────┘    └──────────┘    └──────────┘  │
│       ▲                                          │
│       │          ┌──────────┐                    │
│       └─────────►│ HIVE_MIND│                    │
│                  │(Cortex AI)│                    │
│                  └──────────┘                    │
└─────────────────────────────────────────────────┘

Node Types:
- MASTER:       Command center. Issues orders, sees all nodes.
- LEGIONNAIRE:  Worker node. Receives and executes commands.
- HIVE_MIND:    AI node. Runs Cortex engine, responds to queries.

Communication:
- Phase 1: JSON over HTTP (simple, works through Tailscale VPN)
- Phase 2: WebSocket for real-time (persistent connection)
- Phase 3: gRPC for performance (binary protocol)

Protocol:
  Every message is a GhostMessage:
  {
      "from_node": "ghost-abc123",
      "to_node": "ghost-def456",     # or "*" for broadcast
      "message_type": "COMMAND|QUERY|RESPONSE|HEARTBEAT|REGISTER",
      "payload": { ... },
      "timestamp": "2026-02-12T...",
      "signature": "hmac-sha256-...", # Authenticated messages
  }

Future Integration:
- Tailscale for VPN mesh (100.x.y.z addresses)
- mDNS for local network discovery
- Store-and-forward when nodes are offline (SyncEngine)
"""

import os
import json
from datetime import datetime


class LegionEngine:
    """The Hive - multi-device mesh coordination."""

    ENGINE_NAME = "legion"
    ENGINE_VERSION = "0.1.0-stub"
    OPERATIONAL = False  # Not yet functional

    def __init__(self, kernel):
        self.kernel = kernel
        self.root_dir = kernel.root_dir
        self.legion_dir = os.path.join(self.root_dir, "data", "legion")
        self.known_nodes = {}
        self.node_id = None
        self.node_type = "MASTER"

        os.makedirs(self.legion_dir, exist_ok=True)

        # Load our node identity from GhostCore
        core = kernel.get_engine("ghost_core")
        if core:
            self.node_id = core.node_id
            self.node_type = core.node_type

        # Load known nodes registry
        self._load_node_registry()

    # =========================================================================
    # NODE REGISTRY
    # =========================================================================

    def _load_node_registry(self):
        """Load the registry of known Legion nodes."""
        reg_file = os.path.join(self.legion_dir, "nodes.json")
        if os.path.exists(reg_file):
            try:
                with open(reg_file, 'r') as f:
                    self.known_nodes = json.load(f)
            except Exception:
                self.known_nodes = {}

    def _save_node_registry(self):
        """Save the node registry."""
        reg_file = os.path.join(self.legion_dir, "nodes.json")
        with open(reg_file, 'w') as f:
            json.dump(self.known_nodes, f, indent=2)

    def register_node(self, node_id, node_type, address, label=None):
        """
        Register a node in the mesh.
        Future: This would be called during handshake protocol.
        """
        self.known_nodes[node_id] = {
            "node_type": node_type,
            "address": address,
            "label": label or node_id,
            "first_seen": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat(),
            "status": "registered",
        }
        self._save_node_registry()
        return self.known_nodes[node_id]

    def list_nodes(self):
        """List all known nodes."""
        nodes = []
        for nid, info in self.known_nodes.items():
            info_copy = dict(info)
            info_copy["node_id"] = nid
            info_copy["is_self"] = (nid == self.node_id)
            nodes.append(info_copy)
        return nodes

    # =========================================================================
    # MESSAGE PROTOCOL (Placeholder)
    # =========================================================================

    def create_message(self, to_node, message_type, payload):
        """
        Create a GhostMessage for the mesh protocol.
        Future: will be sent over HTTP/WebSocket/gRPC.
        """
        return {
            "from_node": self.node_id,
            "to_node": to_node,
            "message_type": message_type,
            "payload": payload,
            "timestamp": datetime.now().isoformat(),
            "version": self.ENGINE_VERSION,
        }

    def send_message(self, message):
        """
        Send a message to another node.
        STUB: Currently just queues for store-and-forward.
        """
        # Future: HTTP POST to node address
        # For now: queue via SyncEngine
        sync = self.kernel.get_engine("sync")
        if sync:
            sync.queue_operation("legion_message", message)
            return {"status": "queued", "message": "Legion not yet operational. Message queued."}
        return {"status": "failed", "message": "SyncEngine unavailable"}

    def broadcast(self, message_type, payload):
        """Broadcast a message to all known nodes."""
        msg = self.create_message("*", message_type, payload)
        return self.send_message(msg)

    # =========================================================================
    # STATUS
    # =========================================================================

    def get_status(self):
        """Return Legion engine status."""
        return {
            "operational": self.OPERATIONAL,
            "node_id": self.node_id,
            "node_type": self.node_type,
            "known_nodes": len(self.known_nodes),
            "version": self.ENGINE_VERSION,
            "message": "Legion Mode is stubbed. Architecture ready for implementation.",
        }
