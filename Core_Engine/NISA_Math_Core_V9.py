import numpy as np

class NISA_Math_Core_V9:
    def __init__(self, hub_data):
        self.entities = hub_data['characters']
        self.orgs = hub_data['organizations']
        self.critical_tns = hub_data['world_constants'].get('critical_tns_threshold', 0.9)

    def calculate_drive_and_tension(self, char_name):
        """計算位能差 (Drive)，若路徑受阻則轉化為張力 (TNS)"""
        char = self.entities[char_name]
        l1 = char.get('init_l1', {})
        target_linking = char.get('motivation_engine', {}).get('target_linking', {})
        
        if not target_linking:
            return 0.0

        target_id = target_linking.get('target_id')
        target_params = target_linking.get('target_params', {})
        
        # 取得目標實體 (組織或個人)
        target_entity = self.orgs.get(target_id, self.entities.get(target_id, {}))
        target_l1 = target_entity.get('init_l1', {})
        
        total_drive = 0.0
        
        # 計算 ∑ w_i * (P_target - P_current)
        for param, desired_val in target_params.items():
            current_val = target_l1.get(param, 0.5)
            delta = desired_val - current_val
            if delta > 0:
                total_drive += delta

        # 【對價路徑封鎖邏輯】
        # 檢測角色自身的 POW (權力) 是否足以推動這個 Drive。若阻力 > 動力，則驅動力無法釋放。
        char_pow = l1.get('POW', 0.5)
        environmental_resistance = target_entity.get('group_constants', {}).get('ENT', 0.5) # 熵值即阻力
        
        if char_pow < environmental_resistance:
            # 動能被封鎖，100% 轉化為內部張力 (TNS)
            blocked_energy = total_drive * (environmental_resistance - char_pow)
            l1['TNS'] = min(1.0, l1.get('TNS', 0.0) + blocked_energy)
            print(f"[引擎警告] {char_name} 的驅動力遭到系統熵封鎖。張力 (TNS) 暴增至 {l1['TNS']:.3f}")
            
            # 觸發強制代價支付
            self._apply_sacrifice_order(char_name, blocked_energy)

        return total_drive

    def _apply_sacrifice_order(self, char_name, tension_amount):
        """當張力無法釋放時，強制依照 sacrifice_order 扣除參數"""
        char = self.entities[char_name]
        l1 = char.get('init_l1', {})
        sacrifice_order = char.get('sacrifice_order',[])
        
        remaining_penalty = tension_amount
        
        for stat in sacrifice_order:
            if remaining_penalty <= 0:
                break
            current_stat_val = l1.get(stat, 0.0)
            if current_stat_val > 0:
                deduction = min(current_stat_val, remaining_penalty)
                l1[stat] -= deduction
                remaining_penalty -= deduction
                print(f"[物理結算] {char_name} 為了抵銷張力，獻祭了 {stat} (-{deduction:.3f})。剩餘: {l1[stat]:.3f}")

        # 如果連 SAF (安全) 都歸零，宣告崩潰
        if l1.get('SAF', 1.0) <= 0.0:
            char['status'] = 'DECEASED'
            print(f"💀 [狀態塌縮] {char_name} SAF 歸零，生命體徵終止。")