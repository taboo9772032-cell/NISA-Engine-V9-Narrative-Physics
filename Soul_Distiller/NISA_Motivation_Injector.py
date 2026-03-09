import json

# 定義 5 大意圖原型的對價習慣
PROTOTYPE_HABITS = {
    "Expander": {"POW_efficiency": 1.2, "pref_sacrifice": ["MOR", "BND", "SAF"]},
    "Preserver": {"SAF_efficiency": 1.2, "pref_sacrifice": ["PRD", "RES", "POW"]},
    "Opportunist": {"RES_efficiency": 1.5, "pref_sacrifice": ["LOA", "MOR", "BND"]},
    "Seeker": {"INT_efficiency": 1.5, "pref_sacrifice": ["SAF", "RES", "MOR"]},
    "Avenger": {"TNS_output": 1.5, "pref_sacrifice": ["HLT", "MOR", "SAF"]}
}

def inject_dual_drive(hub_path):
    with open(hub_path, 'r', encoding='utf-8') as f:
        hub = json.load(f)

    # 針對您的建議：純參數化的跨對象目標
    goals_map = {
        "劉備": {"proto": "Preserver", "target_id": "大漢皇室", "target_params": {"RES": 1.0, "MOR": 0.9}},
        "關羽": {"proto": "Preserver", "target_id": "劉備", "target_params": {"TNS": 0.0, "SAF": 1.0}},
        "曹操": {"proto": "Expander", "target_id": "曹操", "target_params": {"POW": 1.0, "INF": 1.0}},
        "呂布": {"proto": "Opportunist", "target_id": "呂布", "target_params": {"RES": 1.0, "SAF": 0.9}},
        # ... 其餘 20 人依此類推
    }

    print("[*] 正在注入雙軌驅動系統：動力 vs 對價習慣...")
    for name, config in goals_map.items():
        if name in hub["characters"]:
            char = hub["characters"][name]
            char["motivation_engine"] = {
                "intent_prototype": config["proto"],
                "habits": PROTOTYPE_HABITS[config["proto"]],
                "target_linking": {
                    "target_id": config["target_id"],
                    "target_params": config["target_params"]
                },
                "current_drive": 0.0
            }
            print(f" [✔] {name} 注入完成")

    with open(hub_path, 'w', encoding='utf-8') as f:
        json.dump(hub, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    inject_dual_drive(r"M:\AI生成\NISA\NISA_Soul_Master_Hub.json")