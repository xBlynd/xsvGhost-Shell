import os
from typing import Any


class BlackBoxEngine:
    """The Shadow Network.

    Phoenix base:
    - OS-aware ping + RTT parsing
    - Jitter calculation
    - CSV logging hooks into data/logs/
    """

    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel

    def ping(self, host: str, count: int = 10) -> dict:
        """Run OS ping and compute basic jitter stats.

        Returns a dict with raw samples and stats so commands can
        render however they like.
        """
        from core.root_engine import RootEngine  # avoid cycles

        root = self.kernel.get_engine("root")
        if not isinstance(root, RootEngine):
            raise RuntimeError("RootEngine not available for ping")

        is_windows = self.kernel.os_type == "windows"
        count_flag = "-n" if is_windows else "-c"
        cmd = ["ping", count_flag, str(count), host]
        res = root.run_subprocess(cmd)

        lines = (res.stdout or res.stderr or "").splitlines()
        rtts = []
        for line in lines:
            line = line.strip()
            if "time=" in line.lower():
                # windows: time=23ms, *nix: time=23.4 ms
                try:
                    part = line.lower().split("time=")[-1]
                    num = "".join(ch for ch in part if (ch.isdigit() or ch == "."))
                    if num:
                        rtts.append(float(num))
                except Exception:
                    continue

        stats = {"samples": rtts}
        if rtts:
            import statistics as _st

            stats["min"] = min(rtts)
            stats["max"] = max(rtts)
            stats["avg"] = sum(rtts) / len(rtts)
            if len(rtts) > 1:
                stats["jitter"] = float(_st.pstdev(rtts))
            else:
                stats["jitter"] = 0.0

        # Hook: write CSV log via VaultEngine (jitter forensic logs)
        try:
            vault = self.kernel.get_engine("vault")
            if vault is not None and hasattr(vault, "save_text") and rtts:
                rows = ["rtt_ms"] + [str(v) for v in rtts]
                content = "\n".join(rows)
                vault.save_text("logs", f"ping_{host}", content)
        except Exception:
            # logging failure must not kill shell
            pass

        stats["raw_output"] = res.stdout or res.stderr or ""
        return stats
