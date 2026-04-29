import streamlit as st
import os
import subprocess
import tempfile
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment

st.set_page_config(page_title="Vocal & Stem Extractor", layout="centered")
st.title("Vocal & Instrument Stem Extractor")
st.markdown("Upload a media file to isolate specific audio elements using deep learning.")

process_mode = st.radio("Select Input Type:", ("Video", "Audio"))
uploaded_file = st.file_uploader(f"Upload a {process_mode} file (Max 50MB recommended)", type=["mp4", "mov"] if process_mode == "Video" else ["mp3", "wav"])

if uploaded_file is not None:
    st.subheader("Select sounds to extract and combine:")
    keep_vocals = st.checkbox("Vocals (Voice)", value=True)
    keep_drums = st.checkbox("Drums")
    keep_bass = st.checkbox("Bass")
    keep_other = st.checkbox("Other (Guitar, Keys, etc.)")

    if st.button("Process File"):
        if not any([keep_vocals, keep_drums, keep_bass, keep_other]):
            st.error("Please select at least one audio element to extract.")
        else:
            # Create a secure temporary directory for this specific user session
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    file_ext = uploaded_file.name.split(".")[-1]
                    input_path = os.path.join(temp_dir, f"input.{file_ext}")
                    
                    with open(input_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                        
                    with st.spinner("Processing AI Source Separation... This takes a few minutes on standard CPUs."):
                        
                        audio_path = os.path.join(temp_dir, "working_audio.wav")
                        if process_mode == "Video":
                            video = VideoFileClip(input_path)
                            video.audio.write_audiofile(audio_path, logger=None)
                        else:
                            audio_path = input_path

                        # Run Demucs outputting to our secure temp directory
                        out_dir = os.path.join(temp_dir, "separated")
                        subprocess.run(["demucs", "-n", "htdemucs", "--out", out_dir, audio_path], check=True)

                        track_name = "working_audio" if process_mode == "Video" else "input"
                        stem_dir = os.path.join(out_dir, "htdemucs", track_name)

                        mixed_audio = None
                        stems_to_mix = []
                        
                        if keep_vocals: stems_to_mix.append(os.path.join(stem_dir, "vocals.wav"))
                        if keep_drums: stems_to_mix.append(os.path.join(stem_dir, "drums.wav"))
                        if keep_bass: stems_to_mix.append(os.path.join(stem_dir, "bass.wav"))
                        if keep_other: stems_to_mix.append(os.path.join(stem_dir, "other.wav"))

                        for stem_file in stems_to_mix:
                            if os.path.exists(stem_file):
                                stem_audio = AudioSegment.from_wav(stem_file)
                                if mixed_audio is None:
                                    mixed_audio = stem_audio
                                else:
                                    mixed_audio = mixed_audio.overlay(stem_audio)

                        final_audio_path = os.path.join(temp_dir, "final_audio.wav")
                        mixed_audio.export(final_audio_path, format="wav")

                        if process_mode == "Video":
                            final_video_path = os.path.join(temp_dir, "final_video.mp4")
                            video_clip = VideoFileClip(input_path)
                            new_audio = AudioFileClip(final_audio_path)
                            final_video = video_clip.set_audio(new_audio)
                            final_video.write_videofile(final_video_path, codec="libx264", audio_codec="aac", logger=None)
                            
                            st.video(final_video_path)
                            with open(final_video_path, "rb") as file:
                                st.download_button("Download Processed Video", file, file_name="extracted_video.mp4")
                        else:
                            st.audio(final_audio_path)
                            with open(final_audio_path, "rb") as file:
                                st.download_button("Download Processed Audio", file, file_name="extracted_audio.wav")

                        st.success("Extraction Complete!")
                
                except Exception as e:
                    st.error(f"An error occurred during processing: {e}")