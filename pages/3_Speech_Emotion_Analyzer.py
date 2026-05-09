import streamlit as st
import speech_recognition as sr
import io
import re
import time
from audio_recorder_streamlit import audio_recorder

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Speech Emotion Analyzer", page_icon="🎭", layout="wide")

# ─── Session State ────────────────────────────────────────────────────────────
if "emotion_history" not in st.session_state:
    st.session_state.emotion_history = []

# ─── Emotion Keyword Bank ─────────────────────────────────────────────────────
EMOTION_KEYWORDS = {
    "angry": {
        "emoji": "😡",
        "label": "Angry",
        "color": "#e74c3c",
        "bg": "#fdf0f0",
        "words": [
            "angry", "furious", "mad", "rage", "hate", "horrible", "terrible",
            "awful", "disgusting", "stupid", "idiot", "worst", "annoyed",
            "irritated", "frustrated", "ridiculous", "pathetic", "useless",
            "shut up", "get out", "leave me alone", "stop it", "enough",
            "damn", "hell", "outraged", "infuriated", "livid", "enraged",
            "upset", "fight", "attack", "destroy", "kill", "never again",
            "sick of", "fed up", "can't stand", "unbearable", "unacceptable",
            "toxic", "hostile", "aggressive", "violent", "rude", "disrespect",
        ],
    },
    "happy": {
        "emoji": "😊",
        "label": "Happy",
        "color": "#f39c12",
        "bg": "#fffbf0",
        "words": [
            "happy", "joyful", "excited", "love", "great", "wonderful", "amazing",
            "fantastic", "awesome", "brilliant", "excellent", "perfect", "beautiful",
            "good", "nice", "fun", "enjoy", "glad", "delighted", "thrilled",
            "cheerful", "smile", "laugh", "celebrate", "congratulations", "success",
            "grateful", "thankful", "blessed", "lucky", "positive", "incredible",
            "superb", "outstanding", "marvelous", "splendid", "yay", "hooray",
            "yes", "love it", "so good", "feel good", "best day", "can't wait",
            "overjoyed", "ecstatic", "elated", "bliss", "pleasure", "delight",
        ],
    },
    "sad": {
        "emoji": "😢",
        "label": "Sad",
        "color": "#2980b9",
        "bg": "#eaf4fb",
        "words": [
            "sad", "unhappy", "depressed", "cry", "crying", "tears", "grief",
            "sorrow", "heartbroken", "miserable", "lonely", "alone", "miss",
            "missing", "lost", "hopeless", "helpless", "disappointed", "hurt",
            "pain", "suffer", "suffering", "gloomy", "dark", "empty", "broken",
            "failure", "failed", "regret", "sorry", "unfortunate", "tragic",
            "terrible loss", "give up", "no hope", "devastated", "shattered",
            "melancholy", "despair", "mourning", "dead inside", "worthless",
            "nothing", "no one", "nobody cares", "tired", "exhausted", "done",
        ],
    },
    "neutral": {
        "emoji": "😐",
        "label": "Neutral",
        "color": "#7f8c8d",
        "bg": "#f4f6f7",
        "words": [
            "okay", "fine", "alright", "maybe", "perhaps", "normal", "usual",
            "regular", "so so", "neither", "whatever", "don't know", "not sure",
            "average", "standard", "medium", "moderate", "fair", "ordinary",
            "common", "typical", "routine", "nothing special", "just okay",
        ],
    },
}

# Intensity modifiers
INTENSIFIERS = ["very", "really", "so", "extremely", "absolutely", "totally", "completely", "super", "quite"]
NEGATORS     = ["not", "never", "no", "don't", "doesn't", "didn't", "isn't", "wasn't", "can't", "won't"]

# ─── Helpers ─────────────────────────────────────────────────────────────────
def transcribe_audio(audio_bytes: bytes) -> tuple[str, str]:
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
        return "", f"⚠️ Speech service error: {e}"
    except Exception as e:
        return "", f"❌ Error: {e}"


def normalize(text: str) -> str:
    return re.sub(r"[^\w\s]", "", text.lower()).strip()


def analyze_emotion(text: str) -> dict:
    """
    Keyword-based emotion detector.
    Returns {emotion, emoji, color, bg, label, scores, matched_words, confidence, transcript}
    """
    words = normalize(text).split()
    scores = {e: 0.0 for e in EMOTION_KEYWORDS}
    matched = {e: [] for e in EMOTION_KEYWORDS}

    i = 0
    while i < len(words):
        word = words[i]
        # Check 3-gram, 2-gram, 1-gram
        for n in (3, 2, 1):
            phrase = " ".join(words[i:i+n])
            for emotion, data in EMOTION_KEYWORDS.items():
                if phrase in data["words"]:
                    weight = 1.0
                    # Check preceding negator → flip to opposite
                    if i > 0 and words[i-1] in NEGATORS:
                        # negated happy → sad, negated sad → neutral, negated angry → neutral
                        flip = {"happy": "sad", "sad": "neutral", "angry": "neutral", "neutral": "neutral"}
                        emotion = flip.get(emotion, emotion)
                        weight = 0.8
                    # Check preceding intensifier → boost weight
                    elif i > 0 and words[i-1] in INTENSIFIERS:
                        weight = 1.6
                    elif i > 1 and words[i-2] in INTENSIFIERS:
                        weight = 1.4
                    scores[emotion] += weight * n          # longer phrase = more weight
                    matched[emotion].append(phrase)
                    i += n - 1
                    break
            else:
                continue
            break
        i += 1

    total = sum(scores.values())

    # If no keywords found, default to neutral
    if total == 0:
        scores["neutral"] = 1
        total = 1

    # Percentage breakdown
    pct = {e: round((s / total) * 100, 1) for e, s in scores.items()}
    top_emotion = max(scores, key=lambda e: scores[e])

    # Confidence: how dominant the top emotion is
    top_pct = pct[top_emotion]
    if top_pct >= 70:
        confidence = "High"
    elif top_pct >= 45:
        confidence = "Medium"
    else:
        confidence = "Low"

    return {
        "emotion":       top_emotion,
        "emoji":         EMOTION_KEYWORDS[top_emotion]["emoji"],
        "label":         EMOTION_KEYWORDS[top_emotion]["label"],
        "color":         EMOTION_KEYWORDS[top_emotion]["color"],
        "bg":            EMOTION_KEYWORDS[top_emotion]["bg"],
        "scores":        pct,
        "matched_words": matched,
        "confidence":    confidence,
        "transcript":    text,
    }


def intensity_bar(pct: float, color: str) -> str:
    return (
        f"<div style='background:#ecf0f1;border-radius:8px;height:18px;width:100%;overflow:hidden'>"
        f"<div style='background:{color};width:{pct}%;height:100%;border-radius:8px;"
        f"transition:width 0.5s ease'></div></div>"
    )


# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <style>
    .page-title {
        font-size:2rem; font-weight:800; letter-spacing:-0.5px;
        background:linear-gradient(90deg,#8e44ad,#e74c3c,#f39c12,#2980b9);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    }
    .emotion-card {
        border-radius:20px; text-align:center; padding:32px 24px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.10);
        animation: popIn 0.4s ease;
    }
    @keyframes popIn {
        0% { transform:scale(0.85); opacity:0; }
        100% { transform:scale(1); opacity:1; }
    }
    .big-emoji { font-size: 6rem; line-height:1.2; }
    .emotion-label { font-size:2rem; font-weight:800; margin-top:8px; }
    .confidence-tag {
        display:inline-block; padding:4px 14px; border-radius:20px;
        font-size:0.82rem; font-weight:700; margin-top:8px;
        background:rgba(0,0,0,0.10);
    }
    </style>
    <div class='page-title'>🎭 Speech Emotion Analyzer</div>
    """,
    unsafe_allow_html=True,
)
st.markdown("Speak freely — we'll detect the **emotion in your words** using smart keyword analysis. No paid API needed!")
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
left, right = st.columns([1, 2], gap="large")

with left:
    st.markdown("### 🎤 Record Your Speech")
    st.markdown("Click the mic, speak naturally, then stop.")

    audio_bytes = audio_recorder(
        text="",
        recording_color="#e74c3c",
        neutral_color="#8e44ad",
        icon_name="microphone",
        icon_size="4x",
        pause_threshold=3.0,
        sample_rate=16000,
        key="emotion_recorder",
    )

    st.markdown("---")
    st.markdown("#### 🎯 Emotion Legend")
    for emo, data in EMOTION_KEYWORDS.items():
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:10px;margin:6px 0'>"
            f"<span style='font-size:1.6rem'>{data['emoji']}</span>"
            f"<span style='color:{data['color']};font-weight:700;font-size:1rem'>{data['label'].upper()}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### 💡 Try saying things like:")
    st.caption('😡 Angry: I am so angry and frustrated right now!')
    st.caption('😊 Happy: This is amazing, I feel so happy and excited!')
    st.caption('😢 Sad: I feel sad and lonely, I miss everyone.')
    st.caption('😐 Neutral: I guess its okay, nothing special today.')

with right:
    if not audio_bytes:
        # Placeholder card
        st.markdown(
            """
            <div style='border-radius:20px;border:3px dashed #d5d8dc;padding:60px 40px;text-align:center;color:#aab7b8'>
                <div style='font-size:5rem'>🎭</div>
                <div style='font-size:1.3rem;font-weight:700;margin-top:16px'>Your emotion will appear here</div>
                <div style='margin-top:8px'>Record your speech using the mic on the left</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.audio(audio_bytes, format="audio/wav")

        with st.spinner("🔄 Transcribing & analyzing your emotion..."):
            transcript, error = transcribe_audio(audio_bytes)

        if error:
            st.error(error)
        elif transcript:
            result = analyze_emotion(transcript)

            # Save to history
            st.session_state.emotion_history.append(result)

            # ── Big Emotion Card ──────────────────────────────────────────
            st.markdown(
                f"""
                <div class='emotion-card' style='background:{result["bg"]};border:3px solid {result["color"]}'>
                    <div class='big-emoji'>{result["emoji"]}</div>
                    <div class='emotion-label' style='color:{result["color"]}'>{result["label"].upper()}</div>
                    <div class='confidence-tag' style='color:{result["color"]}'>
                        🎯 {result["confidence"]} Confidence
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ── Transcript ────────────────────────────────────────────────
            st.markdown("#### 📝 What you said:")
            st.info(f'*"{transcript}"*')

            # ── Emotion Breakdown Bars ────────────────────────────────────
            st.markdown("#### 📊 Emotion Score Breakdown")
            order = sorted(result["scores"], key=lambda e: result["scores"][e], reverse=True)
            for emo in order:
                pct = result["scores"][emo]
                data = EMOTION_KEYWORDS[emo]
                col_label, col_bar, col_pct = st.columns([2, 5, 1])
                with col_label:
                    st.markdown(
                        f"<span style='font-size:1.2rem'>{data['emoji']}</span> "
                        f"<span style='font-weight:600;color:{data['color']}'>{data['label']}</span>",
                        unsafe_allow_html=True,
                    )
                with col_bar:
                    st.markdown(intensity_bar(pct, data["color"]), unsafe_allow_html=True)
                    st.markdown("")
                with col_pct:
                    st.markdown(f"**{pct}%**")

            # ── Matched Keywords ──────────────────────────────────────────
            any_matched = any(result["matched_words"][e] for e in result["matched_words"])
            if any_matched:
                st.markdown("#### 🔍 Detected Keywords")
                tag_cols = st.columns(4)
                for i, (emo, words_found) in enumerate(result["matched_words"].items()):
                    if words_found:
                        data = EMOTION_KEYWORDS[emo]
                        with tag_cols[i % 4]:
                            st.markdown(
                                f"**{data['emoji']} {data['label']}**",
                                unsafe_allow_html=True,
                            )
                            for w in set(words_found):
                                st.markdown(
                                    f"<span style='background:{data['color']};color:white;"
                                    f"padding:2px 10px;border-radius:20px;font-size:0.8rem;"
                                    f"display:inline-block;margin:2px'>{w}</span>",
                                    unsafe_allow_html=True,
                                )

# ══════════════════════════════════════════════════════════════════════════════
# HISTORY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("### 📜 Emotion History (This Session)")

if not st.session_state.emotion_history:
    st.caption("No recordings yet. Record your first speech above!")
else:
    num = len(st.session_state.emotion_history)
    st.caption(f"{num} recording(s) this session")

    # Summary bar
    from collections import Counter
    counts = Counter(e["emotion"] for e in st.session_state.emotion_history)
    summary_cols = st.columns(4)
    for i, (emo, data) in enumerate(EMOTION_KEYWORDS.items()):
        with summary_cols[i]:
            st.markdown(
                f"<div style='text-align:center;background:{data['bg']};border:2px solid {data['color']};"
                f"border-radius:12px;padding:12px'>"
                f"<div style='font-size:2rem'>{data['emoji']}</div>"
                f"<div style='font-weight:700;color:{data['color']}'>{counts.get(emo,0)}x</div>"
                f"<div style='font-size:0.8rem;color:#7f8c8d'>{data['label']}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("")

    # Individual entries
    for i, entry in enumerate(reversed(st.session_state.emotion_history), 1):
        with st.expander(
            f"#{i} — {entry['emoji']} {entry['label']}  |  🎯 {entry['confidence']} confidence",
            expanded=(i == 1),
        ):
            st.markdown(f"**Said:** *\"{entry['transcript']}\"*")
            cols = st.columns(4)
            for j, (emo, data) in enumerate(EMOTION_KEYWORDS.items()):
                with cols[j]:
                    st.markdown(
                        f"<div style='text-align:center'>"
                        f"<div style='font-size:1.5rem'>{data['emoji']}</div>"
                        f"<div style='font-weight:700;color:{data['color']}'>{entry['scores'][emo]}%</div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

    st.markdown("")
    if st.button("🗑️ Clear History", type="secondary"):
        st.session_state.emotion_history = []
        st.rerun()
