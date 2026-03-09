import json
import os

# 定義 20 位武將的「跨實體目標」
# 邏輯：目標 = 對象 (Target) + 期望參數 (Param) + 目標值
DYNAMIC_GOALS = {
    "劉備": {"target_type": "Organization", "target_id": "大漢皇室", "params": {"RES": 1.0, "MOR": 0.9}},
    "關羽": {"target_type": "Character", "target_id": "劉備", "params": {"TNS": 0.0, "SAF": 1.0}},
    "張飛": {"target_type": "Character", "target_id": "劉備", "params": {"TNS": 0.0, "POW": 1.0}},
    "諸葛亮": {"target_type": "Organization", "target_id": "劉備流浪集團", "params": {"INF": 1.0, "INT": 1.0}},
    "趙雲": {"target_type": "Character", "target_id": "劉備", "params": {"SAF": 1.0, "BND": 1.0}},
    
    "曹操": {"target_type": "Self", "target_id": "曹操", "params": {"POW": 1.0, "INF": 1.0}},
    "荀彧": {"target_type": "Organization", "target_id": "大漢皇室", "params": {"MOR": 1.0, "LOA": 1.0}},
    "郭嘉": {"target_type": "Character", "target_id": "曹操", "params": {"INT": 1.0, "INF": 1.0}},
    "張遼": {"target_type": "Character", "target_id": "曹操", "params": {"POW": 1.0, "LOA": 1.0}},
    "司馬懿": {"target_type": "Self", "target_id": "司馬懿", "params": {"POW": 1.0, "INT": 1.0}},
    
    "孫權": {"target_type": "Organization", "target_id": "江東豪族盟約", "params": {"SAF": 1.0, "RES": 0.9}},
    "周瑜": {"target_type": "Organization", "target_id": "江東豪族盟約", "params": {"POW": 1.0, "INF": 1.0}},
    "魯肅": {"target_type": "Organization", "target_id": "江東豪族盟約", "params": {"BND": 0.9, "MOR": 0.8}},
    "呂蒙": {"target_type": "Organization", "target_id": "江東豪族盟約", "params": {"POW": 0.9, "INT": 0.9}},
    "陸遜": {"target_type": "Organization", "target_id": "江東豪族盟約", "params": {"SAF": 1.0, "PRD": 0.8}},
    
    "呂布": {"target_type": "Self", "target_id": "呂布", "params": {"RES": 1.0, "SAF": 0.9}},
    "董卓": {"target_type": "Self", "target_id": "董卓", "params": {"POW": 1.0, "RES": 1.0}},
    "袁紹": {"target_type": "Self", "target_id": "袁紹", "params": {"INF": 1.0, "PRD": 1.0}},
    "賈詡": {"target_type": "Self", "target_id": "賈詡", "params": {"SAF": 1.0, "INT": 0.9}},
    "魏延": {"target_type": "Self", "target_id": "魏延", "params": {"POW": 0.9, "PRD": 0.8}}
}

def inject_cross_goals(hub_path):
    if not os.path.exists(hub_path):
        print(f"[!] 找不到 Hub 檔案：{hub_path}")
        return

    with open(hub_path, 'r', encoding='utf-8') as f:
        hub = json.load(f)

    print("[*] 正在將「目標」升級為「跨實體參數連結」...")
    
    for name, char in hub["characters"].items():
        if name in DYNAMIC_GOALS:
            goal_config = DYNAMIC_GOALS[name]
            # 更新 motivation_engine
            # 如果原本就有 engine，我們保留 prototype (對價習慣) 但更新 target_linking (目標位能)
            if "motivation_engine" not in char:
                char["motivation_engine"] = {}
                
            char["motivation_engine"]["target_linking"] = {
                "target_type": goal_config["target_type"],
                "target_id": goal_config["target_id"],
                "target_params": goal_config["params"],
                "logic": "位能差補完模式"
            }
            print(f" [✔] {name} 目標已鎖定：{goal_config['target_id']} 的 {list(goal_config['params'].keys())}")

    with open(hub_path, 'w', encoding='utf-8') as f:
        json.dump(hub, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 20 位武將之「跨實體目標」注入完成。")

if __name__ == "__main__":
    HUB_FILE = r"M:\AI生成\NISA\NISA_Soul_Master_Hub.json"
    inject_cross_goals(HUB_FILE)