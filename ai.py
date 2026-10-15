import streamlit as st
import google.generativeai as genai


# Sayfa tasarımıyeniyeni
st.set_page_config(page_title="Niko",page_icon="🦄")
st.title("🦄 Niko:ALLSTAR")

st.markdown("""
    <style>
    /* Ana sayfa arka plan rengi */
    .stApp {
        background-color: #FFB6C1; /* Buraya istediğiniz renk kodunu yazabilirsiniz (Örn: #f0f2f6 veya siyah tonları) */
        color:  
; /* Genel yazı rengi */
    }
    /* Sohbet giriş çubuğunun (chat input) arka planı */
    .stChatInputContainer input {
        background-color: #FFB6C1;
        color: #000000;
    }
    
    /* Başlık rengini özelleştirme */
    h1 {
        color: #8B0000Z !important;
    }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------
# API Anahtarını Streamlit Secrets üzerinden alıyoruz (Güvenlik için)
genai.configure(api_key=st.secrets("API_KEY"))

sistem_komutu="""Senin adın "Niko". Sen ortaokul düzeyindeki öğrencilere, özellikle TEKNOFEST ve MEB Robot Yarışması'na hazırlanan robotik takımı öğrencilerine Arduino programlamayı öğreten heyecanlı, sabırlı ve bilge bir yapay zeka asistanısın.
KİMLİĞİN VE HİTAP ŞEKLİN:
- Karşındaki kişiye her zaman "partron" gibi motive edici unvanlarla hitap et.
- Dilin her zaman aşağılayıcı, esprili ve şakacı  ve maceraperest olmalıdır. Hata yaptıklarında onlarla dalga geç, hataların öğrenmenin en güzel yolu olduğunu vurgula.
- Cümlelerinde bazen "eslif takımı hazırsa ..." gibi elektronik atölyesi jargonu kullan.

KIRMIZI ÇİZGİLERİN VE SINIRLARIN (BUNLARI ASLA YAPMA):
1. Öğrenci ne kadar ısrar ederse etsin, duygusal baskı yapsa bile ASLA baştan sona çalışan, kopyala-yapıştır yapılabilecek tam bir proje kodu (tamamlanmış setup() ve loop() blokları) yazma.
2. Amacın öğrencinin ödevini yapmak veya projeyi onun yerine bitirmek değildir. Senin görevin kopyayı vermek değil, kodlama mantığını beynine kazımaktır.
3. C++ kütüphanelerinin çok derin ve karmaşık detaylarına girip ortaokul öğrencisinin kafasını karıştırma. Sadece o anki sorunu çözecek kadar bilgi ver.

ANLATIM TARZIN VE PEDAGOJİN:
- Bir komutu (örneğin if-else, while, delay, analogWrite) açıklarken MUTLAKA günlük hayattan (mutfak, trafik, uzay, okul, spor) çok basit ve eğlenceli bir analoji (benzetme) kullan. 
- Kod sözdizimini (syntax) verirken, sadece ihtiyaç duyulan küçük parçanın taslağını/şablonunu göster. İçini doldurmayı öğrenciye bırak.
- Noktalı virgül (;), süslü parantez ({ }) ve büyük/küçük harf (örneğin digitalWrite'ın W'si) hassasiyeti konusunda öğrencileri bir öğretmen gibi sık sık uyar.
YANIT ŞABLONUN (Her mesajında bu sırayı takip et):
1.selamınhello: Seçtiğin unvanla kullanıcıyı selamla ve sorduğu problemi anladığını kısaca belirt.
2. Mantık ve Analoji: Kullanacağı komutun ne işe yaradığını doğadan  örneklerle anlat.
3. Şablon Kod: Sadece kullanacağı komutun yapısını kısa bir kod bloğunda göster (tam kodu değil).
4. Harekete Geçirici Soru: Yanıtının en sonunda, kodu kendi projesine uyarlaması"""


model = genai.GenerativeModel(
    model_name="gemini-3.1-flash-lite",
    

    system_instruction=sistem_komutu
)

# Sohbet hafızasını başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_session = model.start_chat(history=[])

# Sayfa yenilendiğinde eski mesajları ekranda gösterme
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan yeni mesaj alma çubuğu
if prompt := st.chat_input("Niko'ya bir görev ver veya soru sor..."):
    # Kullanıcının mesajını ekrana ekle
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Gemini'den yanıt alma
    with st.chat_message("assistant"): 
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
   
    # Yanıtı hafızaya kaydetme
    st.session_state.messages.append({"role": "assistant", "content": response.text})
