import json
import os

class NISA_Social_Ignition_V8:
    def __init__(self, hub_path):
        self.hub_path = hub_path
        if not os.path.exists(hub_path):
            raise FileNotFoundError(f"找不到 Master Hub 檔案：{hub_path}")
            
        with open(hub_path, 'r', encoding='utf-8') as f:
            self.hub = json.load(f)
        self.chars = self.hub['characters']

    def _calculate_pair_aff(self, name_a, name_b):
        """
        計算 A 與 B 之間的初始引力數值
        包含：集團重力、目標鎖定、意圖相性、相位差衝突
        """
        char_a = self.chars[name_a]
        char_b = self.chars[name_b]
        aff = 0.0

        # --- 1. 集團重力 (Group Gravity) ---
        # 同陣營提供基礎凝聚力
        if char_a.get('affiliation') == char_b.get('affiliation') and char_a.get('affiliation') != "無":
            aff += 0.4

        # --- 2. 跨實體目標連結 (Target Linking) ---
        # 若 A 的驅動力目標是 B，則產生極強吸引力 (如關羽對劉備)
        target_a = char_a.get('motivation_engine', {}).get('target_linking', {}).get('target_id')
        target_b = char_b.get('motivation_engine', {}).get('target_linking', {}).get('target_id')
        
        if target_a == name_b or target_b == name_a:
            aff += 0.5

        # --- 3. 意圖原型相性 (Intent Resonance) ---
        # 根據習慣對價模式判斷相性
        proto_a = char_a.get('motivation_engine', {}).get('intent_prototype')
        proto_b = char_b.get('motivation_engine', {}).get('intent_prototype')

        if proto_a == "Expander" and proto_b == "Expander":
            aff -= 0.6  # 權力擴張者互為零和競爭
        elif proto_a == "Preserver" and proto_b == "Preserver":
            aff += 0.3  # 守護者互為秩序共鳴
        elif (proto_a == "Expander" and proto_b == "Preserver") or (proto_a == "Preserver" and proto_b == "Expander"):
            aff -= 0.2  # 侵略習慣與保守習慣的固有摩擦

        # --- 4. 相位差衝突 (Value/Phase Difference) ---
        # 即使同陣營，若核心參數偏好差距過大，產生「相位斥力」
        l1_a = char_a.get('init_l1', {})
        l1_b = char_b.get('init_l1', {})
        
        # PRD (自尊/禮法) 衝突：關羽 (高 PRD) vs 簡雍 (低 PRD)
        prd_diff = abs(l1_a.get('PRD', 0.5) - l1_b.get('PRD', 0.5))
        if prd_diff > 0.5:
            aff -= 0.35
            
        # MOR (道德/正當性) 衝突：不同價值底線產生的排斥
        mor_diff = abs(l1_a.get('MOR', 0.5) - l1_b.get('MOR', 0.5))
        if mor_diff > 0.4:
            aff -= 0.2

        # 數值箝制在 -1.0 到 1.0 之間
        return round(max(-1.0, min(1.0, aff)), 3)

    def ignite(self):
        names = list(self.chars.keys())
        print(f"[*] 正在建立社交重力場 (V8.1)：計算 {len(names)} 名武將的相位對撞...")

        for i, name_a in enumerate(names):
            # 初始化矩陣槽位
            if "current_aff_matrix" not in self.chars[name_a]['social_field']:
                self.chars[name_a]['social_field']['current_aff_matrix'] = {}

            for name_b in names[i+1:]:
                # 初始化 B 的矩陣槽位
                if "current_aff_matrix" not in self.chars[name_b]['social_field']:
                    self.chars[name_b]['social_field']['current_aff_matrix'] = {}

                aff_value = self._calculate_pair_aff(name_a, name_b)
                
                # 寫入雙向矩陣
                self.chars[name_a]['social_field']['current_aff_matrix'][name_b] = aff_value
                self.chars[name_b]['social_field']['current_aff_matrix'][name_a] = aff_value
                
        # 更新版本號
        self.hub['version'] = "V8.1_Field_Ignited"
        
        with open(self.hub_path, 'w', encoding='utf-8') as f:
            json.dump(self.hub, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 點火完成！社交引力矩陣已根據「相位差」完成極化。")

if __name__ == "__main__":
    # 使用正確的路徑
    HUB_FILE_PATH = r"M:\AI生成\NISA\NISA_Soul_Master_Hub.json"
    
    try:
        igniter = NISA_Social_Ignition_V8(HUB_FILE_PATH)
        igniter.ignite()
    except Exception as e:
        print(f"[!] 點火失敗：{e}")