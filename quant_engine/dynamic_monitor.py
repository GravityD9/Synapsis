from ai_agents.report_generator import generate_breach_memo
import os
import sys
import yfinance as yf

# quant engine to AI engine connection
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai_agents.covenant_extractor import extract_covenants_from_db

def run_credit_analysis(ticker: str):
    print("🧠 1. AI Agent: Extracting Corporate Debt Covenants from SEC Exhibit 10.1...")
    rules = extract_covenants_from_db()
    
    print(f"📈 2. Quant Engine: Fetching live financials for {ticker}...")
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # pulling corporate finance metrics 
    total_debt = info.get('totalDebt', 0)
    ebitda = info.get('ebitda', 0)
    
    # leverage calculation, with safeguard against division by zero
    actual_leverage = total_debt / ebitda if ebitda and ebitda > 0 else 0
    
    print("\n⚖️ 3. Credit Risk Monitor: Executing Default Checks...")
    breaches = []
    
    # comparing real company data against the AI-extracted bank limits
    if rules.max_leverage_ratio and actual_leverage > rules.max_leverage_ratio:
        breaches.append(f"LEVERAGE DEFAULT RISK: Actual {actual_leverage:.2f}x > Bank Limit {rules.max_leverage_ratio:.2f}x")
        
    if not breaches:
        print(f"\n✅ PASS: {ticker} is fully compliant with its debt covenants.")
    else:
        print(f"\n❌ CRITICAL WARNING: {ticker} IS APPROACHING TECHNICAL DEFAULT!")
        for b in breaches:
            print(f"  - {b}")
        
        print("\n📝 4. Generative AI: Drafting Executive Breach Memo...")
        memo = generate_breach_memo(ticker, breaches, rules)
        
        print("\n" + "="*60)
        print("MEMO TO CHIEF RISK OFFICER".center(60))
        print("="*60 + "\n")
        print(memo)
        print("\n" + "="*60)
        
    return breaches, rules

if __name__ == "__main__":
    # Pass the ticker of the company whose credit agreement you downloaded
    # Example: "AMC", "CCL" (Carnival Cruise Line), or "CVNA" (Carvana)
    run_credit_analysis(ticker="CCL")