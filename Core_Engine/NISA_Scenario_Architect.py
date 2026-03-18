# NISA Engine V9: 劇情編排模組 (Scenario Module)
# 功能：自動生成各類型小說的物理參數序列 (H, TNS, WC)

import json
import math

class NISAScenarioArchitect:
    def __init__(self):
        # 類型定義矩陣：{類型: (初始H, 初始TNS, 建議單章字數WC)}
        self.genre_profiles = {
            "Historical_Strategy": { # 歷史權謀 (如: 三國)
                "base_h": 0.85,      # 高資訊熵 (政治博弈、虛實不明)
                "base_tns": 0.4,     # 中低張力 (慢節奏佈局)
                "avg_wc": 3000,      # 長篇幅 (詳盡描述對白與大勢)
                "h_trend": "wave",   # 資訊熵呈波浪狀揭露
                "tns_trend": "linear_up"
            },
            "Wuxia_Action": {        # 武俠動作 (如: 金庸)
                "base_h": 0.3,       # 低資訊熵 (敵我分明、直觀衝突)
                "base_tns": 0.7,     # 高張力 (戰鬥頻率高)
                "avg_wc": 1500,      # 中短篇幅 (節奏明快)
                "h_trend": "stable",
                "tns_trend": "sawtooth" # 鋸齒狀張力 (打鬥-休息-打鬥)
            },
            "Suspense_Thriller": {   # 懸疑驚悚
                "base_h": 0.95,      # 極高資訊熵 (真相完全鎖死)
                "base_tns": 0.6,     # 持續壓迫感
                "avg_wc": 2000,      # 中篇幅
                "h_trend": "collapse", # 結尾資訊熵崩潰 (真相大白)
                "tns_trend": "exponential" # 指數級張力飆升
            },
            "Power_Fantasy": {       # 爽文模式
                "base_h": 0.1,       # 極低資訊熵 (碾壓態勢)
                "base_tns": 0.2,     # 低張力 (主角掌控全局)
                "avg_wc": 1200,      # 短篇幅 (快速收割)
                "h_trend": "zero",
                "tns_trend": "burst"  # 爆發式張力 (平時低，高潮瞬間極高)
            }
        }

    def generate_chapter_config(self, genre, chapter_index):
        """
        計算特定章節的物理參數建議
        """
        profile = self.genre_profiles.get(genre)
        if not profile:
            return "Genre not found."

        # 基於章節序號計算動態演化
        # 範例：張力隨章節增加而波動
        tns_calc = profile["base_tns"] + (0.1 * math.sin(chapter_index))
        h_calc = profile["base_h"] * (0.95 ** chapter_index) # 資訊熵隨劇情推進逐漸減少

        return {
            "chapter": chapter_index,
            "physics_params": {
                "H_Entropy": round(max(0.1, h_calc), 2),
                "TNS_Tension": round(min(1.0, tns_calc), 2),
                "WC_Budget": profile["avg_wc"]
            },
            "narrative_focus": self._get_focus(genre, tns_calc)
        }

    def _get_focus(self, genre, tns):
        # 根據張力水準決定渲染焦點
        if tns > 0.8: return "Action_Intensive (動作重寫)"
        if genre == "Historical_Strategy": return "Dialogue_Subtext (對白潛台詞)"
        return "Environmental_Atmosphere (環境氛圍)"

# 中文註記：此腳本輸出的 JSON 將作為核心引擎的輸入變量