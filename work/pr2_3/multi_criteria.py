"""
Практична робота №3 (розділ 2) — Варіант 6
Прийняття рішень в задачах багатокритеріальної оптимізації

Задача: оптимальне завантаження трьох комбайнів (I, II, III), які виконують
три види робіт (A, B, C), за критеріями максимізації сумарного обсягу робіт
(f1) та мінімізації сумарної вартості (f2).

Усі обчислені результати також зберігаються у data.json, який читає
безпосередньо Typst-звіт.
"""
import json
import pathlib

import numpy as np
from scipy.optimize import linprog

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent


def r2(x):
    if isinstance(x, np.ndarray):
        return np.round(x, 2).tolist()
    return round(float(x), 2)


# ---------------------------------------------------------------
# Вихідні дані (варіант 6, Додаток В)
# ---------------------------------------------------------------
machines = ["I", "II", "III"]
jobs = ["A", "B", "C"]

q = np.array([
    [30, 20, 40],
    [40, 30, 20],
    [20, 40, 30],
], dtype=float)  # продуктивність q_ij, м3/год

c = np.array([
    [3, 6, 4],
    [4, 2, 3],
    [5, 3, 2],
], dtype=float)  # питома вартість c_ij, грн/год

T = np.array([450.0, 320.0, 300.0])  # ресурс часу, год

q_flat = q.flatten()
c_flat = c.flatten()

A_ub = np.zeros((3, 9))
for i in range(3):
    A_ub[i, i * 3:(i + 1) * 3] = 1
b_ub = T
bounds = [(0, None)] * 9


def solve(coef, extra_A=None, extra_b=None):
    A = A_ub if extra_A is None else np.vstack([A_ub, extra_A])
    b = b_ub if extra_b is None else np.append(b_ub, extra_b)
    res = linprog(coef, A_ub=A, b_ub=b, bounds=bounds, method="highs")
    return res.x


print("=" * 70)
print("Побудова математичної моделі (варіант 6)")
print("=" * 70)
print(f"q (продуктивність) =\n{q}")
print(f"c (питома вартість) =\n{c}")
print(f"T (ресурс часу) = {T}")

# ---------------------------------------------------------------
# Знаходження f1_max, f1_min, f2_max, f2_min для нормалізації
# ---------------------------------------------------------------
x_f1max = solve(-q_flat)
f1_max = q_flat @ x_f1max
f1_min = 0.0
f2_at_f1max = c_flat @ x_f1max

x_f2max = solve(-c_flat)
f2_max = c_flat @ x_f2max
f2_min = 0.0

print("\n--- Пошук max/min значень критеріїв для нормалізації ---")
print(f"f1_max = {f1_max} при x = {np.round(x_f1max, 2)}")
print(f"f1_min = {f1_min}")
print(f"f2_max = {f2_max} при x = {np.round(x_f2max, 2)}")
print(f"f2_min = {f2_min}")
print(f"f2 у розв'язку f1_max: {f2_at_f1max}")

# ---------------------------------------------------------------
# 2.1 Метод згортки (лінійна адитивна згортка нормованих критеріїв)
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("2.1 Метод згортки")
print("=" * 70)

alpha1, alpha2 = 0.5, 0.5
# F(x) = a1*(f1max-f1(x))/f1max + a2*(f2(x)-f2min)/f2max  -> min
coef_conv = -alpha1 / f1_max * q_flat + alpha2 / f2_max * c_flat
x_conv = solve(coef_conv)
f1_conv = q_flat @ x_conv
f2_conv = c_flat @ x_conv
F_conv = alpha1 * (f1_max - f1_conv) / f1_max + alpha2 * (f2_conv - f2_min) / f2_max

print(f"Вагові коефіцієнти: alpha1={alpha1}, alpha2={alpha2}")
print(f"x = {np.round(x_conv, 2)}")
print(f"f1 = {f1_conv}, f2 = {f2_conv}, F = {F_conv:.6f}")

# для довідки: результат зі значеннями ваг з методички (0.7/0.3) —
# ілюструє вироджений випадок, коли компроміс збігається з чистим max(f1)
coef_conv_ref = -0.7 / f1_max * q_flat + 0.3 / f2_max * c_flat
x_conv_ref = solve(coef_conv_ref)
f1_conv_ref = q_flat @ x_conv_ref
f2_conv_ref = c_flat @ x_conv_ref
print(f"\nДовідково, alpha1=0.7, alpha2=0.3: x = {np.round(x_conv_ref, 2)}, "
      f"f1={f1_conv_ref}, f2={f2_conv_ref} "
      f"({'збігається з чистим max(f1)' if np.allclose(x_conv_ref, x_f1max) else 'відрізняється'})")

# ---------------------------------------------------------------
# 2.2 Метод головного критерію
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("2.2 Метод головного критерію")
print("=" * 70)

f2_threshold = 3000.0
x_mc = solve(-q_flat, extra_A=c_flat, extra_b=f2_threshold)
f1_mc = q_flat @ x_mc
f2_mc = c_flat @ x_mc

print(f"Головний критерій: f1 -> max, додаткове обмеження f2(x) <= {f2_threshold}")
print(f"x = {np.round(x_mc, 2)}")
print(f"f1 = {f1_mc}, f2 = {f2_mc}")

# ---------------------------------------------------------------
# 2.3 Метод послідовної поступки
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("2.3 Метод послідовної поступки")
print("=" * 70)

delta_frac = 0.163
delta = round(delta_frac * f1_max)
f1_floor = f1_max - delta
x_seq = solve(c_flat, extra_A=-q_flat, extra_b=-f1_floor)
f1_seq = q_flat @ x_seq
f2_seq = c_flat @ x_seq

print(f"Крок 1: f1 -> max на всій множині: f1_max = {f1_max} (x = {np.round(x_f1max, 2)})")
print(f"Поступка Delta = {delta} ({delta_frac*100:.1f}% від f1_max), f1_floor = {f1_floor}")
print(f"Крок 2: f2 -> min за умови f1(x) >= {f1_floor}")
print(f"x = {np.round(x_seq, 2)}")
print(f"f1 = {f1_seq}, f2 = {f2_seq}")

# ---------------------------------------------------------------
# 2.4 Аналіз результатів
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("2.4 Зведена таблиця результатів")
print("=" * 70)

methods = [
    {"name": "Згортки", "x": x_conv, "f1": f1_conv, "f2": f2_conv},
    {"name": "Головного критерію", "x": x_mc, "f1": f1_mc, "f2": f2_mc},
    {"name": "Послідовної поступки", "x": x_seq, "f1": f1_seq, "f2": f2_seq},
]
for m in methods:
    print(f"{m['name']:<24} x={np.round(m['x'], 2)}  f1={m['f1']:.1f}  f2={m['f2']:.1f}")

# ---------------------------------------------------------------
# Збереження результатів у data.json
# ---------------------------------------------------------------
data = {
    "setup": {
        "machines": machines,
        "jobs": jobs,
        "q": q.astype(int).tolist(),
        "c": c.astype(int).tolist(),
        "T": T.astype(int).tolist(),
    },
    "normalization": {
        "f1_max": r2(f1_max),
        "f1_min": r2(f1_min),
        "x_f1max": r2(x_f1max),
        "f2_max": r2(f2_max),
        "f2_min": r2(f2_min),
        "x_f2max": r2(x_f2max),
        "f2_at_f1max": r2(f2_at_f1max),
    },
    "convolution": {
        "alpha1": alpha1,
        "alpha2": alpha2,
        "x": r2(x_conv),
        "f1": r2(f1_conv),
        "f2": r2(f2_conv),
        "F": round(float(F_conv), 6),
        "reference_0703": {
            "x": r2(x_conv_ref),
            "f1": r2(f1_conv_ref),
            "f2": r2(f2_conv_ref),
            "matches_f1max": bool(np.allclose(x_conv_ref, x_f1max)),
        },
    },
    "main_criterion": {
        "f2_threshold": f2_threshold,
        "x": r2(x_mc),
        "f1": r2(f1_mc),
        "f2": r2(f2_mc),
    },
    "sequential": {
        "delta_frac": delta_frac,
        "delta": delta,
        "f1_floor": r2(f1_floor),
        "x": r2(x_seq),
        "f1": r2(f1_seq),
        "f2": r2(f2_seq),
    },
    "summary": [
        {"method": m["name"], "x": r2(m["x"]), "f1": r2(m["f1"]), "f2": r2(m["f2"])}
        for m in methods
    ],
}

out_path = SCRIPT_DIR / "data.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\nДані збережено у {out_path}")
