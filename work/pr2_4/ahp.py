"""
Практична робота №4 (розділ 2) — Варіант 6
Прийняття рішень з використанням методу аналізу ієрархій (МАІ)

Задача 1 (Додаток Д, варіант 6): вибір виду транспорту для подорожі
    (залізничний / автомобільний / авіа) за критеріями час, комфорт,
    безпека, вартість — власна побудова ієрархії.

Задача 2 (Додаток Ж, варіант 6): вибір постачальника продукції з п'яти
    альтернатив за критеріями інтервал поставок, обсяг поставок, вартість,
    місце розташування, надійність.

Усі обчислені результати також зберігаються у data.json, який читає
безпосередньо Typst-звіт.
"""
import json
import pathlib

import numpy as np

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent

RI_TABLE = {1: 0, 2: 0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}


def geom_priority(M):
    """Метод середнього геометричного (нормований власний вектор), табл. 4.4."""
    n = M.shape[0]
    gm = np.prod(M, axis=1) ** (1 / n)
    w = gm / gm.sum()
    return w, gm


def consistency(M, w):
    n = M.shape[0]
    lam_max = (M.sum(axis=0) * w).sum()
    CI = abs(lam_max - n) / (n - 1) if n > 1 else 0.0
    RI = RI_TABLE.get(n, 1.12)
    CR = CI / RI if RI > 0 else 0.0
    return lam_max, CI, CR


def ratio_matrix(values, lower_better):
    """Побудова ідеально узгодженої МПП безпосередньо з кількісних даних:
    a_ij = v_j/v_i (якщо менше — краще) або v_i/v_j (якщо більше — краще)."""
    v = np.array(values, dtype=float)
    n = len(v)
    M = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            M[i, j] = (v[j] / v[i]) if lower_better else (v[i] / v[j])
    return M


def r4(x):
    if isinstance(x, np.ndarray):
        return np.round(x, 4).tolist()
    return round(float(x), 4)


def report_matrix(M, w, label):
    lam_max, CI, CR = consistency(M, w)
    print(f"--- {label} ---")
    print(f"M =\n{M}")
    print(f"w = {np.round(w, 4)}")
    print(f"lambda_max = {lam_max:.4f}, CI = {CI:.4f}, CR = {CR:.4f}"
          + ("  (CR > 0.1 !)" if CR > 0.1 else ""))
    return lam_max, CI, CR


data = {}

print("=" * 70)
print("ЗАДАЧА 1. Вибір виду транспорту для подорожі (варіант 6, Додаток Д)")
print("=" * 70)

# ---------------------------------------------------------------
# Ієрархія: мета - вибір транспорту; критерії - час, комфорт, безпека,
# вартість; альтернативи - залізничний (A), автомобільний (B), авіа (C)
# ---------------------------------------------------------------
alt_names_1 = ["Залізничний (A)", "Автомобільний (B)", "Авіа (C)"]
crit_names_1 = ["Час у дорозі", "Комфорт", "Безпека", "Вартість проїзду"]

# Матриця попарних порівнянь критеріїв (власна експертна оцінка)
C1 = np.array([
    [1, 3, 1 / 2, 2],
    [1 / 3, 1, 1 / 4, 1 / 2],
    [2, 4, 1, 3],
    [1 / 2, 2, 1 / 3, 1],
])
w_crit1, gm_crit1 = geom_priority(C1)
lam1, CI1, CR1 = report_matrix(C1, w_crit1, "Матриця попарних порівнянь критеріїв (Задача 1)")

# Вихідні кількісні дані для альтернатив за кожним критерієм (умовні, для ілюстрації)
time_v = [6, 8, 2]        # години в дорозі (менше -> краще)
comfort_v = [8, 5, 7]     # бали комфорту, 0-10 (більше -> краще)
safety_v = [8, 6, 9]      # бали безпеки, 0-10 (більше -> краще)
cost_v = [800, 500, 2000]  # вартість, грн (менше -> краще)

print("\nВихідні дані альтернатив:")
print(f"Час, год: {time_v}")
print(f"Комфорт, бали: {comfort_v}")
print(f"Безпека, бали: {safety_v}")
print(f"Вартість, грн: {cost_v}")

crit_data_1 = {
    "Час у дорозі": (time_v, True),
    "Комфорт": (comfort_v, False),
    "Безпека": (safety_v, False),
    "Вартість проїзду": (cost_v, True),
}

local_1 = {}
local_1_details = {}
print()
for name, (v, lower) in crit_data_1.items():
    M = ratio_matrix(v, lower)
    w, gm = geom_priority(M)
    lam, CI, CR = report_matrix(M, w, f"МПП альтернатив за критерієм «{name}»")
    local_1[name] = w
    local_1_details[name] = {"matrix": r4(M), "w": r4(w), "CR": r4(CR)}

local_matrix_1 = np.array([local_1[c] for c in crit_names_1])  # rows=criteria, cols=alternatives
global_1 = w_crit1 @ local_matrix_1

print("\nГлобальні пріоритети альтернатив (Задача 1):")
for name, val in zip(alt_names_1, global_1):
    print(f"  {name}: {val:.4f}")
best_1 = alt_names_1[int(np.argmax(global_1))]
print(f"Найкраща альтернатива: {best_1}")

data["task1"] = {
    "alt_names": alt_names_1,
    "crit_names": crit_names_1,
    "criteria_matrix": r4(C1),
    "criteria_w": r4(w_crit1),
    "criteria_lambda_max": r4(lam1),
    "criteria_CI": r4(CI1),
    "criteria_CR": r4(CR1),
    "raw_data": {
        "Час у дорозі": time_v,
        "Комфорт": comfort_v,
        "Безпека": safety_v,
        "Вартість проїзду": cost_v,
    },
    "local": local_1_details,
    "global": r4(global_1),
    "best": best_1,
}

print("\n" + "=" * 70)
print("ЗАДАЧА 2. Вибір постачальника продукції (варіант 6, Додаток Ж)")
print("=" * 70)

suppliers = ["Постачальник 1", "Постачальник 2", "Постачальник 3", "Постачальник 4", "Постачальник 5"]
crit_names_2 = ["Інтервал поставок", "Обсяг поставок", "Вартість", "Місце розташування", "Надійність"]

# Матриця попарних порівнянь критеріїв (табл. 4.12 методичних вказівок,
# однакова для всіх варіантів — відображає загальні пріоритети ОПР
# незалежно від конкретних даних постачальників)
C2 = np.array([
    [1, 3, 1 / 5, 1 / 6, 1 / 8],
    [1 / 3, 1, 1 / 6, 1 / 8, 1 / 9],
    [5, 6, 1, 1 / 3, 1 / 5],
    [6, 8, 3, 1, 1 / 3],
    [8, 9, 5, 3, 1],
])
w_crit2, gm_crit2 = geom_priority(C2)
lam2, CI2, CR2 = report_matrix(C2, w_crit2, "Матриця попарних порівнянь критеріїв (Задача 2, табл. 4.12)")

# Вихідні дані постачальників, варіант 6 (Додаток Ж)
interval_v = [20, 20, 20, 20, 40]
volume_v = [15, 20, 80, 50, 200]  # 200 - умовний еквівалент "необмеженого" обсягу
cost_v2 = [230.00, 240.00, 294.00, 270.00, 97.00]
distance_v = [75, 90, 60, 100, 75]
reliability_v = [99.892, 100.0, 99.407, 98.928, 100.0]

print("\nВихідні дані постачальників (варіант 6):")
print(f"Інтервал поставок, днів: {interval_v}")
print(f"Обсяг поставок, т (5-й умовно = 200): {volume_v}")
print(f"Вартість, тис. грн: {cost_v2}")
print(f"Місце розташування, км: {distance_v}")
print(f"Надійність, %: {reliability_v}")

crit_data_2 = {
    "Інтервал поставок": (interval_v, True),
    "Обсяг поставок": (volume_v, False),
    "Вартість": (cost_v2, True),
    "Місце розташування": (distance_v, True),
    "Надійність": (reliability_v, False),
}

local_2 = {}
local_2_details = {}
print()
for name, (v, lower) in crit_data_2.items():
    M = ratio_matrix(v, lower)
    w, gm = geom_priority(M)
    lam, CI, CR = report_matrix(M, w, f"МПП постачальників за критерієм «{name}»")
    local_2[name] = w
    local_2_details[name] = {"matrix": r4(M), "w": r4(w), "CR": r4(CR)}

local_matrix_2 = np.array([local_2[c] for c in crit_names_2])
global_2 = w_crit2 @ local_matrix_2

print("\nГлобальні пріоритети постачальників (Задача 2):")
for name, val in zip(suppliers, global_2):
    print(f"  {name}: {val:.4f}")
best_2 = suppliers[int(np.argmax(global_2))]
print(f"Найкращий постачальник: {best_2}")

data["task2"] = {
    "suppliers": suppliers,
    "crit_names": crit_names_2,
    "criteria_matrix": r4(C2),
    "criteria_w": r4(w_crit2),
    "criteria_lambda_max": r4(lam2),
    "criteria_CI": r4(CI2),
    "criteria_CR": r4(CR2),
    "raw_data": {
        "Інтервал поставок": interval_v,
        "Обсяг поставок": volume_v,
        "Вартість": cost_v2,
        "Місце розташування": distance_v,
        "Надійність": reliability_v,
    },
    "local": local_2_details,
    "global": r4(global_2),
    "best": best_2,
}

out_path = SCRIPT_DIR / "data.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\nДані збережено у {out_path}")
