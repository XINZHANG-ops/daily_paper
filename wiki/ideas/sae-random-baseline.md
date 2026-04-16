---
title: "Random Decoder Matches Trained SAE"
slug: sae-random-baseline
source: note
last_updated: 2026-04-16
---

# Random Decoder Matches Trained SAE

## The Insight

Sparse Autoencoders (SAEs) trained to find interpretable features in LLM activations achieve nearly identical feature reconstruction quality with random weights as with trained weights. This raises a fundamental question: are SAEs discovering genuine causal features in the network, or are they finding arbitrary directions that happen to reconstruct well due to the decoder's expressive capacity?

## Evidence

- [Note 2026-02-19] — "Sanity Checks for Sparse Autoencoders" shows random decoder SAE matches trained decoder performance
- [[2604.02327]] — SteerViT demonstrates that frozen pretrained models have latent steerability; similarly, SAEs may reveal that LLM internals have far more structure than their training objectives exercise

## Implications

1. **Interpretability crisis**: If random weights work as well as trained ones, what does SAE analysis actually tell us about the network?
2. **Metrics are insufficient**: Reconstruction quality (how well the SAE output matches the original signal) doesn't validate that the SAE found meaningful features
3. **Compression vs interpretation**: An SAE decoder might be more like a compression scheme than an interpretability tool
4. **Need for better evaluation**: The field needs sanity checks that distinguish learned features from statistical artifacts

## Connections

- [[topics/representation-learning]] — SAEs claim to reveal representation structure; random baselines challenge this
- [[ideas/entropy-is-misleading]] — Both SAEs and entropy metrics can appear to work while missing the actual mechanism
