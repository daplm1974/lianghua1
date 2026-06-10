#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyXT[EMOJI] 11 - GUI[EMOJI]
[EMOJI] gui_app [EMOJI]GUI[EMOJI]
[EMOJI]:
  python [EMOJI]/11_GUI[EMOJI].py [--auto] [--run]
  - --auto: [EMOJI]
  - --run: [EMOJI]GUI[EMOJI]
"""

import sys
import os
import subprocess
import shutil
from datetime import datetime

# [EMOJI] Python [EMOJI]
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

GUI_DIR = os.path.join(project_root, "gui_app")
README_PATH = os.path.join(GUI_DIR, "README_Enhanced.md")
MAIN_WINDOW = os.path.join(GUI_DIR, "main_window.py")
SIMPLE_TRADING = os.path.join(GUI_DIR, "trading_interface_simple.py")
BACKTEST_WIDGET = os.path.join(GUI_DIR, "widgets", "backtest_widget.py")
REQUIREMENTS = os.path.join(GUI_DIR, "requirements.txt")

AUTO_MODE = ("--auto" in sys.argv)
RUN_MODE = ("--run" in sys.argv)


def pause():
    if not AUTO_MODE:
        try:
            input("\n[EMOJI]...")
        except KeyboardInterrupt:
            print("\n[EMOJI]")
            sys.exit(0)


def print_header(title: str):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def safe_exists(path: str) -> bool:
    try:
        return os.path.exists(path)
    except Exception:
        return False


def lesson_01_overview():
    """[EMOJI]1[EMOJI]GUI[EMOJI]"""
    print_header("[EMOJI]1[EMOJI]GUI[EMOJI]")
    print("[EMOJI] gui_app [EMOJI]")

    if not safe_exists(GUI_DIR):
        print(f"[X] [EMOJI]: {GUI_DIR}")
        return

    print(f"[OK] [EMOJI]: {GUI_DIR}")

    # [EMOJI]
    key_files = [
        ("[EMOJI]", README_PATH),
        ("[EMOJI]", MAIN_WINDOW),
        ("[EMOJI]", SIMPLE_TRADING),
        ("[EMOJI]", BACKTEST_WIDGET),
        ("[EMOJI]", REQUIREMENTS),
    ]
    for name, path in key_files:
        mark = "[OK]" if safe_exists(path) else "[X]"
        print(f"{mark} {name}: {os.path.relpath(path, project_root)}")

    print("\n[EMOJI]")
    print("- main_window.py: PyQt5 [EMOJI]/[EMOJI]/[EMOJI]/[EMOJI]/[EMOJI]")
    print("- trading_interface_simple.py: [EMOJI]/[EMOJI]/[EMOJI]")
    print("- widgets/backtest_widget.py: [EMOJI]/[EMOJI]/[EMOJI]")
    print("- README_Enhanced.md: [EMOJI]01-10[EMOJI]")
    print("- requirements.txt: GUI[EMOJI]PyQt5[EMOJI]pandas[EMOJI]numpy[EMOJI]matplotlib[EMOJI]pyqtgraph [EMOJI]")

    pause()


def lesson_02_check_dependencies():
    """[EMOJI]2[EMOJI]"""
    print_header("[EMOJI]2[EMOJI]")

    # Python[EMOJI]
    print(f"Python[EMOJI]: {sys.version.split()[0]}")

    # [EMOJI] PyQt5[EMOJI]pandas[EMOJI]numpy[EMOJI]matplotlib[EMOJI]pyqtgraph
    to_check = [
        ("PyQt5", "PyQt5"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("matplotlib([EMOJI])", "matplotlib"),
        ("pyqtgraph([EMOJI])", "pyqtgraph"),
    ]
    for label, mod in to_check:
        try:
            __import__(mod)
            print(f"[OK] [EMOJI]: {label}")
        except Exception:
            print(f"[!] [EMOJI]: {label}")

    if safe_exists(REQUIREMENTS):
        print(f"\n[EMOJI]: {os.path.relpath(REQUIREMENTS, project_root)}")
        print("[EMOJI]:")
        print("  pip install -r gui_app/requirements.txt")
    else:
        print("\n[EMOJI] requirements.txt[EMOJI]:")
        print("  pip install PyQt5 pandas numpy matplotlib pyqtgraph")

    pause()


def _run_gui_script(py_file: str, title: str):
    """[EMOJI] RUN_MODE [EMOJI] GUI [EMOJI]"""
    rel = os.path.relpath(py_file, project_root)
    if not safe_exists(py_file):
        print(f"[X] [EMOJI] {title}: {rel}")
        return

    print(f"[OK] [EMOJI] {title}: {rel}")
    print("[EMOJI]:")
    print(f"  python {rel}")

    if not RUN_MODE:
        print("[EMOJI] --run[EMOJI]")
        return

    # [EMOJI]
    try:
        print("[R] [EMOJI]...")
        creationflags = 0
        # [EMOJI] Windows [EMOJI]subprocess.CREATE_NEW_CONSOLE
        if os.name == "nt" and hasattr(subprocess, "CREATE_NEW_CONSOLE"):
            creationflags = subprocess.CREATE_NEW_CONSOLE

        subprocess.Popen([sys.executable, py_file],
                         cwd=project_root,
                         creationflags=creationflags)
        print("[OK] [EMOJI]")
    except Exception as e:
        print(f"[X] [EMOJI]: {e}")


def lesson_03_launch_main_window():
    """[EMOJI]3[EMOJI] main_window.py"""
    print_header("[EMOJI]3[EMOJI]")
    print("[EMOJI]")
    print("- [EMOJI]/[EMOJI]")
    print("- [EMOJI]/[EMOJI]")
    print("- [EMOJI] [EMOJI] -> [CHART] [EMOJI]")
    print("- EasyXT [EMOJI]")

    _run_gui_script(MAIN_WINDOW, "[EMOJI] (main_window.py)")
    pause()


def lesson_04_launch_simple_trading():
    """[EMOJI]4[EMOJI] trading_interface_simple.py"""
    print_header("[EMOJI]4[EMOJI]")
    print("[EMOJI]/[EMOJI]/[EMOJI]EasyXT[EMOJI]")
    print("[EMOJI]/[EMOJI]/[EMOJI]")

    _run_gui_script(SIMPLE_TRADING, "[EMOJI] (trading_interface_simple.py)")
    pause()


def lesson_05_launch_backtest_widget():
    """[EMOJI]5[EMOJI] widgets/backtest_widget.py"""
    print_header("[EMOJI]5[EMOJI]")
    print("[EMOJI]HTML[EMOJI]")
    print("[EMOJI]DataManager[EMOJI] QMT→QStock→AKShare→[EMOJI]")

    _run_gui_script(BACKTEST_WIDGET, "[EMOJI] (widgets/backtest_widget.py)")
    pause()


def lesson_06_tips_and_troubleshooting():
    """[EMOJI]6[EMOJI]"""
    print_header("[EMOJI]6[EMOJI]")
    print("- [EMOJI]")
    print("  pip install PyQt5 pandas numpy matplotlib pyqtgraph")
    print("- [EMOJI]/[EMOJI]")
    print("- QMT[EMOJI]EasyXT[EMOJI]")
    print("- [EMOJI]")
    print("- [EMOJI] DataManager [EMOJI]")
    print("- Windows[EMOJI]/[EMOJI]")

    print("\n[EMOJI]")
    print("- [EMOJI] main_window [EMOJI] import BacktestWidget [EMOJI]")

    pause()


def main():
    print("[COURSE] GUI[EMOJI]")
    print("[EMOJI] gui_app [EMOJI]")
    print("[EMOJI]--auto [EMOJI]--run [EMOJI]GUI[EMOJI]")

    lessons = [
        lesson_01_overview,
        lesson_02_check_dependencies,
        lesson_03_launch_main_window,
        lesson_04_launch_simple_trading,
        lesson_05_launch_backtest_widget,
        lesson_06_tips_and_troubleshooting,
    ]

    for idx, lesson in enumerate(lessons, 1):
        try:
            lesson()
            if AUTO_MODE:
                print(f"\n[OK] [EMOJI]{idx}[EMOJI]...")
        except KeyboardInterrupt:
            print("\n\n[EMOJI]")
            break
        except Exception as e:
            print(f"\n[EMOJI]: {e}")
            if not AUTO_MODE:
                try:
                    input("[EMOJI]...")
                except KeyboardInterrupt:
                    break

    print("\n[EMOJI] GUI[EMOJI]")
    print("[EMOJI]")
    print("- [EMOJI] --run [EMOJI]")
    print("- [EMOJI] gui_app/README_Enhanced.md [EMOJI]")
    print("- [EMOJI]")


if __name__ == "__main__":
    main()