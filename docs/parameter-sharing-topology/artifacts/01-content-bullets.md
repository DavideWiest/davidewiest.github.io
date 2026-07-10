# Content bullets

- The article replaces the earlier irregular-parameter-sharing post.
- The corrected claim is not that irregular sharing is best. The corrected claim is that topology determines whether hard parameter sharing helps, and that sharing across width is the best tested topology.
- The practical baseline is the ordinary unshared Transformer MLP. The same-parameter baseline is balanced random hard sharing, averaged over three independently sampled balanced layouts.
- All hard-sharing variants use 128 exact MLP blocks for 256 layer-by-chunk MLP positions. Each shared block is used exactly twice. The MLP-bank parameter count is therefore 67,108,864 for every shared variant, compared with 134,217,728 for the unshared dense MLP.
- The experiment uses a 16-layer, width-1024, 16-head Transformer LM, sequence length 256, 100M GPT-2-tokenized OpenWebText training tokens, 2M validation tokens, 5,000 final training steps, and three seeds.
- The tested topologies are sequence depth, cycle depth, sequence width, cycle width, diagonal depth-width, balanced random, maximum-depth-distance, and best-of-12 random.
- The search budget for the searched random topology is best of 12 balanced random layouts, each trained for 800 proxy steps.
- The best result is cycle width sharing, 4.5043 +/- 0.0537 validation CE.
- Maximum-depth-distance sharing is also strong, 4.5279 +/- 0.0243, and beats balanced random by 0.0366 CE. It does not beat cycle width sharing.
- The best-of-12 random topology does not transfer from proxy search to the final run, 4.6057 +/- 0.0523.
- The interpretation is topological: depth positions serve different roles, while width chunks inside the MLP are more redundant and exchangeable. Sharing across width is therefore more tolerable than sharing across depth.
- The result connects to CNNs because CNNs succeed by sharing along a repeated spatial axis. It also connects to butterfly, Monarch, tensor-train, and other structured matrices because these methods reuse parameters along width/channel axes.
