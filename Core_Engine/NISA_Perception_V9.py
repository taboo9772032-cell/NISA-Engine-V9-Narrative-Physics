import random

class NISA_Perception_Filter_V9:
    def __init__(self):
        pass

    def calculate_gamma(self, observer_l1, target_l1, distance_mu):
        """
        計算感知解析度 Gamma (Γ)
        V9 優化：引入臨界張力下的「絕對洞察」效應
        """
        int_val = observer_l1.get('INT', 0.5)
        tns_val = observer_l1.get('TNS', 0.0)
        
        # 【絕對洞察機制】當張力 (TNS) > 0.9 且 智謀 (INT) > 0.8 時，看破所有迷霧
        if tns_val >= 0.9 and int_val >= 0.8:
            print(f"👁️ [感知異常] 觀測者進入臨界張力！觸發「絕對洞察」狀態，Γ = 1.0 (無視所有資訊噪點)。")
            return 1.0
            
        # 正常感知公式
        awa_val = observer_l1.get('AWA', 0.5)
        gamma = (int_val * 0.7 + awa_val * 0.3) / (distance_mu + 0.1)
        return round(max(0.1, min(1.0, gamma)), 4)

    def generate_noisy_snapshot(self, true_l1, gamma):
        """根據 Γ 值產生帶有情報熵噪點的快照"""
        if gamma >= 1.0:
            return true_l1.copy() # 絕對洞察，無損輸出
            
        perceived_l1 = {}
        noise_range = max(0, 1.0 - gamma) * 0.5 

        for key, value in true_l1.items():
            noise = random.uniform(-noise_range, noise_range)
            perceived_l1[key] = round(max(0.0, min(1.0, value + noise)), 3)
            
        return perceived_l1