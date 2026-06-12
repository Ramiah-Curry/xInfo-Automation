import cv2
import pandas as pd
import os

# --- Configuration Variables ---
VIDEO_FILE = '2025-Philadelphia-V-Dallas.mp4'
EXCEL_FILE = 'cd_football_events_2879178-timestamps.xlsx'
OUTPUT_FOLDER = 'Phil-Dal-Screenshots'
SHEET_NAME = 'Subset_TimeStamps'

def extract_frames():
    # 1. Create the output folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created output folder: '{OUTPUT_FOLDER}'")

    # 2. Read the Excel file
    print(f"Reading data from {EXCEL_FILE}...")
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Standardize column names to uppercase to avoid case-sensitivity errors
    df.columns = df.columns.str.upper()

    # Check if required columns exist
    if 'POST_SNAP' not in df.columns or 'PLAY_UNIQUE_ID' not in df.columns:
        print("Error: Excel file must contain both 'POST_SNAP' and 'PLAY_UNIQUE_ID' columns.")
        return

    # 3. Clean the data (Drop rows where POST_SNAP or PLAY_UNIQUE_ID is missing)
    valid_plays = df.dropna(subset=['POST_SNAP', 'PLAY_UNIQUE_ID']).copy()

    # 4. Open the video file
    cap = cv2.VideoCapture(VIDEO_FILE)
    if not cap.isOpened():
        print(f"Error: Could not open video file {VIDEO_FILE}")
        return

    print(f"Found {len(valid_plays)} valid timestamps. Extracting frames...")

    # 5. Loop through each row and extract the frame
    count = 0
    for index, row in valid_plays.iterrows():
        try:
            # Get the timestamp in seconds
            time_in_seconds = float(row['POST_SNAP'])
            
            # Convert Play ID to integer to remove any decimals (e.g., 2545189.0 -> 2545189)
            play_id = int(float(row['PLAY_UNIQUE_ID']))
            
            # Set video reader to the specific millisecond
            cap.set(cv2.CAP_PROP_POS_MSEC, time_in_seconds * 1000)
            
            # Read the frame at that exact moment
            success, frame = cap.read()
            
            if success:
                # Construct the filename requested
                filename = f"{OUTPUT_FOLDER}-{play_id}.png"
                filepath = os.path.join(OUTPUT_FOLDER, filename)
                
                # Save the image
                cv2.imwrite(filepath, frame)
                print(f"Saved: {filename} (Time: {time_in_seconds}s)")
                count += 1
            else:
                print(f"Warning: Could not read frame at {time_in_seconds}s (Play ID: {play_id})")
                
        except ValueError:
            print(f"Warning: Skipped invalid data at row {index}")

    # 6. Cleanup memory and close video file
    cap.release()
    print(f"\nDone! Successfully extracted {count} images to the '{OUTPUT_FOLDER}' folder.")

if __name__ == "__main__":
    extract_frames()