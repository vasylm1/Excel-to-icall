# Generate updated Streamlit code with Apple-like minimalist UI and all previous logic
apple_ui_code = """
import streamlit as st
import pandas as pd
from datetime import datetime
import base64

st.set_page_config(page_title="Class Schedule Converter", layout="centered")

# Apple-like minimal CSS
st.markdown(\"""
<style>
body {
  background: #f8f9fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}
h1, h2 {
  color: #1c1c1e;
  font-weight: 600;
  padding-bottom: 0.5rem;
  text-align: center;
}
.stSelectbox, .stFileUploader, .stTextInput {
  background: #ffffff;
  border: 1px solid #d1d1d6;
  border-radius: 12px;
  padding: 0.6rem 1rem;
}
.stButton button, .stDownloadButton button {
  background: #007aff;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.6rem 1.2rem;
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.stDownloadButton button {
  background: #34c759;
}
a {
  color: #007aff;
  text-decoration: none;
}
</style>
\""", unsafe_allow_html=True)

lang = st.selectbox("🌍 Language / Język / Мова", ["English", "Polski", "Українська"])

text = {
    "English": {
        "title": "📅 Class Schedule Converter",
        "upload": "Select your schedule file:",
        "download": "Download ICS File",
        "success": "ICS file generated!",
        "about_title": "About",
        "about_1": "I'm a marketing professional with a background in office administration, technical support, and product marketing.",
        "about_2": "My work centers around supporting product launches, creating and maintaining marketing assets, and improving content quality using tools like Power BI, Excel, SAP, and Power Platform.",
        "about_3": "I speak Ukrainian, Polish, English, and German, and I'm learning Spanish and Chinese.",
        "about_4": "Outside of work, I'm passionate about travel, reading, exploring technology, staying active, and organizing events.",
        "linkedin": "LinkedIn Profile"
    },
    "Polski": {
        "title": "📅 Konwerter Planu Zajęć",
        "upload": "Wybierz plik z planem zajęć:",
        "download": "Pobierz plik ICS",
        "success": "Plik ICS został wygenerowany!",
        "about_title": "O mnie",
        "about_1": "Jestem specjalistą ds. marketingu z doświadczeniem w administracji biurowej, wsparciu technicznym oraz marketingu produktowym.",
        "about_2": "Moja praca koncentruje się na wsparciu wprowadzania produktów na rynek, tworzeniu i utrzymywaniu materiałów marketingowych oraz poprawie jakości treści przy użyciu narzędzi takich jak Power BI, Excel, SAP i Power Platform.",
        "about_3": "Posługuję się językiem ukraińskim, polskim, angielskim i niemieckim, a obecnie uczę się również hiszpańskiego i chińskiego.",
        "about_4": "Poza pracą pasjonuję się podróżami, czytaniem, nowymi technologiami, aktywnym stylem życia oraz organizacją wydarzeń.",
        "linkedin": "Profil LinkedIn"
    },
    "Українська": {
        "title": "📅 Конвертер Розкладу Занять",
        "upload": "Виберіть файл з розкладом:",
        "download": "Завантажити файл ICS",
        "success": "Файл ICS успішно згенеровано!",
        "about_title": "Про мене",
        "about_1": "Я маркетолог із досвідом у сфері офісного адміністрування, технічної підтримки та продуктового маркетингу.",
        "about_2": "Моя робота зосереджена на підтримці запусків продуктів, створенні та супроводі маркетингових матеріалів, а також на покращенні якості контенту за допомогою Power BI, Excel, SAP та Power Platform.",
        "about_3": "Володію українською, польською, англійською та німецькою мовами, а також вивчаю іспанську та китайську.",
        "about_4": "У вільний час захоплююся подорожами, читанням, новими технологіями, спортом і організацією заходів.",
        "linkedin": "Профіль LinkedIn"
    }
}[lang]

tab1, tab2 = st.tabs(["🛠 " + text["title"], "👤 " + text["about_title"]])

def format_datetime(value):
    if pd.isna(value): return ""
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%d.%m.%Y %H:%M").strftime("%Y%m%dT%H%M00")
        except:
            return ""
    if isinstance(value, (float, int)):
        try:
            parsed = pd.to_datetime("1899-12-30") + pd.to_timedelta(value, unit="D")
            return parsed.strftime("%Y%m%dT%H%M00")
        except:
            return ""
    if isinstance(value, datetime):
        return value.strftime("%Y%m%dT%H%M00")
    return ""

with tab1:
    st.header(text["title"])
    uploaded_file = st.file_uploader(text["upload"], type=["xls", "xlsx"])

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file, header=None)
            events = []
            for i, row in df.iterrows():
                if i == 0: continue
                start = format_datetime(row[0])
                end = format_datetime(row[1])
                summary = str(row[4]) if not pd.isna(row[4]) else ""
                description = "\\n".join(str(row[c]) for c in [6,7,8] if not pd.isna(row[c]))
                location = str(row[10]) if not pd.isna(row[10]) else ""
                if start and end and summary:
                    event = f"BEGIN:VEVENT\\nDTSTART:{start}\\nDTEND:{end}\\nSUMMARY:{summary}"
                    if description: event += f"\\nDESCRIPTION:{description}"
                    if location: event += f"\\nLOCATION:{location}"
                    event += "\\nEND:VEVENT"
                    events.append(event)

            ics = "BEGIN:VCALENDAR\\nVERSION:2.0\\nCALSCALE:GREGORIAN\\n" + "\\n".join(events) + "\\nEND:VCALENDAR"

            st.success(text["success"])
            b64 = base64.b64encode(ics.encode()).decode()
            href = f'<a href="data:text/calendar;charset=utf-8;base64,{b64}" download="class_schedule.ics"><button>{text["download"]}</button></a>'
            st.markdown(href, unsafe_allow_html=True)
            with st.expander("Preview .ics"):
                st.code(ics)

        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.header(text["about_title"])
    st.write(text["about_1"])
    st.write(text["about_2"])
    st.write(text["about_3"])
    st.write(text["about_4"])
    st.markdown(f'<a href="https://www.linkedin.com/in/vasyl-madei-399488247/" target="_blank">{text["linkedin"]}</a>', unsafe_allow_html=True)
"""

with open("/mnt/data/class_schedule_apple_ui.py", "w") as f:
    f.write(apple_ui_code)

"/mnt/data/class_schedule_apple_ui.py"