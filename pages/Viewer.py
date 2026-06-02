import streamlit as st
import pandas as pd
import altair as alt
import subprocess
import os

st.set_page_config(page_title="Football Play Viewer", layout="wide")
st.title("Football Interactive Play Viewer")

# 1. File Configuration
SHEET_NAME = 'Subset_TimeStamps'
CLIP_FILE = 'temp_play_clip.mp4'

VIDEO_FILE = st.session_state.get('selected_video', None)
EXCEL_FILE = st.session_state.get('selected_excel', None)

if not VIDEO_FILE or not os.path.exists(VIDEO_FILE):
    st.error("No valid video selected. Please return to the Home page.")
    st.stop()

if not EXCEL_FILE or not os.path.exists(EXCEL_FILE):
    st.error("No valid Excel file selected. Please return to the Home page.")
    st.stop()

# 2. Load Data
@st.cache_data
def load_data(filepath):
    if os.path.exists(filepath):
        try:
            xls = pd.ExcelFile(filepath)
            actual_sheets = xls.sheet_names
            
            target_sheet = None
            for sheet in actual_sheets:
                if sheet.strip() == SHEET_NAME:
                    target_sheet = sheet
                    break
            
            if target_sheet:
                return pd.read_excel(filepath, sheet_name=target_sheet)
            else:
                st.error(f"Target sheet '{SHEET_NAME}' not found.")
                st.info(f"Sheets available in **{filepath}**: {', '.join(actual_sheets)}")
                st.stop()
                
        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
            st.stop()
            
    return pd.DataFrame()

if 'df' not in st.session_state:
    st.session_state.df = load_data(EXCEL_FILE)

df = st.session_state.df

has_dual_cams = 'TIME_A' in df.columns and 'TIME_B' in df.columns
has_single_cam = 'TIME' in df.columns

if not df.empty and (has_dual_cams or has_single_cam):
    
    st.caption(f"Analyzing: **{VIDEO_FILE}** with data from **{EXCEL_FILE}**")
    
    valid_plays = df.copy() 
    
    # Calculate previous times dynamically on the copy
    if has_dual_cams:
        valid_plays['PREV_TIME_B'] = valid_plays['TIME_B'].replace(0, pd.NA).shift(1).ffill().fillna(0)
    else:
        valid_plays['PREV_TIME'] = valid_plays['TIME'].replace(0, pd.NA).shift(1).ffill().fillna(0)
    
    if 'active_play_id' not in st.session_state:
        st.session_state.active_play_id = valid_plays['PLAY_UNIQUE_ID'].iloc[0]
    if 'active_cam' not in st.session_state:
        st.session_state.active_cam = "Cam A (Side Camera)"
    
    col_video, col_controls = st.columns([2.5, 1])
    
    with col_controls:
        st.subheader("Play Controls")
        
        play_options = valid_plays['PLAY_UNIQUE_ID'].tolist()
        current_play_index = play_options.index(st.session_state.active_play_id) if st.session_state.active_play_id in play_options else 0
        
        selected_play_id = st.selectbox("Select Play ID", play_options, index=current_play_index)
        
        if has_dual_cams:
            cam_options = ["Cam A (Side Camera)", "Cam B (Touchdown Camera)"]
            current_cam_index = cam_options.index(st.session_state.active_cam)
            selected_cam = st.selectbox("Select View", cam_options, index=current_cam_index)
        else:
            st.markdown("**View:** Single Broadcast Camera")
            selected_cam = "Single View"

        if selected_play_id != st.session_state.active_play_id or (has_dual_cams and selected_cam != st.session_state.active_cam):
            st.session_state.active_play_id = selected_play_id
            if has_dual_cams:
                st.session_state.active_cam = selected_cam
            st.rerun()

        row = valid_plays[valid_plays['PLAY_UNIQUE_ID'] == st.session_state.active_play_id].iloc[0]
        
        # Safely extract timestamps using .get()
        if has_dual_cams:
            raw_time_a = row.get('TIME_A', 0)
            raw_time_b = row.get('TIME_B', 0)
            raw_prev = row.get('PREV_TIME_B', 0)
            
            if st.session_state.active_cam == 'Cam A (Side Camera)':
                start_val = raw_prev if pd.notna(raw_prev) else 0
                end_val = raw_time_a
            else:
                start_val = raw_time_a if pd.notna(raw_time_a) else 0
                end_val = raw_time_b
        else:
            raw_prev = row.get('PREV_TIME', 0)
            raw_time = row.get('TIME', 0)
            
            start_val = raw_prev if pd.notna(raw_prev) else 0
            end_val = raw_time

        start_time = int(start_val) if pd.notna(start_val) else 0
        end_time = int(end_val) if pd.notna(end_val) else 0

        st.markdown(f"**Event:** {row.get('EVENT_NAME', 'N/A')}")
        st.markdown(f"**Down:** {row.get('DOWN', 'N/A')} & {row.get('YTG', 'N/A')}")
        
        if end_time > 0:
            st.markdown(f"*Target Clip: {start_time}s to {end_time}s*")
        else:
            st.markdown("*Target Clip: Pending Timestamps*")

    with col_video:
        st.subheader("Isolated Video Playback")
        if start_time < end_time and end_time > 0:
            with st.spinner("Slicing clip..."):
                cmd = [
                    'ffmpeg', '-y', 
                    '-ss', str(start_time), 
                    '-to', str(end_time),
                    '-i', VIDEO_FILE,
                    '-c:v', 'copy', 
                    '-c:a', 'copy', 
                    CLIP_FILE
                ]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                if os.path.exists(CLIP_FILE):
                    st.video(CLIP_FILE)
                else:
                    st.error("FFmpeg failed to slice the video.")
        else:
            st.warning("No valid timestamps for this play yet. Enter them in the grid below to enable playback.")

    st.divider()

    st.subheader("Quarter 1 Timeline")
    
    chart_data = valid_plays[pd.notna(valid_plays['TIME_B']) if has_dual_cams else pd.notna(valid_plays['TIME'])]
    
    if not chart_data.empty:
        click_selection = alt.selection_point(fields=['PLAY_UNIQUE_ID'], name='play_click', on='click')
        
        x_start_col = 'PREV_TIME_B:Q' if has_dual_cams else 'PREV_TIME:Q'
        x_end_col = 'TIME_B:Q' if has_dual_cams else 'TIME:Q'
        
        timeline_chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X(x_start_col, title='Seconds into Video', scale=alt.Scale(domain=[0, 750])),
            x2=x_end_col,
            y=alt.Y('EVENT_NAME:N', title=''),
            tooltip=['PLAY_UNIQUE_ID', 'DOWN', 'YTG', x_start_col, x_end_col],
            color=alt.condition(
                alt.datum.PLAY_UNIQUE_ID == st.session_state.active_play_id,
                alt.value('#ff4b4b'),
                alt.value('#4a4a4a')
            ),
            opacity=alt.condition(click_selection, alt.value(1.0), alt.value(0.6))
        ).add_params(click_selection).properties(height=120)
        
        chart_event = st.altair_chart(timeline_chart, use_container_width=True, on_select="rerun")
        
        if chart_event and len(chart_event.selection.play_click) > 0:
            clicked_play = chart_event.selection.play_click[0]['PLAY_UNIQUE_ID']
            if clicked_play != st.session_state.active_play_id:
                st.session_state.active_play_id = clicked_play
                st.rerun()
    else:
        st.info("The timeline will appear here once you start adding timestamps.")

    st.subheader("Edit Timestamps")
    
    def highlight_active_row(row):
        styles = [''] * len(row)
        if float(row['PLAY_UNIQUE_ID']) == float(st.session_state.active_play_id):
            if has_dual_cams:
                target_col = 'TIME_A' if st.session_state.active_cam == 'Cam A (Side Camera)' else 'TIME_B'
            else:
                target_col = 'TIME'
                
            for i, col_name in enumerate(row.index):
                if col_name == target_col:
                    styles[i] = 'background-color: #ff4b4b; font-weight: bold; color: white;' 
                else:
                    styles[i] = 'background-color: #ffcccc; color: black;' 
        return styles

    styled_df = df.style.apply(highlight_active_row, axis=1)
    edited_df = st.data_editor(styled_df, num_rows="dynamic", use_container_width=True, height=250)
    
    if st.button("Save to Excel", type="primary", key="save_viewer"):
        try:
            with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                edited_df.to_excel(writer, sheet_name=SHEET_NAME, index=False)
            st.session_state.df = edited_df
            st.success("Successfully saved changes to Excel!")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to save: {e}. Ensure the Excel file is closed on your computer.")

else:
    st.error(f"Could not load data. Ensure '{SHEET_NAME}' exists and has 'TIME' or 'TIME_A'/'TIME_B' columns.")