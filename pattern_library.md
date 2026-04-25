# Pattern Library — 常見零件類別模板

從使用者 27 個歷史零件歸類出的典型建模套路。判讀新零件時先從這裡找最接近的模板。

---

## 1. 軸 (Shaft) — Revolution 起始

**典型特徵**：長對短比 > 3:1，多段不同直徑

**標準套路**：
```
1. 起始 Sketch (XZ plane): 畫側面半輪廓（多段折線）
2. Revolution: axis=Z, angle=360
3. 端面 Pocket: 鍵槽、螺紋底孔
4. 圓周 Pocket + PolarPattern: 均分槽
5. Chamfer: 軸端 0.5 x 45° (倒斜角)
6. Fillet: 直徑變化處 R0.5-R1
7. Hole (optional): 端面中心螺紋孔
```

**spec 片段**：
```json
{
  "base": {
    "type": "Revolution",
    "sketch": {
      "plane": "XZ",
      "geometry": [{"type":"polyline","points":[[0,0],[10,0],[10,20],[15,20],[15,40],[0,40]]}]
    },
    "axis": "Z", "angle": 360
  }
}
```

---

## 2. 環 / 套筒 (Ring / Sleeve)

**典型特徵**：外徑 ≈ 高度，中空 (ID/OD > 0.3)

**標準套路**：
```
1. Pad: 實心圓柱 (外徑)
2. Pocket: 中心內孔 (through_all)
3. 端面 Pocket + PolarPattern: 4/6/8 個螺紋孔位
4. Hole: 螺紋孔本體
5. 外緣 Pocket + PolarPattern: castellated notches (如果有)
6. Chamfer 內外倒角 0.5 x 45°
```

**範例**：KE-BH-072-EV-X-BP

---

## 3. 法蘭 (Flange)

**典型特徵**：扁平（高 < 外徑 / 3），多孔陣列

**標準套路**：
```
1. Pad: 圓盤外徑
2. Pocket: 中心孔
3. Hole + PolarPattern: bolt circle 上的螺栓孔（常 4/6/8 個）
4. Fillet: 外緣 R1-R2
5. (選) Pad: 凸緣 (spigot / pilot)
```

---

## 4. 板件 / 底板 (Plate / Base)

**典型特徵**：Pad 起始，矩形輪廓，多孔位

**標準套路**：
```
1. Sketch: 矩形輪廓 (可帶圓角: 用 fillet 2D 或外部 Fillet 特徵)
2. Pad: 厚度
3. Pocket 陣列 (LinearPattern): 通孔或沉頭孔
4. 邊角 Fillet: R5-R10
```

---

## 5. 殼體 / 外殼 (Housing / Shell)

**典型特徵**：Pad 起始，中空（薄壁），多面含特徵

**標準套路**：
```
1. Pad: 外形實心
2. Pocket: 內腔 (shell out)
3. 側壁 Pocket: 貫穿孔、接頭開口
4. 端面 Hole: 固定螺紋孔
5. 多處 Fillet: 內外邊緣 R2-R5
```

---

## 6. 治具 / Jig

**典型特徵**：對稱、定位面、夾持結構

**標準套路**：
```
1. Pad: 基座
2. Pad: 凸起定位塊（可多個）
3. Pocket: 定位孔 / 量測開口
4. Hole: 固定螺紋孔（通常 M4/M6）
5. Chamfer: 定位邊 0.5 方便工件入位
```

**範例**：鐵氟龍治具＿容器、Qnity試片基座

---

## 7. 齒輪 / 鍵合件

**典型特徵**：齒形輪廓 + 中心孔

**標準套路**：
```
1. Sketch: 齒形 (involute profile，可用 FreeCAD Gear workbench)
2. Pad: 齒厚
3. Pocket: 中心孔 + 鍵槽
4. Chamfer: 齒頂 0.3 x 45° (去毛邊)
```

---

## 分類啟發規則（從照片判讀時使用）

| 觀察到 | 判定為 |
|---|---|
| 長度 >> 直徑 | Shaft |
| 高度 ≈ 直徑 + 明顯中孔 | Ring |
| 扁平 + 螺栓陣列 | Flange |
| 矩形 + 多孔 | Plate |
| 有內腔、多面含開口 | Housing |
| 有定位凸塊 + 工件凹座 | Jig |
| 外緣有齒形 | Gear |

---

## 遇到不像上述任何一類的

→ 退回 [workflow_photo.md](workflow_photo.md) 的通用流程，詳細詢問使用者。

---

## 從 27 個歷史檔案歸納的實際模板（2026-04-20 自動萃取）

### 模板 A：Teflon 治具容器類 (`Pad → Pocket`)
適用於：鐵氟龍治具容器、容器上蓋。
```
1. Pad: 矩形 / 圓柱 外形
2. Pocket: 內凹腔（單次或多次）
```

### 模板 B：Sphere-Geneva 分度環類 (`Revolution → Pocket → PolarPattern → Pocket → PolarPattern → Fillet`)
適用於：sphere-geneva, sphere 系列。
```
1. Revolution: 球/盤形輪廓
2. Pocket: 徑向凹槽 seed
3. PolarPattern: 陣列凹槽
4. Pocket: 軸向孔 seed
5. PolarPattern: 陣列孔
6. Fillet: 全體圓角
```

### 模板 C：KE-BH-072 類（密集特徵環）
適用於：KE-BH-072 這種有 20+ 個特徵的複雜環。
```
1. Pad (annular sketch: 外圓+內圓): 中空圓柱一次完成
2. Pocket + PolarPattern x 多組: 每種槽一次
3. Hole (optional): 螺紋孔
4. Chamfer x N: 分別倒不同邊
5. Pad001 (追加): 中途再加凸台（如果有）
6. 更多 Pocket: 細部特徵
```

### 模板 D：階梯軸類 (`Revolution→Revolution→Revolution` 或 單 Revolution)
適用於：anti_G.FCStd 等多段不同直徑的軸。

### 模板 E：ShapeBinder→Pad 類
適用於：EDWARDS 轉子等——先引入一個參考輪廓（ShapeBinder），再 Pad。
```
1. ShapeBinder: 從另一個草圖/檔案匯入輪廓
2. Pad: 從該輪廓拉伸
```

### Starter 分布（從實際資料）
- Pad 7 次
- Revolution 4 次
- ShapeBinder 2 次
- 另有 14 個檔案沒有 PartDesign Body（是 Part workbench 或 STEP 匯入）

**啟示**：Andy 的工作流裡**不一定都是 PartDesign**。遇到匯入的 STEP/STP 檔案是 `Part::Feature`，不能直接套 PartDesign 模板。

