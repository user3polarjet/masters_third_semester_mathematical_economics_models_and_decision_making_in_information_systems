"""
Лабораторна робота №3 — Варіант 6
Моделювання поведінки споживача та функції попиту: класичний підхід і модель Еванса
"""
import pathlib

import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent

print("=" * 70)
print("БЛОК 3.1. Модель поведінки споживача")
print("=" * 70)

# ---------------------------------------------------------------
# Завдання 3.1.1: U(X1,X2) = (2X1+1)(X2+3)
# ---------------------------------------------------------------
print("\n### Завдання 3.1.1 ###")


def U1(X1, X2):
    return (2 * X1 + 1) * (X2 + 3)


# 1. Крива байдужості через точку (3,1)
X1_0, X2_0 = 3.0, 1.0
U_level = U1(X1_0, X2_0)
print(f"Рівень корисності U через точку (3,1): U = {U_level}")

X1_range = np.linspace(0.1, 30, 400)
indiff_curve = U_level / (2 * X1_range + 1) - 3

# 2. Граничні корисності
# dU/dX1 = 2*(X2+3) = 2*X2 + 6
# dU/dX2 = 2*X1 + 1
print("MU_X1 = dU/dX1 = 2*X2 + 6")
print("MU_X2 = dU/dX2 = 2*X1 + 1")

# 3. Норма заміщення другого товару першим: MRS = dX1/dX2 = (dU/dX2)/(dU/dX1)
print("MRS (2-го товару 1-м) = (2X1+1) / (2X2+6)")

# 4. Бюджетна лінія
B, p1, p2 = 500.0, 25.0, 50.0
budget_line = (B - p1 * X1_range) / p2
print(f"Бюджетна лінія: X2 = (B - p1*X1)/p2 = ({B} - {p1}*X1)/{p2}")

plt.figure(figsize=(8, 5))
plt.plot(X1_range, indiff_curve, label=f"Крива байдужості U={U_level}")
plt.plot(X1_range, budget_line, label=f"Бюджетна лінія (B={B}, p1={p1}, p2={p2})")
plt.axhline(0, color="black", linewidth=0.6)
plt.ylim(-2, 20)
plt.xlabel("$X_1$")
plt.ylabel("$X_2$")
plt.title("Крива байдужості та бюджетна лінія (варіант 6)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / "fig1_indifference_budget.svg")
plt.close()

# 5. Точка споживчої рівноваги
X1_eq = (2 * B - p1 + 6 * p2) / (4 * p1)
X2_eq = (B - p1 * X1_eq) / p2
U_eq = U1(X1_eq, X2_eq)
print(f"Точка споживчої рівноваги: X1* = {X1_eq}, X2* = {X2_eq}")
print(f"U в точці рівноваги: {U_eq}")

indiff_curve_eq = U_eq / (2 * X1_range + 1) - 3

plt.figure(figsize=(8, 5))
plt.plot(X1_range, indiff_curve_eq, label=f"Крива байдужості U={U_eq:.4f}")
plt.plot(X1_range, budget_line, label=f"Бюджетна лінія (B={B}, p1={p1}, p2={p2})")
plt.scatter([X1_eq], [X2_eq], color="red", zorder=5, label=f"Рівновага ({X1_eq}; {X2_eq})")
plt.axhline(0, color="black", linewidth=0.6)
plt.ylim(-2, 20)
plt.xlabel("$X_1$")
plt.ylabel("$X_2$")
plt.title("Точка споживчої рівноваги (варіант 6)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / "fig2_equilibrium.svg")
plt.close()

# 6. Функція попиту x*(p, B)
print("Функція попиту:")
print("X1*(p,B) = (2B - p1 + 6*p2) / (4*p1)")
print("X2*(p,B) = (2B + p1 - 6*p2) / (4*p2)")

# ---------------------------------------------------------------
# Завдання 3.1.2: U(x1,x2,x3) = sqrt(x1*x2*x3)
# ---------------------------------------------------------------
print("\n### Завдання 3.1.2 ###")
Bb, q1, q2, q3 = 3000.0, 20.0, 40.0, 10.0

x1 = Bb / (3 * q1)
x2 = x1 * q1 / q2
x3 = x1 * q1 / q3
U2 = (x1 * x2 * x3) ** 0.5

print(f"Оптимальний набір товарів: x1 = {x1}, x2 = {x2}, x3 = {x3}")
print(f"Перевірка бюджету: p1*x1 + p2*x2 + p3*x3 = {q1*x1 + q2*x2 + q3*x3} (має дорівнювати {Bb})")
print(f"Корисність у точці оптимуму: U = {U2:.6f}")

print("\n" + "=" * 70)
print("БЛОК 3.2. Модель Еванса встановлення рівноважної ціни (варіант 6, n=6)")
print("=" * 70)

# ---------------------------------------------------------------
# Завдання 3.2.1: неперервна модель Еванса
# ---------------------------------------------------------------
print("\n### Завдання 3.2.1 ###")
n = 6
gamma = 1.0 / n
a, b = 11.0, 3.0       # D(p) = a - b*p
alpha, beta = 3.0, 2.0  # S(p) = alpha + beta*p
p0 = 7.0

p_star = (a - alpha) / (b + beta)


def p_continuous(t):
    return p_star + (p0 - p_star) * np.exp(-gamma * (b + beta) * t)


p1_val = p_continuous(1)
pn_val = p_continuous(n)
print(f"gamma = 1/n = {gamma}")
print(f"Рівноважна ціна p* = (a-alpha)/(b+beta) = {p_star}")
print(f"p(0) = {p0}")
print(f"p(1) = {p1_val}")
print(f"p(n) = p({n}) = {pn_val}")

t_range = np.linspace(0, 10, 300)
p_t_vals = p_continuous(t_range)

plt.figure(figsize=(8, 5))
plt.plot(t_range, p_t_vals, label="$p(t)$")
plt.axhline(p_star, color="red", linestyle="--", label=f"$p^*={p_star}$")
plt.scatter([0, 1, n], [p0, p1_val, pn_val], color="black", zorder=5)
plt.xlabel("$t$")
plt.ylabel("$p(t)$")
plt.title("Модель Еванса з неперервним часом (варіант 6, n=6)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / "fig3_evans_continuous.svg")
plt.close()

# ---------------------------------------------------------------
# Завдання 3.2.2: дискретна модель Еванса
# ---------------------------------------------------------------
print("\n### Завдання 3.2.2 ###")
p0_disc = 4.0
ratio = -beta / b

i_range = np.arange(0, n + 1)
p_i_vals = (p0_disc - p_star) * ratio ** i_range + p_star

# D_i та S_i мають сенс лише для i>=1: D_i = D(p_i), S_i = S(p_{i-1}),
# а p_0 — це лише задана початкова (нерівноважна) ціна, без "періоду 0".
i_ds = i_range[1:]
D_i_vals = a - b * p_i_vals[1:]
S_i_vals = alpha + beta * p_i_vals[:-1]

print(f"Знаменник геометричної прогресії -beta/b = {ratio}")
for i, p_i in zip(i_range, p_i_vals):
    print(f"  p_{i} = {p_i:.6f}")
print(f"Рівноважна ціна у момент i=n={n}: p_{n} = {p_i_vals[-1]:.6f}")
print(f"Гранична рівноважна ціна (i->inf): {p_star}")
print(f"Перевірка D_i = S_i (мають збігатися): D={D_i_vals}")
print(f"                                       S={S_i_vals}")

plt.figure(figsize=(8, 5))
plt.plot(i_range, p_i_vals, marker="o", label="$p_i$")
plt.axhline(p_star, color="red", linestyle="--", label=f"$p^*={p_star}$")
plt.xlabel("$i$")
plt.ylabel("$p_i$")
plt.title("Модель Еванса з дискретним часом (варіант 6, n=6)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / "fig4_evans_discrete_price.svg")
plt.close()

plt.figure(figsize=(8, 5))
plt.plot(i_ds, D_i_vals, marker="o", label="$D_i$ (попит)")
plt.plot(i_ds, S_i_vals, marker="s", linestyle="--", label="$S_i$ (пропозиція)")
plt.axhline(a - b * p_star, color="gray", linestyle=":", label=f"$D=S \\to {a - b*p_star:.1f}$")
plt.xlabel("$i$")
plt.ylabel("Обсяг")
plt.title("Попит та пропозиція в дискретній моделі Еванса (варіант 6, n=6)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / "fig5_evans_discrete_demand_supply.svg")
plt.close()

print("\nГрафіки збережено у", SCRIPT_DIR)
