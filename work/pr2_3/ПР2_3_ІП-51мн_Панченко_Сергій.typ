#set text(font: "Times New Roman", size: 14pt)
#set page(
  paper: "a4",
  margin: (top: 1.5cm, bottom: 1.5cm, left: 2.5cm, right: 1.5cm)
)

#align(center)[
  #image("kpi.svg", width: 75%)

  Міністерство освіти і науки України

  Національний технічний університет України

  "Київський політехнічний інститут імені Ігоря Сікорського"

  Факультет інформатики та обчислювальної техніки

  Кафедра інформатики та програмної інженерії

  #align(horizon)[
    #text(size: 18pt)[
      Практична робота №3

      Моделі математичної економіки та прийняття рішень в інформаційних системах
    ]

    Тема: Прийняття рішень в задачах багатокритеріальної оптимізації

    Варіант 6
  ]

  #columns(2, gutter: 8pt)[
    #align(left)[
      Виконав:

      студент групи ІП-51мн

      Панченко С. В.
    ]

    #colbreak()

    #align(right)[
      Перевірив:

      #text[Поперешняк С. В.]
    ]
  ]
]

#align(center + bottom)[
  Київ 2026
]

#set page(numbering: "1")
#show outline: it => {
  show heading: set align(center)
  show heading: set text(weight: "regular")
  it
}
#outline(title: upper([Зміст]))

#set heading(numbering: (..nums) => nums.pos().map(str).join("."))
#show heading: it => {
  if it.level == 1 {
    counter(figure.where(kind: table)).update(0)
    counter(figure.where(kind: image)).update(0)
    set align(center)
    set text(weight: "regular", size: 18pt)
    pagebreak()
    upper(it)
  } else {
    set text(weight: "regular", size: 14pt)
    it
  }
}

#let figure-numbering(num) = context {
  let h-num = counter(heading).at(here()).at(0)
  str(h-num) + "." + str(num)
}

#show figure.where(kind: table): it => {
  align(left)[
    #it.supplement #context (it.counter.display(it.numbering)) #it.caption.body
  ]
  v(10pt, weak: true)
  align(center)[#it.body]
}
#show figure.where(kind: image): it => {
  set align(center)
  it.body
  v(8pt, weak: true)
  it.supplement
  [ ]
  context (it.counter.display(it.numbering))
  [ — ]
  it.caption.body
}

#set figure(numbering: figure-numbering)
#show figure.where(kind: image): set figure(supplement: [Рисунок])
#show figure.where(kind: table): set figure(supplement: [Таблиця])

#set par(first-line-indent: (amount: 1.25cm, all: true), justify: true, leading: 1em, spacing: 1em)
#set list(indent: 1.25cm)
#set enum(indent: 1.25cm)

// Усі обчислені результати читаються безпосередньо з data.json (вивід
// multi_criteria.py), щоб текст звіту завжди відповідав фактичному
// розрахунку, без ручного передруку чисел.
#let d = json("data.json")

#let fmtvec(xs) = "(" + xs.map(str).join(", ") + ")"

#let x-table(x-flat, caption) = figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    stroke: 0.5pt,
    inset: 5pt,
    align: center,
    table.header([Комбайн], ..d.setup.jobs.map(j => [$#j$]), [Реальний], [За умовою]),
    ..for (i, m) in d.setup.machines.enumerate() {
      let row = x-flat.slice(i * 3, i * 3 + 3)
      let real = row.sum()
      ([#m],) + row.map(v => [#v]) + ([#real], [$<=$ #d.setup.T.at(i)])
    }
  ),
  caption: caption
)

= Мета

Вивчити методи розв'язання задач багатокритеріальної оптимізації: метод згортки, метод головного критерію та метод послідовної поступки.

Усі розрахунки виконано мовою Python (бібліотека SciPy, функція `linprog` для розв'язання задач лінійного програмування) замість надбудови Excel «Пошук рішення», а звіт підготовлено засобами Typst замість MS Word.

= Постановка задачі (варіант 6)

Три комбайни (I, II, III) виконують три види робіт (A, B, C). Задано продуктивність $q_(i j)$ (м³/год), питому вартість $c_(i j)$ (грн/год) та ресурс часу кожного комбайна:

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto, auto),
    stroke: 0.5pt,
    inset: 5pt,
    align: center,
    table.header([Комбайн], [$q_A$], [$q_B$], [$q_C$], [$c_A$], [$c_B$], [$c_C$], [Ресурс, год]),
    ..for (i, m) in d.setup.machines.enumerate() {
      ([#m],) + d.setup.q.at(i).map(v => [#v]) + d.setup.c.at(i).map(v => [#v]) + ([#d.setup.T.at(i)],)
    }
  ),
  caption: [Вихідні дані варіанта 6: продуктивність, вартість, ресурс часу]
)

Позначимо через $x_(i j)$ час виконання $i$-м комбайном $j$-ї роботи. Математична модель задачі:

$ f_1(x) = sum_(i,j) q_(i j) x_(i j) arrow.r max; $

$ f_2(x) = sum_(i,j) c_(i j) x_(i j) arrow.r min; $

$ sum_j x_(i j) <= T_i, quad i = "I, II, III"; quad x_(i j) >= 0. $

= Нормалізація критеріїв

Для застосування методу згортки критерії потрібно звести до безрозмірного вигляду. Спочатку знайдено максимальні й мінімальні значення кожного критерію на множині припустимих альтернатив (розв'язанням відповідних однокритеріальних задач лінійного програмування):

#figure(
  table(
    columns: (auto, auto, auto),
    stroke: 0.5pt,
    inset: 5pt,
    align: center,
    table.header([Критерій], [Максимум], [Мінімум]),
    [$f_1$ (обсяг робіт)], [#d.normalization.f1_max], [#d.normalization.f1_min],
    [$f_2$ (вартість)], [#d.normalization.f2_max], [#d.normalization.f2_min],
  ),
  caption: [Максимальні та мінімальні значення критеріїв]
)

#x-table(d.normalization.x_f1max, [Розв'язок задачі максимізації $f_1$ ($f_1^"max"$ = #d.normalization.f1_max м³; супутня вартість $f_2$ = #d.normalization.f2_at_f1max грн)])

#x-table(d.normalization.x_f2max, [Розв'язок задачі максимізації $f_2$ ($f_2^"max"$ = #d.normalization.f2_max грн)])

Оскільки $f_1$ максимізується, а найгірше (мінімальне) значення дорівнює 0, нормалізований критерій має вигляд:

$ f_1^*(x) = (f_1^"max" - f_1(x)) / f_1^"max" = (#d.normalization.f1_max - f_1(x)) / #d.normalization.f1_max arrow.r min. $

Оскільки $f_2$ мінімізується, а найгірше (максимальне) значення дорівнює #d.normalization.f2_max, нормалізований критерій:

$ f_2^*(x) = (f_2(x) - f_2^"min") / f_2^"max" = f_2(x) / #d.normalization.f2_max arrow.r min. $

= Метод згортки

Прийнято вагові коефіцієнти значущості критеріїв $alpha_1 = #d.convolution.alpha1$, $alpha_2 = #d.convolution.alpha2$ (рівнозначні критерії), оскільки обидва критерії лінійні, застосовано лінійну адитивну згортку:

$ F(x) = alpha_1 f_1^*(x) + alpha_2 f_2^*(x) arrow.r min. $

Розв'язання відповідної скалярної задачі лінійного програмування дає:

#x-table(d.convolution.x, [Розв'язок методом згортки ($alpha_1$=#d.convolution.alpha1, $alpha_2$=#d.convolution.alpha2)])

Отримано $f_1 = $ #d.convolution.f1 м³, $f_2 = $ #d.convolution.f2 грн, значення узагальненого критерію $F = $ #d.convolution.F.

Вплив вибору вагових коефіцієнтів. Якщо, за прикладом методичних вказівок, обрати ваги $alpha_1=0.7$, $alpha_2=0.3$ (значно вищий пріоритет обсягу робіт), розв'язок дає #(if d.convolution.reference_0703.matches_f1max [той самий вектор $x$, що й чиста максимізація $f_1$] else [інший вектор $x$]) ($x = $ #fmtvec(d.convolution.reference_0703.x), $f_1=$ #d.convolution.reference_0703.f1, $f_2=$ #d.convolution.reference_0703.f2). Це пояснюється тим, що обмеження задачі є повністю незалежними по кожному комбайну (кожен рядок $x_(i,dot)$ фігурує лише у своєму обмеженні), тому оптимум лінійної згортки завжди досягається у вершині багатогранника — розподілі всього ресурсу комбайна на одну роботу; за досить великої ваги $alpha_1$ ця вершина збігається з вершиною чистої максимізації $f_1$. Щоб отримати змістовний компроміс (а не вироджений збіг з однокритеріальним розв'язком), у цьому звіті використано рівнозначні ваги $alpha_1=alpha_2=0.5$.

= Метод головного критерію

Головним критерієм обрано $f_1$ (обсяг робіт) як такий, для якого експертна оцінка допустимого рівня є найскладнішою. Встановлено додаткове обмеження на максимально допустиму вартість робіт $f_2(x) <= $ #d.main_criterion.f2_threshold грн:

$ f_1(x) arrow.r max; quad f_2(x) <= #d.main_criterion.f2_threshold\; quad sum_j x_(i j) <= T_i; quad x_(i j) >= 0. $

#x-table(d.main_criterion.x, [Розв'язок методом головного критерію ($f_2 <=$ #d.main_criterion.f2_threshold)])

Отримано $f_1 = $ #d.main_criterion.f1 м³, $f_2 = $ #d.main_criterion.f2 грн (обмеження вартості виконується як рівність, тобто ресурс вартості вичерпано повністю).

= Метод послідовної поступки

Спочатку розв'язано скалярну задачу за найбільш значущим критерієм $f_1$ на всій множині припустимих альтернатив (розв'язок наведено в таблиці розв'язку максимізації $f_1$ вище): $f_1^"max" = $ #d.normalization.f1_max м³.

Прийнято припустиму поступку за першим критерієм $Delta = $ #d.sequential.delta м³ (#calc.round(d.sequential.delta_frac * 100, digits: 1)% від $f_1^"max"$), тобто нова нижня межа: $f_1(x) >= f_1^"max" - Delta = $ #d.sequential.f1_floor. На другому кроці розв'язано задачу мінімізації другого критерію за цього додаткового обмеження:

$ f_2(x) arrow.r min; quad f_1(x) >= #d.sequential.f1_floor\; quad sum_j x_(i j) <= T_i; quad x_(i j) >= 0. $

#x-table(d.sequential.x, [Розв'язок методом послідовної поступки ($f_1 >=$ #d.sequential.f1_floor)])

Отримано $f_1 = $ #d.sequential.f1 м³, $f_2 = $ #d.sequential.f2 грн. Оскільки в задачі лише два критерії, після цього кроку розв'язок вважається остаточним розв'язком методом послідовної поступки.

= Аналіз результатів

#[
  #set text(size: 10pt)
  #figure(
    table(
      columns: (3.1cm,) + (auto,) * 11,
      stroke: 0.5pt,
      inset: 4pt,
      align: center,
      table.header(
        [Метод],
        [$x_(I A)$], [$x_(I B)$], [$x_(I C)$],
        [$x_(I I A)$], [$x_(I I B)$], [$x_(I I C)$],
        [$x_(I I I A)$], [$x_(I I I B)$], [$x_(I I I C)$],
        [$f_1(x)$], [$f_2(x)$],
      ),
      ..for m in d.summary {
        ([#m.method],) + m.x.map(v => [#v]) + ([#m.f1], [#m.f2])
      }
    ),
    caption: [Зведена таблиця розв'язків багатокритеріальної задачі (варіант 6)]
  )
]

Усі три розв'язки є ефективними за Парето — жоден з них не домінується іншим (кожен покращує один критерій ціною погіршення іншого):

- метод згортки (рівні ваги) дає найбільший обсяг робіт ($f_1=$ #d.convolution.f1) ціною найвищої вартості серед трьох методів ($f_2=$ #d.convolution.f2);
- метод головного критерію дозволяє прямо контролювати максимально допустиму вартість (тут — #d.main_criterion.f2_threshold грн) і максимізує обсяг робіт у цих межах;
- метод послідовної поступки дає найменшу вартість ($f_2=$ #d.sequential.f2) ціною найбільшої поступки за обсягом робіт відносно $f_1^"max"$.

Остаточний вибір одного з ефективних розв'язків залежить від пріоритетів особи, яка приймає рішення: чи важливіше мінімізувати витрати, чи максимізувати обсяг виконаних робіт. Жоден із трьох методів не претендує на «єдиний правильний» розв'язок — кожен лише пропонує один із раціональних компромісів на множині Парето-оптимальних альтернатив.

= Висновки

У ході практичної роботи побудовано математичну модель двокритеріальної задачі оптимального завантаження комбайнів для варіанта 6 та розв'язано її трьома методами багатокритеріальної оптимізації, реалізованими програмно мовою Python із застосуванням лінійного програмування (`scipy.optimize.linprog`) замість надбудови Excel «Пошук рішення».

Показано, що метод згортки чутливий до вибору вагових коефіцієнтів: за домінівної ваги одного критерію (наприклад, $alpha_1=0.7$) розв'язок вироджується до чистого однокритеріального оптимуму — це пояснюється розділюваністю обмежень задачі за комбайнами. Використання рівнозначних ваг ($alpha_1=alpha_2=0.5$) дало змістовний компромісний розв'язок. Методи головного критерію та послідовної поступки дали ще два відмінних Парето-оптимальних розв'язки, кожен з яких по-різному балансує між обсягом робіт і вартістю. Усі три отримані розв'язки є ефективними за Парето, а остаточний вибір між ними лежить поза межами математичної моделі й залежить від пріоритетів особи, яка приймає рішення.

= Лістинг коду

#let embed_code(file_path, lang_name) = {
  heading(file_path, level: 2)
  raw(read(file_path), lang: lang_name, block: true)
}

#embed_code("multi_criteria.py", "python")
