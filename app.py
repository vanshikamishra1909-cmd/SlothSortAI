import json
import shutil
from pathlib import Path

import requests
import streamlit as st

# ---------- APP CONFIG ----------
st.set_page_config(
    page_title="SlothSort AI | Smart File Organizer",
    page_icon="🦥",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL = "qwen2.5:3b"

CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".json", ".sql"],
}

ICONS = {
    "Documents": "📄",
    "Images": "🖼️",
    "Videos": "🎬",
    "Audio": "🎵",
    "Spreadsheets": "📊",
    "Presentations": "📽️",
    "Archives": "🗜️",
    "Code": "💻",
    "Other": "📦",
}

# ---------- DARK FOREST BRAND ----------
st.markdown("""
<style>
.stApp {
    background: #101713;
    color: #f1f5f2;
}
[data-testid="stHeader"] {
    background: #101713;
}
[data-testid="stSidebar"] {
    background: #18231c;
}
h1, h2, h3 {
    color: #a7e3b5 !important;
}
.stApp p, .stApp label, .stApp li,
.stApp [data-testid="stMarkdownContainer"] {
    color: #e5eee7;
}
[data-testid="stMetric"] {
    background: #1b2920;
    border: 1px solid #354b3b;
    padding: 16px;
    border-radius: 14px;
}
[data-testid="stMetricValue"] {
    color: #a7e3b5;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #35483b;
    border-radius: 12px;
}
.stButton > button {
    background: #34764d;
    color: #ffffff !important;
    border: 1px solid #5ca775;
    border-radius: 10px;
    min-height: 42px;
}
.stButton > button:hover {
    background: #438d5e;
    border-color: #a7e3b5;
}
input, textarea, [data-baseweb="input"] {
    color: #ffffff !important;
}
.hero {
    background: linear-gradient(120deg, #1b3324, #243e2d);
    padding: 26px;
    border: 1px solid #42634b;
    border-radius: 18px;
    margin-bottom: 20px;
}
.hero-title {
    font-size: 2.25rem;
    font-weight: 800;
    color: #b9edc4;
}
.hero-sub {
    color: #e0eee3;
    font-size: 1.05rem;
}
.small-note {
    color: #bdc9c0;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)


# ---------- HELPERS ----------
def categorize(filename):
    extension = Path(filename).suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Other"


def ai_advice(filenames):
    prompt = (
        "You are SlothSort AI, a cautious file organization assistant. "
        "Give concise advice based only on these filenames. "
        "Do not claim to know their contents. "
        "Do not suggest deleting files. Use readable bullet points.\n"
        + json.dumps(filenames, ensure_ascii=False)
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()
    return response.json()["response"]


def unique_destination(path):
    """Choose a destination without overwriting an existing file."""
    if not path.exists():
        return path

    number = 1
    while True:
        candidate = path.with_name(
            f"{path.stem}_copy{number}{path.suffix}"
        )
        if not candidate.exists():
            return candidate
        number += 1


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("# 🦥 SlothSort AI")
    st.caption("Your personal file-organizing sloth")
    st.divider()

    st.markdown("### 🌿 Our promise")
    st.write("Less clutter. Less effort. More peace of mind.")

    st.markdown("### 🧠 AI engine")
    st.code(MODEL, language="text")
    st.caption("Powered by local Ollama inference.")

    st.markdown("### 🛡️ Safety first")
    st.write(
        "Original files stay untouched. "
        "You review the plan before copying."
    )

    st.divider()
    st.caption("Open-source friendly · Made for a calmer digital life")


# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <div class="hero-title">🦥 SlothSort AI</div>
    <div class="hero-sub">
        Your files are a mess. Let the sloth handle it.
    </div>
    <p class="small-note">
        A local-first AI file organizer that helps you sort
        digital clutter at your own pace.
    </p>
</div>
""", unsafe_allow_html=True)

st.info(
    "🔒 Privacy-minded by design: filenames are sent to your local "
    "Ollama service, not a cloud AI API. Keep the app and model "
    "running locally for this workflow."
)

# ---------- FOLDER SCAN ----------
st.header("📂 Your workspace")

folder_text = st.text_input(
    "Folder to organize",
    placeholder=r"C:\Users\YourName\Downloads",
    help="Start with a test folder containing copies of unimportant files.",
)

if st.button("🔍 Scan folder", use_container_width=True):
    folder = Path(folder_text.strip().strip('"')).expanduser()

    if not folder.is_dir():
        st.error("Please enter a valid folder path.")
    else:
        try:
            found = sorted(
                [p for p in folder.iterdir() if p.is_file()],
                key=lambda p: p.name.lower(),
            )

            st.session_state["source"] = str(folder.resolve())
            st.session_state["plan"] = [
                {
                    "name": p.name,
                    "category": categorize(p.name),
                }
                for p in found
            ]
            st.session_state["scanned"] = True
            st.session_state.pop("ai_advice", None)
            st.session_state.pop("copy_report", None)

            st.success(f"Scan complete — {len(found)} files found.")

        except OSError as exc:
            st.error(f"Could not scan the folder: {exc}")


# ---------- DASHBOARD ----------
if st.session_state.get("scanned"):
    source = Path(st.session_state["source"])
    plan = st.session_state["plan"]

    counts = {}
    for item in plan:
        counts[item["category"]] = counts.get(item["category"], 0) + 1

    st.header("📈 Your file overview")

    m1, m2, m3 = st.columns(3)
    m1.metric("Total files", len(plan))
    m2.metric("Categories used", len(counts))
    m3.metric("Originals protected", "Yes")

    st.subheader("🗂️ Category breakdown")

    if counts:
        columns = st.columns(3)
        for index, category in enumerate(sorted(counts)):
            with columns[index % 3]:
                st.markdown(
                    f"{ICONS.get(category, '📁')} **{category}**"
                )
                st.metric("Files", counts[category])
    else:
        st.write("This folder is empty. Scan another folder to begin.")

    # ---------- AI ----------
    st.divider()
    st.header("🧠 Your local AI assistant")

    st.write(
        "Ask your local model for organization advice based on "
        "filenames only."
    )

    if plan and st.button("✨ Generate AI suggestions"):
        try:
            with st.spinner("The sloth is thinking..."):
                result = ai_advice([item["name"] for item in plan])

            st.session_state["ai_advice"] = result

        except requests.RequestException:
            st.error(
                "Could not connect to Ollama. Make sure Ollama is running "
                "and the selected model is installed."
            )

    if st.session_state.get("ai_advice"):
        with st.container(border=True):
            st.markdown("### 🦥 Sloth's recommendations")
            st.markdown(st.session_state["ai_advice"])

    # ---------- EDITABLE PREVIEW ----------
    st.divider()
    st.header("👀 Review your organization plan")

    st.write(
        "Change any category before copying. Nothing is moved or renamed "
        "in the original folder."
    )

    available = list(CATEGORIES.keys()) + ["Other"]

    for index, item in enumerate(plan):
        with st.container(border=True):
            left, right = st.columns([3, 2])

            with left:
                st.write(f"{ICONS.get(item['category'], '📦')} **{item['name']}**")

            with right:
                item["category"] = st.selectbox(
                    "Category",
                    available,
                    index=available.index(item["category"]),
                    key=f"category_{index}",
                )

    st.session_state["plan"] = plan

    # ---------- SAFE COPY ----------
    st.divider()
    st.header("📁 Create organized copies")

    default_destination = source.parent / f"{source.name}_Organized"

    destination_text = st.text_input(
        "Destination folder",
        value=str(default_destination),
        help="Choose a separate folder outside the source folder.",
    )

    destination = Path(destination_text.strip().strip('"')).expanduser()

    st.caption(
        "Files are copied into category subfolders. Existing destination "
        "files are not overwritten; conflicts receive a numbered suffix."
    )

    confirmed = st.checkbox(
        "I have reviewed the plan and approve copying these files."
    )

    if st.button("🚀 Organize my copies", use_container_width=True):
        if not plan:
            st.warning("No files are available to copy.")
        elif not confirmed:
            st.warning("Please confirm the plan first.")
        elif not destination_text.strip():
            st.error("Enter a destination folder.")
        else:
            try:
                src = source.resolve()
                dst = destination.resolve()

                if (
                    dst == src
                    or src in dst.parents
                    or dst in src.parents
                ):
                    st.error(
                        "Choose a separate destination outside the source "
                        "folder and its parent tree."
                    )
                else:
                    missing = [
                        item["name"]
                        for item in plan
                        if not (source / item["name"]).is_file()
                    ]

                    if missing:
                        st.error(
                            "Some source files changed or disappeared. "
                            "Please scan the folder again."
                        )
                    else:
                        completed = 0
                        errors = []

                        progress = st.progress(0)

                        for index, item in enumerate(plan):
                            original = source / item["name"]
                            target_folder = dst / item["category"]

                            try:
                                target_folder.mkdir(
                                    parents=True,
                                    exist_ok=True,
                                )

                                target = unique_destination(
                                    target_folder / original.name
                                )

                                shutil.copy2(original, target)
                                completed += 1

                            except OSError as exc:
                                errors.append(f"{item['name']}: {exc}")

                            progress.progress(
                                (index + 1) / len(plan)
                            )

                        st.session_state["copy_report"] = {
                            "completed": completed,
                            "total": len(plan),
                            "destination": str(dst),
                            "errors": errors,
                        }

                        st.success(
                            f"Copied {completed} of {len(plan)} files. "
                            "Originals remain in the source folder."
                        )

                        st.write(f"**Destination:** `{dst}`")

                        if errors:
                            st.warning(
                                "Some files could not be copied:\n\n"
                                + "\n".join(errors)
                            )
                        elif completed:
                            st.balloons()

            except OSError as exc:
                st.error(f"Organization failed: {exc}")

    report = st.session_state.get("copy_report")
    if report:
        st.caption(
            f"Last copy report: {report['completed']}/{report['total']} "
            "files copied."
        )

st.divider()
st.markdown(
    "<p style='text-align:center;color:#a7e3b5;'>"
    "🦥 SlothSort AI · Slow down. Sort smarter. "
    "Keep your originals safe.</p>",
    unsafe_allow_html=True,
)