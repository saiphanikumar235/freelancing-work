import streamlit as st
import speech_recognition as sr
import io
import difflib
import re
from audio_recorder_streamlit import audio_recorder

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Speech to Text", page_icon="🎙️", layout="wide")

# ─── Session State ────────────────────────────────────────────────────────────
if "transcript_history" not in st.session_state:
    st.session_state.transcript_history = []
if "last_transcript" not in st.session_state:
    st.session_state.last_transcript = ""

# ─── Sample Phrases for Accuracy Testing ─────────────────────────────────────
SAMPLE_PHRASES = {
    "Easy": [
        "The quick brown fox jumps over the lazy dog.",
        "She sells seashells by the seashore.",
        "Good morning, how are you today?",
        "The weather is sunny and warm outside.",
        "I enjoy reading books in the evening.",
    ],
    "Medium": [
        "Artificial intelligence is transforming the way we work and communicate.",
        "The stock market experienced significant volatility during the third quarter.",
        "Python is a versatile programming language used in data science and web development.",
        "Climate change poses a significant threat to global ecosystems and biodiversity.",
        "The organization implemented a new hierarchy management system this quarter.",
    ],
    "Hard": [
        "The entrepreneur's idiosyncratic methodology necessitated unprecedented organizational restructuring.",
        "Photosynthesis is the biochemical process through which chlorophyll absorbs sunlight to synthesize nutrients.",
        "The pharmaceutical company's clinical trials demonstrated statistically significant efficacy improvements.",
        "Supercalifragilisticexpialidocious is an extraordinary word from the classic musical film.",
        "The multifaceted geopolitical negotiations encompassed numerous socioeconomic considerations.",
    ],
}

# ─── Helpers ──────────────────────────────────────────────────────────────────
def transcribe_audio(audio_bytes: bytes) -> tuple[str, str]:
    """Returns (transcript, error_message)."""
    recognizer = sr.Recognizer()
    try:
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text, ""
    except sr.UnknownValueError:
        return "", "🔇 Could not understand the audio. Please speak clearly and try again."
    except sr.RequestError as e:
        return "", f"⚠️ Speech Recognition service error: {e}. Check your internet connection."
    except Exception as e:
        return "", f"❌ Unexpected error: {e}"


def normalize(text: str) -> str:
    return re.sub(r"[^\w\s]", "", text.lower()).strip()


def word_accuracy(reference: str, hypothesis: str) -> tuple[float, list]:
    """Returns (accuracy_pct, list of (word, status)) where status in correct/wrong/missing/extra."""
    ref_words = normalize(reference).split()
    hyp_words = normalize(hypothesis).split()

    matcher = difflib.SequenceMatcher(None, ref_words, hyp_words)
    result = []
    matched = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for w in ref_words[i1:i2]:
                result.append((w, "correct"))
                matched += 1
        elif tag == "replace":
            for w in ref_words[i1:i2]:
                result.append((w, "wrong"))
            for w in hyp_words[j1:j2]:
                result.append((w, "extra"))
        elif tag == "delete":
            for w in ref_words[i1:i2]:
                result.append((w, "missing"))
        elif tag == "insert":
            for w in hyp_words[j1:j2]:
                result.append((w, "extra"))

    total = max(len(ref_words), 1)
    accuracy = round((matched / total) * 100, 1)
    return accuracy, result


def render_word_diff(diff_result: list) -> str:
    """Build HTML string with color-coded words."""
    color_map = {
        "correct": ("#27ae60", "✓"),
        "wrong":   ("#e74c3c", "✗"),
        "missing": ("#e67e22", "?"),
        "extra":   ("#3498db", "+"),
    }
    parts = []
    for word, status in diff_result:
        color, icon = color_map[status]
        parts.append(
            f"<span style='color:{color};font-weight:600;margin:0 2px' title='{status}'>{word}</span>"
        )
    return " ".join(parts)


def clipboard_button(text: str, button_label: str = "📋 Copy to Clipboard"):
    """Renders a JS-powered copy button."""
    escaped = text.replace("`", "\\`").replace("\\", "\\\\").replace("\n", "\\n")
    st.components.v1.html(
        f"""
        <style>
          .copy-btn {{
            background: linear-gradient(135deg,#1a5276,#2980b9);
            color: white; border: none; padding: 10px 22px;
            border-radius: 8px; font-size: 15px; font-weight: 600;
            cursor: pointer; transition: all 0.2s;
            font-family: 'Segoe UI', sans-serif;
          }}
          .copy-btn:hover {{ opacity: 0.85; transform: translateY(-1px); }}
          .copy-btn:active {{ transform: translateY(0); }}
          #msg {{ margin-top: 8px; font-size: 13px; color: #27ae60; font-weight:600; height:18px; }}
        </style>
        <button class="copy-btn" onclick="copyText()">{button_label}</button>
        <div id="msg"></div>
        <script>
          function copyText() {{
            const text = `{escaped}`;
            navigator.clipboard.writeText(text).then(() => {{
              document.getElementById('msg').innerText = '✅ Copied to clipboard!';
              setTimeout(() => document.getElementById('msg').innerText = '', 2000);
            }}).catch(() => {{
              const el = document.createElement('textarea');
              el.value = text;
              document.body.appendChild(el);
              el.select();
              document.execCommand('copy');
              document.body.removeChild(el);
              document.getElementById('msg').innerText = '✅ Copied!';
              setTimeout(() => document.getElementById('msg').innerText = '', 2000);
            }});
          }}
        </script>
        """,
        height=70,
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <style>
    .page-title {
        font-size:2rem; font-weight:800; letter-spacing:-0.5px;
        background:linear-gradient(90deg,#1a5276,#27ae60);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    }
    .accuracy-box {
        border-radius:12px; padding:18px 24px; margin:12px 0;
        font-size:1rem; border-left:5px solid;
    }
    </style>
    <div class='page-title'>🎙️ Speech to Text & Accuracy Tester</div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ─── Mode Tabs ────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🎤  Free Speech → Text",
    "🎯  Accuracy Test Mode",
    "📜  Transcript History",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 – Free Speech Recording
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("🎤 Record Your Speech")
    st.markdown("Click the microphone button, speak, then click again to stop. Your speech will be converted to text.")

    col_rec, col_info = st.columns([1, 2])

    with col_rec:
        st.markdown("##### 🔴 Tap to Record")
        audio_bytes = audio_recorder(
            text="",
            recording_color="#e74c3c",
            neutral_color="#1a5276",
            icon_name="microphone",
            icon_size="3x",
            pause_threshold=3.0,
            sample_rate=16000,
            key="free_recorder",
        )

    with col_info:
        st.markdown("##### ℹ️ Tips for best results")
        st.markdown("""
        - 🔇 Speak in a **quiet environment**
        - 🎙️ Stay **6–12 inches** from the microphone
        - 🗣️ Speak **clearly** and at a **moderate pace**
        - ⏹️ Click the mic again to **stop recording**
        - 🌐 Requires an **internet connection** (uses Google Speech API)
        """)

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        with st.spinner("🔄 Transcribing your speech..."):
            transcript, error = transcribe_audio(audio_bytes)

        if error:
            st.error(error)
        elif transcript:
            st.session_state.last_transcript = transcript
            st.session_state.transcript_history.append({"mode": "Free Speech", "text": transcript})

            st.success("✅ Transcription complete!")
            st.markdown("#### 📝 Transcribed Text")

            # Editable text area
            edited = st.text_area("You can edit the text below:", value=transcript, height=120, key="free_edit")

            col_copy, col_clear = st.columns([1, 3])
            with col_copy:
                clipboard_button(edited)
            with col_clear:
                st.markdown(f"**Word count:** {len(edited.split())}  |  **Characters:** {len(edited)}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 – Accuracy Test Mode
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🎯 Accuracy Test Mode")
    st.markdown("Read the reference phrase aloud and see how accurately your speech is recognized.")

    # ── Phrase Selector ──
    col_diff, col_phrase = st.columns([1, 2])
    with col_diff:
        difficulty = st.selectbox("📊 Difficulty Level", list(SAMPLE_PHRASES.keys()), key="difficulty")
    with col_phrase:
        phrases = SAMPLE_PHRASES[difficulty]
        chosen_phrase = st.selectbox("📖 Choose a Phrase", phrases, key="phrase_pick")

    # Custom phrase option
    use_custom = st.checkbox("✏️ Use my own custom phrase")
    if use_custom:
        reference_text = st.text_area("Enter your custom reference phrase:", height=80, key="custom_ref")
    else:
        reference_text = chosen_phrase

    if reference_text:
        # Display reference phrase prominently
        st.markdown("#### 📖 Reference Phrase — Read this aloud:")
        st.markdown(
            f"""
            <div style='
                background:linear-gradient(135deg,#eaf4fb,#fdfefe);
                border:2px solid #2980b9; border-radius:12px;
                padding:20px 24px; font-size:1.3rem; font-weight:600;
                color:#1a252f; line-height:1.8; letter-spacing:0.3px;
                margin-bottom:16px;
            '>{reference_text}</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### 🔴 Now Record Yourself:")

        acc_audio = audio_recorder(
            text="",
            recording_color="#e74c3c",
            neutral_color="#117a65",
            icon_name="microphone",
            icon_size="3x",
            pause_threshold=3.0,
            sample_rate=16000,
            key="accuracy_recorder",
        )

        if acc_audio:
            st.audio(acc_audio, format="audio/wav")
            with st.spinner("🔄 Transcribing & analysing accuracy..."):
                hyp_text, error = transcribe_audio(acc_audio)

            if error:
                st.error(error)
            elif hyp_text:
                st.session_state.transcript_history.append({
                    "mode": f"Accuracy Test ({difficulty})",
                    "text": hyp_text,
                })

                accuracy_pct, diff_result = word_accuracy(reference_text, hyp_text)

                # ── Accuracy Score ──
                st.markdown("### 📊 Results")
                m1, m2, m3 = st.columns(3)
                m1.metric("🎯 Accuracy", f"{accuracy_pct}%")
                ref_words = normalize(reference_text).split()
                hyp_words = normalize(hyp_text).split()
                correct_count = sum(1 for _, s in diff_result if s == "correct")
                m2.metric("✅ Correct Words", f"{correct_count} / {len(ref_words)}")
                m3.metric("🗣️ Words Spoken", str(len(hyp_words)))

                # Accuracy colour feedback
                if accuracy_pct >= 90:
                    feedback_color = "#1e8449"; feedback_bg = "#eafaf1"
                    feedback_msg = "🌟 Excellent! Outstanding accuracy!"
                elif accuracy_pct >= 70:
                    feedback_color = "#d68910"; feedback_bg = "#fef9e7"
                    feedback_msg = "👍 Good job! A little more practice and you'll nail it."
                elif accuracy_pct >= 50:
                    feedback_color = "#cb4335"; feedback_bg = "#fdedec"
                    feedback_msg = "🔁 Keep practicing. Try speaking more slowly and clearly."
                else:
                    feedback_color = "#922b21"; feedback_bg = "#f9ebea"
                    feedback_msg = "❌ Low accuracy. Try in a quieter space or speak louder."

                st.markdown(
                    f"<div class='accuracy-box' style='background:{feedback_bg};border-color:{feedback_color};color:{feedback_color}'>"
                    f"{feedback_msg}</div>",
                    unsafe_allow_html=True,
                )

                # ── Word Diff ──
                st.markdown("#### 🔍 Word-by-Word Comparison")
                legend_html = (
                    "<span style='color:#27ae60;font-weight:700'>■ Correct</span> &nbsp;"
                    "<span style='color:#e74c3c;font-weight:700'>■ Wrong/Missed</span> &nbsp;"
                    "<span style='color:#e67e22;font-weight:700'>■ Missing from speech</span> &nbsp;"
                    "<span style='color:#3498db;font-weight:700'>■ Extra word spoken</span>"
                )
                st.markdown(legend_html, unsafe_allow_html=True)

                diff_html = render_word_diff(diff_result)
                st.markdown(
                    f"<div style='background:#fdfefe;border:1px solid #d5d8dc;border-radius:10px;"
                    f"padding:18px;font-size:1.15rem;line-height:2;margin-top:10px'>{diff_html}</div>",
                    unsafe_allow_html=True,
                )

                # ── Side by Side ──
                st.markdown("#### 📋 Side-by-Side Comparison")
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**📖 Reference Text**")
                    st.info(reference_text)
                with c2:
                    st.markdown("**🗣️ Your Speech (Transcribed)**")
                    st.info(hyp_text)

                # ── Copy buttons ──
                st.markdown("#### 📤 Copy Options")
                cp1, cp2, cp3 = st.columns(3)
                with cp1:
                    clipboard_button(hyp_text, "📋 Copy Transcript")
                with cp2:
                    clipboard_button(reference_text, "📋 Copy Reference")
                with cp3:
                    report = (
                        f"Speech Accuracy Report\n"
                        f"======================\n"
                        f"Reference: {reference_text}\n"
                        f"Transcript: {hyp_text}\n"
                        f"Accuracy: {accuracy_pct}%\n"
                        f"Correct Words: {correct_count}/{len(ref_words)}\n"
                    )
                    clipboard_button(report, "📋 Copy Full Report")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 – History
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("📜 Transcript History (This Session)")

    if not st.session_state.transcript_history:
        st.info("No transcripts yet. Use **Free Speech** or **Accuracy Test** tabs to record.")
    else:
        for i, entry in enumerate(reversed(st.session_state.transcript_history), 1):
            with st.expander(f"#{i} — {entry['mode']}", expanded=(i == 1)):
                st.write(entry["text"])
                clipboard_button(entry["text"], f"📋 Copy #{i}")

        st.markdown("---")
        col_dl, col_clr = st.columns([2, 1])
        with col_dl:
            all_text = "\n\n".join(
                f"[{e['mode']}]\n{e['text']}" for e in st.session_state.transcript_history
            )
            st.download_button(
                "⬇️ Download All Transcripts (.txt)",
                data=all_text,
                file_name="transcripts.txt",
                mime="text/plain",
            )
        with col_clr:
            if st.button("🗑️ Clear History", type="secondary"):
                st.session_state.transcript_history = []
                st.rerun()
