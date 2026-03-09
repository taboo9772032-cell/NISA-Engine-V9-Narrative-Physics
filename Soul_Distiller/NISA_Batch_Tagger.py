import json
import os

# --- 配置區 ---
CHAR_DIR = r"M:\AI生成\NISA\01_Engine\nisa_soul_roms" # 您的角色 JSON 存放處

# 定義角色與模板的對照表 (請根據您的需求微調)
# 這裡列出 20 人的對應關係
TAG_MAP = {
    "曹操": "霸主 (The Sovereign)",
    "劉備": "守護者 (The Guardian)",
    "孫權": "霸主 (The Sovereign)",
    "諸葛亮": "智者 (The Sage)",
    "關羽": "義士 (The Loyalist)",
    "呂布": "投機者 (The Opportunist)",
    "司馬懿": "潛伏者 (The Lurker)",
    "張飛": "莽夫 (The Berserker)",
    "趙雲": "守護者 (The Guardian)",
    "魏延": "投機者 (The Opportunist)",
    "郭嘉": "智者 (The Sage)",
    "荀彧": "義士 (The Loyalist)",
    "張遼": "義士 (The Loyalist)",
    "周瑜": "霸主 (The Sovereign)",
    "陸遜": "智者 (The Sage)",
    "呂蒙": "守護者 (The Guardian)",
    "魯肅": "智者 (The Sage)",
    "董卓": "支配者 (The Mastermind)",
    "袁紹": "霸主 (The Sovereign)",
    "賈詡": "潛伏者 (The Lurker)"
}

def batch_tag_characters():
    print(f"[*] 啟動批次標籤化作業...")
    count = 0
    
    for char_name, template_name in TAG_MAP.items():
        file_path = os.path.join(CHAR_DIR, f"{char_name}.json")
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 注入模板參考標籤
            data["template_ref"] = template_name
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"[✔] 已為 {char_name} 標記模板：{template_name}")
            count += 1
        else:
            print(f"[!] 找不到檔案：{file_path}，請檢查檔名是否完全一致。")
            
    print(f"\n[*] 標籤化完成。共處理 {count} 個檔案。")

if __name__ == "__main__":
    batch_tag_characters()