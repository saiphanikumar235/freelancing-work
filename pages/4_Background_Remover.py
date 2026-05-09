import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import base64

st.set_page_config(page_title="Background Remover", page_icon="🖼️", layout="wide")

for key, default in [("original_image", None), ("result_image", None), ("bg_removed", False)]:
    if key not in st.session_state:
        st.session_state[key] = default

def remove_background_grabcut(pil_image, iterations=10):
    img_rgb = np.array(pil_image.convert("RGB"))
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    h, w = img_bgr.shape[:2]
    margin_x = int(w * 0.05)
    margin_y = int(h * 0.05)
    rect = (margin_x, margin_y, w - 2 * margin_x, h - 2 * margin_y)
    mask = np.zeros((h, w), np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(img_bgr, mask, rect, bgd_model, fgd_model, iterations, cv2.GC_INIT_WITH_RECT)
    fg_mask = np.where((mask == 2) | (mask == 0), 0, 255).astype(np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel, iterations=3)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    fg_mask = cv2.GaussianBlur(fg_mask, (9, 9), 0)
    img_rgba = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2BGRA)
    img_rgba[:, :, 3] = fg_mask
    return Image.fromarray(cv2.cvtColor(img_rgba, cv2.COLOR_BGRA2RGBA))

def pil_to_bytes(img, fmt="PNG"):
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()

def image_to_b64(img):
    return base64.b64encode(pil_to_bytes(img)).decode()

def checker():
    return (
        "background-image:linear-gradient(45deg,#ccc 25%,transparent 25%),"
        "linear-gradient(-45deg,#ccc 25%,transparent 25%),"
        "linear-gradient(45deg,transparent 75%,#ccc 75%),"
        "linear-gradient(-45deg,transparent 75%,#ccc 75%);"
        "background-size:20px 20px;"
        "background-position:0 0,0 10px,10px -10px,-10px 0;"
    )

st.markdown("""
<style>
.page-title{font-size:2rem;font-weight:900;background:linear-gradient(90deg,#6c3483,#1a5276,#117a65);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.chip{display:inline-block;padding:3px 12px;border-radius:20px;font-size:0.8rem;font-weight:700;margin:3px;}
.step-badge{display:inline-block;background:#1a5276;color:white;border-radius:50%;
width:28px;height:28px;line-height:28px;text-align:center;font-weight:800;margin-right:8px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='page-title'>🖼️ Camera Background Remover</div>", unsafe_allow_html=True)
st.markdown(
    "<span class='chip' style='background:#eafaf1;color:#1e8449'>✅ 100% Local</span>"
    "<span class='chip' style='background:#eaf4fb;color:#1a5276'>🤖 OpenCV GrabCut</span>"
    "<span class='chip' style='background:#f5eef8;color:#6c3483'>🔒 No Model Download</span>"
    "<span class='chip' style='background:#fef9e7;color:#9a7d0a'>💰 No Paid API</span>",
    unsafe_allow_html=True,
)
st.markdown("Capture or upload an image — background removed **instantly** using OpenCV GrabCut. No internet or model download needed.")
st.markdown("---")

st.markdown("<div><span class='step-badge'>1</span><b>Provide Your Image</b></div>", unsafe_allow_html=True)
st.markdown("")

tab_cam, tab_up = st.tabs(["📷 Use Device Camera", "📂 Upload Image"])
raw_image = None

with tab_cam:
    st.info("Click **Take Photo** below. Allow camera access if prompted.")
    cam = st.camera_input("Camera", label_visibility="collapsed")
    if cam:
        raw_image = Image.open(cam).convert("RGB")

with tab_up:
    uploaded = st.file_uploader("Upload JPG / PNG / WEBP", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
    if uploaded:
        raw_image = Image.open(uploaded).convert("RGB")

if raw_image is not None:
    st.session_state.original_image = raw_image
    st.session_state.bg_removed = False
    st.session_state.result_image = None

if st.session_state.original_image:
    st.markdown("---")
    st.markdown("<div><span class='step-badge'>2</span><b>Preview & Remove Background</b></div>", unsafe_allow_html=True)
    st.markdown("")

    col_orig, col_result = st.columns(2, gap="large")

    with col_orig:
        st.markdown("#### 🖼️ Original Image")
        st.image(st.session_state.original_image, use_container_width=True)
        w, h = st.session_state.original_image.size
        st.caption("Size: " + str(w) + " x " + str(h) + " px")

    with col_result:
        st.markdown("#### ✂️ Background Removed")
        if not st.session_state.bg_removed:
            st.markdown(
                "<div style='border:3px dashed #aab7b8;border-radius:16px;"
                "padding:80px 20px;text-align:center;color:#aab7b8;font-size:1rem'>"
                "🪄 Click <b>Remove Background</b> below to process</div>",
                unsafe_allow_html=True,
            )
        else:
            result = st.session_state.result_image
            b64 = image_to_b64(result)
            st.markdown(
                "<div style='" + checker() + "border-radius:12px;overflow:hidden'>"
                "<img src='data:image/png;base64," + b64 + "' style='width:100%;display:block'/></div>",
                unsafe_allow_html=True,
            )
            st.caption("Output: " + str(result.width) + " x " + str(result.height) + " px | Transparent PNG")

    st.markdown("")
    iterations = 10
    with st.expander("⚙️ Advanced Settings"):
        iterations = st.slider("GrabCut Iterations (higher = sharper edges)", 3, 20, 10)
        st.caption("Default 10 is ideal for most portraits and objects with clear foreground.")

    bcol, hcol = st.columns([1, 3])
    with bcol:
        remove_btn = st.button("🪄 Remove Background", type="primary", use_container_width=True, disabled=st.session_state.bg_removed)
    with hcol:
        st.markdown("<div style='padding-top:10px;color:#7f8c8d;font-size:0.88rem'>⚡ Instant — no download. Best with subject centred in frame.</div>", unsafe_allow_html=True)

    if remove_btn:
        with st.spinner("🤖 Removing background..."):
            try:
                result_img = remove_background_grabcut(st.session_state.original_image, iterations=iterations)
                st.session_state.result_image = result_img
                st.session_state.bg_removed = True
                st.rerun()
            except Exception as e:
                st.error("Processing failed: " + str(e))

    if st.session_state.bg_removed and st.session_state.result_image:
        result = st.session_state.result_image
        st.markdown("---")
        st.markdown("<div><span class='step-badge'>3</span><b>Download & Customise</b></div>", unsafe_allow_html=True)
        st.markdown("")

        tab_dl, tab_bg, tab_cmp = st.tabs(["⬇️ Download", "🎨 Custom Background", "🔍 Compare"])

        with tab_dl:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**PNG — Transparent**")
                st.download_button("⬇️ Download PNG", data=pil_to_bytes(result, "PNG"),
                    file_name="bg_removed.png", mime="image/png", use_container_width=True, type="primary")
            with c2:
                st.markdown("**JPG — White BG**")
                cw = Image.new("RGB", result.size, (255,255,255))
                cw.paste(result, mask=result.split()[3])
                st.download_button("⬇️ Download JPG", data=pil_to_bytes(cw, "JPEG"),
                    file_name="bg_white.jpg", mime="image/jpeg", use_container_width=True)
            with c3:
                st.markdown("**JPG — Black BG**")
                cb = Image.new("RGB", result.size, (0,0,0))
                cb.paste(result, mask=result.split()[3])
                st.download_button("⬇️ Download JPG", data=pil_to_bytes(cb, "JPEG"),
                    file_name="bg_black.jpg", mime="image/jpeg", use_container_width=True)

        with tab_bg:
            bg_type = st.radio("Background type:", ["🎨 Solid Color", "🖼️ Upload Image"], horizontal=True)
            if bg_type == "🎨 Solid Color":
                hex_c = st.color_picker("Pick a color", "#3498db")
                h_val = hex_c.lstrip("#")
                rgb_c = tuple(int(h_val[i:i+2], 16) for i in (0, 2, 4))
                cc = Image.new("RGB", result.size, rgb_c)
                cc.paste(result, mask=result.split()[3])
                b64c = image_to_b64(cc)
                st.markdown("<img src='data:image/png;base64," + b64c + "' style='width:100%;border-radius:12px;margin-top:10px'/>", unsafe_allow_html=True)
                st.download_button("⬇️ Download", data=pil_to_bytes(cc,"JPEG"), file_name="color_bg.jpg", mime="image/jpeg", type="primary")
            else:
                bf = st.file_uploader("Upload background image", type=["jpg","jpeg","png"], key="bg_upload")
                if bf:
                    bi = Image.open(bf).convert("RGB").resize(result.size, Image.LANCZOS)
                    bi.paste(result, mask=result.split()[3])
                    b64i = image_to_b64(bi)
                    st.markdown("<img src='data:image/png;base64," + b64i + "' style='width:100%;border-radius:12px;margin-top:10px'/>", unsafe_allow_html=True)
                    st.download_button("⬇️ Download", data=pil_to_bytes(bi,"JPEG"), file_name="custom_bg.jpg", mime="image/jpeg", type="primary")
                else:
                    st.info("Upload a background image above.")

        with tab_cmp:
            cc1, cc2 = st.columns(2)
            with cc1:
                st.markdown("**Before**")
                st.image(st.session_state.original_image, use_container_width=True)
            with cc2:
                st.markdown("**After**")
                b64r = image_to_b64(result)
                st.markdown(
                    "<div style='" + checker() + "border-radius:8px;overflow:hidden'>"
                    "<img src='data:image/png;base64," + b64r + "' style='width:100%;display:block'/></div>",
                    unsafe_allow_html=True,
                )

    st.markdown("---")
    if st.button("🔄 Start Over / New Image", type="secondary"):
        st.session_state.original_image = None
        st.session_state.result_image = None
        st.session_state.bg_removed = False
        st.rerun()
else:
    st.markdown(
        "<div style='border:3px dashed #d5d8dc;border-radius:20px;padding:60px;"
        "text-align:center;color:#aab7b8;margin-top:20px'>"
        "<div style='font-size:5rem'>📷</div>"
        "<div style='font-size:1.4rem;font-weight:700;margin-top:16px'>No image yet</div>"
        "<div style='margin-top:8px'>Use your camera or upload a file above</div></div>",
        unsafe_allow_html=True,
    )
