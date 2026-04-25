# FreeCAD Sketcher Constraint 參考

## 約束類型 ID 對照表（FreeCAD 1.0.x）

| ID | Python 常數 | 中文 | 用途 |
|---|---|---|---|
| 0 | `None` | 無 | (佔位) |
| 1 | `Coincident` | 重合 | 點對點重合 |
| 2 | `Horizontal` | 水平 | 線段水平 |
| 3 | `Vertical` | 垂直 | 線段垂直 |
| 4 | `Parallel` | 平行 | 線段平行 |
| 5 | `Tangent` | 相切 | 曲線相切 |
| 6 | `Distance` | 距離 | 兩元素距離 |
| 7 | `DistanceX` | X距離 | X 方向距離 |
| 8 | `DistanceY` | Y距離 | Y 方向距離 |
| 9 | `Angle` | 角度 | 兩線段夾角 |
| 10 | `Perpendicular` | 垂直 | 線段互相垂直 |
| 11 | `Radius` | 半徑 | 圓弧半徑 |
| 12 | `Equal` | 相等 | 長度/半徑相等 |
| 13 | `PointOnObject` | 點在物上 | 點落在線/圓上 |
| 14 | `Symmetric` | 對稱 | 對某元素對稱 |
| 15 | `InternalAlignment` | 內部對齊 | 橢圓/BSpline 內部 |
| 16 | `SnellsLaw` | 司乃耳定律 | 光學 |
| 17 | `Block` | 鎖定 | 固定位置 |
| 18 | `Diameter` | 直徑 | 圓直徑 |
| 19 | `Weight` | 權重 | BSpline 控制點 |

## Python API 用法

```python
import Sketcher

sketch.addConstraint(Sketcher.Constraint('Coincident', geo1, vtx1, geo2, vtx2))
sketch.addConstraint(Sketcher.Constraint('Horizontal', line_idx))
sketch.addConstraint(Sketcher.Constraint('Distance', p1_geo, p1_vtx, p2_geo, p2_vtx, 50.0))
sketch.addConstraint(Sketcher.Constraint('DistanceX', geo_idx, vtx, 30.0))
sketch.addConstraint(Sketcher.Constraint('Symmetric', g1, v1, g2, v2, axis_line_idx))
sketch.addConstraint(Sketcher.Constraint('Diameter', circle_idx, 50.0))
sketch.addConstraint(Sketcher.Constraint('Equal', line1, line2))
```

## 頂點索引 (vertex index)

- `1` = 起點
- `2` = 終點
- `3` = 中心點（圓 / 弧 / 橢圓）
- `-1` = 整條邊

## 特殊 geometry 索引

- `-1` = H_axis（水平軸）
- `-2` = V_axis（垂直軸）
- `0, 1, 2, ...` = 草圖內 geometry 的索引

## 充分約束 (Fully constrained) 檢查

```python
sketch.solve()  # 返回 0 = OK
dof = sketch.FullyConstrained  # True = 已充分約束
```

## 奎邦風格建議

根據使用者歷史（228 Coincident, 87 PointOnObject, 73 H/V, 70 Distance, 28 Diameter, 23 Equal）：

1. **優先使用 Coincident** 連接端點而不是畫 Polyline 後手動對齊
2. **Horizontal/Vertical 用於主要線段**，斜線用 Angle
3. **圓用 Diameter**，不用 Radius（使用者習慣）
4. **Distance 比 DistanceX/Y 常用**，但 X/Y 適合表達「往右 20」「往上 15」這種語意
5. **Symmetric 用於左右對稱設計**，搭配中心軸
6. **Equal 用於重複特徵的半徑統一**，減少錯漏
