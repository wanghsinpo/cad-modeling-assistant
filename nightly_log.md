# Nightly Run Log

每次排程任務跑完會在這裡寫一筆摘要。最新的在最上面。

---

## 2026-04-25 (Andy 手動驗證)

**狀況確認**：scheduled task `cad-nightly-improve` 在 4/22–4/25 期間有 lastRunAt 紀錄但**沒有完整跑完流程**（沒寫 nightly_log、沒 push GitHub、backlog 只完成 1/20）。發現原因：

### 排程跑了什麼（從檔案修改時間推斷）
- 4/22 ~ 4/24：可能跑了，但無法確認（沒 log）
- 4/25 (Apr 25 15:10)：產出 `tools/example_specs/ke_bh_072_v2.json`，新增 `radial_notch` 原語在 generator + test_harness 加入 v2 測試
- 但同時**搞壞了 generator**：`_auto_dimension` docstring 裡的 `{"type": ...}` 沒用 `{{ }}` escape，導致 `MACRO_PREAMBLE.format()` KeyError，**所有 7 個 spec 全部 0/7 失敗**

### Andy 手動修復
1. 把 4 處未 escape 的 `{...}` 改成 `{{...}}`（line 475–476 docstring + lines 516, 521, 526, 532 的 `% {{"value": value}}`）
2. 重跑 `test_harness.py` → **7/7 passed**（含新增的 ke_bh_072_v2）
3. 把 skill 推上 GitHub：https://github.com/wanghsinpo/cad-modeling-assistant — 之後每晚 nightly task 會 commit + push，可以從 GitHub commits 看每天進度

### Backlog 進度
- ✅ Q1 radial_notch primitive — 已實作（ke_bh_072_v2.json + generate_macro.py:665）
- 其他 19 題未動

### 對 nightly task 的修正
更新 SKILL prompt：
1. **必須**在開始/結束跑 `python3 tools/test_harness.py`，pass 數量降低就 git stash 還原
2. **必須**把 commit 推到 origin（已加 git remote）
3. **必須**寫 nightly_log.md，否則視為失敗
4. 強調 `format()` 字串裡所有 `{...}` 都要 escape

---

（等待下一次自動執行：2026-04-26 02:17 Taipei）
