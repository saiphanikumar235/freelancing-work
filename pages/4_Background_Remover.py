import streamlit as st
from PIL import Image
import io
import base64
import time

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Background Remover", page_icon="🖼️", layout="wide")

# ─── Session State ────────────────────────────────────────────────────────────
if "original_image" not in st.session_state:
    st.session_state.original_image = None
if "result_image" not in st.session_state:
    st.session_state.result_image = None
if "bg_removed" not in st.session_state:
    st.session_state.bg_removed = False

# ─── Helper: Load rembg lazily ───────────────────────────────────────────────
@st.cache_resource(show_spinner="🤖 Loading AI background removal model (first time only)...")
def load_rembg_session():
    from rembg import new_session
    return new_session("u2net")   # u2net – best general-purpose local model


def remove_background(img: Image.Image) -> Image.Image:
    from rembg import remove
    session = load_rembg_session()
    return remove(img, session=session)


def pil_to_bytes(img: Image.Image, fmt="PNG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


def image_to_b64(img: Image.Image) -> str:
    return base64.b64encode(pil_to_bytes(img)).decode()


def checkerboard_bg_css():
    """CSS for transparent-area checkerboard preview."""
    return (
        "background-image: linear-gradient(45deg,#ccc 25%,transparent 25%),"
        "linear-gradient(-45deg,#ccc 25%,transparent 25%),"
        "linear-gradient(45deg,transparent 75%,#ccc 75%),"
        "linear-gradient(-45deg,transparent 75%,#ccc 75%);"
        "background-size:20px 20px;"
        "background-position:0 0,0 10px,10px -10px,-10px 0px;"
    )


# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <style>
    .page-title {
        font-size:2rem; font-weight:800;
        background:linear-gradient(90deg,#6c3483,#1a5276,#117a65);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    }
    .step-badge {
        display:inline-block; background:#1a5276; color:white;
        border-radius:50%; width:28px; height:28px; line-height:28px;
        text-align:center; font-weight:800; margin-right:8px; font-size:0.9rem;
    }
    .info-chip {
        display:inline-block; background:#eaf4fb; color:#1a5276;
        border:1px solid #aed6f1; border-radius:20px; padding:3px 12px;
        font-size:0.82rem; font-weight:600; margin:3px;
    }
    </style>
    <div class='page-title'>🖼️ Camera Background Remover</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<span class='info-chip'>✅ 100% Local Processing</span>"
    "<span class='info-chip'>🤖 U2Net AI Model</span>"
    "<span class='info-chip'>🔒 No Data Sent Online</span>"
    "<span class='info-chip'>💰 No Paid API</span>",
    unsafe_allow_html=True,
)
st.markdown("Capture a photo with your **device camera** or **upload an image**, and the AI will remove the background locally.")
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# INPUT SECTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### <span class='step-badge'>1</span> Provide Your Image", unsafe_allow_html=True)

input_method = st.radio(
    "Choose input method:",
    ["📷 Use Device Camera", "📂 Upload an Image"],
    horizontal=True,
    label_visibility="collapsed",
)

raw_image = None

if input_method == "📷 Use Device Camera":
    st.info("📷 Allow browser camera access when prompted. Click **Take Photo** to capture.")
    cam_img = st.camera_input("Take a photo", label_visibility="collapsed")
    if cam_img:
        raw_image = Image.open(cam_img).convert("RGBA")

else:
    uploaded = st.file_uploader(
        "Upload an image (JPG, PNG, WEBP)",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )
    if uploaded:
        raw_image = Image.open(uploaded).convert("RGBA")

# ══════════════════════════════════════════════════════════════════════════════
# PROCESS & RESULT
# ══════════════════════════════════════════════════════════════════════════════
if raw_image:
    st.session_state.original_image = raw_image
    st.session_state.bg_removed = False
    st.session_state.result_image = None

if st.session_state.original_image:
    st.markdown("---")
    st.markdown("### <span class='step-badge'>2</span> Preview & Remove Background", unsafe_allow_html=True)

    col_orig, col_result = st.columns(2, gap="large")

    with col_orig:
        st.markdown("#### 🖼️ Original Image")
        st.image(st.session_state.original_image, use_container_width=True)
        orig_bytes = pil_to_bytes(st.session_state.original_image.convert("RGB"), "JPEG")
        st.caption(f"Size: {st.session_state.original_image.width} × {st.session_state.original_image.height} px")

    with col_result:
        st.markdown("#### ✂️ Background Removed")

        if not st.session_state.bg_removed:
            st.markdown(
                "<div style='border:3px dashed #aab7b8;border-radius:16px;padding:60px 20px;"
                "text-align:center;color:#aab7b8;font-size:1.1rem'>"
                "🪄 Click <b>Remove Background</b> below to process"
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            result = st.session_state.result_image
            # Show with checkerboard to visualise transparency
            b64 = image_to_b64(result)
            st.markdown(
                f"<div style='{checkerboard_bg_css()}border-radius:16px;overflow:hidden;'>"
                f"<img src='data:image/png;base64,{b64}' style='width:100%;display:block'/>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.caption(f"Output: {result.width} × {result.height} px  |  Transparent background (PNG)")

    # ── Remove Button ─────────────────────────────────────────────────────────
    st.markdown("")
    btn_col, tip_col = st.columns([1, 3])
    with btn_col:
        remove_btn = st.button(
            "🪄 Remove Background",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.bg_removed,
        )
    with tip_col:
        st.markdown(
            "<div style='padding-top:8px;color:#7f8c8d;font-size:0.88rem'>"
            "⏱️ First run downloads the U2Net model (~170 MB). Subsequent runs are instant."
            "</div>",
            unsafe_allow_html=True,
        )

    if remove_btn:
        with st.spinner("🤖 AI is removing the background... please wait"):
            try:
                result_img = remove_background(st.session_state.original_image.convert("RGBA"))
                st.session_state.result_image = result_img
                st.session_state.bg_removed = True
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to remove background: {e}")

    # ══════════════════════════════════════════════════════════════════════════
    # DOWNLOAD & CUSTOMISE
    # ══════════════════════════════════════════════════════════════════════════
    if st.session_state.bg_removed and st.session_state.result_image:
        result = st.session_state.result_image
        st.markdown("---")
        st.markdown("### <span class='step-badge'>3</span> Download & Customise", unsafe_allow_html=True)

        tab_dl, tab_bg, tab_compare = st.tabs([
            "⬇️ Download",
            "🎨 Custom Background",
            "🔍 Side-by-Side Compare",
        ])

        # ── Download Tab ───────────────────────────────────────────────────
        with tab_dl:
            st.markdown("#### Download the processed image")

            dl_col1, dl_col2, dl_col3 = st.columns(3)

            with dl_col1:
                st.markdown("**PNG (Transparent)**")
                st.caption("Best for web, keeps transparency")
                png_bytes = pil_to_bytes(result, "PNG")
                st.download_button(
                    label="⬇️ Download PNG",
                    data=png_bytes,
                    file_name="background_removed.png",
                    mime="image/png",
                    use_container_width=True,
                    type="primary",
                )

            with dl_col2:
                st.markdown("**JPG (White Background)**")
                st.caption("Smaller file, white fill behind object")
                jpg_canvas = Image.new("RGB", result.size, (255, 255, 255))
                jpg_canvas.paste(result, mask=result.split()[3])
                jpg_bytes = pil_to_bytes(jpg_canvas, "JPEG")
                st.download_button(
                    label="⬇️ Download JPG",
                    data=jpg_bytes,
                    file_name="background_removed_white.jpg",
                    mime="image/jpeg",
                    use_container_width=True,
                )

            with dl_col3:
                st.markdown("**JPG (Black Background)**")
                st.caption("Smaller file, dark fill behind object")
                blk_canvas = Image.new("RGB", result.size, (0, 0, 0))
                blk_canvas.paste(result, mask=result.split()[3])
                blk_bytes = pil_to_bytes(blk_canvas, "JPEG")
                st.download_button(
                    label="⬇️ Download JPG",
                    data=blk_bytes,
                    file_name="background_removed_black.jpg",
                    mime="image/jpeg",
                    use_container_width=True,
                )

        # ── Custom Background Tab ──────────────────────────────────────────
        with tab_bg:
            st.markdown("#### Place your object on a custom background")

            bg_option = st.radio(
                "Background type:",
                ["🎨 Solid Color", "🖼️ Custom Image"],
                horizontal=True,
            )

            if bg_option == "🎨 Solid Color":
                picked = st.color_picker("Pick a background color", "#3498db")
                # Convert hex to RGB
                h = picked.lstrip("#")
                rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                bg_canvas = Image.new("RGB", result.size, rgb)
                bg_canvas.paste(result, mask=result.split()[3])

                b64c = image_to_b64(bg_canvas)
                st.markdown(
                    f"<img src='data:image/png;base64,{b64c}' "
                    f"style='width:100%;border-radius:12px;margin-top:12px'/>",
                    unsafe_allow_html=True,
                )
                custom_bytes = pil_to_bytes(bg_canvas, "JPEG")
                st.download_button(
                    "⬇️ Download with Color Background",
                    data=custom_bytes,
                    file_name="custom_background.jpg",
                    mime="image/jpeg",
                    type="primary",
                )

            else:  # Custom Image background
                bg_upload = st.file_uploader(
                    "Upload a background image",
                    type=["jpg", "jpeg", "png"],
                    key="bg_upload",
                )
                if bg_upload:
                    bg_img = Image.open(bg_upload).convert("RGB")
                    bg_img = bg_img.resize(result.size, Image.LANCZOS)
                    bg_canvas = bg_img.copy()
                    bg_canvas.paste(result, mask=result.split()[3])

                    b64c = image_to_b64(bg_canvas)
                    st.markdown(
                        f"<img src='data:image/png;base64,{b64c}' "
                        f"style='width:100%;border-radius:12px;margin-top:12px'/>",
                        unsafe_allow_html=True,
                    )
                    custom_bytes = pil_to_bytes(bg_canvas, "JPEG")
                    st.download_button(
                        "⬇️ Download with Custom Background",
                        data=custom_bytes,
                        file_name="custom_background.jpg",
                        mime="image/jpeg",
                        type="primary",
                    )
                else:
                    st.info("Upload a background image above to composite your object onto it.")

        # ── Compare Tab ────────────────────────────────────────────────────
        with tab_compare:
            st.markdown("#### Original vs Processed — side-by-side")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Before**")
                st.image(st.session_state.original_image, use_container_width=True)
            with c2:
                st.markdown("**After (transparent background)**")
                b64r = image_to_b64(result)
                st.markdown(
                    f"<div style='{checkerboard_bg_css()}border-radius:8px;overflow:hidden;'>"
                    f"<img src='data:image/png;base64,{b64r}' style='width:100%;display:block'/>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    # Reset button
    st.markdown("---")
    if st.button("🔄 Start Over / New Image", type="secondary"):
        st.session_state.original_image = None
        st.session_state.result_image = None
        st.session_state.bg_removed = False
        st.rerun()

else:
    # Empty state
    st.markdown(
        """
        <div style='border:3px dashed #d5d8dc;border-radius:20px;padding:60px;text-align:center;color:#aab7b8;margin-top:20px'>
            <div style='font-size:5rem'>📷</div>
            <div style='font-size:1.4rem;font-weight:700;margin-top:16px'>No image yet</div>
            <div style='margin-top:8px'>Use your camera or upload a file above to get started</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
