"""
Лабораторна робота №1, Блок 1.2 — Варіант 6
Чотирифакторна економетрична модель: Y = a0 + a1*X1 + a2*X1^2 + a3*X2 + a4*X2^2
"""
import numpy as np
from scipy import stats

# ---------------------------------------------------------------
# 1. Вихідні дані (варіант 6)
# ---------------------------------------------------------------
Y  = np.array([36.82, 39.14, 41.26, 42.53, 41.98, 45.56, 56.25, 58.92, 64.12, 66.64])
X1 = np.array([29.65, 34.56, 38.29, 42.23, 40.55, 51.87, 52.12, 62.41, 66.49, 68.42])
X2 = np.array([32.65, 38.85, 39.51, 42.12, 44.62, 48.12, 51.21, 58.64, 56.94, 62.35])

n = len(Y)

# ---------------------------------------------------------------
# 2. Заміна: U1=X1, U2=X1^2, U3=X2, U4=X2^2
# ---------------------------------------------------------------
U1 = X1
U2 = X1 ** 2
U3 = X2
U4 = X2 ** 2

A = np.column_stack([np.ones(n), U1, U2, U3, U4])
coef, _, _, _ = np.linalg.lstsq(A, Y, rcond=None)
a0, a1, a2, a3, a4 = coef

Y_pred = A @ coef
resid = Y - Y_pred

p = A.shape[1]      # m = 5
dof = n - p         # ступені свободи залишку

ss_tot = np.sum((Y - Y.mean()) ** 2)
ss_res = np.sum(resid ** 2)
r2 = 1 - ss_res / ss_tot

k1 = p - 1           # m - 1
k2 = n - p           # n - m
F_stat = (r2 / k1) / ((1 - r2) / k2)
F_crit = stats.f.ppf(0.95, k1, k2)

sigma2 = ss_res / dof
cov = sigma2 * np.linalg.inv(A.T @ A)
se = np.sqrt(np.diag(cov))
se_a0, se_a1, se_a2, se_a3, se_a4 = se

print("=" * 70)
print("БЛОК 1.2. Чотирифакторна модель (Варіант 6)")
print("=" * 70)
print(f"n = {n}, m = {p}")
print(f"a0 = {a0:.6f}  SE = {se_a0:.6f}")
print(f"a1 = {a1:.6f}  SE = {se_a1:.6f}")
print(f"a2 = {a2:.6f}  SE = {se_a2:.6f}")
print(f"a3 = {a3:.6f}  SE = {se_a3:.6f}")
print(f"a4 = {a4:.6f}  SE = {se_a4:.6f}")
print(f"R^2 = {r2:.6f}")
print(f"F = {F_stat:.4f}   F_кр(0.95; {k1}; {k2}) = {F_crit:.4f}")
print(f"Модель {'адекватна' if F_stat > F_crit else 'неадекватна'} статистичним даним з ймовірністю 0.95")

t_crit = stats.t.ppf(0.975, dof)
t_vals = coef / se
print("-" * 70)
print(f"t_кр(0.95; df={dof}) = {t_crit:.4f}")
for name, t in zip(["a0", "a1", "a2", "a3", "a4"], t_vals):
    print(f"t({name}) = {t:.4f} -> {'значущий' if abs(t) > t_crit else 'незначущий'}")

print("-" * 70)
print(f"Модель: Y = {a0:.4f} + {a1:.4f}*X1 + {a2:.4f}*X1^2 + {a3:.4f}*X2 + {a4:.4f}*X2^2")

# ---------------------------------------------------------------
# Пошук екстремуму (максимум прибутку), якщо модель адекватна
# ---------------------------------------------------------------
if F_stat > F_crit:
    X1_star = -a1 / (2 * a2)
    X2_star = -a3 / (2 * a4)

    D = (2 * a2) * (2 * a4)
    d2y_dx1sq = 2 * a2

    print("=" * 70)
    print("Критична точка:")
    print(f"X1* = {X1_star:.6f}")
    print(f"X2* = {X2_star:.6f}")
    print(f"D = {D:.6f}")

    if D > 0 and d2y_dx1sq < 0:
        kind = "максимум"
    elif D > 0 and d2y_dx1sq > 0:
        kind = "мінімум"
    else:
        kind = "сідлова точка (не екстремум)"
    print(f"Тип критичної точки: {kind}")

    Y_star = a0 + a1 * X1_star + a2 * X1_star ** 2 + a3 * X2_star + a4 * X2_star ** 2
    print(f"Y_max = {Y_star:.6f}")
    print("-" * 70)
    print(f"Висновок: комерційне підприємство може отримати найбільший прибуток "
          f"Y_max = {Y_star:.5f} у.г.о. при X1 = {X1_star:.5f}, X2 = {X2_star:.5f}.")
else:
    print("Модель неадекватна — пошук екстремуму не проводиться.")
