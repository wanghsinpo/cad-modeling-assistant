# Quick Start — 5 分鐘上手

## 情境 1：使用者丟照片 + 尺寸

```
使用者："幫我畫一個零件，外徑 80，中間有孔 30，4 個 M6 螺紋孔均分"
```

你要做的：

1. **先輸出特徵清單**（不要直接寫程式碼）：
```
零件：法蘭類
尺寸：外徑 80, 中孔 ⌀30, 厚度 ? (建議 10)
特徵：4 x M6 螺紋孔於 PCD ?（建議 56 = 外徑 * 0.7）
要確認：孔深、倒角、材質
```

2. 使用者確認 / 補充後，**寫 spec.json**（參考 `tools/example_specs/simple_flange.json`）

3. **生成 macro**：
```bash
python3 ~/.claude/skills/cad-modeling-assistant/tools/generate_macro.py \
    spec.json \
    output.FCMacro
```

4. **告訴使用者執行**：
```
把 output.FCMacro 複製到 ~/Library/Preferences/FreeCAD/Macro/
然後 FreeCAD → 工具列 Macro → Macros → 選擇 → Execute
```

或者直接在 terminal 跑：
```bash
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd output.FCMacro
```
這會自動產生 `output.FCStd` 在同目錄。

## 情境 2：使用者丟現有 FCStd 想改

先解析：
```bash
python3 ~/.claude/skills/cad-modeling-assistant/tools/parse_fcstd.py some.FCStd
```

輸出特徵樹給使用者看，確認要改哪裡，再處理。

## 情境 3：使用者丟工程圖 PDF

1. `Read` tool 讀 PDF
2. 萃取尺寸、視圖
3. 走 [workflow_drawing.md](workflow_drawing.md)

## 關鍵自我檢查

寫 spec 前問自己：
- [ ] 起始特徵是 Pad 還是 Revolution？
- [ ] 有對稱嗎？用 PolarPattern
- [ ] 螺紋用 Hole feature 不用 Pocket
- [ ] Fillet 優於 Chamfer（除非軸端）
- [ ] 要不要 TechDraw 出圖？

## FreeCAD 路徑 (macOS)

- CLI: `/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd`
- GUI: `/Applications/FreeCAD.app`
- User macros: `~/Library/Preferences/FreeCAD/Macro/`

## 常見錯誤

| 錯誤訊息 | 修法 |
|---|---|
| `AttributeError: 'SketchObject' object has no attribute 'Support'` | FreeCAD 1.0+ 用 `AttachmentSupport` |
| `Base feature's TopoShape is invalid` | Fillet/Chamfer 要在 `body.addObject()` **之前**設 Base |
| `Cannot make face from profile` | Hole 需要圓，不是點 → 自動轉換已實作 |
| `Source shape is Null` (TechDraw) | ProjGroup 的 Source 要在 addProjection **之前**設定 |
