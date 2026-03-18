import json
import os
from Scenario_Director.NISA_Scenario_Architect import NISAScenarioArchitect

def run_production():
    # 1. 初始化編排器
    architect = NISAScenarioArchitect()
    
    # 2. 設定參數：選擇小說類別與章節範圍
    genre = "Suspense_Thriller"  # 可選: Historical_Strategy, Wuxia_Action, Suspense_Thriller, Power_Fantasy
    total_chapters = 5
    
    story_blueprint = []

    print(f"--- 開始生產 {genre} 劇本序列 ---")
    
    # 3. 循環生產每一章的物理參數
    for i in range(1, total_chapters + 1):
        chapter_data = architect.generate_chapter_config(genre, i)
        story_blueprint.append(chapter_data)
        print(f"第 {i} 章參數生產完畢...")

    # 4. 產出實體 JSON 檔案 (這就是方案 B 的輸入源)
    output_path = "Output_Snapshots/scenario_blueprint.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(story_blueprint, f, indent=4, ensure_ascii=False)
    
    print(f"--- 劇本 JSON 已成功匯出至: {output_path} ---")

if __name__ == "__main__":
    run_production()