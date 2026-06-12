# Football Analytics Hub (xInfo-Automation)

A Streamlit-based web application designed for interactive football play analysis, video synchronization, and timeline creation. The app allows users to toggle between different phases of a play (Pre-Snap, Post-Snap), view live expected metrics, and edit timestamps that save directly back to the source Excel files.

## Prerequisites

Before running the application, ensure you have Python installed on your machine along with the required libraries. 

You can install the Python dependencies by running:
```bash
pip install streamlit pandas openpyxl altair
```

*Note: For the isolated video clipping feature to work, you must also have [FFmpeg](https://ffmpeg.org/download.html) installed and added to your system's PATH.*

## How to Run the App

1. Open your terminal and navigate to the project directory:
   ```bash
   cd path/to/xInfo-Automation
   ```
2. Launch the Streamlit application by running the `Home.py` file:
   ```bash
   streamlit run Home.py
   ```
3. The app will automatically open in your default web browser (usually at `http://localhost:8501`).

## How to Add New Files

The app automatically scans the root directory for available video and data files to populate the dropdown menus on the Home page.

### 1. Adding Videos
Simply drop any `.mp4` video files directly into the main project folder.

### 2. Adding Excel Data
Drop your `.xlsx` files into the main project folder.

**Formatting Rules:** For the application to read the data correctly, the Excel file must meet the following criteria:
* It must contain a sheet exactly named `Subset_TimeStamps`.
* The sheet must include the timeline columns: `PRE_SNAP` and `POST_SNAP` (or `TIME`/`TIME_A`/`TIME_B` depending on the specific module being used).
* The sheet must include the play identifier column: `PLAY_UNIQUE_ID`.
* Column headers are case-insensitive (the app will auto-capitalize them), but the spelling must match the app's logic (e.g., `HOME_SCORE`, `AWAY_SCORE`, `DOWN`, `DISTANCE`, `EVENT_NAME`).

---

## File Structure & Page Explanations

### Core Application
* **`Home.py`**
  The main entry point and global settings dashboard. It scans the directory for compatible `.mp4` and `.xlsx` files and allows the user to select the active video and data source for the entire session. It acts as the navigation hub for the rest of the application.

* **`pages/Phase_Timeline_Creator.py`**
  The primary, updated workspace for two-phase video playback (Pre-Snap and Post-Snap). This page features a dynamic HTML scoreboard banner, an expected metrics dashboard, and full 22-player offensive/defensive roster displays. It includes an interactive data editor for logging timestamps that safely saves changes directly back to the source Excel workbook using `openpyxl`.

### Alternative & Specialized Modules
* **`Timeline_Creator.py`**
  A robust timeline creation workspace tailored for datasets using single or dual-camera angles (`TIME` or `TIME_A`/`TIME_B`). It features full video playback and visualizes logged events using an interactive Altair bar chart timeline.

* **`Viewer.py`**
  An interactive video isolation tool. Rather than playing the full video, this module reads logged timestamps and utilizes `ffmpeg` to automatically slice and generate temporary, isolated `.mp4` clips for the exact duration of a selected play. 

### Utilities
* **`prep_data.py`**
  A backend data-wrangling script used to format raw tracking data before importing it into the Streamlit app. It ingests a raw game CSV, filters for specific quarters, sorts by Play ID, isolates the necessary columns, and outputs a mathematically clean `.xlsx` file containing the required `Subset_TimeStamps` sheet.
