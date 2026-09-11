$p=\begin{pmatrix}p_1\\p_2\\\vdots\\p_n\end{pmatrix}$ – вектор цін продуктів, що задає загальний виробник.

$\omega=\begin{pmatrix}\omega_1\\\vdots\\\omega_m\end{pmatrix}$ – вектор цін факторів ($\omega_i$ – ціна одиниці $i$-того фактору).

У векторній формі: $x=\Phi(p,\omega)$ // теж саме що (1.58)
Властивості, яким задовольняє функція $\Phi_i(p,\omega)$:
1) функція неперервна;
2) для будь-яких напівдодатних векторів $p$ і $\omega$ вектор $x$ завжди напівдодатний;
3) $\underbrace{p^Tx}_{\substack{\text{вартість,за}\\\text{яку}\\\text{хоче}\\\text{отримати}\\\text{виробник}}}=\underbrace{\omega^Tv_0}_{\substack{\text{вартість,заяку}\\\text{хоче}\\\text{придбати}\\\text{споживач}}}$
4) $X(p)$ є опуклий компакт, якщо $W$ є опуклий ком пакт: $X(P)=\Phi(P,W)$.
*Примітка*. $X(p)$ складається з усіх можливих векторів $x=\Phi(p,\omega),\forall\omega\in W$
$X(p)=\Phi(P,W)$.
5) $\Phi_i(p,\omega)$ – однорідна функція, нульового степеня: $\Phi_i(p,\omega)=\Phi_i(tp,t\omega)\forall t>0\Rightarrow X(tP,tW=\Phi(P,W))$.

Метою дослідження не є стратегія знаходження вектора цін $p$ і вектора цін $\omega$, що є оптимальними в певному сенсі для користувача і виробника, а дослідження існування в цій моделі ситуації ринкової рівноваги.
Таким чином, треба показати, чи існує в цій моделі ситуація ринкової рівноваги, тобто
$$\exists x^*,y^*,p^*,\omega^*\ z^*=x^*-y^*\left.\begin{matrix}\\\end{matrix}\right\}\text{першаполовина}$$
$$p^{*T}z^*=0\ z_j^*\le0,j=\overline{1,n}$$
$$u^*=Ay^*-v_0\left.\begin{matrix}\\\end{matrix}\right\}\text{другаполовина}$$
$$\omega^{*T}u^*=0\ u_i^*\le0,i=\overline{1,m}$$

Запишемо пряму та двійчату задачі лінійного програмування:
$$\max_yp^Ty$$
$$Ay\le v_0\qquad(1.59)$$
$$y_j\ge0\qquad j=\overline{1,n}$$
і
$$\min_\omega v_0^T\omega$$
$$\omega^TA\ge p^T\qquad(1.60)$$
$$\omega_i\ge0\quad i=\overline{1,m}$$
