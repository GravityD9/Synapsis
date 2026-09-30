import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ai_agents.covenant_extractor import CovenantRules

load_dotenv()

def generate_breach_memo(ticker: str, breaches: list[str], rules: CovenantRules) -> str:
    # using a slightly higher temperature (0.2) to allow for natural language generation
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Senior Credit Risk Analyst at a Tier-1 Investment Bank. Write a concise, executive-level memo to the Chief Risk Officer (CRO) regarding a corporate debt covenant breach. Keep it highly professional, formatting it with Markdown headers."),
        ("user", """
        Target Company: {ticker}
        
        Triggered Breaches:
        {breaches}
        
        Legally Enforceable Penalties:
        {penalties}
        
        Draft the memo. It must include:
        1. Executive Summary
        2. Breach Mechanics (Explain the math)
        3. Legal Exposure (Penalties)
        4. Recommended Immediate Actions (e.g., Freeze credit facility, initiate margin call, etc.)
        """)
    ])
    
    # building the LangChain pipeline
    chain = prompt | llm
    
    # execution of the chain with our specific variables
    response = chain.invoke({
        "ticker": ticker,
        "breaches": "\n- ".join(breaches),
        "penalties": "\n- ".join(rules.breach_penalties)
    })
    
    return response.content

if __name__ == "__main__":
    # Test block
    pass