# Workflow: 文字描述 → FCStd

最快的路徑：使用者直接用文字描述需求，一來一回釐清規格。

## 步驟

### Step 1: 接收初始描述
例子：
> 幫我畫一個法蘭，外徑 100，內孔 60，厚度 15，4 個 M8 螺孔 PCD 80，全圓角

### Step 2: 判讀 + 補齊缺失資訊
根據 [pattern_library.md](pattern_library.md) 的模板比對出零件類別（此例：穿孔法蘭），然後問缺失的：
- 材質？（影響是否要做表面處理標註）
- 孔深？（M8 通孔 or 盲孔）
- 圓角半徑具體值？
- 有無倒角？

### Step 3: 列特徵清單讓使用者確認
```
零件類型: 穿孔法蘭
主體: 外徑100, 內孔60, 厚度15
孔: 4 x M8 盲孔深12, PCD 80, 均分
圓角: 外緣上下邊 R1, 內孔上下邊 R0.5
材質: [待定]
```

### Step 4-7: 同 photo workflow

## 文字輸入常見模式

使用者常用簡寫，理解一下：
- **PCD 80** = Pitch Circle Diameter = 孔圓直徑 80 = bolt circle
- **⌀ / 直徑 / OD** = 外徑, **ID** = 內徑
- **盲孔** = blind hole, **通孔** = through hole
- **沉頭 / Counter-sink (CSK)** = 錐形埋頭（用於埋頭螺絲）
- **沉座 / Counter-bore (CBore)** = 圓柱形埋頭（用於六角孔螺栓）
- **攻牙 / tap** = 內螺紋
- **銑平 / spotface** = 局部削平

## 單位預設
- 若未指明：毫米 (mm)
- 角度預設為度 (°)
- 螺紋預設 ISO metric，除非指定 UNC/UNF
