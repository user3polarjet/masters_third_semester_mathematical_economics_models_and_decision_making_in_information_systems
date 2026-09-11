"""
Практична робота №2 (розділ 2) — Варіант 6
Використання експертних оцінок та шкали Сааті в задачах прийняття рішень

Усі обчислені результати також зберігаються у data.json, який читає
безпосередньо Typst-звіт — це виключає розбіжності між текстом звіту
та фактичним виводом скрипта.
"""
import json
import pathlib

import numpy as np

np.set_printoptions(suppress=True, linewidth=120)

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent


def r4(x):
    """Округлення до 4 знаків, придатне для JSON (list/float/int)."""
    if isinstance(x, np.ndarray):
        return np.round(x, 4).tolist()
    return round(float(x), 4)


data = {}

print("=" * 70)
print("БЛОК 1. Метод Делфі (варіант 6: радіоаматорська сфера діяльності)")
print("=" * 70)

topics = [
    "Комп'ютеризація радіопередавальної апаратури",
    "Заміщення аналогових процесів цифровими",
    "Уведення нових стандартів та розширення діапазону частот",
    "Співпраця зі службами спасіння (зокрема «112»)",
    "Участь у великих проєктах («Вивчення Місяця»)",
    "Популяризація радіоаматорства серед молоді",
]
n_topics = len(topics)

# --- Коефіцієнти компетентності експертів (метод самооцінки) ---
experts_raw = {
    1: dict(Kz_score=7, args=dict(theory=0.3, experience=0.4, literature=0.04, intuition=0.04)),
    2: dict(Kz_score=5, args=dict(theory=0.2, experience=0.5, literature=0.1, intuition=0.02)),
    3: dict(Kz_score=9, args=dict(theory=0.3, experience=0.5, literature=0.08, intuition=0.05)),
    4: dict(Kz_score=3, args=dict(theory=0.1, experience=0.4, literature=0.04, intuition=0.02)),
}

Kk = {}
experts_table = []
print("Розрахунок коефіцієнтів компетентності K_k = (K_з + K_а) / 2:")
for e, d in experts_raw.items():
    Kz = d["Kz_score"] * 0.1
    Ka = sum(d["args"].values())
    Kk[e] = (Kz + Ka) / 2
    print(f"  Експерт {e}: K_з = {Kz:.2f}, K_а = {Ka:.2f}, K_k = {Kk[e]:.4f}")
    experts_table.append({
        "expert": e,
        "Kz": r4(Kz),
        "theory": d["args"]["theory"],
        "experience": d["args"]["experience"],
        "literature": d["args"]["literature"],
        "intuition": d["args"]["intuition"],
        "Ka": r4(Ka),
        "Kk": r4(Kk[e]),
    })

Kk_vec = np.array(list(Kk.values()))
m = len(Kk)

# --- Оцінки експертів щодо напрямків (0-10 балів) ---
scores = np.array([
    [8, 7, 9, 6, 4, 5],
    [9, 8, 7, 8, 5, 6],
    [7, 9, 8, 5, 6, 7],
    [5, 6, 6, 7, 3, 4],
], dtype=float)

print("\nОцінки експертів (f1..f6):")
for i, row in enumerate(scores, start=1):
    print(f"  Експерт {i}: {row}")

Mj = (Kk_vec[:, None] * scores).sum(axis=0) / m
print(f"\nУзагальнена оцінка важливості M_j = sum(K_k * c_ij) / m:")
for j, val in enumerate(Mj, start=1):
    print(f"  f{j} ({topics[j-1]}): M_{j} = {val:.4f}")

order = np.argsort(-Mj)
Ri = np.empty(n_topics, dtype=int)
for rank, idx in enumerate(order, start=1):
    Ri[idx] = rank

print("\nРанжирування напрямків (від найважливішого):")
for rank, idx in enumerate(order, start=1):
    print(f"  {rank}. f{idx+1} — {topics[idx]} (M = {Mj[idx]:.4f})")

lam = 2 * (n_topics + 1 - Ri) / (n_topics * (n_topics + 1))
print(f"\nВідносні коефіцієнти значущості (лямбда), сума = {lam.sum():.4f}:")
for j in range(n_topics):
    print(f"  f{j+1}: R_i = {Ri[j]}, lambda_i = {lam[j]:.6f}")

data["block1"] = {
    "topics": topics,
    "experts": experts_table,
    "scores": scores.astype(int).tolist(),
    "Mj": r4(Mj),
    "Ri": [int(x) for x in Ri],
    "lambda": [round(float(x), 6) for x in lam],
    "lambda_sum": round(float(lam.sum()), 6),
    "ranking": [
        {"rank": rank, "code": f"f{idx+1}", "topic": topics[idx], "Mj": r4(Mj[idx])}
        for rank, idx in enumerate(order, start=1)
    ],
}

print("\n" + "=" * 70)
print("БЛОК 2. Шкала Сааті — вибір автомобіля (АВТО1-АВТО4)")
print("=" * 70)


def eig_weights(M):
    """Ваги методом власного вектора (принциповий власний вектор AHP)."""
    eigvals, eigvecs = np.linalg.eig(M)
    idx = np.argmax(eigvals.real)
    lam_max = eigvals[idx].real
    v = eigvecs[:, idx].real
    w = v / v.sum()
    n = M.shape[0]
    CI = (lam_max - n) / (n - 1) if n > 1 else 0.0
    RI_table = {1: 0, 2: 0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24}
    RI = RI_table.get(n, 1.12)
    CR = CI / RI if RI > 0 else 0.0
    return w, lam_max, CI, CR


def rowsum_weights(M):
    rs = M.sum(axis=1)
    return rs / rs.sum()


alt_names = ["АВТО1", "АВТО2", "АВТО3", "АВТО4"]

# --- Параметр "Дизайн" (задано у методичних вказівках) ---
Design = np.array([
    [1, 0.25, 4, 1 / 6],
    [4, 1, 4, 0.25],
    [0.25, 0.25, 1, 0.2],
    [6, 4, 5, 1],
])
w_design_rs = rowsum_weights(Design)
w_design_eig, lam_d, ci_d, cr_d = eig_weights(Design)
print("--- Дизайн (МПП з методички) ---")
print(f"Ваги (метод рядкових сум): {np.round(w_design_rs, 4)}")
print(f"Ваги (метод власного вектора): {np.round(w_design_eig, 4)}")
print(f"lambda_max = {lam_d:.4f}, CI = {ci_d:.4f}, CR = {cr_d:.4f}"
      + ("  (CR > 0.1 — оцінки ОПР недостатньо узгоджені)" if cr_d > 0.1 else ""))

design_frac = [["1", "1/4", "4", "1/6"], ["4", "1", "4", "1/4"], ["1/4", "1/4", "1", "1/5"], ["6", "4", "5", "1"]]

# --- Параметр "Надійність" (самостійно побудована МПП) ---
Reliab = np.array([
    [1, 3, 5, 2],
    [1 / 3, 1, 3, 0.5],
    [1 / 5, 1 / 3, 1, 0.25],
    [0.5, 2, 4, 1],
])
w_reliab, lam_r, ci_r, cr_r = eig_weights(Reliab)
print("\n--- Надійність (самостійно побудована МПП) ---")
print(f"Ваги (метод власного вектора): {np.round(w_reliab, 4)}")
print(f"lambda_max = {lam_r:.4f}, CI = {ci_r:.4f}, CR = {cr_r:.4f}")

reliab_frac = [["1", "3", "5", "2"], ["1/3", "1", "3", "1/2"], ["1/5", "1/3", "1", "1/4"], ["1/2", "2", "4", "1"]]

# --- Параметр "Економічність" (самостійно побудована МПП) ---
Econ = np.array([
    [1, 3, 1 / 3, 2],
    [1 / 3, 1, 0.2, 0.5],
    [3, 5, 1, 4],
    [0.5, 2, 0.25, 1],
])
w_econ, lam_e, ci_e, cr_e = eig_weights(Econ)
print("\n--- Економічність (самостійно побудована МПП) ---")
print(f"Ваги (метод власного вектора): {np.round(w_econ, 4)}")
print(f"lambda_max = {lam_e:.4f}, CI = {ci_e:.4f}, CR = {cr_e:.4f}")

econ_frac = [["1", "3", "1/3", "2"], ["1/3", "1", "1/5", "1/2"], ["3", "5", "1", "4"], ["1/2", "2", "1/4", "1"]]

# --- Ваги параметрів між собою (задано у методичних вказівках) ---
Params = np.array([
    [1, 0.5, 3],
    [2, 1, 4],
    [1 / 3, 0.25, 1],
])
w_params = rowsum_weights(Params)
print("\n--- Ваги параметрів (Дизайн, Надійність, Економічність) ---")
print(f"Ваги (метод рядкових сум): {np.round(w_params, 4)}")

params_frac = [["1", "1/2", "3"], ["2", "1", "4"], ["1/3", "1/4", "1"]]

# --- Інтегральна оцінка (лінійна згортка) ---
utility = w_params[0] * w_design_eig + w_params[1] * w_reliab + w_params[2] * w_econ
print("\n--- Інтегральна оцінка (функція корисності) ---")
for name, u in zip(alt_names, utility):
    print(f"  {name}: {u:.4f}")

# --- Аналіз вартість/ефективність ---
cost = np.array([4000.0, 3000.0, 2500.0, 7000.0])
cost_norm = cost / cost.sum()
ratio = utility / cost_norm

print("\n--- Аналіз співвідношення вартість/ефективність ---")
print(f"Вартість: {cost}, сума = {cost.sum():.0f}")
print(f"Нормована вартість: {np.round(cost_norm, 4)}")
print(f"Відношення (корисність/нормована вартість): {np.round(ratio, 4)}")
best_idx = int(np.argmax(ratio))
print(f"Найкраще співвідношення вартість/ефективність: {alt_names[best_idx]}")

# --- Параметр "Максимальна швидкість" ---
speed = np.array([140.0, 130.0, 120.0, 150.0])
speed_norm = speed / speed.sum()
print("\n--- Максимальна швидкість ---")
for name, s, sn in zip(alt_names, speed, speed_norm):
    print(f"  {name}: {s:.0f} км/год, нормоване значення = {sn:.4f}")

data["block2"] = {
    "alt_names": alt_names,
    "design": {
        "matrix_frac": design_frac,
        "w_rowsum": r4(w_design_rs),
        "w_eig": r4(w_design_eig),
        "lambda_max": r4(lam_d),
        "CI": r4(ci_d),
        "CR": r4(cr_d),
    },
    "reliability": {
        "matrix_frac": reliab_frac,
        "w_eig": r4(w_reliab),
        "lambda_max": r4(lam_r),
        "CI": r4(ci_r),
        "CR": r4(cr_r),
    },
    "economy": {
        "matrix_frac": econ_frac,
        "w_eig": r4(w_econ),
        "lambda_max": r4(lam_e),
        "CI": r4(ci_e),
        "CR": r4(cr_e),
    },
    "params": {
        "matrix_frac": params_frac,
        "w_rowsum": r4(w_params),
    },
    "utility": r4(utility),
    "cost": {
        "values": cost.tolist(),
        "sum": float(cost.sum()),
        "normalized": r4(cost_norm),
        "ratio": r4(ratio),
        "best_idx": best_idx,
        "best_name": alt_names[best_idx],
    },
    "speed": {
        "values": speed.tolist(),
        "normalized": r4(speed_norm),
    },
}

out_path = SCRIPT_DIR / "data.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\nДані збережено у {out_path}")
