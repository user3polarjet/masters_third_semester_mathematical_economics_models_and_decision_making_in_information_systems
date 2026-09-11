"""
Лабораторна робота №2 — Варіант 6
Аналіз економічних процесів за допомогою міжгалузевих балансових моделей Леонтьєва
"""
import json
import pathlib

import matplotlib.pyplot as plt
import numpy as np

np.set_printoptions(precision=6, suppress=True)

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


def r6(x):
    if isinstance(x, np.ndarray):
        return np.round(x, 6).tolist()
    return round(float(x), 6)


def mat_disp(M, fmt="{:.6f}"):
    return [[fmt.format(v) for v in row] for row in np.atleast_2d(M)]


def vec_disp(v, fmt="{:.3f}"):
    return [fmt.format(x) for x in v]


def check_productivity(A, label):
    n = A.shape[0]
    E = np.eye(n)
    B = np.linalg.inv(E - A)
    inv_nonneg = np.all(B >= -1e-9)
    eig = np.linalg.eigvals(A)
    max_eig = np.max(np.abs(eig))
    productive = inv_nonneg and max_eig < 1
    print(f"--- Перевірка продуктивності матриці A ({label}) ---")
    print(f"(E-A)^-1 =\n{B}")
    print(f"Всі елементи (E-A)^-1 невід'ємні: {inv_nonneg}")
    print(f"Власні значення A: {eig}")
    print(f"max|lambda| = {max_eig:.6f} < 1: {max_eig < 1}")
    print(f"Матриця {'продуктивна' if productive else 'НЕ продуктивна'}")
    return B, productive


def balance_table(A, X, label):
    Q1 = A * X[np.newaxis, :]           # x_ij = a_ij * X_j
    net_product = X - Q1.sum(axis=0)    # Квадрант III (умовно чиста продукція)
    print(f"--- Схема міжгалузевого балансу ({label}) ---")
    print(f"Валова продукція X = {X}")
    print(f"Квадрант I (x_ij = a_ij * X_j):\n{Q1}")
    print(f"Квадрант III (умовно чиста продукція) = {net_product}")
    print(f"Сума Q3 = {net_product.sum():.4f}, сума Y (Квадрант II) = {X.sum() - Q1.sum():.4f}")
    return Q1, net_product


print("=" * 70)
print("БЛОК 2.1. Модель міжгалузевого балансу Леонтьєва")
print("=" * 70)

# ---------------------------------------------------------------
# Завдання 2.1.1 (варіант 6)
# ---------------------------------------------------------------
print("\n### Завдання 2.1.1 (варіант 6) ###")
A1 = np.array([
    [0.3, 0.2, 0.3],
    [0.3, 0.4, 0.0],
    [0.3, 0.2, 0.1],
])
Y1 = np.array([250.0, 150.0, 300.0])

B1, prod1 = check_productivity(A1, "2.1.1")
X1 = B1 @ Y1
print(f"Вектор валової продукції X = B*Y = {X1}")
balance_table(A1, X1, "2.1.1")

# Графічний розв'язок характеристичного рівняння |lambda*E - A| = 0
char_coeffs = np.poly(A1)  # коефіцієнти det(lambda*E - A) за спаданням степенів
lam = np.linspace(-0.5, 1.2, 400)
f_lam = np.polyval(char_coeffs, lam)
roots = np.linalg.eigvals(A1).real

plt.figure(figsize=(8, 5))
plt.axhline(0, color="black", linewidth=0.8)
plt.plot(lam, f_lam, label=r"$f(\lambda) = |\lambda E - A|$")
plt.scatter(roots, np.zeros_like(roots), color="red", zorder=5, label="Корені рівняння")
for r in roots:
    plt.annotate(f"{r:.4f}", (r, 0), textcoords="offset points", xytext=(0, 10), ha="center", fontsize=8)
plt.xlabel(r"$\lambda$")
plt.ylabel(r"$f(\lambda)$")
plt.title("Графічне розв'язання характеристичного рівняння (варіант 6)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(SCRIPT_DIR / "fig1_characteristic_equation.svg")
plt.close()
print(f"Корені характеристичного рівняння: {np.sort(roots)}")
print(f"Найбільший корінь = {roots.max():.6f} < 1: {roots.max() < 1}")

# ---------------------------------------------------------------
# Завдання 2.1.2 (варіант 6, таблиця 6)
# ---------------------------------------------------------------
print("\n### Завдання 2.1.2 (варіант 6) ###")
A2 = np.array([
    [0.25, 0.35, 0.18],
    [0.18, 0.09, 0.30],
    [0.11, 0.50, 0.20],
])
Y2 = np.array([38.0, 14.0, 9.0])

B2, prod2 = check_productivity(A2, "2.1.2")
X2 = B2 @ Y2
print(f"Вектор валової продукції X = B*Y = {X2}")

# ---------------------------------------------------------------
# Завдання 2.1.3 — вже виконано в 2.1.1 та 2.1.2 (перевірка продуктивності
# та обчислення обсягів валової продукції для обох матриць варіанта 6)
# ---------------------------------------------------------------
print("\n### Завдання 2.1.3 ###")
print("Умови продуктивності обох матриць (2.1.1 та 2.1.2) вже перевірено вище;")
print("обсяги валової продукції обчислено як X = (E-A)^-1 * Y.")

# ---------------------------------------------------------------
# Завдання 2.1.4 — схема балансу для даних завдання 2.1.2
# ---------------------------------------------------------------
print("\n### Завдання 2.1.4 (для даних 2.1.2) ###")
balance_table(A2, X2, "2.1.4 / 2.1.2")

# ---------------------------------------------------------------
# Завдання 2.1.5 — новий план випуску для прикладу з вступного алгоритму
# ---------------------------------------------------------------
print("\n### Завдання 2.1.5 ###")
A_ex = np.array([
    [0.3, 0.1, 0.4],
    [0.2, 0.5, 0.0],
    [0.3, 0.1, 0.2],
])
B_ex, _ = check_productivity(A_ex, "приклад з вступу")
Y5 = np.array([250.0, 100.0, 360.0])
X5 = B_ex @ Y5
print(f"Новий план кінцевої продукції Y' = {Y5}")
print(f"Новий вектор валової продукції X' = {X5}")
balance_table(A_ex, X5, "2.1.5")

# ---------------------------------------------------------------
# Завдання 2.1.6 — чотиригалузевий МГБ
# ---------------------------------------------------------------
print("\n### Завдання 2.1.6 ###")
A6 = np.array([
    [0.52, 0.12, 0.04, 0.20],
    [0.07, 0.35, 0.03, 0.12],
    [0.04, 0.03, 0.30, 0.14],
    [0.05, 0.03, 0.04, 0.20],
])
Y6 = np.array([40.3, 21.0, 1.3, 2.5])
B6, prod6 = check_productivity(A6, "2.1.6")
X6 = B6 @ Y6
print(f"Y = {Y6}  (млрд грн)")
print(f"X = (E-A)^-1 * Y = {X6}  (млрд грн)")

# ---------------------------------------------------------------
# Завдання 2.1.7 — модель цін Леонтьєва, шок ціни галузі 1
# ---------------------------------------------------------------
print("\n### Завдання 2.1.7 ###")
X7 = np.array([1893.0, 1241.0, 537.0])
flows7 = np.array([
    [984.4, 173.7, 59.1],
    [227.1, 86.9, 136.3],
    [37.9, 37.2, 48.3],
])
wages = np.array([377.1, 351.9, 75.4])
profit = np.array([563.5, 469.3, 173.9])
taxes = np.array([207.6, 0.0, 40.0])
subsidies = np.array([-579.6, 0.0, 0.0])
capital = np.array([75.0, 122.0, 18.0])

A7 = flows7 / X7[np.newaxis, :]
v7 = (wages + profit + taxes + subsidies + capital) / X7
print(f"Матриця коефіцієнтів прямих витрат A =\n{A7}")
print(f"Вектор коефіцієнтів доданої вартості v = {v7}")
print(f"Перевірка: сума стовпця A + v_j (має дорівнювати ~1) = {A7.sum(axis=0) + v7}")

p0 = np.array([1.0, 1.0, 1.0])
print(f"Базові ціни p0 = (1,1,1), нев'язка рівнянь p - (A^T p + v) = {p0 - (A7.T @ p0 + v7)}")

p1_new = 5.0
M = np.array([
    [1 - A7[1, 1], -A7[2, 1]],
    [-A7[1, 2], 1 - A7[2, 2]],
])
rhs = np.array([
    A7[0, 1] * p1_new + v7[1],
    A7[0, 2] * p1_new + v7[2],
])
p2_new, p3_new = np.linalg.solve(M, rhs)
print(f"Нова ціна першої галузі p1' = {p1_new}")
print(f"Розв'язок для p2', p3' = {p2_new:.6f}, {p3_new:.6f}")
print(f"Відносна зміна цін, %: p2 {(p2_new - 1) * 100:.2f}%, p3 {(p3_new - 1) * 100:.2f}%")

print("\n" + "=" * 70)
print("БЛОК 2.2. Міжгалузеві баланси праці та фондів")
print("=" * 70)

# ---------------------------------------------------------------
# Завдання 2.2.1 (варіант 6, i=6)
# ---------------------------------------------------------------
print("\n### Завдання 2.2.1 (варіант 6, i=6) ###")
i = 6
A_lf = np.array([
    [0.19, 0.23, 0.32, 0.16],
    [0.31, 0.15, 0.21, 0.18],
    [0.18, 0.22, 0.28, 0.17],
    [0.19, 0.21, 0.23, 0.22],
])
Y_lf = np.array([100.0 * i, 200.0 * i, 180.0 * i, 250.0 * i])
L_lf = np.array([120.0 * i, 200.0 * i, 180.0 * i, 250.0 * i])
f_lf = np.array([10.2, 11.3, 7.5, 3.7])

B_lf, prod_lf = check_productivity(A_lf, "2.2.1")
X_lf = B_lf @ Y_lf
t_lf = L_lf / X_lf
T_lf = t_lf @ B_lf
F_lf = f_lf @ B_lf

print(f"Y = {Y_lf}")
print(f"L = {L_lf}")
print(f"X = (E-A)^-1 * Y = {X_lf}")
print(f"t (коефіцієнти прямої трудомісткості) = L / X = {t_lf}")
print(f"T (коефіцієнти повної трудомісткості) = t * B = {T_lf}")
print(f"F (коефіцієнти повної фондомісткості) = f * B = {F_lf}")
print(f"Перевірка балансового рівняння (2.18): t*X = {t_lf @ X_lf:.4f}, T*Y = {T_lf @ Y_lf:.4f}")

# ---------------------------------------------------------------
# Збереження результатів у data.json
# ---------------------------------------------------------------
Q1_1, net1 = balance_table(A1, X1, "2.1.1 (json)")
Q1_4, net4 = balance_table(A2, X2, "2.1.4 (json)")
Q1_5, net5 = balance_table(A_ex, X5, "2.1.5 (json)")

roots_sorted = np.sort(roots)

save_block("task2_1_1", {
    "A": r6(A1), "Y": r6(Y1),
    "B": r6(B1), "B_disp": mat_disp(B1),
    "productive_inv": bool(prod1),
    "roots": r6(roots_sorted),
    "roots_disp": vec_disp(roots_sorted, "{:.4f}"),
    "max_root": r6(roots.max()),
    "productive_char": bool(roots.max() < 1),
    "X": r6(X1), "X_disp": vec_disp(X1),
    "balance": {
        "Q1": r6(Q1_1), "Q1_disp": mat_disp(Q1_1, "{:.3f}"),
        "net": r6(net1), "net_disp": vec_disp(net1),
        "net_sum": round(float(net1.sum()), 3),
        "Y_sum": round(float(X1.sum() - Q1_1.sum()), 3),
        "X_sum": round(float(X1.sum()), 3),
    },
})

save_block("task2_1_2", {
    "A": r6(A2), "Y": r6(Y2),
    "B": r6(B2), "B_disp": mat_disp(B2),
    "col_norms": vec_disp(np.max(np.abs(A2), axis=0), "{:.2f}"),
    "max_eig": r6(np.max(np.abs(np.linalg.eigvals(A2)))),
    "X": r6(X2), "X_disp": vec_disp(X2),
})

save_block("task2_1_4", {
    "balance": {
        "Q1": r6(Q1_4), "Q1_disp": mat_disp(Q1_4, "{:.3f}"),
        "net": r6(net4), "net_disp": vec_disp(net4),
        "net_sum": round(float(net4.sum()), 3),
        "net_sum_disp": f"{net4.sum():.2f}",
        "Y_sum": round(float(X2.sum() - Q1_4.sum()), 3),
        "Y_sum_disp": f"{X2.sum() - Q1_4.sum():.2f}",
        "X": r6(X2), "X_disp": vec_disp(X2),
        "X_sum": round(float(X2.sum()), 3),
        "Y_disp": vec_disp(Y2),
    },
})

save_block("task2_1_5", {
    "A_ex": r6(A_ex), "B_ex": r6(B_ex), "B_ex_disp": mat_disp(B_ex),
    "Y5": r6(Y5), "X5": r6(X5), "X5_disp": vec_disp(X5),
    "X0": r6(B_ex @ np.array([200.0, 100.0, 300.0])),
    "balance": {
        "Q1": r6(Q1_5), "Q1_disp": mat_disp(Q1_5, "{:.3f}"),
        "net": r6(net5), "net_disp": vec_disp(net5),
        "net_sum": round(float(net5.sum()), 3),
        "Y_sum": round(float(X5.sum() - Q1_5.sum()), 3),
        "X_sum": round(float(X5.sum()), 2),
    },
})

save_block("task2_1_6", {
    "A": r6(A6), "Y": r6(Y6),
    "max_eig": r6(np.max(np.abs(np.linalg.eigvals(A6)))),
    "productive": bool(prod6),
    "X": r6(X6), "X_disp": vec_disp(X6),
})

save_block("task2_1_7", {
    "A": r6(A7), "A_disp": mat_disp(A7, "{:.4f}"),
    "v": r6(v7), "v_disp": vec_disp(v7, "{:.4f}"),
    "resid_p0": r6(p0 - (A7.T @ p0 + v7)),
    "a12": f"{A7[0, 1]:.4f}", "a13": f"{A7[0, 2]:.4f}",
    "p1_new": p1_new,
    "p2_new": round(float(p2_new), 4),
    "p3_new": round(float(p3_new), 4),
    "p2_change_pct": round(float((p2_new - 1) * 100), 1),
    "p3_change_pct": round(float((p3_new - 1) * 100), 1),
})

save_block("task2_2_1", {
    "i": i,
    "A": r6(A_lf), "Y": r6(Y_lf), "L": r6(L_lf), "f": r6(f_lf),
    "max_eig": r6(np.max(np.abs(np.linalg.eigvals(A_lf)))),
    "productive": bool(prod_lf),
    "X": r6(X_lf), "X_disp": vec_disp(X_lf, "{:.2f}"),
    "t": r6(t_lf), "t_disp": vec_disp(t_lf, "{:.4f}"),
    "T": r6(T_lf), "T_disp": vec_disp(T_lf, "{:.4f}"),
    "F": r6(F_lf), "F_disp": vec_disp(F_lf, "{:.2f}"),
    "tX": round(float(t_lf @ X_lf), 4),
    "TY": round(float(T_lf @ Y_lf), 4),
    "tX_disp": f"{t_lf @ X_lf:.1f}",
    "TY_disp": f"{T_lf @ Y_lf:.1f}",
    "F_max_idx": int(np.argmax(F_lf)),
    "F_min_idx": int(np.argmin(F_lf)),
})
print(f"Дані збережено у {DATA_PATH}")
