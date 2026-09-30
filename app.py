import streamlit as st
from ai_agents.document_vectorizer import vectorize_pdf
from ai_agents.covenant_extractor import extract_covenants_from_db

# configuring the web page 
st.set_page_config(page_title="Synapse Engine", layout="wide", page_icon="⚡")
st.title("⚡ Synapse Engine")
st.markdown("**Automated Agentic RAG for Middle Office & Regulatory Operations**")
st.markdown("This pipeline ingests SEC filings, extracts strict JSON financial covenants via GPT-4o-mini, and monitors limits for NAV impact analysis.")
st.divider()

# sidebar controls
st.sidebar.header("Pipeline Controls")

if st.sidebar.button("1. Ingest SEC Filing (PDF)"):
    with st.spinner("Chunking and Vectorizing PDF into ChromaDB..."):
        vectorize_pdf("data/credit_agreements/credit_agreement.pdf")
        st.sidebar.success("✅ Vector DB Updated!")

if st.sidebar.button("2. Extract Rules via AI"):
    with st.spinner("Extracting constraints via GPT-4o-mini..."):
        rules = extract_covenants_from_db()
        st.session_state['rules'] = rules.model_dump()
        st.sidebar.success("✅ Extraction Complete!")

# main dashboard display 
if 'rules' in st.session_state:
    rules = st.session_state['rules']
    
    st.subheader("📑 Extracted Financial Guardrails")
    st.json(rules)
    
    st.divider()
    
    # mock live risk monitor 
    st.subheader("📈 Live Risk Monitor (Simulated Market Data)")
    col1, col2 = st.columns(2)
    
    leverage_limit = rules.get('max_leverage_ratio', 0)
    current_leverage = 3.2  #simulated live debt ratio
    
    with col1:
        st.metric(
            label="Current Leverage Ratio", 
            value=f"{current_leverage}x", 
            delta=f"{round(leverage_limit - current_leverage, 2)}x covenant cushion"
        )
        
        if current_leverage >= leverage_limit:
            st.error(f"🚨 BREACH DETECTED: Escalating to Risk Committee. Penalties: {rules.get('breach_penalties', ['None'])[0]}")
        else:
            st.success("✅ Status: COMPLIANT - No NAV Impact Detected.")
else:
    st.info("👈 Use the sidebar to extract covenants and populate the dashboard.")