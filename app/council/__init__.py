"""LLM Council — owner: k3 (@ramazanhsnylmz).

Karpathy tarzı: birden fazla model bağımsız oy verir, bir başkan sentezler.
Son karar her zaman insanda kalır.
"""

from app.council.deliberate import run_council

__all__ = ["run_council"]
