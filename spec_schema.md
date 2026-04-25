# Spec JSON Schema — 結構化零件描述

這是 `cad-modeling-assistant` 的中間表示層（IR）。所有輸入（照片、圖面、文字）最終都翻譯成這個 JSON，再由 `generate_macro.py` 轉成 FreeCAD macro。

## 頂層結構

```json
{
  "part_name": "KE-BH-072-EV-X-BP",
  "description": "環狀定位環",
  "units": "mm",
  "body": {
    "base": { ... },
    "features": [ ... ]
  },
  "drawing": {
    "views": ["front", "top", "iso"],
    "dimensions": [...]
  }
}
```

## `base` — 起始特徵

### Pad（拉伸圓柱 / 拉伸輪廓）
```json
{
  "type": "Pad",
  "sketch": {
    "plane": "XY",
    "geometry": [
      {"type": "circle", "center": [0,0], "radius": 50}
    ]
  },
  "length": 20,
  "midplane": false,
  "reversed": false
}
```

### Revolution（旋轉體）
```json
{
  "type": "Revolution",
  "sketch": {
    "plane": "XZ",
    "geometry": [
      {"type": "polyline", "points": [[20,0],[20,10],[30,10],[30,0]]}
    ]
  },
  "axis": "Z",
  "angle": 360
}
```

## `features` — 加工操作序列

每個 feature 依**執行順序**列出。

### Pocket
```json
{
  "type": "Pocket",
  "name": "Pocket_center_hole",
  "sketch": {
    "plane": "face:top",  // 或具體面 reference
    "geometry": [{"type":"circle","center":[0,0],"radius":15}]
  },
  "depth": 5,
  "through_all": false,
  "reversed": false
}
```

### PolarPattern（環狀陣列）
```json
{
  "type": "PolarPattern",
  "source_features": ["Pocket_center_hole"],
  "axis": "Z",
  "angle": 360,
  "occurrences": 4
}
```

### Hole（螺紋孔）
```json
{
  "type": "Hole",
  "sketch": {
    "plane": "face:top",
    "geometry": [{"type":"point","xy":[25,0]}]
  },
  "thread": {
    "type": "ISOMetricProfile",  // M3 / M4 / M5 / M6 / M8
    "size": "M4",
    "class": "6H"
  },
  "depth": 10,
  "counter_bore": null,
  "counter_sink": null
}
```

### Fillet
```json
{
  "type": "Fillet",
  "edges": ["top_outer", "bottom_outer"],  // 或 face-based selection
  "radius": 2
}
```

### Chamfer
```json
{
  "type": "Chamfer",
  "edges": ["top_bore"],
  "size": 0.5,
  "angle": 45
}
```

## 草圖 geometry 原語

| type | 欄位 | 說明 |
|---|---|---|
| `circle` | `center`, `radius` | 圓 |
| `arc` | `center`, `radius`, `start_angle`, `end_angle` | 圓弧 |
| `line` | `start`, `end` | 線段 |
| `polyline` | `points` | 多段線（會自動連接） |
| `rectangle` | `center`, `width`, `height` | 矩形 |
| `point` | `xy` | 點（用於 Hole 定位） |

## 草圖 constraints（可選，若不提供則生成器自動推論）

```json
"constraints": [
  {"type":"coincident","pts":[0,1]},
  {"type":"horizontal","line":2},
  {"type":"distance","from":0,"to":1,"value":50},
  {"type":"symmetric","about":"X_axis","pts":[3,4]}
]
```

## 平面 reference (`plane` 欄位)

- `"XY"`, `"XZ"`, `"YZ"` — 原點平面
- `"face:top"`, `"face:bottom"` — 目前形狀的頂 / 底面
- `"face:outer_cyl"` — 外圓柱面
- `"datum:offset_xy_20"` — 偏移 datum plane（生成器會自動建立）

## 最小完整範例（簡單法蘭）

```json
{
  "part_name": "simple_flange",
  "units": "mm",
  "body": {
    "base": {
      "type": "Pad",
      "sketch": {
        "plane": "XY",
        "geometry": [{"type":"circle","center":[0,0],"radius":40}]
      },
      "length": 10
    },
    "features": [
      {
        "type": "Pocket",
        "name": "center_bore",
        "sketch": {
          "plane": "face:top",
          "geometry": [{"type":"circle","center":[0,0],"radius":15}]
        },
        "through_all": true
      },
      {
        "type": "Hole",
        "name": "bolt_hole_1",
        "sketch": {
          "plane": "face:top",
          "geometry": [{"type":"point","xy":[28,0]}]
        },
        "thread": {"size":"M6","class":"6H"},
        "depth": 10
      },
      {
        "type": "PolarPattern",
        "source_features": ["bolt_hole_1"],
        "axis": "Z",
        "angle": 360,
        "occurrences": 4
      },
      {
        "type": "Fillet",
        "edges": ["top_outer","bottom_outer"],
        "radius": 1
      }
    ]
  }
}
```
