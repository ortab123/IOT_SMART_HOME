# Smart AC IoT System

A simulated IoT-based smart air conditioning system developed in Python as a final project for an IoT course.

---

## 📦 Project Overview

This system simulates a smart air conditioner with the ability to:

- Collect temperature and motion data from virtual sensors (emulators)
- Automatically control the AC based on predefined logic
- Switch between manual and automatic modes
- Display data and status via a real-time GUI
- Log all data in a local SQLite database

---

## 🧩 System Architecture

- **Data Producers (Emulators)**:
  - `temperature_emulator.py` — generates temperature data
  - `motion_emulator.py` — generates motion detection data
- **Actuators**:
  - `manual_button.py` — allows manual control (ON/OFF)
  - `relay_emulator.py` — displays current AC status based on server
- **Data Manager (Server)**:
  - `server.py` — collects data, stores it, processes logic, and handles alerts
- **Database**:
  - `ac_data.db` — SQLite file storing all sensor events
- **GUI**:
  - `main_gui.py` — displays current temperature, motion, AC status, mode, and alerts

---

## ⚙️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/smart-ac-project.git
   cd smart-ac-project
   ```
