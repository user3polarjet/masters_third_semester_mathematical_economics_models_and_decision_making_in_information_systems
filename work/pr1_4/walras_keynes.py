"""
Лабораторна робота №4
Моделювання економічної рівноваги: підходи Вальраса і Кейнса

Примітка: у цій лабораторній роботі всі вихідні дані фіксовані і не залежать
від номера варіанта (завдання є спільним прикладом для реалізації в Python
замість Excel).
"""
import json
import pathlib

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
DATA_PATH = SCRIPT_DIR / "data.json"


def save_block(key, block):
    data = {}
    if DATA_PATH.exists():
        with open(DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)
    data[key] = block
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("=" * 70)
print("БЛОК 4.1. Модель Вальраса конкурентної рівноваги")
print("=" * 70)

# ---------------------------------------------------------------
# Розв'язання системи рівнянь відносно рівноважних цін P_A, P_B (r=1)
# ---------------------------------------------------------------
r = 1.0


def excess_demand(x):
    p_a, p_b = x
    return [
        10.6 * p_a - 4.2 * p_b - 96 * p_a ** 2 + 19.39 * p_b ** (4 / 3) + 12.8,
        5.8 * p_b - 7.8 * p_a + 19.2 * p_a ** 2 - 47.397 * p_b ** (4 / 3) + 14.4,
    ]


P_A, P_B = fsolve(excess_demand, np.array([1.0, 1.0]))
print(f"Рівноважні ціни: P_A = {P_A:.4f}, P_B = {P_B:.4f}")
print(f"Перевірка (обидва рівняння ~0): {excess_demand([P_A, P_B])}")


def firm_A(p_a, r):
    L_A_D = (8 * p_a / r) ** 2
    pi_A = 64 * p_a ** 2 / r
    Q_A_S = 128 * p_a / r
    return L_A_D, pi_A, Q_A_S


def firm_B(p_b, r):
    L_B_D = (10 * p_b / r) ** (4 / 3)
    pi_B = 64.633 * p_b ** (4 / 3) / r ** (1 / 3)
    Q_B_S = 86.177 * (p_b / r) ** (1 / 3)
    return L_B_D, pi_B, Q_B_S


def household_1(p_a, p_b, r, pi_A):
    Q_A1 = 5 + (0.5 * pi_A + 8 * r - 3 * p_b) / p_a
    Q_B1 = 4.2 + (0.3 * pi_A + 4.8 * r - 3 * p_a) / p_b
    L_A_S = 12.8 - (0.2 * pi_A - 2 * p_a - 1.2 * p_b) / r
    return Q_A1, Q_B1, L_A_S


def household_2(p_a, p_b, r, pi_B):
    Q_A2 = 5.6 + (0.3 * pi_B + 4.8 * r - 1.2 * p_b) / p_a
    Q_B2 = 1.6 + (0.6 * pi_B + 9.6 * r - 4.8 * p_a) / p_b
    L_B_S = 14.4 - (0.1 * pi_B - 0.8 * p_a - 0.4 * p_b) / r
    return Q_A2, Q_B2, L_B_S


L_A_D, pi_A, Q_A_S = firm_A(P_A, r)
L_B_D, pi_B, Q_B_S = firm_B(P_B, r)
Q_A1, Q_B1, L_A_S = household_1(P_A, P_B, r, pi_A)
Q_A2, Q_B2, L_B_S = household_2(P_A, P_B, r, pi_B)

print("-" * 70)
print("Таблиця 1. Виробництво і споживання благ")
print(f"{'Благо':<6}{'Вироблено':>12}{'Праці, год':>14}{'Прибуток':>12}{'Спож.1-м':>12}{'Спож.2-м':>12}")
print(f"{'A':<6}{Q_A_S:>12.1f}{L_A_D:>14.1f}{pi_A:>12.1f}{Q_A1:>12.1f}{Q_A2:>12.1f}")
print(f"{'B':<6}{Q_B_S:>12.1f}{L_B_D:>14.1f}{pi_B:>12.1f}{Q_B1:>12.1f}{Q_B2:>12.1f}")

income1_wage, income1_profit = r * L_A_S, pi_A
income1_total = income1_wage + income1_profit
exp1_A, exp1_B = P_A * Q_A1, P_B * Q_B1
exp1_total = exp1_A + exp1_B

income2_wage, income2_profit = r * L_B_S, pi_B
income2_total = income2_wage + income2_profit
exp2_A, exp2_B = P_A * Q_A2, P_B * Q_B2
exp2_total = exp2_A + exp2_B

print("-" * 70)
print("Таблиця 2. Доходи і витрати домашніх господарств")
print(f"{'Споживач':<10}{'Зарплата':>10}{'Прибуток':>10}{'Доходи':>10}{'Витр.A':>10}{'Витр.B':>10}{'Витр.всього':>13}")
print(f"{'1-й':<10}{income1_wage:>10.1f}{income1_profit:>10.1f}{income1_total:>10.1f}{exp1_A:>10.1f}{exp1_B:>10.1f}{exp1_total:>13.1f}")
print(f"{'2-й':<10}{income2_wage:>10.1f}{income2_profit:>10.1f}{income2_total:>10.1f}{exp2_A:>10.1f}{exp2_B:>10.1f}{exp2_total:>13.1f}")

print("-" * 70)
print("Перевірка ринкової рівноваги (сукупний попит = сукупна пропозиція):")
print(f"  Ринок A: Q_A1+Q_A2 = {Q_A1+Q_A2:.4f}  vs  Q_A^S = {Q_A_S:.4f}")
print(f"  Ринок B: Q_B1+Q_B2 = {Q_B1+Q_B2:.4f}  vs  Q_B^S = {Q_B_S:.4f}")
print(f"  Ринок праці (сукупно): L_A^S+L_B^S = {L_A_S+L_B_S:.4f}  vs  L_A^D+L_B^D = {L_A_D+L_B_D:.4f}")

# ---------------------------------------------------------------
# Рис. 1 — Ринок блага А: попит і пропозиція як функції P_A
# ---------------------------------------------------------------
p_a_range = np.linspace(0.2, 1.0, 200)
supply_A = 128 * p_a_range / r
pi_A_range = 64 * p_a_range ** 2 / r
demand_A = (
    5 + (0.5 * pi_A_range + 8 * r - 3 * P_B) / p_a_range
    + 5.6 + (0.3 * pi_B + 4.8 * r - 1.2 * P_B) / p_a_range
)

plt.figure(figsize=(8, 5))
plt.plot(p_a_range, supply_A, label="$Q_A^S(P_A)$ (пропозиція)")
plt.plot(p_a_range, demand_A, label="$Q_A^D(P_A)$ (попит)")
plt.scatter([P_A], [Q_A_S], color="red", zorder=5, label=f"Рівновага ($P_A$={P_A:.4f})")
plt.xlabel("$P_A$")
plt.ylabel("$Q_A$")
plt.title("Ринок блага А")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / "fig1_market_A.svg")
plt.close()

# ---------------------------------------------------------------
# Рис. 2 — Ринок блага В: попит і пропозиція як функції P_B
# ---------------------------------------------------------------
p_b_range = np.linspace(0.2, 1.0, 200)
supply_B = 86.177 * (p_b_range / r) ** (1 / 3)
pi_B_range = 64.633 * p_b_range ** (4 / 3) / r ** (1 / 3)
demand_B = (
    4.2 + (0.3 * pi_A + 4.8 * r - 3 * P_A) / p_b_range
    + 1.6 + (0.6 * pi_B_range + 9.6 * r - 4.8 * P_A) / p_b_range
)

plt.figure(figsize=(8, 5))
plt.plot(p_b_range, supply_B, label="$Q_B^S(P_B)$ (пропозиція)")
plt.plot(p_b_range, demand_B, label="$Q_B^D(P_B)$ (попит)")
plt.scatter([P_B], [Q_B_S], color="red", zorder=5, label=f"Рівновага ($P_B$={P_B:.4f})")
plt.xlabel("$P_B$")
plt.ylabel("$Q_B$")
plt.title("Ринок блага В")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / "fig2_market_B.svg")
plt.close()

# ---------------------------------------------------------------
# Рис. 3 — Ринок праці (сукупно): попит і пропозиція як функції r
# ---------------------------------------------------------------
r_range = np.linspace(0.5, 2.0, 200)
L_A_D_r = (8 * P_A / r_range) ** 2
L_B_D_r = (10 * P_B / r_range) ** (4 / 3)
labor_demand = L_A_D_r + L_B_D_r

pi_A_r = 64 * P_A ** 2 / r_range
pi_B_r = 64.633 * P_B ** (4 / 3) / r_range ** (1 / 3)
L_A_S_r = 12.8 - (0.2 * pi_A_r - 2 * P_A - 1.2 * P_B) / r_range
L_B_S_r = 14.4 - (0.1 * pi_B_r - 0.8 * P_A - 0.4 * P_B) / r_range
labor_supply = L_A_S_r + L_B_S_r

plt.figure(figsize=(8, 5))
plt.plot(r_range, labor_demand, label="$L^D(r)$ (сукупний попит на працю)")
plt.plot(r_range, labor_supply, label="$L^S(r)$ (сукупна пропозиція праці)")
plt.scatter([r], [L_A_D + L_B_D], color="red", zorder=5, label=f"Рівновага (r={r:.1f})")
plt.xlabel("$r$")
plt.ylabel("$L$")
plt.title("Ринок праці (сукупно)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / "fig3_labor_market.svg")
plt.close()

print("\n" + "=" * 70)
print("БЛОК 4.2. Модель Кейнса (IS-LM)")
print("=" * 70)

# ---------------------------------------------------------------
# Вихідні дані (таблиця 1)
# ---------------------------------------------------------------
a, d, f, b = 127500.0, 85000.0, 229500.0, 0.31
Ms, k, h, j, p = 11000.0, 0.25, 5100.0, 19800.0, 0.3
A_prod, beta = 2400.0, 0.5243006


def Y_G(r):
    return (a + d) / (1 - b) - r * f / (1 - b)


def Y_M(r):
    return (Ms - h) / (k * p) + r * j / (k * p)


r_grid = np.arange(0, 1.0001, 0.05)
print("Таблиця 2/3. r, Y^G(r), Y^M(r):")
for rv in r_grid:
    print(f"  r={rv:.2f}  Y^G={Y_G(rv):.2f}  Y^M={Y_M(rv):.2f}")

r_line = np.linspace(0, 1, 300)

plt.figure(figsize=(8, 5))
plt.plot(r_line, Y_G(r_line), label="$Y^G(r)$ (крива IS — ринок товарів)")
plt.plot(r_line, Y_M(r_line), label="$Y^M(r)$ (крива LM — ринок грошей)")
plt.xlabel("$r$")
plt.ylabel("$Y$")
plt.title("Рівновага на ринках грошей та товарів (IS-LM)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
# позначимо точку рівноваги нижче, після обчислення r0, Y0
r0 = (a * k * p + d * k * p - Ms + b * Ms + h - b * h) / (f * k * p + j - b * j)
Y0 = Y_G(r0)
plt.scatter([r0], [Y0], color="red", zorder=5, label=f"Рівновага ($r_0$={r0:.4f}, $Y_0$={Y0:.2f})")
plt.legend()
plt.savefig(SCRIPT_DIR / "fig4_is_lm.svg")
plt.close()

print("-" * 70)
print(f"Аналітичний розв'язок: r0 = {r0:.9f}")
print(f"Y0 = Y^G(r0) = {Y_G(r0):.4f}, Y0 = Y^M(r0) = {Y_M(r0):.4f}")

# ---------------------------------------------------------------
# Виробнича функція Y = A * L^beta, знаходження L0
# ---------------------------------------------------------------


def Y_prod(L):
    return A_prod * L ** beta


L0 = np.exp((np.log(Y0) - np.log(A_prod)) / beta)
print(f"L0 = exp((ln(Y0)-ln(A))/beta) = {L0:.4f}")
print(f"Перевірка: Y(L0) = {Y_prod(L0):.4f} (має дорівнювати Y0 = {Y0:.4f})")

L_grid = np.arange(0, 20001, 1000)
print("Таблиця 4. L, Y=F3(L):")
for Lv in L_grid:
    print(f"  L={Lv:>6}  Y={Y_prod(Lv):.4f}")

L_line = np.linspace(0, 20000, 300)

plt.figure(figsize=(8, 5))
plt.plot(L_line, Y_prod(L_line), label="$Y = F_3(L) = A \\cdot L^\\beta$")
plt.scatter([L0], [Y0], color="red", zorder=5, label=f"($L_0$={L0:.1f}, $Y_0$={Y0:.1f})")
plt.axhline(Y0, color="gray", linestyle=":", linewidth=0.8)
plt.axvline(L0, color="gray", linestyle=":", linewidth=0.8)
plt.xlabel("$L$")
plt.ylabel("$Y$")
plt.title("Виробнича функція $Y=F_3(L)$")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / "fig5_production_function.svg")
plt.close()

save_block("block4_1", {
    "P_A": round(float(P_A), 4), "P_B": round(float(P_B), 4),
    "table1": {
        "A": {"Q_S": f"{Q_A_S:.1f}", "L_D": f"{L_A_D:.1f}", "pi": f"{pi_A:.1f}",
              "Q1": f"{Q_A1:.1f}", "Q2": f"{Q_A2:.1f}"},
        "B": {"Q_S": f"{Q_B_S:.1f}", "L_D": f"{L_B_D:.1f}", "pi": f"{pi_B:.1f}",
              "Q1": f"{Q_B1:.1f}", "Q2": f"{Q_B2:.1f}"},
    },
    "table2": {
        "h1": {"wage": f"{income1_wage:.1f}", "profit": f"{income1_profit:.1f}",
               "income": f"{income1_total:.1f}", "exp_A": f"{exp1_A:.1f}",
               "exp_B": f"{exp1_B:.1f}", "exp_total": f"{exp1_total:.1f}"},
        "h2": {"wage": f"{income2_wage:.1f}", "profit": f"{income2_profit:.1f}",
               "income": f"{income2_total:.1f}", "exp_A": f"{exp2_A:.1f}",
               "exp_B": f"{exp2_B:.1f}", "exp_total": f"{exp2_total:.1f}"},
    },
    "check": {
        "Q_A_total": round(float(Q_A1 + Q_A2), 2), "Q_A_S": round(float(Q_A_S), 2),
        "Q_B_total": round(float(Q_B1 + Q_B2), 2), "Q_B_S": round(float(Q_B_S), 2),
        "L_S_total": round(float(L_A_S + L_B_S), 2), "L_D_total": round(float(L_A_D + L_B_D), 2),
    },
})

save_block("block4_2", {
    "params": {"a": a, "d": d, "f": f, "b": b, "Ms": Ms, "k": k, "h": h, "j": j, "p": p,
               "A_prod": A_prod, "beta": beta},
    "r_approx": 0.38, "Y_approx": 180000,
    "r0": round(float(r0), 9), "Y0": round(float(Y0), 4),
    "L0": round(float(L0), 4), "Y_prod_L0": round(float(Y_prod(L0)), 4),
})
print(f"Дані збережено у {DATA_PATH}")

print("\nГрафіки збережено у", SCRIPT_DIR)
