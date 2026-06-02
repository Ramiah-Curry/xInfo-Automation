import pandas as pd

# 1. Configuration (Change the game code here for future games)
game_code = "2935664"
input_csv = f"cd_football_events_{game_code}.csv"
output_xlsx = f"cd_football_events_{game_code}-q1.xlsx"
target_sheet = "Subset_TimeStamps"

print(f"Loading raw data from {input_csv}...")

try:
    # 2. Read the raw CSV
    df = pd.read_csv(input_csv)
    
    # 3. Filter for Quarter 1 only
    df = df[df['QUARTER'] == 1]
    
    # 4. Sort by PLAY_UNIQUE_ID lowest to highest
    df = df.sort_values('PLAY_UNIQUE_ID', ascending=True)
    
    # 5. Keep only your specific columns
    columns_to_keep = [
        'OFF_TEAM_NICKNAME', 'DEF_TEAM_NICKNAME', 'PLAY_UNIQUE_ID', 
        'EVENT_NAME', 'FROM_SCRIMMAGE', 'CONTINUATION', 'DOWN', 'YTG'
    ]
    df = df[columns_to_keep]
    
    # 6. Add the empty "TIME" column at the end
    df['TIME'] = pd.NA 
    
    # 7. Save to a mathematically perfect Excel file
    print("Writing to Excel...")
    with pd.ExcelWriter(output_xlsx, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=target_sheet, index=False)
        
    print(f"Success! Processed {len(df)} rows.")
    print(f"File saved perfectly as: {output_xlsx}")

except FileNotFoundError:
    print(f"Error: Could not find '{input_csv}'. Make sure it is in the same folder.")
except KeyError as e:
    print(f"Error: Could not find one of your columns. Check the exact spelling of {e} in the raw CSV.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")