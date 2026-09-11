"""
Практична робота №1 (розділ 2) — Варіант 6
Методи прийняття рішень на основі бінарних відношень та попарних порівнянь

Усі обчислені результати також зберігаються у data.json, який читає
безпосередньо Typst-звіт — це виключає розбіжності між текстом звіту
та фактичним виводом скрипта.
"""
import itertools
import json
import pathlib

import numpy as np

np.set_printoptions(linewidth=120)

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent


def mat(a):
    """numpy-масив -> список списків int, придатний для JSON."""
    return np.asarray(a).astype(int).tolist()


def analyze_relation(R, label):
    n = R.shape[0]
    print(f"=== {label} ===")
    print(f"R =\n{R}")

    reflexive = bool(np.all(np.diag(R) == 1))
    antireflexive = bool(np.all(np.diag(R) == 0))
    symmetric = bool(np.array_equal(R, R.T))
    asymmetric = bool(np.all((R & R.T) == 0))
    off_diag_mask = ~np.eye(n, dtype=bool)
    antisymmetric = bool(np.all((R & R.T)[off_diag_mask] == 0))

    R2 = ((R @ R) > 0).astype(int)
    transitive = bool(np.all(R2 <= R))

    print(f"Рефлексивне: {reflexive}")
    print(f"Антирефлексивне: {antireflexive}")
    print(f"Симетричне: {symmetric}")
    print(f"Асиметричне: {asymmetric}")
    print(f"Антисиметричне: {antisymmetric}")
    print(f"R^2 =\n{R2}")
    print(f"Транзитивне: {transitive}")

    R_inv = R.T
    R_comp = 1 - R
    print(f"Обернене R^-1 = R^T =\n{R_inv}")
    print(f"Доповнення R̄ = 1-R =\n{R_comp}")

    greatest = [i for i in range(n) if np.all(R[i, :] == 1)]
    least = [i for i in range(n) if np.all(R[:, i] == 1)]
    print(f"Найбільші елементи (індекси, з 0): {greatest}")
    print(f"Найменші елементи (індекси, з 0): {least}")

    R_strict = R * (1 - R.T)
    print(f"Строге відношення R^S = R & !R^T =\n{R_strict}")
    maximal = [i for i in range(n) if np.all(R_strict[:, i] == 0)]
    minimal = [i for i in range(n) if np.all(R_strict[i, :] == 0)]
    print(f"Максимальні елементи (індекси, з 0): {maximal}")
    print(f"Мінімальні елементи (індекси, з 0): {minimal}")

    return {
        "reflexive": reflexive,
        "antireflexive": antireflexive,
        "symmetric": symmetric,
        "asymmetric": asymmetric,
        "antisymmetric": antisymmetric,
        "transitive": transitive,
        "R_inv": R_inv,
        "R_comp": R_comp,
        "greatest": greatest,
        "least": least,
        "maximal": maximal,
        "minimal": minimal,
        "R2": R2,
        "R_strict": R_strict,
    }


print("=" * 70)
print("БЛОК 2. Прийняття рішень на основі бінарних відношень (варіант 6)")
print("=" * 70)

# Матриця варіанта 6 (Додаток А)
R6 = np.array([
    [1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1],
    [1, 0, 0, 1, 1],
    [0, 1, 0, 0, 1],
])

result6 = analyze_relation(R6, "Варіант 6")

data = {
    "block2": {
        "R": mat(R6),
        "properties": {
            "reflexive": result6["reflexive"],
            "antireflexive": result6["antireflexive"],
            "symmetric": result6["symmetric"],
            "asymmetric": result6["asymmetric"],
            "antisymmetric": result6["antisymmetric"],
            "transitive": result6["transitive"],
        },
        "R2": mat(result6["R2"]),
        "R_inv": mat(result6["R_inv"]),
        "R_comp": mat(result6["R_comp"]),
        "R_strict": mat(result6["R_strict"]),
        "greatest": [i + 1 for i in result6["greatest"]],
        "least": [i + 1 for i in result6["least"]],
        "maximal": [i + 1 for i in result6["maximal"]],
        "minimal": [i + 1 for i in result6["minimal"]],
    }
}

print("\n" + "=" * 70)
print("БЛОК 3. Попарні порівняння в задачах прийняття рішень")
print("=" * 70)

names = [
    "Моделі математичної економіки",
    "Технології великих даних",
    "Управління ІТ-проєктами",
    "Розподілені системи",
    "Машинне навчання",
    "Кібербезпека",
]
n = len(names)
codes = [f"a{i+1}" for i in range(n)]

# Верхня трикутна частина МПП: суб'єктивні оцінки значущості дисциплін
# для власного навчального плану (1 - краще, -1 - гірше, 0 - однаково)
pairs = {
    (0, 1): -1, (0, 2): 1, (0, 3): -1, (0, 4): -1, (0, 5): 1,
    (1, 2): 1, (1, 3): 1, (1, 4): 1, (1, 5): 1,
    (2, 3): -1, (2, 4): -1, (2, 5): 1,
    (3, 4): -1, (3, 5): 1,
    (4, 5): 1,
}

M = np.zeros((n, n), dtype=int)
for (i, j), v in pairs.items():
    M[i, j] = v
    M[j, i] = -v

print("МПП (матриця попарних порівнянь):")
header = "        " + "".join(f"{c:>5}" for c in codes) + "    сума"
print(header)
row_sums = M.sum(axis=1)
for i, code in enumerate(codes):
    print(f"{code:<8}" + "".join(f"{M[i,j]:>5}" for j in range(n)) + f"{row_sums[i]:>8}")

order = np.argsort(-row_sums)
print("\nРанжирування (від найбільш значущого до найменш значущого):")
ranking = []
for rank, idx in enumerate(order, start=1):
    print(f"  {rank}. {codes[idx]} — {names[idx]} (сума = {row_sums[idx]})")
    ranking.append({
        "rank": rank,
        "code": codes[idx],
        "name": names[idx],
        "sum": int(row_sums[idx]),
    })


def rel_symbol(v):
    return ">" if v == 1 else ("<" if v == -1 else "=")


print("\nПеревірка узгодженості (транзитивності) по всіх трійках об'єктів:")
print(f"{'№':<4}{'Трійка':<12}{'Умова':<20}{'Висновок':<20}{'Оцінка'}")
total_triads = 0
checkable = 0
violations = 0
triads = []
for idx, (i, j, k) in enumerate(itertools.combinations(range(n), 3), start=1):
    total_triads += 1
    a_ij, a_jk, a_ik = M[i, j], M[j, k], M[i, k]
    triple = f"{codes[i]},{codes[j]},{codes[k]}"
    cond = f"{codes[i]}{rel_symbol(a_ij)}{codes[j]}, {codes[j]}{rel_symbol(a_jk)}{codes[k]}"
    if a_ij == 0 or a_jk == 0 or a_ij != a_jk:
        print(f"{idx:<4}{triple:<12}{cond:<20}{'не перевіряється':<20}")
        triads.append({
            "triple": triple, "cond": cond,
            "checkable": False, "conclusion": "", "mark": "",
        })
        continue
    checkable += 1
    expected = a_ij
    ok = a_ik == expected
    concl = f"{codes[i]}{rel_symbol(expected)}{codes[k]}, факт {codes[i]}{rel_symbol(a_ik)}{codes[k]}"
    mark = "+" if ok else "-"
    if not ok:
        violations += 1
    print(f"{idx:<4}{triple:<12}{cond:<20}{concl:<20}{mark}")
    triads.append({
        "triple": triple, "cond": cond,
        "checkable": True, "conclusion": concl, "mark": mark,
    })

print(f"\nВсього трійок: {total_triads}, перевірюваних: {checkable}, порушень транзитивності: {violations}")
print("Матриця узгоджена" if violations == 0 else f"Матриця має {violations} порушень транзитивності")

data["block3"] = {
    "names": names,
    "codes": codes,
    "M": mat(M),
    "row_sums": [int(x) for x in row_sums],
    "ranking": ranking,
    "triads": triads,
    "total_triads": total_triads,
    "checkable": checkable,
    "violations": violations,
}

out_path = SCRIPT_DIR / "data.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\nДані збережено у {out_path}")
