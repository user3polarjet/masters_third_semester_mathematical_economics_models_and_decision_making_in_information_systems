"""
Лабораторна робота №1, Блок 1.1 — Варіант 6
Двофакторна виробнича функція Кобба-Дугласа: Y = a0 * X1^a1 * X2^a2
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pathlib
import os
import json

SCRIPT_PATH = pathlib.Path(os.path.abspath(__file__))
SCRIPT_DIR = SCRIPT_PATH.parent
DATA_PATH = SCRIPT_DIR / "data.json"


def save_block(key, block):
    """Зчитує наявний data.json (якщо є), оновлює один блок і зберігає назад,
    щоб два скрипти лабораторної роботи могли ділити один файл даних."""
    data = {}
    if DATA_PATH.exists():
        with open(DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)
    data[key] = block
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def r6(x):
    if isinstance(x, np.ndarray):
        return np.round(x, 6).tolist()
    return round(float(x), 6)

# ---------------------------------------------------------------
# 1. Вихідні дані (варіант 6)
# ---------------------------------------------------------------
X1 = np.array([55.0, 55.4, 55.6, 56.8, 58.3, 59.7, 60.8, 63.6, 65.6, 68.0, 70.7, 71.4])
X2 = np.array([32.5, 36.7, 40.6, 45.0, 49.4, 52.2, 52.4, 55.3, 59.7, 60.4, 62.3, 65.6])
Y  = np.array([74.9, 81.7, 86.0, 93.1, 99.4, 102.3, 103.2, 109.2, 115.9, 117.4, 120.6, 124.7])

n = len(Y)

# ---------------------------------------------------------------
# 2. Лінеаризація: ln Y = ln a0 + a1 ln X1 + a2 ln X2
# ---------------------------------------------------------------
Z1 = np.log(X1)
Z2 = np.log(X2)
Y1 = np.log(Y)

# Регресія методом найменших квадратів (аналог LINEST)
A = np.column_stack([np.ones(n), Z1, Z2])
coef, residuals, rank, sv = np.linalg.lstsq(A, Y1, rcond=None)
ln_a0, a1, a2 = coef

Y1_pred = A @ coef
resid = Y1 - Y1_pred

# Коваріаційна матриця коефіцієнтів
p = A.shape[1]              # кількість коефіцієнтів (m)
dof = n - p                 # ступені свободи залишку
sigma2 = np.sum(resid ** 2) / dof
cov = sigma2 * np.linalg.inv(A.T @ A)
se = np.sqrt(np.diag(cov))
se_ln_a0, se_a1, se_a2 = se

a0 = np.exp(ln_a0)

# R^2 та F-критерій
ss_tot = np.sum((Y1 - Y1.mean()) ** 2)
ss_res = np.sum(resid ** 2)
r2 = 1 - ss_res / ss_tot
k1 = p - 1          # ступені свободи регресії (m-1)
k2 = n - p          # ступені свободи залишку (n-m)
F_stat = (r2 / k1) / ((1 - r2) / k2)
F_crit = stats.f.ppf(0.95, k1, k2)

print("=" * 70)
print("БЛОК 1.1. Двофакторна модель Кобба-Дугласа (Варіант 6)")
print("=" * 70)
print(f"n = {n}")
print(f"ln(a0) = {ln_a0:.6f}   SE = {se_ln_a0:.6f}")
print(f"a1     = {a1:.6f}   SE = {se_a1:.6f}")
print(f"a2     = {a2:.6f}   SE = {se_a2:.6f}")
print(f"a0     = {a0:.6f}")
print(f"R^2    = {r2:.6f}")
print(f"F      = {F_stat:.4f}   F_кр(0.95; {k1}; {k2}) = {F_crit:.4f}")
print(f"Модель {'достовірна' if F_stat > F_crit else 'недостовірна'} з ймовірністю 0.95")

# ---------------------------------------------------------------
# t-критерій Стьюдента для коефіцієнтів
# ---------------------------------------------------------------
t_crit = stats.t.ppf(0.975, dof)  # двостороння, рівень 0.95, dof=n-p
t_ln_a0 = ln_a0 / se_ln_a0
t_a1 = a1 / se_a1
t_a2 = a2 / se_a2

print("-" * 70)
print(f"t_кр(0.95; df={dof}) = {t_crit:.4f}")
print(f"t(ln a0) = {t_ln_a0:.4f}  -> {'значущий' if abs(t_ln_a0) > t_crit else 'незначущий'}")
print(f"t(a1)    = {t_a1:.4f}  -> {'значущий' if abs(t_a1) > t_crit else 'незначущий'}")
print(f"t(a2)    = {t_a2:.4f}  -> {'значущий' if abs(t_a2) > t_crit else 'незначущий'}")

print("-" * 70)
print(f"Модель: Y = {a0:.6f} * X1^{a1:.6f} * X2^{a2:.6f}")

# ---------------------------------------------------------------
# 3.1 Еластичність
# ---------------------------------------------------------------
print("=" * 70)
print("3.1 Еластичність випуску")
print(f"E_X1(Y) = a1 = {a1:.6f}")
print(f"E_X2(Y) = a2 = {a2:.6f}")
print(f"Випуск більше залежить від {'X1 (працезатрат)' if a1 > a2 else 'X2 (основних фондів)'}")

# ---------------------------------------------------------------
# 3.2 Однорідна функція Кобба-Дугласа
# ---------------------------------------------------------------
scale_sum = a1 + a2
alpha_h = a1 / scale_sum
beta_h = a2 / scale_sum
print("=" * 70)
print("3.2 Однорідна функція Кобба-Дугласа")
print(f"a1 + a2 = {scale_sum:.6f} {'< 1 (спадна віддача)' if scale_sum < 1 else ('> 1 (зростаюча віддача)' if scale_sum > 1 else '= 1 (стала віддача)')}")
print(f"alpha' = {alpha_h:.6f}")
print(f"beta'  = {beta_h:.6f}")
print(f"Y = {a0:.6f} * X1^{alpha_h:.6f} * X2^{beta_h:.6f}")

# ---------------------------------------------------------------
# 3.3 Гранична продуктивність праці (MPL) та гранична фондовіддача (MPK)
# ---------------------------------------------------------------
def MPL(x1, x2):
    return a0 * a1 * x1 ** (a1 - 1) * x2 ** a2

def MPK(x1, x2):
    return a0 * a2 * x1 ** a1 * x2 ** (a2 - 1)

def APL(x1, x2):
    return a0 * x1 ** (a1 - 1) * x2 ** a2

def APK(x1, x2):
    return a0 * x1 ** a1 * x2 ** (a2 - 1)

mpl_vals = MPL(X1, X2)
mpk_vals = MPK(X1, X2)
apl_vals = APL(X1, X2)
apk_vals = APK(X1, X2)

periods = np.arange(1, n + 1)

plt.figure(figsize=(8, 5))
plt.plot(periods, mpl_vals, marker='o', label='MPL (гранична продукт. праці)')
plt.plot(periods, mpk_vals, marker='s', label='MPK (гранична фондовіддача)')
plt.xlabel('Період')
plt.ylabel('Значення')
plt.title('Гранична продуктивність праці та гранична фондовіддача')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / 'fig1_mpl_mpk.svg')
plt.close()

# ---------------------------------------------------------------
# 3.4 Співвідношення MPL/APL та MPK/APK
# ---------------------------------------------------------------
print("=" * 70)
print("3.4 Співвідношення граничних та середніх показників")
print(f"MPL/APL = a1 = {a1:.6f} (перевірка: {np.mean(mpl_vals/apl_vals):.6f})")
print(f"MPK/APK = a2 = {a2:.6f} (перевірка: {np.mean(mpk_vals/apk_vals):.6f})")

# ---------------------------------------------------------------
# 3.5 Ефективність та масштаб виробництва (базовий рік — перший)
# ---------------------------------------------------------------
alpha = a1 / scale_sum
Y_b, X1_b, X2_b = Y[0], X1[0], X2[0]
Y_rel = Y / Y_b
X1_rel = X1 / X1_b
X2_rel = X2 / X2_b

E = (Y_rel / X1_rel) ** alpha * (Y_rel / X2_rel) ** (1 - alpha)
M = X1_rel ** alpha * X2_rel ** (1 - alpha)

plt.figure(figsize=(8, 5))
plt.plot(periods, E, marker='o', label='Ефективність виробництва E')
plt.plot(periods, M, marker='s', label='Масштаб виробництва M')
plt.xlabel('Період')
plt.ylabel('Значення')
plt.title('Ефективність та масштаб виробництва (базовий рік — 1-й)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / 'fig2_efficiency_scale.svg')
plt.close()

print("=" * 70)
print("3.5 Ефективність (E) та масштаб (M) виробництва за періодами")
for i in range(n):
    print(f"  Період {i+1}: E = {E[i]:.6f}, M = {M[i]:.6f}")

# ---------------------------------------------------------------
# 4. Ізокванта для Y = 95
# ---------------------------------------------------------------
Y_target = 95.0
x1_range = np.linspace(20.0, X1.max() * 1.1, 200)
x2_isoquant = (Y_target / (a0 * x1_range ** a1)) ** (1 / a2)

plt.figure(figsize=(8, 5))
plt.plot(x1_range, x2_isoquant, label=f'Ізокванта Y = {Y_target}')
plt.xlabel('X1 (працезатрати)')
plt.ylabel('X2 (основні фонди)')
plt.title(f'Ізокванта для Y = {Y_target}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / 'fig3_isoquant.svg')
plt.close()

print("=" * 70)
print(f"4. Ізокванта для Y = {Y_target}: X2 = (95 / (a0 * X1^a1))^(1/a2)")

# ---------------------------------------------------------------
# 5. Ізокліналь через точку (K0, L0) = (40, 60)  [X1=40, X2=60]
# ---------------------------------------------------------------
K0, L0 = 40.0, 60.0
a_const = L0 ** 2 - (a1 / a2) * K0 ** 2
x1_iso_range = np.linspace(0.1, X1.max() * 1.1 + 10, 200)
inside = (a1 / a2) * x1_iso_range ** 2 + a_const
x1_iso_valid = x1_iso_range[inside >= 0]
x2_isocline = np.sqrt((a1 / a2) * x1_iso_valid ** 2 + a_const)

plt.figure(figsize=(8, 5))
plt.plot(x1_iso_valid, x2_isocline, label=f'Ізокліналь через ({K0}; {L0})')
plt.scatter([K0], [L0], color='red', zorder=5, label='Точка (K0; L0)')
plt.xlabel('X1 (працезатрати)')
plt.ylabel('X2 (основні фонди)')
plt.title('Ізокліналь')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / 'fig4_isocline.svg')
plt.close()

print(f"5. Ізокліналь через точку (X1={K0}; X2={L0}): a = {a_const:.6f}")

# ---------------------------------------------------------------
# 6. Ізокванта + ізокліналь на одному графіку
# ---------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(x1_range, x2_isoquant, label=f'Ізокванта Y = {Y_target}')
plt.plot(x1_iso_valid, x2_isocline, label=f'Ізокліналь через ({K0}; {L0})')
plt.scatter([K0], [L0], color='red', zorder=5, label='Точка (K0; L0)')
plt.xlabel('X1 (працезатрати)')
plt.ylabel('X2 (основні фонди)')
plt.title('Ізокванта та ізокліналь')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / 'fig5_isoquant_isocline.svg')
plt.close()

# ---------------------------------------------------------------
# Точка перетину ізокванти та ізокліналі (для точності звіту)
# ---------------------------------------------------------------
diff = x2_isoquant - np.sqrt(np.clip((a1 / a2) * x1_range ** 2 + a_const, 0, None))
sign_change = np.where(np.diff(np.sign(diff)))[0]
if len(sign_change) > 0:
    idx = sign_change[0]
    intersection = (float(x1_range[idx]), float(x2_isoquant[idx]))
else:
    intersection = None
print(f"Точка перетину ізокванти та ізокліналі: {intersection}")

print("=" * 70)
print(f"Графіки збережено у {SCRIPT_DIR}/*.png")

# ---------------------------------------------------------------
# Збереження результатів у data.json (спільний з lab1_2.py файл)
# ---------------------------------------------------------------
save_block("block1_1", {
    "n": n,
    "X1": X1.tolist(),
    "X2": X2.tolist(),
    "Y": Y.tolist(),
    # Форматовані з фіксованою кількістю знаків рядки для таблиці (щоб
    # уникнути втрати кінцевого нуля, напр. 55.0 -> "55.0", при друці в Typst)
    "X1_disp": [f"{v:.1f}" for v in X1],
    "X2_disp": [f"{v:.1f}" for v in X2],
    "Y_disp": [f"{v:.1f}" for v in Y],
    "params": {
        "ln_a0": r6(ln_a0), "se_ln_a0": r6(se_ln_a0),
        "a1": r6(a1), "se_a1": r6(se_a1),
        "a2": r6(a2), "se_a2": r6(se_a2),
        "a0": r6(a0),
    },
    "r2": r6(r2),
    "F_stat": round(float(F_stat), 4),
    "F_crit": round(float(F_crit), 4),
    "k1": k1, "k2": k2,
    "t_crit": round(float(t_crit), 4),
    "t_ln_a0": round(float(t_ln_a0), 4),
    "t_a1": round(float(t_a1), 4),
    "t_a2": round(float(t_a2), 4),
    "elasticity": {"E_X1": r6(a1), "E_X2": r6(a2)},
    "homogeneous": {
        "scale_sum": r6(scale_sum),
        "alpha_h": r6(alpha_h),
        "beta_h": r6(beta_h),
    },
    "efficiency_scale": {
        "periods": periods.tolist(),
        "E": r6(E),
        "M": r6(M),
    },
    "isoquant": {"Y_target": Y_target},
    "isocline": {"K0": K0, "L0": L0, "a_const": r6(a_const)},
    "intersection": [round(intersection[0], 1), round(intersection[1], 1)] if intersection else None,
})
print(f"Дані блоку 1.1 збережено у {DATA_PATH}")
