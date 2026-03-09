import json
from NISA_Math_Core_V9 import NISA_Math_Core_V9
from NISA_Perception_V9 import NISA_Perception_Filter_V9

# 模擬呼叫本地 LLM 的函數
def call_local_llm(prompt):
    print(">>> 正在呼叫 NISA 敘事渲染模塊 (LLM)...")
    return "（此處為 LLM 輸出的羅貫中筆觸渲染文本：只見空食盒內，不著一物。荀令君慘然一笑，知漢祿已盡，仰天長嘆，遂飲藥而卒...）"

def run_v9_evolution():
    print("🔥 NISA V9.0 引擎點火中...")
    
    # 1. 載入 Hub 數據
    with open("NISA_Soul_Master_Hub.json", "r", encoding="utf-8") as f:
        hub = json.load(f)
        
    physics = NISA_Math_Core_V9(hub)
    perception = NISA_Perception_Filter_V9()
    
    # 2. 注入劇本事件：曹操加封魏公
    print("\n[系統注入] 事件：曹操加九錫。大漢皇室 MOR 暴跌至 0.5。")
    hub['organizations']['大漢皇室']['init_l1']['MOR'] = 0.5
    
    # 3. 遍歷角色進行物理演算
    for char_name, char_data in hub['characters'].items():
        if char_data.get('status') == 'DECEASED':
            continue
            
        print(f"\n[*] 正在結算 {char_name} 的物理狀態...")
        
        # 執行位能傳導與張力計算
        physics.calculate_drive_and_tension(char_name)
        current_tns = char_data['init_l1'].get('TNS', 0.0)
        
        # 4. 【核心機制】偵測 TNS 臨界值並自動觸發 JUMP
        if current_tns >= hub['world_constants']['critical_tns_threshold']:
            print(f"⚠️ [臨界警告] {char_name} TNS ({current_tns:.2f}) 突破臨界點！掃描 Jump Curves...")
            
            for curve in char_data.get('jump_curves',[]):
                if curve['trigger']['parameter'] == 'TNS' and curve['trigger']['val'] <= current_tns:
                    print(f"⚡ [JUMP 觸發] 匹配情境：{curve['scenario']}")
                    
                    # 應用 Jump 效果 (例如 SAF = -1.0)
                    for eff_param, eff_val in curve['effect'].items():
                        char_data['init_l1'][eff_param] = eff_val
                        print(f"   -> 參數覆寫：{eff_param} = {eff_val}")
                    
                    # 檢查是否導致死亡
                    if char_data['init_l1'].get('SAF', 1.0) <= 0:
                        char_data['status'] = 'DECEASED'
                        
                    # 5. 生成 LLM Prompt 進行敘事渲染
                    prompt = f"""
                    【NISA 物理指令】
                    角色：{char_name}
                    事件觸發：{curve['scenario']}
                    物理狀態：張力(TNS)極度過載，代價支付導致生存(SAF)歸零。
                    感知狀態：絕對洞察 (Gamma = 1.0)，看透了權力深淵。
                    要求：請以《三國演義》羅貫中筆觸，描寫此角色在發現動力被封鎖、理想破滅時的最終決志與死亡。嚴禁出現數值。
                    """
                    
                    narrative = call_local_llm(prompt)
                    print(f"\n【敘事渲染輸出】\n{narrative}\n")

    print("✅ V9.0 演算循環結束。")

if __name__ == "__main__":
    run_v9_evolution()