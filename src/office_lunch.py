#!/usr/bin/env python3
"""工位一键麦当劳：按标签生成整单草稿与分摊（mock）。"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "team_sample.json"


def load() -> dict[str, Any]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def pick_for_label(label: str, catalog: list[dict[str, Any]]) -> list[dict[str, Any]]:
    label = label.strip()
    by_code = {c["code"]: c for c in catalog}

    def non_spicy_combos():
        return [c for c in catalog if c.get("tags") and "套餐" in c["tags"] and not c.get("spicy")]

    if label in ("忌辣", "no_spicy", "不辣"):
        combos = sorted(non_spicy_combos(), key=lambda x: x["price"])
        return [combos[0]] if combos else []

    if label in ("儿童", "kids", "儿童少辣"):
        kid = by_code.get("KID-SET")
        if kid:
            return [kid]
        combos = [c for c in non_spicy_combos() if c.get("kid_ok")]
        return [sorted(combos, key=lambda x: x["price"])[0]] if combos else []

    if label in ("少糖", "less_sugar"):
        # 正常套餐 + 无糖饮料（演示：套餐已含饮时仍可展示无糖替换意图）
        combos = sorted(non_spicy_combos(), key=lambda x: x["price"])
        drink = by_code.get("DRINK-0") or by_code.get("DRINK-OJ")
        items = []
        if combos:
            items.append(combos[0])
        if drink:
            items.append(drink)
        return items

    if label in ("只要小食", "小食", "sides"):
        fries = by_code.get("FRIES-M")
        nug = by_code.get("NUG-6")
        return [x for x in (fries, nug) if x]

    # 正常
    big = by_code.get("COMBO-BIG")
    if big:
        return [big]
    combos = sorted([c for c in catalog if "套餐" in c.get("tags", [])], key=lambda x: -x["price"])
    return [combos[0]] if combos else []


def build_order(
    team: list[dict[str, Any]],
    catalog: list[dict[str, Any]],
    *,
    delivery: bool,
    delivery_fee: float,
) -> dict[str, Any]:
    per_person: list[dict[str, Any]] = []
    subtotal = 0.0
    for person in team:
        items = pick_for_label(person["label"], catalog)
        line_sum = sum(float(i["price"]) for i in items)
        subtotal += line_sum
        per_person.append(
            {
                "id": person["id"],
                "label": person["label"],
                "items": [{"name": i["name"], "price": i["price"]} for i in items],
                "subtotal": line_sum,
            }
        )
    fee = delivery_fee if delivery else 0.0
    pay = subtotal + fee
    n = max(1, len(team))
    return {
        "per_person": per_person,
        "subtotal": subtotal,
        "delivery_fee": fee,
        "pay": pay,
        "per_capita": round(pay / n, 2),
    }


def render(store_name: str, mode: str, result: dict[str, Any], mock: bool = True) -> str:
    lines = []
    for p in result["per_person"]:
        names = " + ".join(f"{i['name']}(¥{i['price']:.0f})" for i in p["items"]) or "（未匹配到餐品）"
        lines.append(f"{p['id']}. [{p['label']}] {names} — ¥{p['subtotal']:.2f}")
    body = "\n".join(lines)
    src = "本地 mock" if mock else "MCP"
    return f"""【工位一键麦当劳 · 草稿】（{src}）
门店 / 方式：{store_name} / {mode}
按人明细：
{body}
整单：商品 ¥{result['subtotal']:.2f} + 配送费 ¥{result['delivery_fee']:.2f} → 应付 ¥{result['pay']:.2f}
分摊：人均约 ¥{result['per_capita']:.2f}（按人数均分，含配送费）
忌口核对：已按标签选品（忌辣不点麦辣；儿童走儿童/温和套餐；少糖附加无糖饮料；小食党只点薯条+麦乐鸡）。
状态：仅草稿，未创建订单、未支付。
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--delivery", action="store_true")
    args = ap.parse_args()
    data = load()
    result = build_order(
        data["defaultTeam"],
        data["catalog"],
        delivery=args.delivery,
        delivery_fee=float(data.get("deliveryFeeMock") or 0),
    )
    mode = "外送(模拟配送费)" if args.delivery else "到店"
    print(render(data["store"]["name"], mode, result, mock=True))


if __name__ == "__main__":
    main()
