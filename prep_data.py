import pandas as pd

# 1. Configuration (Change the game code here for future games)
game_code = "2879178"
input_csv = f"cd_football_events_{game_code}.csv"
output_xlsx = f"cd_football_events_{game_code}-timestamps.xlsx"
target_sheet = "Subset_TimeStamps"

print(f"Loading raw data from {input_csv}...")

try:
    # 2. Read the raw CSV, handling encoding and skipping corrupted rows
    df = pd.read_csv(input_csv, encoding='latin1', engine='python', on_bad_lines='skip')
    
    # Force all original column names to uppercase to prevent case-matching errors
    df.columns = df.columns.str.upper()
    
    # 3. Filter for Quarter 1 only (Uncomment if needed)
    # df = df[df['PERIOD'] == 1]
    
    # 4. Sort by PLAY_UNIQUE_ID lowest to highest
    df = df.sort_values('PLAY_UNIQUE_ID', ascending=True)
    
    # 5. Add the empty timeline columns
    df['PRE_SNAP'] = pd.NA 
    df['POST_SNAP'] = pd.NA 

    # 6. Define the exact desired column order
    desired_columns = [
        'GAME_CODE', 'GAME_DATE', 'WEEK', 'HOME_TEAM_NAME', 'HOME_TEAM_NICKNAME', 'HOME_TEAM_ID', 
        'AWAY_TEAM_NAME', 'AWAY_TEAM_NICKNAME', 'AWAY_TEAM_ID', 'OFFENSIVE_TEAM_ID', 'OFFENSIVE_TEAM_NAME', 
        'OFFENSIVE_TEAM_NICKNAME', 'DEFENSIVE_TEAM_ID', 'DEFENSIVE_TEAM_NAME', 'DEFENSIVE_TEAM_NICKNAME', 
        'HOME_SCORE', 'AWAY_SCORE', 'PLAY_UNIQUE_ID', 'EVENT_NAME', 'PERIOD', 'TIME_REMAINING', 'DOWN', 
        'DISTANCE', 'PRE_SNAP', 'POST_SNAP', 'YD_FROM_GOAL', 'OFFENSIVE_FORMATION', 'DEFENSIVE_FRONT', 
        'OFFENSIVE_PERSONNEL', 'DEFENSIVE_PERSONNEL', 'OFF_1_NUMBER', 'OFF_1_PLAYER_FIRST_NAME', 
        'OFF_1_PLAYER_ID', 'OFF_1_PLAYER_LAST_NAME', 'OFF_1_ROLE', 'OFF_2_NUMBER', 'OFF_2_PLAYER_FIRST_NAME', 
        'OFF_2_PLAYER_ID', 'OFF_2_PLAYER_LAST_NAME', 'OFF_2_ROLE', 'OFF_3_NUMBER', 'OFF_3_PLAYER_FIRST_NAME', 
        'OFF_3_PLAYER_ID', 'OFF_3_PLAYER_LAST_NAME', 'OFF_3_ROLE', 'OFF_4_NUMBER', 'OFF_4_PLAYER_FIRST_NAME', 
        'OFF_4_PLAYER_ID', 'OFF_4_PLAYER_LAST_NAME', 'OFF_4_ROLE', 'OFF_5_NUMBER', 'OFF_5_PLAYER_FIRST_NAME', 
        'OFF_5_PLAYER_ID', 'OFF_5_PLAYER_LAST_NAME', 'OFF_5_ROLE', 'OFF_6_NUMBER', 'OFF_6_PLAYER_FIRST_NAME', 
        'OFF_6_PLAYER_ID', 'OFF_6_PLAYER_LAST_NAME', 'OFF_6_ROLE', 'OFF_7_NUMBER', 'OFF_7_PLAYER_FIRST_NAME', 
        'OFF_7_PLAYER_ID', 'OFF_7_PLAYER_LAST_NAME', 'OFF_7_ROLE', 'OFF_8_NUMBER', 'OFF_8_PLAYER_FIRST_NAME', 
        'OFF_8_PLAYER_ID', 'OFF_8_PLAYER_LAST_NAME', 'OFF_8_ROLE', 'OFF_9_NUMBER', 'OFF_9_PLAYER_FIRST_NAME', 
        'OFF_9_PLAYER_ID', 'OFF_9_PLAYER_LAST_NAME', 'OFF_9_ROLE', 'OFF_10_NUMBER', 'OFF_10_PLAYER_FIRST_NAME', 
        'OFF_10_PLAYER_ID', 'OFF_10_PLAYER_LAST_NAME', 'OFF_10_ROLE', 'OFF_11_NUMBER', 'OFF_11_PLAYER_FIRST_NAME', 
        'OFF_11_PLAYER_ID', 'OFF_11_PLAYER_LAST_NAME', 'OFF_11_ROLE', 'DEF_1_NUMBER', 'DEF_1_PLAYER_FIRST_NAME', 
        'DEF_1_PLAYER_ID', 'DEF_1_PLAYER_LAST_NAME', 'DEF_1_ROLE', 'DEF_2_NUMBER', 'DEF_2_PLAYER_FIRST_NAME', 
        'DEF_2_PLAYER_ID', 'DEF_2_PLAYER_LAST_NAME', 'DEF_2_ROLE', 'DEF_3_NUMBER', 'DEF_3_PLAYER_FIRST_NAME', 
        'DEF_3_PLAYER_ID', 'DEF_3_PLAYER_LAST_NAME', 'DEF_3_ROLE', 'DEF_4_NUMBER', 'DEF_4_PLAYER_FIRST_NAME', 
        'DEF_4_PLAYER_ID', 'DEF_4_PLAYER_LAST_NAME', 'DEF_4_ROLE', 'DEF_5_NUMBER', 'DEF_5_PLAYER_FIRST_NAME', 
        'DEF_5_PLAYER_ID', 'DEF_5_PLAYER_LAST_NAME', 'DEF_5_ROLE', 'DEF_6_NUMBER', 'DEF_6_PLAYER_FIRST_NAME', 
        'DEF_6_PLAYER_ID', 'DEF_6_PLAYER_LAST_NAME', 'DEF_6_ROLE', 'DEF_7_NUMBER', 'DEF_7_PLAYER_FIRST_NAME', 
        'DEF_7_PLAYER_ID', 'DEF_7_PLAYER_LAST_NAME', 'DEF_7_ROLE', 'DEF_8_NUMBER', 'DEF_8_PLAYER_FIRST_NAME', 
        'DEF_8_PLAYER_ID', 'DEF_8_PLAYER_LAST_NAME', 'DEF_8_ROLE', 'DEF_9_NUMBER', 'DEF_9_PLAYER_FIRST_NAME', 
        'DEF_9_PLAYER_ID', 'DEF_9_PLAYER_LAST_NAME', 'DEF_9_ROLE', 'DEF_10_NUMBER', 'DEF_10_PLAYER_FIRST_NAME', 
        'DEF_10_PLAYER_ID', 'DEF_10_PLAYER_LAST_NAME', 'DEF_10_ROLE', 'DEF_11_NUMBER', 'DEF_11_PLAYER_FIRST_NAME', 
        'DEF_11_PLAYER_ID', 'DEF_11_PLAYER_LAST_NAME', 'DEF_11_ROLE', 'XYARDS', 'XRUSH%', 'XOVRYDS', 'XSACK%', 
        'XSCRAMBLE%', 'XTD%', 'XRUSHTD%', 'FROM_SCRIMMAGE', 'CONTINUATION'
    ]
    
    # 7. Apply the reordering 
    # This filters the list to only include columns that exist, preventing KeyErrors 
    # if the raw CSV is ever missing a column.
    final_columns = [col for col in desired_columns if col in df.columns]
    df = df[final_columns]
    
    # 8. Save to a mathematically perfect Excel file
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