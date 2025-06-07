# 🦅 SummariLangchainzer (YT and Website)

SummariLangchainzer is a simple, fast, and powerful web app built using **LangChain** and **Streamlit** that summarizes the content of:

- YouTube videos  
- Any public website/article URL  

✨ It allows you to select the summary style (Paragraph, Bullet Points, Key Highlights)  
✨ You can also select the length of the summary (Brief, Medium, Detailed)  

🚧 **Translation feature is currently in progress and will be added soon!**

---

## 🚀 Features

✅ Summarize YouTube videos and website articles  
✅ Choose your preferred **summary style**  
✅ Choose **summary length** (Brief / Medium / Detailed)  
✅ Support for **multiple URLs** at once  
✅ Upload a text file containing list of URLs  
✅ Simple and beautiful Streamlit interface  
✅ Download your summaries as `.txt` files  
🚧 **Translation feature is currently in progress and will be added soon!**

---

## 🛠️ Tech Stack

- **LangChain** (LLM orchestration framework)  
- **Streamlit** (Frontend + App Framework)  
- **LangChain-Groq** (Using Llama3-8b-8192 model via Groq API)  
- **LangChain Community Document Loaders** (Youtube + UnstructuredURL)  
- **Validators** (URL validation)  

---

## ⚙️ How it works

1. You provide one or more **URLs** (YouTube or public web article).  
2. The app loads content using LangChain document loaders:  
   - `YoutubeLoader` for YouTube videos  
   - `UnstructuredURLLoader` for public web pages  
3. The app builds a **custom prompt** dynamically based on your selected style and length.  
4. The selected **Llama 3 model (via Groq API)** summarizes the content.  
5. You can download the generated summary as a `.txt` file.  

---

## 📌 Important Notes (Token Limit / Video Duration)

- We are using a **local model with a token limit of ~6000 tokens**.
- For YouTube videos, it is **recommended to use videos of ~6-7 minutes** in length for best results.
- You can try longer videos — the app will attempt to load and process them — but if it fails or gets truncated, please use shorter videos.

---

## 📥 Setup / Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/summari-langchainzer.git
cd summari-langchainzer
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
# On Linux / macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

```bash
streamlit run app.py
```

Then open your browser at [http://localhost:8501](http://localhost:8501)

---

## 🔑 API Key

You will need a valid **Groq API Key** for this app to work.

- Get it from: [https://console.groq.com/keys](https://console.groq.com/keys)
- Enter your API key inside the app when prompted.

---

## 🗺 Roadmap

- [x] Summarize YouTube videos
- [x] Summarize public web articles
- [x] Multiple URLs support
- [ ] Translation feature (in progress 🚧)
- [ ] Save summaries to PDF / DOCX
- [ ] Better progress tracking for large batches

---

## 📝 License

MIT License

---

## 🙏 Acknowledgements

- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [Groq](https://groq.com/)
- [Googletrans](https://github.com/ssut/py-googletrans) *(for upcoming translation feature)*

---

## ⚠️ Disclaimer

This app is for educational purposes only. It is not guaranteed to perfectly summarize all web content, and it depends on the availability and correctness of the source data.
