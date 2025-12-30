import streamlit as st
import pandas as pd

st.title("授業設計サポートアプリ")

# --- CSV URL ---
official_url = "https://docs.google.com/spreadsheets/d/1nuy7U8iEYxfAvsQMAJD6j25zy5ht4v7leveIjskvXI0/export?format=csv&gid=0"
memo_url = "https://docs.google.com/spreadsheets/d/1y3RhipP1vlK1esFUeAypQnyQ7JWH58yau7Sv4gH0Wjo/export?format=csv&gid=0"

# --- データ読み込み ---
official_df = pd.read_csv(official_url)
memo_df = pd.read_csv(memo_url)

# --- 校種選択 ---
school = st.selectbox("校種を選択", sorted(official_df["校種"].unique()))

# --- 学年選択 ---
grade_df = official_df[official_df["校種"] == school]
grade = st.selectbox("学年を選択", sorted(grade_df["学年"].unique()))

# --- 単元選択 ---
unit_df = grade_df[grade_df["学年"] == grade]
unit = st.selectbox("単元を選択", sorted(unit_df["単元"].unique()))

# --- 小単元選択 ---
subunit_df = unit_df[unit_df["単元"] == unit]
subunit = st.selectbox("小単元を選択", sorted(subunit_df["小単元"].unique()))

# --- 本時の学習内容選択 ---
lesson_df = subunit_df[subunit_df["小単元"] == subunit]
lesson = st.selectbox("本時の学習内容を選択", sorted(lesson_df["本時の学習内容"].unique()))

# --- 本時に完全一致する行を抽出 ---
selected = lesson_df[lesson_df["本時の学習内容"] == lesson].iloc[0]

# --- 教員加筆データ（同じ小単元＋本時で抽出） ---
memo_match = memo_df[
    (memo_df["小単元"] == subunit) &
    (memo_df["本時の学習内容"] == lesson)
]

# --- カード風表示用関数 ---
def card(title, content, color):
    st.markdown(
        f"""
        <div style="
            border: 2px solid {color};
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 12px;
        ">
            <h4 style="color:{color}; margin-bottom:6px;">{title}</h4>
            <div>{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")
st.subheader("📘 公式データ（学習指導要領）")

card("ねらい（最終到達目標）", selected["ねらい(最終到達目標)"], "#1E90FF")
card("既習内容", selected["既習内容"], "#1E90FF")
card("本時の学習内容", selected["本時の学習内容"], "#1E90FF")
card("目的", selected["目的"], "#1E90FF")
card("知識・技能", selected["知識・技能"], "#1E90FF")
card("思考力・判断力・表現力", selected["思考力・表現力・判断力"], "#1E90FF")
card("学びに向かう人間性等", selected["学びに向かう人間性等"], "#1E90FF")
card("次回の学習内容", selected["次回の学習内容"], "#1E90FF")

st.markdown("---")
st.subheader("📝 教員加筆（あなたの学校の実践）")

if len(memo_match) == 0:
    st.info("まだ教員加筆データがありません。")
else:
    memo_row = memo_match.iloc[0]
    card("評価基準", memo_row["評価基準(知識・技能、思考力・表現力・判断力、学びに向かう人間性等)"], "#FF8C00")
    card("生徒のつまづき", memo_row["生徒のつまづき"], "#FF8C00")
    card("指導上の工夫・手立て", memo_row["指導上の工夫・手立て"], "#FF8C00")
    card("使用した教材・ICTツール等", memo_row["使用した教材・ICTツール等"], "#FF8C00")
    card("次時への引継ぎ事項", memo_row["次時への引継ぎ事項"], "#FF8C00")
    card("メモ", memo_row["メモ"], "#FF8C00")




                    

