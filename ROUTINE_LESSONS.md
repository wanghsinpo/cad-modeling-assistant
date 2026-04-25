# Lessons Learned from Past Routine Runs

每次自動排程跑壞東西，把教訓寫在這裡，**新的 routine 開始前必讀**。

---

## 2026-04-25 v1 routine（cad-nightly-improve）失敗教訓

### 問題清單

1. **沒 git push** → Andy 完全看不到進度，以為 routine 沒跑
2. **沒寫 nightly_log.md** → 連本機都看不到做了什麼
3. **改 generator 沒跑 test_harness** → 把測試從 5/5 弄成 0/7
4. **format() 字串 bug**：在 `MACRO_PREAMBLE` 三引號字串裡的 docstring 寫 `{"type": ...}` 沒 escape，導致 `KeyError`
5. **凹槽幾何概念錯**：把 rectangle 隨便放在 `(35, 0)` → 應該要中心通過原點、左右對稱於徑向線

### 鐵律（之後 routine 必須遵守）

| 鐵律 | 違反後果 |
|---|---|
| 動 generator 前 + 後都要跑 `test_harness.py` | pass 數降低 = 整次 stash 還原 |
| 任何 format() 字串裡的 `{` `}` 字面要 `{{` `}}` | KeyError |
| 結束必須 `git add -A && git commit && git push origin main` | 沒 push 算失敗 |
| 結束必須寫 nightly_log.md（最上面新增一筆） | 沒寫算失敗 |
| 不准動 user_corpus/ | 那是 Andy 的原始資料 |
| 一個 GitHub repo 只能由**一個** routine 寫入 | 避免衝突 |

### 凹槽 / 徑向特徵幾何規則

環/盤類零件上的徑向槽：
1. 中心線必須**通過圓心**（從原點出發的徑向線）
2. 寬度沿該徑向線的**垂直方向對稱**（左右各 W/2）
3. 長度沿徑向往內延伸從外緣到 inner_r
4. 多個槽用 PolarPattern 陣列，第一個放在 `angle=0` 或 `90` 然後陣列

已實作：`radial_notch` primitive in `tools/generate_macro.py:665`

### Format String 鐵律
```python
MACRO_PREAMBLE = '''
def f():
    """Doc with literal dict like {{"type": "od"}}"""  # 必須 escape
    x = {{"X": "X_Axis"}}                              # 必須 escape
    pct = "%s" % {{"k": v}}                            # 必須 escape
# Only {part_name} and {description} are real placeholders
'''
```

### 一個 routine 一個 repo 原則

| Routine | 寫入的 repo |
|---|---|
| cad-skill-improver（新版，本檔） | `cad-modeling-assistant` |
| ~~cad-nightly-improve~~ | 已 disable，2026-04-26 起停跑 |
| daily-onenote-selfquiz | `ai-code-framework` |
| gdrive-daily-index | （另外的 gdrive repo） |
| onenote-daily-review | （另外的） |
| kueipang-daily-log（cron 在主機本地，不是 routine） | `kueipang-daily-log` |

---

## 修改本檔的時機

每次新的 routine 跑壞東西、或學到新教訓、或新增規則，把它**寫進這裡**，下次 routine 開始時必讀。
