# Draft notes

- Avoid resurrecting the failed article's "irregular sharing wins" claim.
- Avoid saying the unshared dense model is parameter-matched. It is the practical baseline.
- Say explicitly that all shared variants are parameter-matched.
- Say explicitly that balanced random uses a fresh balanced random layout for each final seed, then the reported number is the mean over those three sampled layouts.
- Say explicitly that best-of-12 random uses 12 proxy layouts, 800 steps each, then retrains the selected layout for final seeds.
- Do not overinterpret cycle versus sequence within width. Chunk order is artificial. The stable conclusion is axis selection: width sharing is better than depth sharing.
- Keep the phrase "hard sharing" visible. The experiment is not a soft shared-basis or tensorized-coefficient experiment.
- Use "validation cross-entropy" and "CE" consistently.
- Use the figure captions to explain what lower means and what the error bars mean.
