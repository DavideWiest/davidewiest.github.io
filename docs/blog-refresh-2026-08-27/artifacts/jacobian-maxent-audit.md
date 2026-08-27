# Why the Jacobian/max-entropy post was not published

For a representation $h=f_\theta(x)$, downstream map $z=F(h)$, and loss $\ell(z)$, the local parameter gradient is

\[
\nabla_\theta\ell
=
\left(\frac{\partial h}{\partial\theta}\right)^\top
\left(\frac{\partial F}{\partial h}\right)^\top
\nabla_z\ell.
\]

Write the missing representation-space teaching signal as $v=J^\top\nabla_z\ell$. If the downstream is unknown and the prior over its orientation is rotation-symmetric, then $\mathbb E[v]=0$. Under squared-error risk, the Bayes-optimal estimate of $v$ is therefore zero. Neither whitening nor a maximum-entropy representation objective follows.

A separate valid statement is available. If a future task is restricted to a linear readout and representation covariance $\Sigma$ has fixed trace, minimizing worst-direction estimation variance gives

\[
\max_{\Sigma\succeq0,\ \operatorname{tr}\Sigma=B}
\lambda_{\min}(\Sigma),
\]

whose solution is $\Sigma=(B/d)I$. The same covariance maximizes Gaussian entropy under the trace constraint. This is the standard minimax-conditioning/whitening argument; it concerns future linear readouts, not the unknown Jacobian-induced parameter update above. Conflating the two would turn an analogy into a derivation.

Maximum-entropy regularization can still accompany invariance or predictive objectives in self-supervised learning, and local objectives can still suit greedy training. Those observations do not establish the proposed forward-Jacobian $\rightarrow$ minimum-risk $\rightarrow$ max-entropy chain.
