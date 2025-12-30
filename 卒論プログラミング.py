import streamlit as st

units = [
    {
        "学年": "小5",
        "単元": "月と星",
        "小単元": "月の満ち欠け",
        "学習内容": "月の形の変化を観察し、満ち欠けの仕組みを理解する",
        "ねらい": "月の見え方の変化を時間的変化として捉える",
        "知識・技能": "月の満ち欠けの規則性を説明できる",
        "思考力・判断力・表現力": "観察結果から規則性を見いだし説明する",
        "学びに向かう力": "主体的に観察し、疑問を持って調べようとする態度",
        "既習内容": "太陽の動き、方位の理解",
        "次回の学習内容": "地球の自転と日周運動"
    }
]

st.title("授業設計サポートアプリ")

学年一覧 = sorted(list(set([unit["学年"] for unit in units])))
単元一覧 = sorted(list(set([unit["単元"] for unit in units])))

学年 = st.selectbox("学年を選んでください", 学年一覧)
単元 = st.selectbox("単元を選んでください", 単元一覧)

if st.button("表示"):
    for unit in units:
        if unit["学年"] == 学年 and unit["単元"] == 単元:
            st.subheader(f"{unit['学年']}：{unit['単元']}（{unit['小単元']}）")
            st.write("---")
            for key, value in unit.items():
                if key not in ["学年", "単元", "小単元"]:
                    st.markdown(f"### {key}")
                    st.write(value)
                    