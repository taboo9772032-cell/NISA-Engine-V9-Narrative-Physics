import csv
import json
import time
import requests
import os
import re

# --- 1. 配置與 API ---
API_KEY = ""
MODEL = "anthropic/claude-3-5-sonnet"
INPUT_CSV = "tasks.csv"
OUTPUT_DIR = "nisa_soul_roms"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- 2. 新 12 參數標準定義 (對齊 MD 檔案) ---
L1_STANDARDS = """
【硬資產簇】: POW(實力), RES(資源), SAF(安全)
【軟實力簇】: MOR(正當性), CHR(魅力), INF(影響力)
【內驅力簇】: TNS(張力), INT(智略), PRD(自尊)
【結構簇】: LDR(統御), BND(羈絆), LOA(忠誠)
"""

def generate_prompt(name, source):
    return f"""
    你現在是 NISA 靈魂動力學觀測員。
    任務：將《{source}》中的「{name}」進行底層邏輯逆向工程。
    
    【參數標準】
    {L1_STANDARDS}
    
    【蒸餾要求】
    1. 初始位能 (L1 State): 根據原著開場，給出這 12 項參數的 0.0-1.0 初始值。
    2. 靈魂常數 (L2 Constants): 
       - alpha (驅動力): 追求 POW 的斜率。
       - beta (風險偏好): SAF 下降時的響應。
       - gamma (韌性): 參數自然衰減的阻尼。
       - delta (耦合度): 個人與組織的同步率。
       - epsilon (抗性): 對壓力 TNS 的過濾係數。
    3. 性格跳躍點 (Phase Transition): 
       找出該角色 2 個關鍵轉折場景，分析觸發條件(Trigger)與參數突變結果(Effect)。
    4. 對價順序 (Sacrifice Order): 當面臨壓力，角色願意支付(犧牲)的參數順序。
    
    輸出純 JSON：
    {{
      "name": "{name}",
      "init_l1": {{ "POW":0, "RES":0, "SAF":0, "MOR":0, "CHR":0, "INF":0, "TNS":0, "INT":0, "PRD":0, "LDR":0, "BND":0, "LOA":0 }},
      "l2_constants": {{ "alpha": 0, "beta": 0, "gamma": 0, "delta": 0, "epsilon": 0 }},
      "jump_curves": [
        {{ "scenario": "描述", "trigger": {{ "parameter": "BND", "val": 0.1, "op": "<" }}, "effect": {{ "MOR": -0.8, "TNS": 1.0 }} }}
      ],
      "sacrifice_order": ["PRD", "MOR", "RES"],
      "logic_signature": "一句話總結其行為邏輯"
    }}
    """

def run_batch():
    # 讀取任務
    targets = []
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        targets = [row for row in reader if row['source'] == '三國演義']
    
    print(f"[*] 偵測到 {len(targets)} 位三國武將待蒸餾。")
    
    for i, char in enumerate(targets):
        name = char['name']
        source = char['source']
        file_path = os.path.join(OUTPUT_DIR, f"{name}.json")
        
        if os.path.exists(file_path):
            print(f"[-] {name} 已存在，跳過。")
            continue
            
        print(f"[*] [{i+1}/{len(targets)}] 正在分析靈魂：{name}...")
        
        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": generate_prompt(name, source)}],
            "temperature": 0.2
        }
        
        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                                headers={"Authorization": f"Bearer {API_KEY}"}, 
                                json=payload, timeout=120)
            content = res.json()['choices'][0]['message']['content']
            
            # 清理並存檔
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                with open(file_path, "w", encoding="utf-8") as out:
                    out.write(match.group(0))
                print(f"    [✔] {name} 分析完成並存入數據庫。")
            
            time.sleep(10) # 防止 API 過熱
        except Exception as e:
            print(f"    [!] {name} 分析出錯: {e}")

if __name__ == "__main__":
    run_batch()