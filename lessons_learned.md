# Lessons Learned — 使用者回饋累積

每次使用者糾正後，把規則寫進這裡。格式：**規則 + 原因 + 何時套用**。

---

## 2026-04-20 初始建立

### 風格總結（從 27 個歷史 FCStd 萃取）

1. **偏好 PartDesign Body，不用 Part booleans**
   - 原因：Body 有特徵樹可追溯修改
   - 套用：所有新模型

2. **螺紋孔一律用 Hole feature，不用 Pocket 畫牙型**
   - 原因：Hole feature 自帶螺紋規格參數，工程圖可以自動標「M4」
   - 套用：任何螺紋特徵

3. **環狀重複用 PolarPattern**
   - 原因：單點修改就更新所有陣列
   - 套用：≥ 3 個相同特徵均分圓周時

4. **Fillet 優先 Chamfer**
   - 原因：歷史 Fillet 13 次 vs Chamfer 4 次
   - 套用：除非明確要倒斜角（軸端、銑牙入口），其他邊緣用 Fillet

5. **Fillet 半徑預設 1–3 mm**
   - 原因：歷史 mean 3.46, 多數 ≤ 3
   - 套用：沒指定尺寸時的 fallback

6. **Chamfer 預設 0.5 x 45°**
   - 原因：歷史 mean 0.82
   - 套用：軸端、螺紋入口

7. **一律輸出 TechDraw 工程圖**
   - 原因：歷史每個檔案都有 ProjGroup + Dimensions
   - 套用：產生 FCStd 後追加 macro 建立工程圖

---

## （之後的回饋寫在下面）

### 2026-04-21 KE-BH-072 凹槽畫錯了（重要！）

使用者指正：「凹槽應該要中心指向圓心，然後往左右兩邊對稱的一個距離然後開槽」

**規則**：環狀零件上的 castellated notch / 徑向槽必須：
1. **中心線通過圓心**（槽的對稱軸是一條從原點出發的徑向線）
2. **槽的寬度沿該徑向線的垂直方向對稱**（左右各 W/2）
3. **槽的長度沿該徑向線方向**（從外緣往內延伸 L）

**我之前做錯的**：把 rectangle 放在 (35, 0) 隨便一個位置 → 應該要用**對稱於 X 軸 + 一端對齊外緣**的 sketch。

**正確的 spec 表達法**（之後 spec schema 新增 `radial_notch` 原語）：
```json
{
  "type": "radial_notch",
  "angle": 0,              // 槽的中心角度（從 X 軸開始，度）
  "width": 8,              // 切線方向寬度
  "depth_radial": 6,       // 徑向深度（從外緣往內）
  "outer_radius": 45       // 外緣半徑（從 sketch 推論）
}
```

**對應的 sketch geometry**（如果手畫）：
- 4 條線形成矩形
- 使用 `Symmetric` 約束（Type 14）把矩形對稱於 X 軸（或指定徑向線）
- `DistanceX` 約束鎖外緣 X 座標 = outer_radius
- `DistanceX` 約束鎖內緣 X 座標 = outer_radius - depth_radial
- `DistanceY` 鎖寬度（相對 X 軸對稱 → 上下 ±width/2）

**何時套用**：所有「環/盤類零件上的徑向槽」，包括 KE-BH-072、分度環、卡槽環、鎖緊環。

**原件 KE-BH-072 的實際做法**（從 Sketch003 分析）：
- 4 條 LineSegment
- Vertical (3) 2 條（左右短邊）
- Horizontal (2) 2 條（上下長邊）
- Symmetric (14) 約束：兩短邊對稱於某點（很可能是 X 軸）
- PointOnObject (13)：點在 V_axis (vertical axis)
- 一個 GeomPoint 放在 Y=49.47（外緣標示點）

→ 所以原件的槽是**沿徑向對稱於 X 軸**，左右各半寬。我之前放 `rectangle center=(35,0)` 雖然位置對但幾何意義錯了——應該要用**向 X 軸對稱**的約束系統。

### 2026-04-26 Q4: PolarPattern 後 BoundBox 異常變大

**現象**：simple_flange spec 設外徑 80mm，但 PolarPattern(Hole) 後 bbox 變 86.591mm。

**逐步追蹤**：
- Pad (base_disk):  bbox 80.0 ✅
- Pocket (center_bore): bbox 80.0 ✅
- Hole (bolt_hole, 單個): bbox 80.0 ✅
- **PolarPattern (4 holes): bbox 86.591** ⚠️
- Fillet: bbox 86.591（繼承）

**結論**：FreeCAD 1.0.x PartDesign Hole + PolarPattern 在計算 BoundBox 時包含了**螺紋的 cosmetic geometry**（threads helix 的外接幾何），不是實際零件外形。零件的 actual solid 仍是 ⌀80。

**何時要注意**：
- 用 bbox 估體積時要扣這個誤差（約 +8% on diameter for M4-M6）
- 跟客戶溝通要用「設計尺寸 OD 80」不是 bbox 數字
- TechDraw 出圖時的尺寸是從 sketch 讀取，不受影響

**工程師備註**：把這當 FreeCAD 的「特性」接受。如果未來要報告精確 bbox，先 suppress Hole 的螺紋 (Threaded=False) 量完再恢復。

### 2026-04-26 Q6: External corpus 下載

成功下載到 `/Users/linda/Downloads/cad/learn/external_corpus/`：
- `yann_parts/` — 107 個 FCStd（含吉他零件、機箱、支架、鍵盤支架）
- `fasteners_wb/`（FreeCAD Fasteners workbench source code，無 FCStd 但有螺絲生成邏輯參考）
- `freecad-parts/`（kilork — 含 CNC/3D printer 零件）

**這 20 個 sample 觀察**：
- 100% 用 Pad 起始（無 Revolution，因為這 corpus 主要是板件/盒體，非旋轉體）
- 主流 pattern: `Pad → Pocket (×N) → Pad → Fillet/Chamfer`
- 平均每件 4–8 個 feature
- 跟 Andy 風格相似度高（也用 PartDesign Body）

**可學習的新點**：
- `db-37-receiver` 連續 5 個 Pocket → 證實複雜零件確實要寫多個 Pocket spec
- `eletronic-box-bottom-cover` 用了 `Pad→Pad→Fillet→Pocket→Chamfer→Fillet→Pocket` — Fillet 可以**穿插在 Pocket 之間**（不是只在最後）

<!-- 格式範例
### YYYY-MM-DD 零件名稱

使用者指正：「XXX」

**規則**：...
**原因**：...
**何時套用**：...
-->

### 2026-04-26 新增 3 大類特徵支援

**Q22 ✅ Groove (revolutionary subtractive)**：
- 用途：環狀內凹槽 (O-ring 槽、卡簧槽、退刀槽)、車刀加工的旋轉減材
- spec：`{"type": "Groove", "sketch": {...}, "axis": "Z", "angle": 360}`
- 草圖畫**槽的橫截面**（封閉輪廓），系統繞 axis 旋轉減材
- vs Pocket+PolarPattern：Groove 是真正連續的環，PolarPattern 是離散陣列。**KE-BH-072 內溝其實該用 Groove**

**新增 PartDesign 原語 (primitive features)**：
- `AdditiveBox` (Length, Width, Height)
- `AdditiveCylinder` (Radius, Height, Angle)
- `AdditiveSphere` / `AdditiveCone` / `AdditiveTorus` / `AdditivePrism` / `AdditiveWedge`
- 對應的 `Subtractive*` 系列
- 用 `position: {"xyz": [x,y,z], "ypr": [yaw,pitch,roll]}` 定位
- 適合**不需要 sketch 的簡單形狀**（如螺栓孔、凸柱），比 Pad+sketch 簡潔

**新增規則**：
- 如果一個特徵可以用 sketch+Pad 也可以用 AdditiveCylinder，**優先用 primitive**（簡單、少一層 sketch 容易出錯）
- 環狀凹槽 (連續) → Groove；陣列槽 (離散) → Pocket+PolarPattern
