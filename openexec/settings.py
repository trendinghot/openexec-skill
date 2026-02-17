import os

MODE = os.getenv("OPENEXEC_MODE", "demo")

def is_demo():
    return MODE == "demo"

def is_clawshield():
    return MODE == "clawshield"
