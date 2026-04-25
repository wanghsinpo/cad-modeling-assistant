---
name: cad-modeling-assistant
description: 從照片、工程圖或文字描述自動生成 FreeCAD 1.0.x 參數化模型（FCStd + Python macro）。觸發時機：使用者提到「幫我畫」「建模」「畫 CAD」「照片轉模型」「reverse engineer」「逆向工程」「FreeCAD 腳本」「參數化」，或上傳零件照片 / 工程圖 PDF / STEP 檔並要求產生 FCStd。專門針對奎邦精機廠風格（精密機械零件：環、軸、套筒、法蘭、殼體、治具），使用 PartDesign Body 工作流、PolarPattern 做環狀特徵、Fillet 優先於 Chamfer、TechDraw 出圖。
---

# CAD Modeling Assistant — 照片/圖面 → FreeCAD 參數化模型

## 用途
協助使用者把零件的視覺或描述性輸入（照片、工程圖 PDF、文字需求）轉換成**可修改的 FreeCAD 1.0.x 參數化模型**，包含完整特徵樹、草圖約束、TechDraw 工程圖。

## 適用情境

| 觸發訊號 | 動作 |
|---|---|
| 使用者上傳 2D 工程圖 PDF + 要求「幫我畫」 | 執行 [圖面 → FCStd 流程](workflow_drawing.md) |
| 使用者上傳零件照片（1 張或多張）+ 已知尺寸 | 執行 [照片 → FCStd 流程](workflow_photo.md) |
| 使用者給純文字描述（如「法蘭外徑 100，4 孔 M6」） | 執行 [描述 → FCStd 流程](workflow_text.md) |
| 使用者丟現有 FCStd 要求「修改」或「逆向」 | 先用 `tools/parse_fcstd.py` 讀特徵樹再處理 |

## 核心流程（不可跳過）

### 1. 語意判讀（在寫程式碼前先對齊）
**絕對不要**直接跳去寫 Python。先輸出**結構化特徵清單**給使用者確認：

```
零件類型：[軸/環/法蘭/板件/殼體]
主體起始特徵：[Pad / Revolution]
基本尺寸：外徑 __ / 總高 __ / 內孔 __
特徵清單（依加工順序）：
 1. [特徵名稱]：尺寸、位置、數量、陣列方式
 2. ...
我不確定的地方：
 - ...
```

使用者確認 / 修正清單後才進入第 2 步。

### 2. 結構化 JSON 產出
把特徵清單翻譯成 `spec.json`，格式見 [spec_schema.md](spec_schema.md)。

### 3. 執行生成器
```bash
python3 ~/.claude/skills/cad-modeling-assistant/tools/generate_macro.py spec.json output.FCMacro
```

### 4. 使用者在 FreeCAD 執行 macro
指示使用者：
1. 打開 FreeCAD
2. Macro → Macros → 選擇 `output.FCMacro` → Execute
3. 產生 FCStd 後用 TechDraw 出工程圖

### 5. 驗證迴圈
使用者回報哪裡錯 → 修 JSON 或 macro → 把學到的新規則**寫進 [lessons_learned.md](lessons_learned.md)**

---

## 奎邦建模風格（從使用者 27 個歷史 FCStd 萃取）

### 必遵守的風格規則

1. **一律使用 PartDesign Body** 工作流，不直接用 Part booleans
2. **起始特徵**：旋轉體類用 `Revolution`，其他用 `Pad`（54% Pad、31% Revolution）
3. **環狀重複特徵**：用 **PolarPattern**（不手動畫多個），`Angle=360`, `Occurrences` 依數量設定
4. **倒角優先順序**：`Fillet` > `Chamfer`（Fillet 出現 13 次 vs Chamfer 4 次）。除非明確要求銳邊倒角才用 Chamfer。
5. **Chamfer 預設**：0.5–1.0 mm @ 45°
6. **Fillet 預設**：1–3 mm（mean 3.46）
7. **螺紋孔**：用 PartDesign `Hole` feature（帶 `ThreadType`, `ThreadSize`），**不要**用 Pocket 畫螺紋牙型
8. **草圖幾何**：優先用 Line + Circle + Arc，不用 Spline 或 Ellipse
9. **最後產 TechDraw**：至少一個投影群組 (ProjGroup) + 關鍵尺寸標註

### 常用草圖約束分布（參考用，顯示使用者習慣）
| 約束 ID | 類型 | 出現次數 | 意義 |
|---|---|---|---|
| 1 | Coincident | 228 | 大量點對點重合 |
| 2 | Horizontal | 73 | 水平 |
| 3 | Vertical | 73 | 垂直 |
| 6 | Distance | 70 | 距離 |
| 7 | DistanceX | 36 | X 距離 |
| 8 | DistanceY | 34 | Y 距離 |
| 13 | PointOnObject | 87 | 點在物上 |
| 18 | Diameter | 28 | 直徑 |
| 12 | Equal | 23 | 相等 |

→ 產生草圖時**應充分約束**（fully constrained），優先用 Coincident + 距離約束。

### 典型特徵順序（bigram 分析）
- `Sketch → Pocket`（26 次，最常見）
- `Sketch → Pad`（17 次）
- `Pocket → PolarPattern`（10 次，挖槽後做環狀陣列）
- `Sketch → Revolution`（7 次，旋轉體起始）
- `Pad → Fillet`（3 次，最後收邊）

**建議順序**：基體（Pad/Revolution） → 挖槽（Pocket）→ 環狀陣列（PolarPattern）→ 倒角/圓角（Fillet/Chamfer）→ 螺紋孔（Hole）→ TechDraw

---

## 輸入資料品質排序（告訴使用者什麼最好給）

| 輸入格式 | 清晰度 | 備註 |
|---|---|---|
| FreeCAD Python macro | ★★★★★ | 直接執行可得 FCStd |
| FCStd 檔案 | ★★★★★ | 用 `tools/parse_fcstd.py` 解析 |
| 工程圖 PDF（含標註） | ★★★★ | 視覺 OCR 解析 |
| STEP / IGES | ★★★ | 只有幾何、無特徵樹 |
| 多視角照片 + 已知尺寸 | ★★★ | 需要視覺判讀 + 尺寸校正 |
| 單張照片 | ★ | 猜測成分高，不鼓勵 |
| STL / OBJ | ★ | 網格無語意 |

## 子檔案導覽

- [QUICK_START.md](QUICK_START.md) — **5 分鐘上手**（先看這個）
- [spec_schema.md](spec_schema.md) — 結構化零件描述 JSON schema
- [workflow_drawing.md](workflow_drawing.md) — 工程圖 → 模型流程
- [workflow_photo.md](workflow_photo.md) — 照片 → 模型流程
- [workflow_text.md](workflow_text.md) — 文字描述 → 模型流程
- [constraint_reference.md](constraint_reference.md) — FreeCAD 約束 ID 對照表
- [pattern_library.md](pattern_library.md) — 常見零件類別的建模模板
- [lessons_learned.md](lessons_learned.md) — 使用者回饋累積的規則
- `tools/parse_fcstd.py` — 解析 FCStd 特徵樹
- `tools/generate_macro.py` — 從 spec.json 生成 FreeCAD macro
- `tools/compare_fcstd.py` — 比對兩個 FCStd 特徵樹
- `tools/test_harness.py` — 自動測試框架
- `tools/example_specs/` — 5 個範例 JSON（含 KE-BH-072 重現）

## 驗證過的能力（2026-04-20）

測試過 5 個 spec → 100% 成功產出有效 FCStd：

| Spec | 產出體積 | 特徵數 | 備註 |
|---|---|---|---|
| simple_flange | 42,878 mm³ | 5 | Pad + Pocket + Hole + PolarPattern + Fillet |
| castellated_ring | 75,292 mm³ | 7 | 包含 2 組 PolarPattern |
| shaft_stepped | 19,620 mm³ | 2 | Revolution 起始 |
| shaft_with_keyway | 23,900 mm³ | 4 | 軸 + 端面螺紋孔 + 倒角 |
| ke_bh_072_reproduction | 93,442 mm³ | 7 + TechDraw | 重現真實客戶零件骨架 |

**FreeCAD 版本**：測試在 1.0.2 (Revision 39319)

## 和相關 skill 的關係

- 若使用者提到**草圖約束、TechDraw、Sketcher 細節**，可參考 `anthropic-skills:freecad-modeling` skill
- 若對象是星博（奎邦），搭配 `anthropic-skills:kueipang-andy-assistant`
