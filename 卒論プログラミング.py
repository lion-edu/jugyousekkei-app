import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="授業設計サポート", layout="wide")
st.title("授業設計サポートアプリ")

# ========= Google Sheets の設定 =========

# 教員メモを保存するスプレッドシートIDとシート名
MEMO_SPREADSHEET_ID = "あなたのメモ用スプレッドシートID"
MEMO_SHEET_NAME = "シート1"  # 実際のシート名に変更

# サービスアカウント情報を Streamlit Secrets から取得
def get_gspread_client():
    credentials_info = st.secrets["gcp_service_account"]
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
    gc = gspread.authorize(credentials)
    return gc

# ========= データ読み込み =========

official_url = "https://docs.google.com/spreadsheets/d/1nuy7U8iEYxfAvsQMAJD6j25zy5ht4v7leveIjskvXI0/export?format=csv&gid=0"
memo_url = "https://docs.google.com/spreadsheets/d/1y3RhipP1vlK1esFUeAypQnyQ7JWH58yau7Sv4gH0Wjo/export?format=csv&gid=0"

@st.cache_data
def load_data():
    official = pd.read_csv(official_url)
    memo = pd.read_csv(memo_url)
    return official, memo

official_df, memo_df = load_data()

# ========= 見た目用の関数 =========

def format_bullets(text):
    lines = str(text).split("\n")
    bullets = [f"・{line}" for line in lines if line.strip() != ""]
    return "<br>".join(bullets)

def card(title, content):
    st.markdown(
        f"""
        <div style="
            background-color: #F9FAFB;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 14px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        ">
            <h4 style="margin-bottom:8px;">{title}</h4>
            <div>{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ========= 選択 UI =========

st.subheader("① 校種・学年を選択")

col1, col2 = st.columns(2)
with col1:
    school = st.selectbox("校種", sorted(official_df["校種"].unique()))
with col2:
    grade = st.selectbox(
        "学年",
        sorted(official_df[official_df["校種"] == school]["学年"].unique())
    )

st.subheader("② 単元・小単元・本時を選択")

filtered_grade = official_df[
    (official_df["校種"] == school) &
    (official_df["学年"] == grade)
]

col3, col4, col5 = st.columns(3)
with col3:
    unit = st.selectbox("単元", sorted(filtered_grade["単元"].unique()))
with col4:
    subunit = st.selectbox(
        "小単元",
        sorted(filtered_grade[filtered_grade["単元"] == unit]["小単元"].unique())
    )
with col5:
    lesson = st.selectbox(
        "本時の学習内容",
        sorted(
            filtered_grade[
                filtered_grade["小単元"] == subunit
            ]["本時の学習内容"].unique()
        )
    )

selected = filtered_grade[
    (filtered_grade["単元"] == unit) &
    (filtered_grade["小単元"] == subunit) &
    (filtered_grade["本時の学習内容"] == lesson)
].iloc[0]

memo_match = memo_df[
    (memo_df["小単元"] == subunit) &
    (memo_df["本時の学習内容"] == lesson)
]

# ========= タブ =========

tab1, tab2 = st.tabs(["📘 公式データ", "📝 教員メモ"])

# ----- タブ1：公式データ -----
with tab1:
    st.subheader("📘 学習指導要領（公式）")

    card("ねらい（最終到達目標）", format_bullets(selected["ねらい(最終到達目標)"]))
    card("既習内容", format_bullets(selected["既習内容"]))
    card("本時の学習内容", format_bullets(selected["本時の学習内容"]))
    card("目的", format_bullets(selected["目的"]))
    card("知識・技能", format_bullets(selected["知識・技能"]))
    card("思考力・表現力・判断力", format_bullets(selected["思考力・表現力・判断力"]))
    card("学びに向かう人間性等", format_bullets(selected["学びに向かう人間性等"]))
    card("次回の学習内容", format_bullets(selected["次回の学習内容"]))

# ----- タブ2：教員メモ -----
with tab2:
    st.subheader("📝 教員メモ（既存データの閲覧）")

    if len(memo_match) == 0:
        st.info("この小単元・本時に対応する教員メモは、まだ登録されていません。")
    else:
        memo_row = memo_match.iloc[0]
        card("評価基準", format_bullets(
            memo_row["評価基準(知識・技能、思考力・表現力・判断力、学びに向かう人間性等)"]
        ))
        card("生徒のつまづき", format_bullets(memo_row["生徒のつまづき"]))
        card("指導上の工夫・手立て", format_bullets(memo_row["指導上の工夫・手立て"]))
        card("使用した教材・ICTツール等", format_bullets(memo_row["使用した教材・ICTツール等"]))
        card("次時への引継ぎ事項", format_bullets(memo_row["次時への引継ぎ事項"]))
        card("メモ", format_bullets(memo_row["メモ"]))

    st.markdown("---")
    st.subheader("✏️ 教員が新しくメモを書く欄（Google Sheets に保存）")

    with st.form("teacher_memo_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            new_eval = st.text_area("評価基準", height=80)
            new_stumble = st.text_area("生徒のつまづき", height=80)
            new_idea = st.text_area("指導上の工夫・手立て", height=80)
        with col_b:
            new_tools = st.text_area("使用した教材・ICTツール等", height=80)
            new_next = st.text_area("次時への引継ぎ事項", height=80)
            new_memo = st.text_area("自由記述メモ", height=80)

        submitted = st.form_submit_button("Google Sheets に保存する")

    if submitted:
        try:
            gc = get_gspread_client()
            sh = gc.open_by_key(MEMO_SPREADSHEET_ID)
            ws = sh.worksheet(MEMO_SHEET_NAME)

            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_row = [
                subunit,
                lesson,
                new_eval,
                new_stumble,
                new_idea,
                new_tools,
                new_next,
                new_memo,
                now_str,
            ]

            ws.append_row(new_row)
            st.success("Google Sheets に保存しました。ページを再読み込みすると反映されます。")

        except Exception as e:
            st.error("保存中にエラーが発生しました。Secrets や シート名を確認してください。")
            st.write(e)


