$${}^{max}_{min}f(x)$$
$$g(x)=0$$
де $f(x)=\sum_{i=1}^{n}a_ix_i$ – лінійна функція, $g(x)$ – нелінійне обмеження.
Матриця $\hat{L}$ має вигляд:
$$\hat{L}=\begin{pmatrix}0&g_1&g_2&\cdots&g_n\\g_1&&&&\\g_2&&&-\lambda^*g_{ij}&\\\vdots&&&&\\g_n&&&&\end{pmatrix}\leftarrow G[n\times1]$$
$$\uparrow$$
$$G^T$$
$$g_i=\left.\frac{\partial g(x)}{\partial x_i}\right|_{x=x^*}$$
$$g_i=\left.\frac{\partial g(x)}{\partial x_i\partial x_j}\right|_{x=x^*}$$
$L=f(x)-\lambda g(x)(m=1)$.
*Примітка*. В усіх задачах математичної економіки множники Лагранжа завжди $>0$.
Введемо $k=-\frac{1}{\lambda^*}$. І введемо дві матриці:
$$L^*=\begin{pmatrix}0&kg_1&kg_2&\cdots&kg_n\\kg_1&&&&\\kg_2&&&g_{ij}&\\\vdots&&&&\\kg_n&&&&\end{pmatrix}\quad\text{і}\quad G=\begin{pmatrix}0&g_1&g_2&\cdots&g_n\\g_1&&&&\\g_2&&&g_{ij}&\\\vdots&&&&\\g_n&&&&\end{pmatrix}.$$

**Означення 1.13**. Матриця $G$ – обрамлена матриця Гесса функції $g(x)$.

Має місце наступна рівність:
$$\overline{\det L}=(-\lambda)^{n+1}\det L^*=(-\lambda^*)^{n+1}k^2\det G.$$
І еквівалентна рівність:
$$\overline{\det L_s}=(-\lambda^*)^sk^2\det G_s.$$
$\hat{L}_s$ і $G_s$ – матриці, отримані з $\hat{L}$ і $G$ шляхом викреслення відповідної кількості їх останніх рядків і стовпців ($s$ – розмірність).
Якщо $x^*$ є мінімум функції $f(x)$ на одному нелінійному обмеженні, а детермінанти перших $n-m$ мінорів матриці $G$ не нулі, то необхідною умовою є чергування знаків цих детермінантів.
