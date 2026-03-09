import requests
import json
import os
import time
import re

# --- 配置 ---
BASE_PATH = r""
OUTPUT_FILE = os.path.join(BASE_PATH, "NISA_Core_Templates_Part1.json")
# 建議將 API KEY 存在環境變數中，此處維持您的設定
API_KEY = "" 

GOLDEN_PROTOTYPES = [
    {"name": "曹操", "source": "三國演義", "template": "霸主 (The Sovereign)"},
    {"name": "劉備", "source": "三國演義", "template": "守護者 (The Guardian)"},
    {"name": "諸葛亮", "source": "三國演義", "template": "智者 (The Sage)"},
    {"name": "關羽", "source": "三國演義", "template": "義士 (The Loyalist)"},
    {"name": "呂布", "source": "三國演義", "template": "投機者 (The Opportunist)"}
]

# NISA 12 參數標準 (對齊您的 MD 文件標準)
L1_STANDARDS = "POW, RES, SAF, MOR, CHR, INF, TNS, INT, PRD, LDR, BND, LOA"

SCENARIOS = ["絕對權力的誘惑", "核心羈絆受威脅", "生存絕境", "獲得關鍵情報"]

def clean_json_content(raw):
    """
    強大的 JSON 提取器，確保即便 AI 輸出 Markdown 也能正確抓取內容
    """
    try:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        return match.group(0) if match else None
    except Exception:
        return None

def generate_burst_prompt(char):
    # 修正了變數名稱錯誤：{name} -> {char['name']}
    return f"""
    你現在是 NISA 靈魂逆向工程師。
    任務：將《{char['source']}》中的角色「{char['name']}」蒸餾為「{char['template']}」模板的物理常數與行為邏輯。
    
    【核心參數參考】
    L1 參數標準：{L1_STANDARDS}
    L2 常數：alpha(驅動), beta(風險偏好), gamma(韌性), delta(耦合), epsilon(抗性)
    
    【蒸餾要求】
    1. 靈魂常數 (L2 Constants)：根據角色性格慣性給出 0.0-1.0 數值。
    2. 意圖向量 (Intent Vector)：該角色最渴望提升的「L1 參數」優先級（最多3項）。
    3. 對價順序 (Sacrifice Order)：面臨壓力時，該角色願意優先支付/犧牲的「L1 參數」順序。
    4. 性格跳躍點 (Jump Curves)：分析在以下 4 個情境中的參數跳變：{", ".join(SCENARIOS)}。
    
    要求輸出純 JSON，嚴禁任何解釋文字，格式如下：
    {{
      "template_id": "{char['template']}",
      "l2_constants": {{ "alpha": 0.0, "beta": 0.0, "gamma": 0.0, "delta": 0.0, "epsilon": 0.0 }},
      "intent_vector": ["參數名"],
      "sacrifice_order": ["參數名1", "參數名2", "參數名3", "參數名4"],
      "jump_curves": [
        {{ "scenario": "描述", "trigger": {{ "parameter": "TNS", "val": 0.8, "op": ">" }}, "effect": {{ "MOR": -0.5, "POW": 0.8 }} }}
      ],
      "logic_signature": "一句話總結該模板的行為邏輯"
    }}
    """

def run_burst():
    all_templates = {}
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    print(f"[*] 啟動 NISA 核心原型爆破計畫...")

    for char in GOLDEN_PROTOTYPES:
        print(f"[*] 正在爆破核心原型：{char['name']} ({char['template']})...")
        payload = {
            "model": "anthropic/claude-3-5-sonnet",
            "messages": [{"role": "user", "content": generate_burst_prompt(char)}],
            "temperature": 0.1
        }
        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=120)
            
            # 增加 API 狀態檢查
            if res.status_code != 200:
                print(f"[!] API 錯誤 (Status: {res.status_code}): {res.text}")
                continue

            res_json = res.json()
            if 'choices' not in res_json:
                print(f"[!] 無效的響應格式: {res_json}")
                continue
                
            raw_content = res_json['choices'][0]['message']['content']
            json_str = clean_json_content(raw_content)
            
            if json_str:
                all_templates[char['name']] = json.loads(json_str)
                print(f"[✔] {char['name']} 模板蒸餾成功。")
            else:
                print(f"[!] 無法解析 {char['name']} 的 JSON 內容。")
            
            # 保護頻率，延遲 10 秒
            time.sleep(10) 
            
        except Exception as e: 
            print(f"[!] {char['name']} 執行中斷: {e}")

    # 最終存檔
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_templates, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 全部核心原型已編譯完成。檔案路徑：{OUTPUT_FILE}")

if __name__ == "__main__":
    run_burst()