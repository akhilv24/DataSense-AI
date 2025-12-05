##import os
##import streamlit as st
##import pandas as pd
##import matplotlib.pyplot as plt
##import seaborn as sns
##import io
##import contextlib
##from dotenv import load_dotenv
##from langchain_groq import ChatGroq
##from langchain.prompts import PromptTemplate
##from langchain.chains import LLMChain

##load_dotenv()
##GROQ_API_KEY = os.getenv("GROQ_API_KEY")

##st.set_page_config(page_title="DataSense AI", layout="wide")
##uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

##if uploaded_file:
    ##df = pd.read_csv(uploaded_file)
    ##st.write("### Preview of Data", df.head())

    ##user_query = st.text_input("Ask something about this dataset (e.g., total sales by region):")

    ##if user_query:
        ##llm = ChatGroq(model="llama3-70b-8192", groq_api_key=GROQ_API_KEY)

        ##prompt = PromptTemplate.from_template("""You are a data analyst. Here's a dataset:{data}Question: {question}Answer in simple and clear terms.""")

        ##chain = LLMChain(llm=llm, prompt=prompt)

        ##short_df = df.head(5).to_csv(index=False)
        ##response = chain.run(data=short_df, question=user_query)

        ##st.markdown("### AI Insight")
        ##st.success(response)

import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tabula 
import pdfplumber
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

col1, col2 = st.columns([1, 5])  # Adjust proportions as needed

with col1:
    st.image("logo.png", width=200)  # Logo on the left

st.set_page_config(page_title="DataSense AI", layout="wide")
st.title("DataSense AI – Your Conversational File Analyst")

uploaded_file = st.file_uploader("Upload your File", type=["csv", "xlsx", "PDF", "txt", "docx", "xls"])

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1].lower()

    try:
        if file_type == "csv":
            df = pd.read_csv(uploaded_file, encoding='latin1')
        elif file_type in ["xlsx", "xls"]:
            df = pd.read_excel(uploaded_file)
        elif file_type == "pdf":
            st.warning("📄 PDF preview below – analysis in progress...")
            df = None
        else:
            st.error("Unsupported file type!")
            df = None

        if df is not None:
            st.write("### Preview of Data", df)

    except Exception as e:
        st.error(f"Error reading file: {e}")
        df = None

    # PDF handling block
    if file_type == "pdf":
        try:
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())

            df_list = tabula.read_pdf("temp.pdf", pages="all", multiple_tables=True)

            if df_list:
                df = df_list[0]
                st.write("### Extracted Table from PDF", df.head())
            else:
                st.warning(" No tables found in the PDF.")
                df = None
        except Exception as e:
            st.error(f"PDF table processing failed: {e}")
            df = None

        try:
            with pdfplumber.open("temp.pdf") as pdf:
                all_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        all_text += text
            st.text_area("📄 Extracted PDF Text", all_text[:3000])
        except Exception as e:
            st.error(f"PDF text extraction failed: {e}")

    user_query = st.text_input("Ask something about this dataset (e.g., total sales by region):")

    if user_query and df is not None:
        llm = ChatGroq(model="llama3-70b-8192", groq_api_key=GROQ_API_KEY)

        prompt = PromptTemplate.from_template("""You are a data analyst. Here's a dataset:{data}Question: {question}Answer in simple and clear terms.""")

        chain = LLMChain(llm=llm, prompt=prompt)

        # Random sample of 100 rows for diverse context
        short_df = df.sample(100, random_state=42).to_csv(index=False)
        response = chain.run(data=short_df, question=user_query)

        st.markdown("### AI Insight")
        st.markdown("Answer For Your Query: " + response)
