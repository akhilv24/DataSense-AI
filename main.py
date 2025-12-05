import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tabula
import pdfplumber
from dotenv import load_dotenv

# LangChain (new API)
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ================================
#           UI LAYOUT
# ================================
st.set_page_config(page_title="DataSense AI", layout="wide")

col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=150)

with col2:
    st.title("DataSense AI – Your Conversational File Analyst")
    st.caption("Upload a dataset and ask anything about it. DataSense AI will analyze it for you!")


# ================================
#      FILE UPLOAD SECTION
# ================================
uploaded_file = st.file_uploader(
    "📁 Upload your dataset",
    type=["csv", "xlsx", "xls", "pdf", "txt"]
)

df = None
pdf_text = ""

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1].lower()

    try:
        # CSV
        if file_type == "csv":
            df = pd.read_csv(uploaded_file, encoding="latin1")

        # Excel
        elif file_type in ["xlsx", "xls"]:
            df = pd.read_excel(uploaded_file)

        # TXT
        elif file_type == "txt":
            df = pd.read_csv(uploaded_file, sep=None, engine="python")

        # PDF
        elif file_type == "pdf":
            st.warning("📄 Extracting PDF data...")

            # Save PDF temporarily
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())

            # Extract tables using Tabula
            try:
                df_list = tabula.read_pdf("temp.pdf", pages="all", multiple_tables=True)
                if df_list:
                    df = df_list[0]
                    st.success("Extracted table from PDF!")
                else:
                    df = None
                    st.warning("No tables found in the PDF.")
            except:
                st.warning("PDF table extraction failed.")

            # Extract PDF text
            try:
                with pdfplumber.open("temp.pdf") as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            pdf_text += text + "\n\n"

                st.text_area("📄 Extracted PDF Text", pdf_text[:3000])
            except:
                st.error("Could not extract text from PDF")

        else:
            st.error("❌ Unsupported file format!")

    except Exception as e:
        st.error(f"❌ File error: {e}")


# ================================
#     SHOW DATA PREVIEW
# ================================
if df is not None:
    st.subheader("🔎 Data Preview")
    st.dataframe(df)

    # Sample Summary
    st.subheader("📊 Dataset Summary")
    st.write(df.describe(include="all"))


# ================================
#      AI QUERY SECTION
# ================================
st.divider()
user_query = st.text_input("💬 Ask something about this dataset:")

if user_query:
    if df is None and file_type == "pdf":
        st.info("Analyzing PDF text content...")

    elif df is None:
        st.error("Upload a dataset first!")
    else:
        # Initialize Groq LLM
        llm = ChatGroq(
            model_name="openai/gpt-oss-20b",  # Correct parameter
            groq_api_key=GROQ_API_KEY
        )

        # Prompt Template
        prompt = PromptTemplate.from_template(
            """
You are DataSense AI, an expert data analyst.

Here is the dataset (sampled rows):
{data}

User question: {question}

Give a clear, simple, analytical answer.
"""
        )

        # Runnable chain
        chain = prompt | llm | StrOutputParser()

        # Auto sample (fixes your error)
        sample_size = min(len(df), 100)
        short_df = df.sample(sample_size, random_state=42).to_csv(index=False)

        # Run AI
        with st.spinner("Analyzing with AI..."):
            response = chain.invoke({"data": short_df, "question": user_query})

        st.subheader("🤖 AI Insight")
        st.write(response)
