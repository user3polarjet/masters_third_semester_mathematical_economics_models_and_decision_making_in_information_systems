**Альтернативний метод обробки емпіричної матриці парних порівнянь**

Даний метод належить О. А. Павлову та його учням
Якщо матриця $\Gamma$ ідеально узгоджена, то $\gamma_{ij}=\frac{\omega_i}{\omega_j}$, або $\omega_i=\omega_j\gamma_{ij}$. Можна запропонувати дві міри відхилення $\gamma_{ij}$ від значення $\frac{\omega_i}{\omega_j}$:
1) $|\omega_i-\gamma_{ij}\omega_j|$,  2) $\frac{1}{\gamma_{ij}}\left|\frac{\omega_i}{\omega_j}-\gamma_{ij}\right|,\ \forall\gamma_{ij}\ge1,i\ne j$.
Друга міра за змістом якісно краще, ніж перша міра. Але пряме використання другої міри приводить до нелінійних задач математичного програмування, на відміну від першої міри, яка приводить до задач лінійного програмування.
Розглянемо можливість ефективного використання другої міри шляхом рекурентної реалізації множини задач ЛП.
Для прикладу розглянемо лінійну модель для знаходження ваг з використанням першої міри.
$$min\sum_{(ij)\in|\Gamma|}y_{ij}\qquad(2.4)$$
$$-y_{ij}\le\omega_i-\gamma_{ij}\omega_j\le y_{ij},\ y_{ij}\ge0,\omega_i\ge0,\sum_{i=1}^{n}\omega_i=1.$$
$$\forall(ij)\in|\Gamma|$$
Змінні: $\forall y_{ij},\omega_i,i=\overline{1,n},\forall(ij)\in|\Gamma|$. $|\Gamma|$ – це множина всіх пар $(ij),i\ne j$, яким відповідають всі елементи матриці $\Gamma$, $\gamma_{ij}\ge1$.
Зрозуміло, що чим більше $\gamma_{ij}$більше одиниці, тим вірогідніше більше спотворення експертом числа $\gamma_{ij}$. Це дозволило запропонувати якісно більш ефективну наступну лінійну модель.
$$min\sum_{(ij)\in|\Gamma|}r_{ij}y_{ij}\qquad(2.5)$$
$$-y_{ij}\le\omega_i-\gamma_{ij}\omega_j\le y_{ij},\ y_{ij}\ge0,\omega_i\ge0,\sum_{i=1}^{n}\omega_i=1.$$
$$\forall(ij)\in|\Gamma|$$
Змінні: $\forall y_{ij},\omega_i,i=\overline{1,n},\forall(ij)\in|\Gamma|$.
В якості невід'ємних коефіцієнтів $r_{ij}$ досліджувались наступні:
$$r_{ij}=\frac{1}{\gamma_{ij}-1},\gamma_{ij}>1;r_{ij}=1,\gamma_{ij}=1;$$
$$r_{ij}=\frac{1}{\sqrt{\gamma_{ij}-1}},\gamma_{ij}>1;r_{ij}=1,\gamma_{ij}=1;$$
$$r_{ij}=\frac{1}{\sqrt[3]{(\gamma_{ij}-1)^2}},\gamma_{ij}>1;r_{ij}=1,\gamma_{ij}=1.$$
Результати статистичних досліджень показали, що інваріантними за ефективністю до різних ймовірнісних законів спотворення дійсних значень ваг $\omega_i,i=\overline{1,n}$, виявилися коефіцієнти $r_{ij}=\frac{1}{\sqrt[3]{(\gamma_{ij}-1)^2}},\gamma_{ij}>1;r_{ij}=1,\gamma_{ij}=1$.
*Примітка*. Мають місце нерівності:
$$-y_{ij}\le\frac{\omega_i}{\omega_j}-\gamma_{ij}\le y_{ij},\ y_{ij}\ge0,$$
звідки $-y_{ij}\omega_j\le\omega_i-\gamma_{ij}\omega_j\le y_{ij}\omega_j$;
$$-z_{ij}\le\omega_i-\gamma_{ij}\omega_j\le z_{ij},z_{ij}\ge0,$$
звідки$z_{ij}=y_{ij}\omega_j\Rightarrow z_{ij}\le y_{ij}\ (\forall\omega_j\le1)$.
Таким чином, якщо в розв'язку моделі (2.5) $\omega_j<<\omega_i$, то коефіцієнт $r_{ij}$ дозволяє величині $\left|\frac{\omega_i}{\omega_j}-\gamma_{ij}\right|$ не бути дуже малою.
