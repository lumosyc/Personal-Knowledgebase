---
title: "Score Function"
type: concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["raw/clips/What-are-Diffusion-Models.md", "raw/papers/Ho et al. - 2020 - Denoising Diffusion Probabilistic Models.pdf", "raw/papers/Song and Ermon - 2020 - Generative Modeling by Estimating Gradients of the Data Distribution.pdf", "raw/papers/Song et al. - 2021 - Score-Based Generative Modeling through Stochastic Differential Equations.pdf"]
questions: [Q2, Q4, Q5]
tags: [score-matching, energy-based-models, generative-modeling, gradient-field]
---

<!--
这是一个【格式示例】页（通用概念 score function），展示 concept 页应该长什么样。
真正使用时，由 Codex 按 templates/research/concept.md 自动生成到 wiki/concepts/。
-->

## Definition
Score function 是概率密度 $p(\mathbf{x})$ 的对数梯度：
$$s(\mathbf{x}) = \nabla_{\mathbf{x}} \log p(\mathbf{x})$$

它是一个**向量场**，指向概率密度增长最快的方向。关键性质：score 不依赖配分函数（partition function），因为 $\nabla_{\mathbf{x}} \log \frac{p^*(\mathbf{x})}{Z} = \nabla_{\mathbf{x}} \log p^*(\mathbf{x})$，$Z$ 的梯度为零。这使得 score 可以绕过 intractable 的归一化常数直接估计。

## Key Ideas

### Score 即能量的负梯度
对于 energy-based model $p(\mathbf{x}) = \frac{1}{Z} e^{-E(\mathbf{x})}$：
$$s(\mathbf{x}) = \nabla_{\mathbf{x}} \log p(\mathbf{x}) = -\nabla_{\mathbf{x}} E(\mathbf{x})$$

**Score function 就是能量景观的负梯度场。** 这直接连接到"学习规则能否从能量最小化中涌现"这一核心问题：如果我们能估计 score，就等价于知道了能量的梯度，可以做 gradient descent on energy landscape 进行采样或学习。

### Score Matching
直接估计 score 的方法（Hyvärinen 2005）。训练目标：
$$\mathbb{E}_{p(\mathbf{x})} \left[\frac{1}{2}\|s_\theta(\mathbf{x}) - \nabla_{\mathbf{x}} \log p(\mathbf{x})\|^2\right]$$

可以展开为只依赖 $s_\theta$ 的形式（不需要知道真实 score），有两个可行变体：
- **Denoising score matching**（Vincent 2011）：给数据加噪，估计噪声数据的 score
- **Sliced score matching**（Song et al. 2019）：随机投影降低计算成本

### 多尺度噪声扰动（NCSN, Song & Ermon 2019）
Naive score matching 面临两个根本困难：

1. **Manifold hypothesis**：真实数据集中在低维流形上，ambient space 大部分区域 $p(\mathbf{x}) \approx 0$，score undefined（$\log 0$ 无梯度）。实验验证：CIFAR-10 上不加噪声的 sliced score matching loss 不收敛；加 $\mathcal{N}(0, 10^{-4})$ 后收敛。
2. **Slow mixing**：modes 间低密度区导致 Langevin dynamics 混合慢。关键分析：在各 mode 的 support 内 $\nabla_{\mathbf{x}} \log p_{\text{data}} = \nabla_{\mathbf{x}} \log p_k$，**不依赖 mixing weight $\pi$**，因此 Langevin 采不到正确的 mode 比例。

Song & Ermon 2019 的解决方案：用 $L$ 个递增噪声尺度 $\{\sigma_i\}_{i=1}^L$（几何级数）扰动数据，训练一个 noise-conditioned score network $\mathbf{s}_\theta(\mathbf{x}, \sigma)$ 联合估计所有尺度的 score。训练目标（denoising score matching）：
$$\ell(\theta; \sigma) = \frac{1}{2}\mathbb{E}\left[\left\|\mathbf{s}_\theta(\tilde{\mathbf{x}}, \sigma) + \frac{\tilde{\mathbf{x}} - \mathbf{x}}{\sigma^2}\right\|^2\right], \quad \mathcal{L} = \frac{1}{L}\sum_i \sigma_i^2 \cdot \ell(\theta; \sigma_i)$$

权重 $\lambda(\sigma) = \sigma^2$ 的选择使各尺度的 loss 贡献量级相同（因为 $\|\mathbf{s}_\theta\| \propto 1/\sigma$）。

大噪声填平 modes 间的低密度谷（解决 mixing），高斯噪声使 support 覆盖全空间（解决 manifold）。这个多尺度噪声 schedule 直接对应 diffusion 的 forward process。

### 与 Diffusion 的等价（Ho et al. 2020, Eq. 12）
在 DDPM 中，给定 $q(\mathbf{x}_t|\mathbf{x}_0) = \mathcal{N}(\sqrt{\bar\alpha_t}\mathbf{x}_0, (1-\bar\alpha_t)\mathbf{I})$：
$$\nabla_{\mathbf{x}_t} \log q(\mathbf{x}_t | \mathbf{x}_0) = -\frac{\epsilon}{\sqrt{1-\bar\alpha_t}}$$

因此 DDPM 的 $\epsilon$-prediction 等价于 score estimation（差一个已知的 scaling factor）。

Ho et al. 2020 进一步证明 DDPM 的 VLB 中 $L_{t-1}$ 项展开后（Eq. 12）：
$$L_{t-1} \propto \mathbb{E}\left[\frac{\beta_t^2}{2\sigma_t^2\alpha_t(1-\bar\alpha_t)}\|\epsilon - \epsilon_\theta(\mathbf{x}_t, t)\|^2\right]$$
这**就是** denoising score matching over multiple noise scales，权重 $\frac{\beta_t^2}{2\sigma_t^2\alpha_t(1-\bar\alpha_t)}$ 对应不同尺度的 reweighting。Simplified loss $L_\text{simple}$ 去掉此权重，下权 small-$t$（near-imperceptible），让网络专注大尺度结构。

### Score 作为 SDE 框架的唯一 Learned Object（Song et al. 2021）
在 SDE 统一框架中，score function 的地位进一步提升：reverse SDE 和 probability flow ODE 都**只依赖** time-dependent score $\nabla_{\mathbf{x}} \log p_t(\mathbf{x})$。一旦 score 估出：
- Reverse SDE → stochastic 采样
- Probability flow ODE → deterministic 采样 + exact likelihood + invertible encoding

连续时间 score matching 目标统一了 NCSN 的 $\sigma^2$-weighted loss 和 DDPM 的 $(1-\alpha_t)$-weighted loss——二者是同一个 $\lambda(t)$ 的不同离散化。

## Connections
- [[diffusion-models]]: score function 是 diffusion models 的核心数学对象
- [[langevin-dynamics]]: 给定 score 即可用 Langevin dynamics 采样——score 是从密度到采样的桥梁
- [[Song2021-sde]]: SDE 框架中 score 是唯一 learned object；probability flow ODE 提供 exact likelihood

## Open Questions
- Score function 作为向量场的几何性质（曲率、奇点）与生成质量有什么关系？（几何视角）
- 在 Hopfield network / modern Hopfield model 中，energy 的梯度 = attention update rule。能否把 attention 理解为一种 score-based 的 iterative refinement？（能量 / 变分视角）
- Score matching 的 denoising 变体与 denoising autoencoder (DAE) 的关系：Vincent 2011 已经证明二者等价。这暗示表征学习和密度估计可能共享更深的数学结构。
