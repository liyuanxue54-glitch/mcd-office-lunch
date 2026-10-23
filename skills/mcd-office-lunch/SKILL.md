---
name: mcd-office-lunch
description: >-
  当用户要给办公室多人点麦当劳午餐、按忌口/儿童/少糖标签凑一单、工位团餐或「工位一键麦当劳」时使用。
  调 mcd-mcp 查菜单与算价，输出购物车草稿与人均分摊；默认不下单支付。
---

# 工位一键麦当劳

办公室 N 人午餐：收集膳食标签 → 麦当劳 MCP 选品 → 一整单草稿 + 分摊估算。

## 硬规则

1. **禁止默认下单**：不调用 `create-order`。  
2. **标签优先于「随便」**：忌辣 / 儿童 / 少糖 / 只要小食 必须落到具体商品。  
3. **中文对用户输出**。  
4. **无 MCP**：用 `fixtures/team_sample.json` + `src/office_lunch.py`，并声明 mock。  
5. **分摊说明**：均为估算；外送费计入整单再平分（除非用户指定某人不参与配送费）。

## 收集输入

- 人数 N（或显式名单）  
- 每人标签：`忌辣` | `儿童` | `少糖` | `正常` | `只要小食` | 自由补充  
- 到店 / 外送（外送要地址）  
- 预算上限（可选）

## 工具顺序（有 mcd-mcp）

1. `now-time-info`  
2. `query-nearby-stores` 或 `delivery-query-stores`  
3. `query-meals`；按需 `query-meal-detail`、`list-nutrition-foods`  
4. 可选企业场景 `query-meal-assistance`  
5. 只读券：`query-store-coupons` / `query-my-coupons`  
6. 映射选品（见下）后 `calculate-price`  
7. 输出草稿 + 分摊，停止  

## 标签 → 选品策略

| 标签 | 策略 |
|---|---|
| 忌辣 | 排除 tags/名称含辣的汉堡与套餐，改选吉士/麦香鸡等 |
| 儿童 | 优先儿童向或小份套餐；避免重辣；饮料偏果汁/无糖 |
| 少糖 | 饮料选无糖或少糖可选；主食不依赖甜品 |
| 正常 | 当日性价比工作餐套餐一份 |
| 只要小食 | 薯条 + 麦乐鸡等，不强制套餐 |

## 输出模板

```text
【工位一键麦当劳 · 草稿】
门店 / 方式：…
按人明细：
1. … — ¥x
…
整单：原价 ¥A，优惠 ¥C，应付 ¥P（含配送费 ¥D）
分摊：人均约 ¥P/N（明细见上，可按实付四舍五入）
忌口核对：忌辣✓ 儿童✓ 少糖✓ …
状态：仅草稿，未下单未支付。
```

## 参考

- `src/office_lunch.py`  
- `fixtures/team_sample.json`  
- `MCP_INTEGRATION.md`
