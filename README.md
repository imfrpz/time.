# FocusTimer: Technical Documentation and Repository Overview

**Project Identity**

* **Name:** FocusTimer
* **Version:** 1.0.0
* **Type:** Desktop GUI Application (Neuro-Performance Tool)
* **Stack:** Python 3.11 / Tkinter / PyInstaller

**Core Functionality**

* **Precision Countdown:** MM:SS input validation with automated parsing.
* **Window Persistence:** Always-on-top positioning at the Top-Center of the screen.
* **Temporal Grounding:** Real-time logging of session start time (`S: HH:MM`).
* **Aesthetic Integration:** Minimalist dark-mode UI optimized for Obsidian/Code-editor environments.

**Neurobiological Stimulation Framework**

| Stimulus | Trigger | Mechanism | Neurochemical Response |
| --- | --- | --- | --- |
| **Red Flash (3px)** | Deadline (00:00) | Peripheral retina activation. | **Norepinephrine** (Urgency) |
| **Green Flash (3px)** | Success (`Ctrl+Enter`) | Visual confirmation of goal. | **Dopamine** (Reinforcement) |
| **Audio Alarm** | Failure/Deadline | 1000Hz frequency (high ear sensitivity). | Cortisol/Adrenaline (Arousal) |
| **Ghost Focus** | Active Mode | Cursor hiding & Read-only state. | Reduced cognitive load/noise. |

**Technical Architecture**

* **Event Loop:** Tkinter mainloop with asynchronous `.after()` task scheduling.
* **CPU Optimization:** <0.1% load via OS-level event queue.
* **Focus Management:** Advanced focus-stealing prevention using `root.focus_set()` on background interaction.
* **Transparency:** `-alpha 0.9` for peripheral visibility without content occlusion.

**Build and Deployment**

* **Source Control:** Git-managed. `.gitignore` active for build artifacts.
* **Packaging:** Single-executable (`--onefile`) with suppressed console (`--noconsole`).
* **Asset Embedding:** Integrated `.ico` for Shell and Taskbar recognition.

**Developer Instructions**

```powershell
# Setup virtual environment
python -m venv venv
.\venv\Scripts\activate
pip install pyinstaller

# Compilation command
pyinstaller --noconsole --onefile --clean --icon=icon.ico --name=FocusTimer main.py

```

**Visual States & Telemetry**

* **S: HH:MM** — Session start time.
![0IdobJqAWS](https://github.com/user-attachments/assets/5c72385d-81da-4315-b50d-f9a848f8e862)
![DGXzgGLQ3J](https://github.com/user-attachments/assets/4ddac5c2-b924-45a3-b486-a0cbed457e73)
* **TASK COMPLETED** — Positive reinforcement display (Success).
![FocusTimer_pATXbcYMkL](https://github.com/user-attachments/assets/8122f633-4a98-404f-b089-2f0baed7dfac)
* **TIME IS UP** — Deadline breach indicator (Danger).
![FocusTimer_VcgotYaRu9](https://github.com/user-attachments/assets/fddbd818-6cc9-4bb5-affc-ae62fa554115)

