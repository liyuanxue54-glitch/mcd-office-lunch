# WorkBuddy 开发对话记录 · 工位一键麦当劳

> 使用 WorkBuddy + mcd-mcp 开发本 Skill 的关键对话，供参赛核验。默认不下单。

---

## 回合 1 — 场景

**用户：**  
第二个参赛作品：办公室多人点麦当劳，有人忌辣、有儿童、有人要少糖，想一键出购物车和人均分摊。

**WorkBuddy：**  
立项「工位一键麦当劳」。流程：收集每人标签 → `query-nearby-stores` / `query-meals` →（可选）`list-nutrition-foods` → 整单 `calculate-price` → 输出草稿与人均。不调用 `create-order`。

---

## 回合 2 — 标签映射

**用户：**  
标签就五种：忌辣、儿童、少糖、正常、只要小食。先 mock。

**WorkBuddy：**  
已在 `src/office_lunch.py` 实现映射；`fixtures/team_sample.json` 含 5 人默认队。模拟跑到店草稿：吉士套餐 / 儿童欢乐套餐 / 麦香鸡+无糖可乐 / 巨无霸套餐 / 薯条+麦乐鸡，并给出人均。

（工具意图）

```text
→ query-meals
← catalog
→ calculate-price(整单)
← 商品合计 + 可选配送费
```

---

## 回合 3 — 外送

**用户：**  
加一个外送演示，配送费进人均。

**WorkBuddy：**  
`--delivery` 时计入 mock 配送费；真机用 `delivery-query-stores` + `calculate-price` 的配送费字段。仍不下单。

---

## 回合 4 — 材料

**用户：**  
CONTEST_DECLARATION 用官方原文，补 MCP_INTEGRATION、USAGE、README。

**WorkBuddy：**  
已复制官方声明（未改字）。USAGE 控制 3 分钟。可推 Public 仓并发 Issue 报名。

---

---

## 回合 5 — 实机 MCP 冒烟

**用户：**  
Token 已就绪，跑一遍只读 live smoke，确认工具名和营养列表可用。

**WorkBuddy：**  
已用 `scripts/live_smoke.py` 对 `https://mcp.mcd.cn` 完成：`initialize` → `tools/list` → `list-nutrition-foods`（无需门店）。结果写入 `/tmp/mcd-smoke-*.json`。**Live MCP verified**（只读）。演示仍不调用 `create-order` / `mall-create-order` / `cancel-order` / `auto-bind-coupons` / `draw-lottery`。Token 仅存仓库外 `.secrets/`，未写入本对话、未提交。

---

## 验收自检

- [x] 调用链只读 + 算价  
- [x] 中文输出模板  
- [x] mock 可演示  
- [x] **Live MCP verified**（tools/list + list-nutrition-foods）  
- [x] 声明文件齐全；无 Token 进仓  
