# 工位一键麦当劳

一句话：给办公室 N 人按忌辣/儿童/少糖等标签一键生成麦当劳午餐购物车草稿，并估算人均分摊。

## 这是什么

WorkBuddy Skill。场景是「谁去点餐」——同事在群里丢标签（忌辣、儿童餐、少糖、只要小食），Skill 调用麦当劳 MCP 拉菜单与营养信息，生成**一份可共享的购物车草稿** + **人均分摊估算**，减少来回确认。

默认**不下单、不支付**，只出草稿；有 Token 时用真菜单与 `calculate-price`。

## 目标用户

- 办公室团建 / 项目组午饭  
- 行政或「今天谁点外卖」的那个人  
- 需要快速照顾忌口与儿童的小团队（约 3–12 人）

## 安装（WorkBuddy）

1. MCP Token：见 `../TOKEN_SETUP.md` 或 https://open.mcd.cn/mcp  
2. WorkBuddy 启用 `mcd-mcp`  
3. 导入 `skills/mcd-office-lunch/`  
4. 对照 `USAGE.md` 录 ≤3 分钟演示  

## 快速用法

> 用「工位一键麦当劳」：5 人午餐，到店。标签——A忌辣，B儿童少辣，C少糖饮料，D正常，E只要薯条和麦乐鸡。出购物车草稿和人均分摊，别下单。

## 仓库结构

```
README.md
CONTEST_DECLARATION.md
MCP_INTEGRATION.md
workbuddy.md
USAGE.md
skills/mcd-office-lunch/SKILL.md
src/office_lunch.py
fixtures/team_sample.json
```

## 安全与合规

- 无真实 Token 入库  
- 不调用 `create-order`（演示）  
- 分摊仅为估算，实际以结账为准  

## 许可

参赛演示作品，非麦当劳官方产品。
