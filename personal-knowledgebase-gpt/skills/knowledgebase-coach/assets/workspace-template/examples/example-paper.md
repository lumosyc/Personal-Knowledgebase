---
title: "Denoising Diffusion Probabilistic Models"
type: paper
authors: [Jonathan Ho, Ajay Jain, Pieter Abbeel]
year: 2020
venue: NeurIPS 2020
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["raw/papers/Ho et al. - 2020 - Denoising Diffusion Probabilistic Models.pdf"]
questions: [Q2, Q4, Q5]
tags: [diffusion-models, score-matching, langevin-dynamics, variational-inference, lossy-compression]
domain: research
---

<!--
这是一个【格式示例】页（基于公开经典论文 DDPM），展示 paper 页应该长什么样。
真正使用时，由 Codex 按 templates/research/paper.md 自动生成到 wiki/papers/。
frontmatter 里的 `questions: [Q2, Q4, Q5]` 指向你在 meta/core_questions.md 定义的 driving questions 编号。
正文里的 [[...]] 是 Obsidian wikilink，指向你自己的 concept / paper 页。
-->

## Core Contribution
首次证明 diffusion probabilistic models 能生成高质量样本（CIFAR10 FID 3.17, IS 9.46），并建立了 **diffusion models、denoising score matching、annealed Langevin dynamics 三者之间的等价性**。作者认为这个等价性是论文的 primary contribution。

## Reading Mission

- **Role**: ingredient
- **Target Level**: L2
- **Main Question**: ε-prediction 参数化为什么等价于 score matching？VLB 分解如何导出 simplified loss？

## Paper Spine

1. **Problem**: 如何用 diffusion probabilistic model 生成高质量图像？以往方法质量远不如 GAN。
2. **Gap**: VLB 的 weighted 形式对 sample quality 并非最优；如何参数化 reverse process 是关键。
3. **Idea**: ε-prediction 参数化——让网络预测加入的噪声而非均值，简化 VLB 为均匀权重。
4. **Method**: Forward Markov chain 加高斯噪声 → 训练 U-Net 预测 ε → reverse 用 learned score 采样；$L_\text{simple}$ 去掉权重项。
5. **Result**: CIFAR-10 FID 3.17（超越当时所有 unconditional 模型）；证明 DDPM = DSM = annealed Langevin 等价。

## Key Claims

- **三者等价**：ε-prediction ≡ denoising score matching ≡ annealed Langevin dynamics（Eq. 12）。（theory-supported）
- **Simplified loss 更优**：去掉 VLB 权重项（下权 small-$t$ 细节，让网络专注 large-$t$ 大尺度结构）比加权 VLB 生成质量更好。（experiment-supported）
- **Progressive generation**：reverse process 先生成 large-scale 结构，后填充 fine details——中间 latent 编码语义内容。（experiment-supported）

## Method

### Forward Process
固定 Markov chain，variance schedule $\beta_1 = 10^{-4}$ 到 $\beta_T = 0.02$ 线性递增，$T = 1000$。
$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\sqrt{1-\beta_t}\,\mathbf{x}_{t-1},\; \beta_t\mathbf{I})$$

Nice property（闭式采样）：$q(\mathbf{x}_t|\mathbf{x}_0) = \mathcal{N}(\sqrt{\bar\alpha_t}\,\mathbf{x}_0, (1-\bar\alpha_t)\mathbf{I})$

### VLB 分解
$$L = \underbrace{D_{\mathrm{KL}}(q(\mathbf{x}_T|\mathbf{x}_0) \| p(\mathbf{x}_T))}_{L_T} + \sum_{t>1} \underbrace{D_{\mathrm{KL}}(q(\mathbf{x}_{t-1}|\mathbf{x}_t, \mathbf{x}_0) \| p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t))}_{L_{t-1}} - \underbrace{\log p_\theta(\mathbf{x}_0|\mathbf{x}_1)}_{L_0}$$

关键：conditioned on $\mathbf{x}_0$ 后，posterior $q(\mathbf{x}_{t-1}|\mathbf{x}_t, \mathbf{x}_0)$ 是 tractable Gaussian，均值为：
$$\tilde\mu_t(\mathbf{x}_t, \mathbf{x}_0) = \frac{\sqrt{\bar\alpha_{t-1}}\beta_t}{1-\bar\alpha_t}\mathbf{x}_0 + \frac{\sqrt{\alpha_t}(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}\mathbf{x}_t$$

### ε-Prediction 参数化（核心推导）
将 $\mathbf{x}_0 = (\mathbf{x}_t - \sqrt{1-\bar\alpha_t}\,\epsilon) / \sqrt{\bar\alpha_t}$ 代入 $\tilde\mu_t$，模型预测 $\epsilon$：

$$\mu_\theta(\mathbf{x}_t, t) = \frac{1}{\sqrt{\alpha_t}}\left(\mathbf{x}_t - \frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(\mathbf{x}_t, t)\right)$$

采样步骤：
$$\mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}}\left(\mathbf{x}_t - \frac{1-\alpha_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(\mathbf{x}_t, t)\right) + \sigma_t \mathbf{z}$$

这就是 Langevin dynamics：$\epsilon_\theta$ 扮演 learned score function，$\sigma_t \mathbf{z}$ 是 stochastic noise 项。

### Simplified Loss
$$L_{\text{simple}} = \mathbb{E}_{t, \mathbf{x}_0, \epsilon}\left[\|\epsilon - \epsilon_\theta(\sqrt{\bar\alpha_t}\mathbf{x}_0 + \sqrt{1-\bar\alpha_t}\epsilon,\; t)\|^2\right]$$

## Evidence

| Dataset | FID | IS | NLL (bits/dim) |
|---|---|---|---|
| CIFAR10 (unconditional) | **3.17** | 9.46 | $\leq 3.75$ |
| LSUN Bedroom 256² | 4.90 | — | — |

- FID 3.17 超过所有 unconditional 模型（包括 conditional BigGAN 14.73）
- NLL 不 competitive（vs Sparse Transformer 2.80），但样本质量远优于 likelihood-based models
- Rate-distortion 分析：1.78 bits/dim rate + 1.97 bits/dim distortion，超过半数 lossless codelength 用于 imperceptible distortions
- Ablation (Table 2)：预测 ε 在 $L_\text{simple}$ 下最优；学习 $\Sigma$ 导致训练不稳定

## Assumptions

- $\beta_t$ 足够小，使 $q(\mathbf{x}_T|\mathbf{x}_0) \approx \mathcal{N}(0, \mathbf{I})$（$D_{\mathrm{KL}} \approx 10^{-5}$ bits/dim），且 forward/reverse 有相同函数形式
- Variance $\Sigma_\theta = \sigma_t^2 \mathbf{I}$ 可以固定（不需要学）——实验证明学 $\Sigma$ 不稳定
- $T=1000$ 步的离散化足够精细（后来 Song et al. 2021 给出连续时间极限）

## Limitations

- NLL 不 competitive：diffusion 有 inductive bias 偏向 perceptual quality 而非 likelihood
- 采样需要 $T=1000$ 步，极慢（后续 DDIM、progressive distillation 解决）
- $\beta_t$ schedule 和 $T$ 的选择是 ad-hoc 的，缺乏理论指导

## Connections

- [[diffusion-models]]: DDPM 是 diffusion 生成模型的奠基工作
- [[score-function]]: 论文证明 ε-prediction ≡ denoising score matching，建立了 denoising 和 score-based 两条路线的等价
- [[langevin-dynamics]]: Algorithm 2 的采样过程就是 learned annealed Langevin dynamics

## Questions Raised

- 为什么 simplified loss 的 reweighting 反而更好？暗示 VLB 中不同 $t$ 的 KL 项对 sample quality 重要性不同——可能与人类视觉系统的 perceptual sensitivity 有关，或与 score estimation variance 在不同噪声尺度下的行为有关
- $\beta_t$ schedule 的最优选择是否有理论依据？→ Song et al. 2021 给出连续时间极限，但最优 schedule 问题仍开放

## Raw Source
- [[raw/papers/Ho et al. - 2020 - Denoising Diffusion Probabilistic Models.pdf]]
