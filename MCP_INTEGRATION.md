# MCP 集成说明：工位一键麦当劳

## MCP Server

| 项 | 值 |
|---|---|
| Server | `mcd-mcp` |
| URL | `https://mcp.mcd.cn` |
| 协议 | Streamable HTTP / JSON-RPC 2.0 |
| 鉴权 | `Authorization: Bearer <MCP_TOKEN>`（仅 env / 仓库外 `.secrets/`，永不提交） |
| 文档 | https://open.mcd.cn/mcp/doc |

## 实机已验证（只读）

- `scripts/live_smoke.py`：`tools/list` + `list-nutrition-foods`（无需门店）
- 落盘 `/tmp/mcd-smoke-*.json`；**永不打印 Token**
- **禁止演示调用：** `create-order`、`mall-create-order`、`cancel-order`、`auto-bind-coupons`、`draw-lottery`；`delivery-create-address` 仅用户明确要求时

## 使用的 Tools

| Tool | 用途 |
|---|---|
| `now-time-info` | 确认午餐时段 |
| `query-nearby-stores` / `delivery-query-stores` | 到店 / 外送门店 |
| `delivery-query-addresses` | 外送：已有地址列表（只读） |
| `query-meals` | 可售菜单（需门店） |
| `query-meal-detail` | 套餐可否替换（儿童/忌辣） |
| `list-nutrition-foods` | 少糖/儿童向过滤（无需门店） |
| `query-meal-assistance` | 企业团餐助餐（可选，`beType=6`） |
| `query-store-coupons` / `query-my-coupons` | 团餐优惠只读展示 |
| `calculate-price` | 整单报价（含配送费若外送） |

## Safe 调用流程

```
输入：人数 N、每人标签、取餐方式、工位地址（可选）
  → now-time-info
  → 选店（query-nearby-stores / delivery-query-stores）
  → query-meals (+ meal-detail / list-nutrition-foods)
  → 按标签映射选品（src/office_lunch.py）
  → calculate-price(整单草稿)
  → 输出：购物车、总价、人均、按人明细 · 未下单
```

无 Token：`fixtures/team_sample.json` mock。

## 业务价值

- 一次对齐忌口；分摊透明；可执行草稿，支付仍由人工在官方渠道完成。
