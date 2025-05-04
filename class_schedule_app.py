import streamlit as st
import pandas as pd
from datetime import datetime
import base64

st.set_page_config(page_title="Class Schedule Converter", layout="centered")

# CSS styling (modern design)
st.markdown("""
<style>
body {
  background: linear-gradient(135deg, #f5f7fa 0%, #dfe7f5 100%);
  font-family: 'Segoe UI', sans-serif;
}
h1, h2 {
  background: linear-gradient(45deg, #4361ee, #3f37c9);
  color: white;
  padding: 1rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
.stButton button, .stDownloadButton button {
  background: linear-gradient(45deg, #4361ee, #3f37c9);
  color: white;
  font-weight: bold;
  border-radius: 8px;
  padding: 0.6rem 1.2rem;
  margin-top: 1rem;
  border: none;
}
.stDownloadButton button {
  background: linear-gradient(45deg, #2ecc71, #27ae60);
}
</style>
""", unsafe_allow_html=True)

# Language options and translations
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
        "about_3": "I speak Ukrainian, Polish, English, and German, and I'm learning Spanish and Chinese. I enjoy working in international environments and collaborating across teams.",
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
        "about_3": "Володію українською, польською, англійською та німецькою мовами, а також вивчаю іспанську та китайську. Мені подобається працювати в міжнародному середовищі та співпрацювати з різними командами.",
        "about_4": "У вільний час захоплююся подорожами, читанням, новими технологіями, спортом і організацією заходів.",
        "linkedin": "Профіль LinkedIn"
    }
}[lang]

tab1, tab2 = st.tabs(["🛠 " + text["title"], "👤 " + text["about_title"]])

with tab1:
    st.header(text["title"])
    uploaded_file = st.file_uploader(text["upload"], type=["xls", "xlsx"])

    def format_datetime(value):
        if pd.isna(value): return ""
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d.%m.%Y %H:%M").strftime("%Y%m%dT%H%M00")
            except:
                return ""
        if isinstance(value, (float, int)):
            try:
                return (pd.to_datetime("1899-12-30") + pd.to_timedelta(value, unit="D")).strftime("%Y%m%dT%H%M00")
            except:
                return ""
        if isinstance(value, datetime):
            return value.strftime("%Y%m%dT%H%M00")
        return ""

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
                    event = f"""BEGIN:VEVENT
DTSTART:{start}
DTEND:{end}
SUMMARY:{summary}"""
                    if description: event += f"\nDESCRIPTION:{description}"
                    if location: event += f"\nLOCATION:{location}"
                    event += "\nEND:VEVENT"
                    events.append(event)

            ics = "BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\n" + "\n".join(events) + "\nEND:VCALENDAR"

            st.success(text["success"])

            b64 = base64.b64encode(ics.encode()).decode()
            href = f'<a href="data:text/calendar;charset=utf-8;base64,{b64}" download="class_schedule.ics"><button class="stDownloadButton">{text["download"]}</button></a>'
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
    st.markdown(f'<a href="https://www.linkedin.com/in/vasyl-madei-399488247/" target="_blank"><button class="stButton">{text["linkedin"]}</button></a>', unsafe_allow_html=True)
