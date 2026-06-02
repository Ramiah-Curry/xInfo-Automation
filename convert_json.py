import pandas as pd
import json

# 1. The raw JSON output from Google AI Studio
raw_json = """
[
{
"OFF_TEAM_NICKNAME": "Chippewas",
"DEF_TEAM_NICKNAME": "Wildcats",
"PLAY_UNIQUE_ID": 0,
"EVENT_NAME": "Kick Off",
"DOWN": null,
"YTG": null,
"TIME": 11
},
{
"OFF_TEAM_NICKNAME": "Wildcats",
"DEF_TEAM_NICKNAME": "Chippewas",
"PLAY_UNIQUE_ID": 1,
"EVENT_NAME": "Incomplete Pass",
"DOWN": 1,
"YTG": 10,
"TIME": 56
},
{
"OFF_TEAM_NICKNAME": "Wildcats",
"DEF_TEAM_NICKNAME": "Chippewas",
"PLAY_UNIQUE_ID": 2,
"EVENT_NAME": "Run",
"DOWN": 2,
"YTG": 10,
"TIME": 93
},
{
"OFF_TEAM_NICKNAME": "Wildcats",
"DEF_TEAM_NICKNAME": "Chippewas",
"PLAY_UNIQUE_ID": 3,
"EVENT_NAME": "Pass Completion",
"DOWN": 3,
"YTG": 8,
"TIME": 135
},
{
"OFF_TEAM_NICKNAME": "Wildcats",
"DEF_TEAM_NICKNAME": "Chippewas",
"PLAY_UNIQUE_ID": 4,
"EVENT_NAME": "Run",
"DOWN": 4,
"YTG": 1,
"TIME": 172
},
{
"OFF_TEAM_NICKNAME": "Chippewas",
"DEF_TEAM_NICKNAME": "Wildcats",
"PLAY_UNIQUE_ID": 5,
"EVENT_NAME": "Pass Completion",
"DOWN": 1,
"YTG": 10,
"TIME": 259
},
{
"OFF_TEAM_NICKNAME": "Chippewas",
"DEF_TEAM_NICKNAME": "Wildcats",
"PLAY_UNIQUE_ID": 6,
"EVENT_NAME": "Run",
"DOWN": 1,
"YTG": 10,
"TIME": 301
},
{
"OFF_TEAM_NICKNAME": "Chippewas",
"DEF_TEAM_NICKNAME": "Wildcats",
"PLAY_UNIQUE_ID": 7,
"EVENT_NAME": "Pass Completion",
"DOWN": 2,
"YTG": 9,
"TIME": 345
},
{
"OFF_TEAM_NICKNAME": "Chippewas",
"DEF_TEAM_NICKNAME": "Wildcats",
"PLAY_UNIQUE_ID": 8,
"EVENT_NAME": "Run",
"DOWN": 3,
"YTG": 9,
"TIME": 388
},
{
"OFF_TEAM_NICKNAME": "Wildcats",
"DEF_TEAM_NICKNAME": "Chippewas",
"PLAY_UNIQUE_ID": 9,
"EVENT_NAME": "Run",
"DOWN": 1,
"YTG": 10,
"TIME": 456
},
{
"OFF_TEAM_NICKNAME": "Wildcats",
"DEF_TEAM_NICKNAME": "Chippewas",
"PLAY_UNIQUE_ID": 10,
"EVENT_NAME": "Run",
"DOWN": 2,
"YTG": 12,
"TIME": 499
},
{
"OFF_TEAM_NICKNAME": "Wildcats",
"DEF_TEAM_NICKNAME": "Chippewas",
"PLAY_UNIQUE_ID": 11,
"EVENT_NAME": "Incomplete Pass",
"DOWN": 3,
"YTG": 17,
"TIME": 538
},
{
"OFF_TEAM_NICKNAME": "Chippewas",
"DEF_TEAM_NICKNAME": "Wildcats",
"PLAY_UNIQUE_ID": 12,
"EVENT_NAME": "Run",
"DOWN": 1,
"YTG": 10,
"TIME": 613
},
{
"OFF_TEAM_NICKNAME": "Chippewas",
"DEF_TEAM_NICKNAME": "Wildcats",
"PLAY_UNIQUE_ID": 13,
"EVENT_NAME": "Pass Completion",
"DOWN": 3,
"YTG": 17,
"TIME": 701
},
{
"OFF_TEAM_NICKNAME": "Wildcats",
"DEF_TEAM_NICKNAME": "Chippewas",
"PLAY_UNIQUE_ID": 14,
"EVENT_NAME": "Run",
"DOWN": 1,
"YTG": 10,
"TIME": 769
},
{
"OFF_TEAM_NICKNAME": "Wildcats",
"DEF_TEAM_NICKNAME": "Chippewas",
"PLAY_UNIQUE_ID": 15,
"EVENT_NAME": "Pass Completion",
"DOWN": 2,
"YTG": 7,
"TIME": 792
},
{
"OFF_TEAM_NICKNAME": "Wildcats",
"DEF_TEAM_NICKNAME": "Chippewas",
"PLAY_UNIQUE_ID": 16,
"EVENT_NAME": "Run",
"DOWN": 1,
"YTG": 10,
"TIME": 826
},
{
"OFF_TEAM_NICKNAME": "Wildcats",
"DEF_TEAM_NICKNAME": "Chippewas",
"PLAY_UNIQUE_ID": 17,
"EVENT_NAME": "Pass Completion",
"DOWN": 1,
"YTG": 10,
"TIME": 883
},
{
"OFF_TEAM_NICKNAME": "Wildcats",
"DEF_TEAM_NICKNAME": "Chippewas",
"PLAY_UNIQUE_ID": 18,
"EVENT_NAME": "End of Quarter",
"DOWN": null,
"YTG": null,
"TIME": 935
}
]
"""

# 2. Parse the string using the json module (this safely converts 'null' to 'None')
ai_data = json.loads(raw_json)

# 3. Convert to DataFrame
df = pd.DataFrame(ai_data)

# 4. Format the columns for the Streamlit app
# Keep only the TIME column and ensure consistent column ordering
df = df[['OFF_TEAM_NICKNAME', 'DEF_TEAM_NICKNAME', 'PLAY_UNIQUE_ID', 'EVENT_NAME', 'DOWN', 'YTG', 'TIME']]

# 5. Export to a new Excel file
game_code = "2935664"
output_file = f"ai_events_{game_code}.xlsx"
sheet_name = "Subset_TimeStamps"

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Success! Data converted and saved to '{output_file}' under the tab '{sheet_name}'.")