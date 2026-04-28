# 客戶風格簽名分析（Q15）
從使用者 user_corpus 27 個 FCStd 依客戶/系列分群，萃取每群的設計指紋（feature 分布、起始類型、bigram、典型尺寸）。
用途：spec 階段判讀照片時，若已知客戶名 → 直接套用該客戶的常見模板。
---

## 未分類 / 練習件  （6 個檔案）
**檔案**：`20251229-01.FCStd`, `20260227-1.FCStd`, `test260107.FCStd`, `未命名.FCStd`, `未命名1.FCStd`, `未命名2.FCStd`

**起始特徵**：Pad(1)

**特徵分布**：Pad×2, Fillet×1

**Top bigrams**：`Pad→Pad`×1, `Pad→Fillet`×1

**平均複雜度**：每件 1.0 個 feature，1.2 個尺寸標註

## 杜邦/聯電 鐵氟龍治具  （5 個檔案）
**檔案**：`鐵氟龍guider.FCStd`, `鐵氟龍治具＿容器.FCStd`, `鐵氟龍治具＿容器上蓋.FCStd`, `鐵氟龍治具＿試片上蓋_矩形.FCStd`, `鐵氟龍治具＿試片基座_矩形.FCStd`

**起始特徵**：Pad(4)

**特徵分布**：Pocket×16, Pad×6, Plane×3, Fillet×3

**Top bigrams**：`Pocket→Pocket`×9, `Pad→Pocket`×6, `Pocket→Plane`×3, `Plane→Fillet`×3, `Fillet→Pad`×2

**平均複雜度**：每件 10.0 個 feature，39.2 個尺寸標註

## 其他  （4 個檔案）
**檔案**：`model_solid.FCStd`, `part01.FCStd`, `reverse_engineering_project.FC`, `早餐杯.FCStd`

**起始特徵**：Pad(1)

**特徵分布**：Pad×1

**平均複雜度**：每件 0.5 個 feature，0.5 個尺寸標註

## 雜項軸/旋轉體  （3 個檔案）
**檔案**：`anti_G.FCStd`, `cj1.FCStd`, `cj2.FCStd`

**起始特徵**：Revolution(1)

**特徵分布**：Revolution×3

**Top bigrams**：`Revolution→Revolution`×2

**平均複雜度**：每件 2.0 個 feature，35.0 個尺寸標註

## Sphere-Geneva 分度球  （3 個檔案）
**檔案**：`sphere-geneva-v1.FCStd`, `sphere-geneva-v2.FCStd`, `sphere.FCStd`

**起始特徵**：Revolution(3)

**特徵分布**：Fillet×9, Pocket×8, PolarPattern×6, Pad×6, Revolution×5, CoordinateSystem×2

**Top bigrams**：`Pocket→PolarPattern`×6, `Revolution→Pocket`×5, `Pad→Pad`×4, `Fillet→Fillet`×4, `PolarPattern→Pocket`×3

**平均複雜度**：每件 18.7 個 feature，16.7 個尺寸標註

## EDWARDS / 乾泵轉子  （2 個檔案）
**檔案**：`EDWARSD_IXH1210H-LV轉子.FCStd`, `EDWARSD_IXH1210H-LV轉子_2.FCStd`

**起始特徵**：ShapeBinder(2)

**特徵分布**：ShapeBinder×2, Pad×2

**Top bigrams**：`ShapeBinder→Pad`×2

**平均複雜度**：每件 3.0 個 feature，17.0 個尺寸標註

## 啟辰小馬  （2 個檔案）
**檔案**：`馬.FCStd`, `馬2.FCStd`

**平均複雜度**：每件 0.0 個 feature，0.0 個尺寸標註

## 培林座 (BH-bearing housing)  （1 個檔案）
**檔案**：`20260306_培林座.FCStd`

**平均複雜度**：每件 0.0 個 feature，0.0 個尺寸標註

## 奎邦 KE-BH 系列（自家料號）  （1 個檔案）
**檔案**：`KE-BH-072-EV-X-BP.FCStd`

**起始特徵**：Pad(1)

**特徵分布**：Pocket×11, PolarPattern×4, Chamfer×4, Pad×2, Hole×1

**Top bigrams**：`Pocket→Pocket`×4, `Pocket→PolarPattern`×4, `PolarPattern→Pocket`×3, `Pad→Pocket`×2, `Pocket→Chamfer`×2

**平均複雜度**：每件 37.0 個 feature，193.0 個尺寸標註

---
## 總結 — 推論時的快速查找表

| 客戶/系列 | 起始 | 主要特徵 | 建議模板 |
|---|---|---|---|
| 未分類 / 練習件 | Pad | Pad, Fillet | Pad → Pocket |
| 杜邦/聯電 鐵氟龍治具 | Pad | Pocket, Pad, Plane | Pad → Pocket |
| 其他 | Pad | Pad | Pad → Pocket |
| 雜項軸/旋轉體 | Revolution | Revolution | Revolution + Pocket+PolarPattern |
| Sphere-Geneva 分度球 | Revolution | Fillet, Pocket, PolarPattern | Revolution + Pocket+PolarPattern |
| EDWARDS / 乾泵轉子 | ShapeBinder | ShapeBinder, Pad | ShapeBinder→Pad（外部輪廓） |
| 啟辰小馬 | — |  | Pad → Pocket |
| 培林座 (BH-bearing housing) | — |  | Pad → Pocket |
| 奎邦 KE-BH 系列（自家料號） | Pad | Pocket, PolarPattern, Chamfer | Pad → Pocket |
