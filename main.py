import streamlit as st
import pandas as pd
import random
import time
import folium
import requests
from streamlit.components.v1 import html
from streamlit_folium import st_folium


st.title('お試しアプリ')
st.badge(label='badge', icon=':material/potted_plant:', color='blue' )
st.caption('これはお試しアプリです。')

if 'registered_spots' not in st.session_state:
    st.session_state.registered_spots = []
if 'just_registered' not in st.session_state:
    st.session_state.just_registered = False

kiminonawa = st.toggle(label="あなたは「君の名は」が好きですか？")
if kiminonawa:
    st.header('「君の名は」聖地巡礼アプリ')
    st.write('「君の名は」の聖地巡礼スポットを登録しよう！')

    spot = st.text_input('スポット名')
    genre = st.selectbox('ジャンル', ['レストラン', '公園', '道', '寺・神社', '駅','その他'])
    scene = st.text_input('該当シーン説明')
    area = st.text_input('都道府県（○○県まで書いてね')
    address = st.text_input('住所(都道府県から書いてね)')

    if st.button('登録'):
        url = "https://msearch.gsi.go.jp/address-search/AddressSearch?q=" 
        q = address
        res = requests.get(url + q) 
        lon, lat = res.json()[0]["geometry"]["coordinates"]

        st.session_state.registered_spots.append({
            'スポット名': spot,
            'ジャンル': genre,
            "シーン説明": scene,
            "都道府県": area,
            "住所": address,
            '緯度': lat,
            '経度': lon
        })
        st.session_state.just_registered = True

    if st.session_state.registered_spots:
        st.write('Thank you!')
        if st.session_state.just_registered:
            st.balloons()
            time.sleep(2)
            st.session_state.just_registered = False
        df = pd.DataFrame(st.session_state.registered_spots)
        df_drop = df.drop(columns=['緯度', '経度'])
        st.dataframe(df_drop)

        st.write('**【Map】**')
        map = folium.Map(location=[df['緯度'].mean(),df['経度'].mean()], zoom_start=15)

        for row in df.itertuples():
            popup_text = f"{row.スポット名}（{row.シーン説明}）"
            popup = folium.Popup(popup_text, max_width=300) 
            folium.Marker(location=[row.緯度, row.経度], popup= popup, icon=folium.Icon(color="red", icon="info-sign")).add_to(map) 
        st_folium(map, width=700, height=500)


@st.dialog("理由を教えて")
def vote(item):
    st.write(f"なぜ {item} がいいの？")
    reason = st.text_input("なぜなら…")
    if st.button("送信"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()

if "vote" not in st.session_state:
    st.write("どっちが好き？")
    if st.button("アニメ"):
        vote("アニメ")
    if st.button("漫画"):
        vote("漫画")
else:
    f"君が {st.session_state.vote['item']}に投票したのは{st.session_state.vote['reason']}だから。素敵！"

st.title("名言返事ボット")
choice = st.radio("使いたい？", ["はい", "いいえ"], index=1)

if choice == "はい":
    st.write("これは名言を返すボットです。以下の３つ中からどれかを選んで入力してください。")
    st.write("「海賊王に」")
    st.write("「月に代わって」")
    st.write("「ぼく」")
    st.write("「見た目は子ども」")

# Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

# Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
    if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
    # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    # Streamed response emulator
        with st.chat_message("assistant"):

            if prompt == "海賊王に":
                response = "俺はなる！"
            elif prompt == "月に代わって":
                response = "おしおきよ！"
            elif prompt == "ぼく":
                response = "ドラえもん"
            elif prompt == "見た目は子ども":
                response = "頭脳は大人　その名は名探偵コナン"
            else:
                response = "そんな名言は知りません。"
    
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

st.write('満足度は？')
st.feedback("stars")

