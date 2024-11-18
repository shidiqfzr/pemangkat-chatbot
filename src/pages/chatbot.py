import openai
import streamlit as st

def chatbot():
    st.markdown("<h1 style='text-align: center; margin-bottom: 1em;'>Pemangkat Chatbot</h1>", unsafe_allow_html=True)

    openai.api_key = st.secrets["OPENAI_API_KEY"]

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Instruksi sistem untuk membatasi cakupan jawaban
    context = """
    Anda adalah chatbot yang hanya dapat memberikan informasi mengenai Kecamatan Pemangkat dan desa-desa yang ada di dalamnya. Jawaban harus singkat dan jelas. 
    Desa-desa yang termasuk dalam Kecamatan Pemangkat adalah:
    - Desa Pemangkat Kota
    - Desa Harapan
    - Desa Penjajab
    - Desa Jelutung
    - Desa Lonam
    - Desa Gugah Sejahtera
    - Desa Sebatuan
    - Desa Perapakan

    Selain itu, Anda dapat memberikan informasi mengenai:
    - Pembentukan dan pemekaran wilayah administratif Kecamatan Pemangkat
    - Peraturan terkait Kecamatan Pemangkat, seperti Peraturan Daerah Kabupaten Sambas No. 3 Tahun 2003 yang mengatur pembentukan Kecamatan Semparuk
    - Topik-topik lainnya yang berhubungan dengan administrasi kecamatan dan desa

    Jika pertanyaan tidak terkait dengan topik-topik ini, jawab dengan:
    Kami hanya dapat memberikan informasi mengenai Kecamatan Pemangkat dan wilayah administratifnya
    """

    if not st.session_state.messages:
        # Menambahkan konteks awal dalam percakapan untuk mengarahkan model tanpa menampilkannya di UI
        st.session_state.messages.append({"role": "system", "content": context})

    # Menampilkan pesan-pesan sebelumnya dalam percakapan, kecuali pesan sistem
    for message in st.session_state.messages:
        if message["role"] != "system":  # Hanya tampilkan pesan selain pesan sistem
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Menangani input pesan dari pengguna
    if prompt := st.chat_input("Kirim pesan"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + " ")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
