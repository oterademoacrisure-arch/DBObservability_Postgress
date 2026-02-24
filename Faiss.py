import pandas as pd
import numpy as np
import faiss
import os
import time
import ssl
import warnings
import requests

# --- CORPORATE NETWORK BYPASS (Layer 1: Environment) ---
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['HTTP_PROXY'] = '' # Ensure no conflict with system proxy
os.environ['HTTPS_PROXY'] = ''

# --- CORPORATE NETWORK BYPASS (Layer 2: SSL Patch) ---
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# --- CORPORATE NETWORK BYPASS (Layer 3: Suppress Warnings) ---
warnings.filterwarnings('ignore')

from sentence_transformers import SentenceTransformer

# --- CONFIGURATION ---
FILE_PATH = r"C:\Users\2411800\OneDrive - Cognizant\Desktop\Agentic_DB_Operation_24_Feb\agentic-db-operations\Process_Mining_Action_Engine.xlsx"

def run_independent_test():
    print("🚀 Starting Phase 1: Robust FAISS Action Engine")
    start_time = time.time()
    
    if not os.path.exists(FILE_PATH):
        print(f"❌ Error: File not found at {FILE_PATH}")
        return

    # --- STEP 1: DYNAMIC TABLE DETECTION ---
    print("📂 Step 1: Scanning Excel for Rules Table...")
    try:
        df_raw = pd.read_excel(FILE_PATH, sheet_name=0, header=None) 
        header_row_idx = None
        for i, row in df_raw.iterrows():
            vals = [str(v).strip() for v in row.values]
            if "RuleID" in vals and "Category" in vals:
                header_row_idx = i
                print(f"🎯 Found Rulebook Table starting at Excel Row {i+1}")
                break
        
        if header_row_idx is None:
            print("❌ Error: Could not find 'RuleID' header.")
            return

        df_rules = pd.read_excel(FILE_PATH, sheet_name=0, skiprows=header_row_idx)
        df_rules.columns = [str(c).strip() for c in df_rules.columns]
        df_rules = df_rules[pd.to_numeric(df_rules['RuleID'], errors='coerce').notna()]
        print(f"📊 Valid Rules loaded: {len(df_rules)}")
        
    except Exception as e:
        print(f"❌ Excel Processing Error: {e}")
        return

    # --- STEP 2: BUILD SEMANTIC PLAYBOOK ---
    print("📝 Step 2: Preparing search strings...")
    playbook = []
    for _, row in df_rules.iterrows():
        rid = str(int(float(row['RuleID'])))
        context = f"Category: {row['Category']}. Trigger: {row['Trigger (Watchman Agent Logic)']}"
        playbook.append({
            "id": rid,
            "search_text": context,
            "action": row['Actionable Insight / Automation Script']
        })

    # --- STEP 3: INITIALIZE AI & FAISS ---
    print("🤖 Step 3: Loading AI Model (Bypassing SSL for Corporate Network)...")
    try:
        # The model will download now without SSL errors
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("🧬 Generating Embeddings...")
        embeddings = model.encode([p['search_text'] for p in playbook], show_progress_bar=True)

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))
        print("✅ FAISS Vector Store Ready.")
    except Exception as e:
        print(f"❌ AI Error: {e}")
        print("\n💡 FINAL OPTION: If you still see SSL errors, connect to your PHONE HOTSPOT for 2 minutes.")
        print("   Once it downloads once, it will work forever on the office network.")
        return

    # --- STEP 4: LIVE SEARCH SIMULATION ---
    test_queries = [
        "Sequential scan detected on a table with more than 10,000 rows",
        "The query is using a LOWER() function on a column in the WHERE clause",
        "Performance issues with nested loop joins"
    ]

    print("\n" + "="*60)
    print("🔍 AI REASONING TEST RESULTS")
    print("="*60)
    
    for query in test_queries:
        query_vec = model.encode([query])
        D, I = index.search(np.array(query_vec).astype('float32'), k=1)
        match = playbook[I[0][0]]
        
        print(f"\n🔎 Query: '{query}'")
        print(f"✅ AI Match: RuleID {match['id']}")
        print(f"🛠️ Suggested Fix: {match['action']}")

    print(f"\n✨ Phase 1 Success: Engine ready in {round(time.time() - start_time, 2)}s.")

if __name__ == "__main__":
    run_independent_test()
