# Structure

1. Summary
   - State the conclusion first: parameter sharing is a topology choice, and the best tested topology shares across width.
   - Give the main scale and result numbers.

2. The topology question
   - Existing Transformer sharing work mostly asks how much to share across depth.
   - This experiment asks which positions should share a hard MLP block.

3. Experimental object
   - Define layer-by-chunk positions and the hard-sharing map.
   - Define the practical and parameter-matched baselines.

4. Candidate topologies
   - Explain depth, width, diagonal, random, max-distance, and searched random.
   - Introduce max-distance intuition early.

5. Experimental setup
   - State model, data, training, seeds, and search budget.
   - Emphasize that language modeling is the stress test, not a caveat.

6. Results
   - Show the main table and figures.
   - Separate observed facts from interpretation.

7. What cycle width sharing is
   - Give the exact schedule formula and plain-language explanation.

8. Interpretation
   - Different layers serve different purposes.
   - Width chunks are more exchangeable.
   - Max-distance confirms that distant depth sharing is better than random, but preserving depth is better.

9. Transfer to other architectures
   - Connect to CNNs and structured matrices.
   - State the design rule: share along repeated/exchangeable axes before ordered computational axes.

10. References
   - Include 12+ citations spanning Transformers, parameter sharing, data, CNNs, and structured matrices.
