# Nightly Improvement Backlog

每晚排程任務會從這裡挑 10 題來回答 / 驗證 / 修正。已完成的打 ✅ 並註明日期。

---

## 🔴 High priority — 先答這些

- [ ] Q1. 徑向槽 (radial notch) 正確畫法：如何用 Symmetric 約束 + DistanceX 實作「中心指向圓心、左右對稱」？產出一個工作的 sketch geometry emitter，並在 ke_bh_072_reproduction_v2.json 裡使用。
- [ ] Q2. KE-BH-072 原件的 Sketch003/004/005 到底怎麼構成？逐一解碼 GeomPoint 座標、Symmetric 對象、PointOnObject 參考，寫成精確重建。
- [ ] Q3. 如何自動加 TechDraw Dimension？至少支援：外徑、總高、孔位 PCD。寫一個 `_auto_dimension()` helper 讓 spec 可以宣告哪些尺寸要標。
- [x] Q4. ✅ 2026-04-26：解開了 — Hole 的 cosmetic thread geometry 影響 PolarPattern bbox 計算。實體仍正確。記在 lessons_learned。
- [ ] Q5. Sketch on 圓柱面：除了 datum plane 還有哪些方法？PartDesign 有沒有直接 map to cylindrical face 的 MapMode？

## 🟡 Medium — 補齊能力

- [ ] Q6. 到 GitHub 找 10 個 FCStd + 對應 PDF/PNG 圖面的配對。優先領域：半導體精密件、pump parts、motor cores。來源候選：FreeCAD forum repos, grabcad 下載、McMaster 的 STEP+PDF、iso-3-d-parts。把找到的放進 `~/Downloads/cad/learn/external_corpus/`。
- [ ] Q7. 驗證 Hole feature 對 M3 / M4 / M5 / M6 / M8 / M10 全系列都能正確產生，包含盲孔 + 通孔 + counter_bore + counter_sink 變體。寫一個測試檔。
- [ ] Q8. 複雜 Pocket 幾何：橢圓孔、腰型孔 (slot) 怎麼畫？擴展 spec_schema 加入 `slot` 原語。
- [ ] Q9. Mirrored 和 LinearPattern 我實作了但沒測過。寫一個測試 spec 驗證。
- [ ] Q10. ShapeBinder 支援：Andy 的 EDWARDS 轉子系列用 ShapeBinder → Pad，現在 generator 不支援。如何支援？
- [ ] Q11. Revolution 起始輪廓的閉合檢查：polyline 最後一點要回到起點，但目前如果使用者忘了我沒檢查。加入自動閉合。
- [ ] Q12. 充分約束 (fully constrained) 檢查：每個 sketch 產完之後呼叫 `sk.solve()`，如果 DOF > 0 就報警並嘗試補約束。
- [ ] Q13. STEP import workflow：Andy 有時候從 STEP 開始做逆向。寫一個 import STEP → 提取主要幾何 → 建立 PartDesign Body 的流程。
- [ ] Q14. 材質標示：spec 裡的 material 欄位應該會寫到 TechDraw 的 title block。實作。
- [ ] Q15. Andy 的完整客戶零件風格比對：跑 compare_fcstd.py 對 EDWARDS 轉子、sphere-geneva、teflon jig 系列，找出每一系列的簽名特徵。

## 🟢 Low — 錦上添花

- [ ] Q16. 開源齒輪 workbench 整合：FreeCAD 有 Gear workbench，怎麼在 macro 裡引用？
- [ ] Q17. 導出到其他格式：STEP / DXF / STL 的 one-liner。
- [ ] Q18. 公差標註：ISO 2768 / 位置度 / 平行度 的 TechDraw 呈現。
- [ ] Q19. Spreadsheet 參數綁定：把關鍵尺寸連到 App::Spreadsheet，讓 Andy 改一處 update 整個模型。
- [ ] Q20. 多零件組立 (Assembly)：從多個 FCStd 拼起來做組立圖。

---

## 自我新增規則
每次 nightly run 結束時，若想到新問題就加到下面：

### （自動新增區）
