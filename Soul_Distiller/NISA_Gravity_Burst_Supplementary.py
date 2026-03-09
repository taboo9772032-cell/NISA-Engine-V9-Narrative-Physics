import requests
import json
import os
import time
import re

# --- 配置 ---
BASE_PATH = r""
OUTPUT_FILE = os.path.join(BASE_PATH, "NISA_Core_Templates_Part2.json")
API_KEY = ""

SUPPLEMENTARY_PROTOTYPES = [
    {"name": "司馬懿", "source": "三國演義", "template": "潛伏者 (The Lurker)"},
    {"name": "張飛", "source": "三國演義", "template": "莽夫 (The Berserker)"},
    {"name": "甄士隱", "source": "紅樓夢", "template": "隱士 (The Hermit)"},
    {"name": "法里亞神父", "source": "基度山恩仇記", "template": "殉道者 (The Martyr)"},
    {"name": "費爾南", "source": "基度山恩仇記", "template": "寄生者 (The Parasite)"},
    {"name": "福爾摩斯", "source": "福爾摩斯探案全集", "template": "探求者 (The Seeker)"},
    {"name": "莫里亞蒂", "source": "福爾摩斯探案全集", "template": "支配者 (The Mastermind)"}
]

# NISA 12 參數標準 (確保跨作品邏輯對齊)
L1_STANDARDS = "POW, RES, SAF, MOR, CHR, INF, TNS, INT, PRD, LDR, BND, LOA"

def clean_json_content(raw):
    """
    精確抓取 JSON 區塊，過濾 AI 的前言與後語
    """
    try:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        return match.group(0) if match else None
    except Exception:
        return None

def generate_burst_prompt(char):
    # 針對特定模板強化邏輯權重
    special_hint = ""
    if "Lurker" in char['template']:
        special_hint = "重點在於：極高的 INT (智略) 與對 PRD (自尊) 的極端支付能力，以換取 SAF (安全)。"
    elif "Berserker" in char['template']:
        special_hint = "重點在於：高 TNS (張力) 瞬間壓制 MOR (道德) 與 INT (智略) 的相變過程。"
    elif "Mastermind" in char['template']:
        special_hint = "重點在於：極高的 INF (影響力) 輻射與對 LDR (統御) 的非對稱控制。"

    # 修正了 {name} 為 {char['name']}
    return f"""
    你現在是 NISA 靈魂編譯器。
    任務：將《{char['source']}》中的角色「{char['name']}」蒸餾為「{char['template']}」模板。
    
    【核心指令】
    {special_hint}
    要求使用 NISA 12 參數標準：{L1_STANDARDS}。
    提取 L2 常數、意圖向量 (Intent Vector)、對價順序 (Sacrifice Order) 與 2 個性格跳躍點。
    
    【輸出格式要求】
    僅輸出純 JSON 內容，格式需與 Part 1 嚴格對齊：
    {{
      "template_id": "{char['template']}",
      "l2_constants": {{ "alpha": 0.0, "beta": 0.0, "gamma": 0.0, "delta": 0.0, "epsilon": 0.0 }},
      "intent_vector": ["追求參數"],
      "sacrifice_order": ["支付參數1", "支付參數2", "支付參數3"],
      "jump_curves": [
        {{ "scenario": "場景名", "trigger": {{ "parameter": "TNS", "val": 0.8, "op": ">" }}, "effect": {{ "INT": -0.5, "POW": 0.9 }} }}
      ],
      "logic_signature": "一句話總結該邏輯特徵"
    }}
    """

def run_burst():
    all_templates = {}
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    print(f"[*] 啟動 NISA 補完計畫：正在提取 7 個邊緣與特殊邏輯模板...")

    for char in SUPPLEMENTARY_PROTOTYPES:
        print(f"[*] 正在處理補完模板：{char['name']} ({char['template']})...")
        payload = {
            "model": "anthropic/claude-3-5-sonnet",
            "messages": [{"role": "user", "content": generate_burst_prompt(char)}],
            "temperature": 0.2
        }
        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=120)
            
            if res.status_code != 200:
                print(f"[!] API 錯誤 ({res.status_code}): {res.text}")
                continue

            raw_content = res.json()['choices'][0]['message']['content']
            json_str = clean_json_content(raw_content)
            
            if json_str:
                all_templates[char['name']] = json.loads(json_str)
                print(f"[✔] {char['name']} 的邏輯 ROM 編譯成功。")
            else:
                print(f"[!] 無法解析 {char['name']} 的數據。")
            
            time.sleep(10) # 頻率控制
            
        except Exception as e:
            print(f"[!] {char['name']} 執行中斷: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_templates, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 補完計畫完成！檔案已存於：{OUTPUT_FILE}")

if __name__ == "__main__":
    run_burst()