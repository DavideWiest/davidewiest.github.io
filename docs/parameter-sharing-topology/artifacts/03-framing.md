# Framing

The article should read as an experiment that decides a topology question.

The old framing treated irregularity as the main object. The corrected evidence says the stronger result is simpler: at a fixed hard-sharing budget, the axis of sharing dominates the question. Width sharing wins. Maximum-distance depth-and-width sharing is useful evidence because it beats random, but it is not the best topology.

The central claim is transferable because the experiment is not a toy schedule probe. It uses a real Transformer, sufficient depth and width for specialization, a rich token-prediction task, and a multi-seed, parameter-matched comparison. Language modeling is the stress test for the architectural prior.

The article should not say that language modeling limits the result. It should say that a rich language-modeling setting makes the topology result meaningful. At the same time, the prose should report concrete facts rather than making a universal theorem out of one experiment.

The ending should connect the result to two broader families. CNNs share across repeated spatial positions. Structured matrices share and reuse parameters across width or channel axes. Both families fit the same design rule: share along axes where the same computation is naturally reusable, and preserve axes where position changes computational role.
