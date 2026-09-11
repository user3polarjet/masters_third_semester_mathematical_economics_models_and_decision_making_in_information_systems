$$
\pi_B=16P_AL_A^{0.5}+40P_BL_B^{0.25}-rL_B.
$$

Максимум прибутку фірми B:

$$
\frac{\partial\pi_B}{\partial L_B}
=\frac{40\cdot0.25\cdot P_B}{L_B^{0.75}}-r=0
\quad\Rightarrow\quad
L_B^D=\left(\frac{10P_B}{r}\right)^{4/3}.
$$

Тепер прибуток фірм можна подати функціями від цін:

$$
\pi_A=16P_A\left(\frac{8P_A}{r}\right)^{0.5}-r\left(\frac{8P_A}{r}\right)^2
=\frac{128P_A^2}{r}-\frac{64P_A^2}{r}
=\frac{64P_A^2}{r};
$$

$$
\begin{aligned}
\pi_B&=40P_B\left(\frac{10P_B}{r}\right)^{1/3}
-r\left(\frac{10P_B}{r}\right)^{4/3}\\
&=\frac{86.177P_B^{4/3}}{r^{1/3}}
-\frac{21.544P_B^{4/3}}{r^{1/3}}
=\frac{64.633P_B^{4/3}}{r^{1/3}}.
\end{aligned}
$$

Підставивши функції попиту на працю у виробничі функції, отримаємо функції пропозиції благ:

$$
Q_A^S=16L_A^{0.5}
=16\left(\frac{8P_A}{r}\right)^{2\cdot0.5}
=16\cdot\frac{8P_A}{r}
=128\frac{P_A}{r};
$$

$$
Q_B^S=40L_B^{0.25}
=40\left(\frac{10P_B}{r}\right)^{(4/3)\cdot(1/4)}
=40\left(\frac{10P_B}{r}\right)^{1/3}
=86.177\left(\frac{P_B}{r}\right)^{1/3}.
$$

Поведінка споживачів на кожному з ринків визначається їх бажанням максимізувати свою функцію корисності при заданих бюджетних обмеженнях. Перед 1-м споживачем стоїть задача максимізувати функцію Лагранжа $\Phi_1$:

$$
\Phi_1=(Q_{A1}-10)^{0.5}(Q_{B1}-6)^{0.3}(16-L_A)^{0.2}
+\lambda(P_AQ_{A1}+P_BQ_{B1}-\pi_A-rL_A).
$$

Необхідні умови:

$$
\frac{\partial\Phi_1}{\partial Q_{A1}}
=\frac{(Q_{B1}-6)^{0.3}(16-L_A)^{0.2}}{2(Q_{A1}-10)^{0.5}}+\lambda P_A=0;
$$

$$
\frac{\partial\Phi_1}{\partial Q_{B1}}
=\frac{3(Q_{A1}-10)^{0.5}(16-L_A)^{0.2}}{10(Q_{B1}-6)^{0.7}}+\lambda P_B=0;
$$

$$
\frac{\partial\Phi_1}{\partial L_A}
=\frac{(Q_{A1}-10)^{0.5}(Q_{B1}-6)^{0.3}}{5(16-L_A)^{0.8}}+\lambda r=0;
$$

$$
\frac{\partial\Phi_1}{\partial\lambda}
=P_AQ_{A1}+P_BQ_{B1}-\pi_A-rL_A=0.
$$

Звідси:

$$
Q_{B1}=\frac{3(Q_{A1}-10)P_A}{5P_B}+6.
$$
