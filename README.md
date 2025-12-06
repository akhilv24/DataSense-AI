# 📊 DataSense AI  
### *Conversational File Analyst powered by Groq + LangChain*

DataSense AI is an interactive Streamlit application that transforms your datasets into meaningful insights through natural conversation.  
Upload CSV, Excel, or PDF files → Ask questions → Get AI-powered analysis instantly.

This project uses:
- **Groq LLMs (LLaMA / GPT-OSS)**
- **LangChain Runnable Pipelines**
- **Streamlit**
- **Pandas, Tabula, PDFPlumber**
- **Dynamic Token-Optimized Prompting**

---

## 🚀 Features

### ✅ **1. Conversational Data Analysis**
Ask questions like:
- “What is the total sales by region?”
- “Which category has the highest profit?”
- “Summarize this dataset in simple language.”

DataSense AI understands the dataset and responds clearly.

---

### ✅ **2. Multi-Format File Support**
Upload:
- 📄 **CSV**
- 📘 **Excel (xlsx / xls)**
- 📝 **Text files**
- 🔍 **PDFs with tables & text**

The app automatically extracts tables and text from PDFs using **Tabula + PDFPlumber**.

---

### ✅ **3. Auto-Sampling for Token Optimization**
To avoid Groq 413 token errors, the app:
- Detects dataset size  
- Samples rows dynamically  
- Keeps response fast & efficient  

No more token limit crashes.

---

### ✅ **4. Clean Data Previews & Summaries**
- View dataset preview  
- Automatic `describe()` summary  
- Column types, stats, and structure  

---

### ✅ **5. Powered by Groq LLMs (Ultra-Fast)**
Uses cutting-edge LLMs like:
- `llama3-70b-8192`
- `openai/gpt-oss-20b`
- `llama3-8b-8192`

---

## 🧠 How It Works (Architecture)

