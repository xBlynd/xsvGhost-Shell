"""
Engine 12: Legion Engine - The Hive
======================================
Multi-device mesh coordination. One Ghost Shell becomes many.

STATUS: OPERATIONAL (Phase 1 - HTTP messaging via Tailscale)

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
│                  │(Eve AI) │                    │
│                  └──────────┘                    │
└─────────────────────────────────────────────────┘

Node Types:
- MASTER:       Command center. Issues orders, sees all nodes.
- LEGIONNAIRE:  Worker node. Receives and executes commands.
- HIVE_MIND:    AI node. Runs Eve engine, responds to queries.

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
    ENGINE_VERSION = "1.0.0"
    OPERATIONAL = True  # Phase 1: HTTP messaging

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

    def send_message(self, message, target_address=None):
        """
        Send a message to another node via HTTP.
        Phase 1: Simple JSON POST over Tailscale VPN.
        Falls back to store-and-forward if unreachable.
        """
        if not target_address:
            # Look up address from node registry
            to_node = message.get("to_node")
            if to_node and to_node != "*" and to_node in self.known_nodes:
                target_address = self.known_nodes[to_node].get("address")

        if not target_address:
            # Queue for later via SyncEngine
            sync = self.kernel.get_engine("sync")
            if sync:
                sync.queue_operation("legion_message", message)
                return {"status": "queued", "reason": "No address for target node"}
            return {"status": "failed", "reason": "No address and SyncEngine unavailable"}

        # Attempt HTTP delivery
        try:
            import urllib.request
            import json as _json

            url = f"http://{target_address}/ghost/message"
            data = _json.dumps(message).encode("utf-8")
            req = urllib.request.Request(
                url, data=data,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"status": "delivered", "response": resp.read().decode()}
        except Exception as e:
            # Delivery failed - queue for retry
            sync = self.kernel.get_engine("sync")
            if sync:
                sync.queue_operation("legion_message", message)
            return {"status": "queued", "reason": f"Delivery failed: {e}"}

    def broadcast(self, message_type, payload):
        """Broadcast a message to all known nodes."""
        msg = self.create_message("*", message_type, payload)
        results = {}
        for nid, info in self.known_nodes.items():
            if nid == self.node_id:
                continue  # Don't broadcast to self
            addr = info.get("address")
            if addr:
                results[nid] = self.send_message(msg, addr)
        return results

    # =========================================================================
    # REMOTE OPERATIONS
    # =========================================================================

    def query_remote_eve(self, node_id, prompt):
        """
        Query Eve AI on a remote node.
        Use case: Laptop sends heavy query to desktop mothership.
        """
        if node_id not in self.known_nodes:
            return {"error": f"Unknown node: {node_id}"}

        msg = self.create_message(node_id, "QUERY", {
            "type": "eve_ask",
            "prompt": prompt,
        })
        address = self.known_nodes[node_id].get("address")
        return self.send_message(msg, address)

    def execute_remote(self, node_id, command, args=""):
        """
        Execute a Ghost Shell command on a remote node.
        Use case: Fix grandma's PC from your couch.
        """
        if node_id not in self.known_nodes:
            return {"error": f"Unknown node: {node_id}"}

        msg = self.create_message(node_id, "COMMAND", {
            "command": command,
            "args": args,
        })
        address = self.known_nodes[node_id].get("address")
        return self.send_message(msg, address)

    def find_mothership(self):
        """
        Locate the mothership (most powerful node) in the mesh.
        Returns node info or None.
        """
        for nid, info in self.known_nodes.items():
            if info.get("node_type") in ("MASTER", "HIVE_MIND"):
                info_copy = dict(info)
                info_copy["node_id"] = nid
                return info_copy
        return None

    # =========================================================================
    # STATUS
    # =========================================================================

    def get_status(self):
        """Return Legion engine status."""
        mothership = self.find_mothership()
        return {
            "operational": self.OPERATIONAL,
            "node_id": self.node_id,
            "node_type": self.node_type,
            "known_nodes": len(self.known_nodes),
            "mothership": mothership.get("node_id") if mothership else None,
            "version": self.ENGINE_VERSION,
            "phase": "Phase 1 - HTTP messaging via Tailscale",
        }
