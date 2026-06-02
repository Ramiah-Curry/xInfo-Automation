import streamlit as st
import pandas as pd
import os
import glob

st.set_page_config(page_title="Analytics Hub", layout="wide")

# Find files in directory
mp4_files = [f for f in glob.glob("*.mp4") if f != 'temp_play_clip.mp4']
# Ignore temporary Excel files that start with ~$
xlsx_files = [f for f in glob.glob("*.xlsx") if not f.startswith('~$')]

# Initialize global states for file selections
if 'selected_video' not in st.session_state:
    st.session_state.selected_video = mp4_files[0] if mp4_files else None
if 'selected_excel' not in st.session_state:
    st.session_state.selected_excel = xlsx_files[0] if xlsx_files else None

st.title("Football Analytics Hub")
st.markdown("Welcome. Please set your global settings below and select a workspace from the sidebar.")

st.divider()

# Global Settings Section
st.subheader("Global Settings")

col_vid, col_exc = st.columns(2)

with col_vid:
    if mp4_files:
        current_vid_index = mp4_files.index(st.session_state.selected_video) if st.session_state.selected_video in mp4_files else 0
        selected_vid = st.selectbox("Select Video Source (.mp4):", mp4_files, index=current_vid_index)
        
        if selected_vid != st.session_state.selected_video:
            st.session_state.selected_video = selected_vid
            st.rerun()
    else:
        st.warning("No MP4 files found in the current directory.")

with col_exc:
    if xlsx_files:
        current_exc_index = xlsx_files.index(st.session_state.selected_excel) if st.session_state.selected_excel in xlsx_files else 0
        selected_exc = st.selectbox("Select Data Source (.xlsx):", xlsx_files, index=current_exc_index)
        
        if selected_exc != st.session_state.selected_excel:
            st.session_state.selected_excel = selected_exc
            # Clear the dataframe from memory so it forces a reload of the new file
            if 'df' in st.session_state:
                del st.session_state['df']
            st.rerun()
    else:
        st.warning("No XLSX files found in the current directory.")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Football Play Viewer")
    st.write("Interactive video synchronization with isolated clip slicing.")
        
with col2:
    st.subheader("Timeline Creator")
    st.write("Full video playback for creating and editing your own timelines.")