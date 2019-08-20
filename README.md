# dataset-utils

A simple util to make your dataset flexable.

# Requirements
- Python >3.6
- pillow 6.1.0

# How to

```python
    dataset = MixInDataset('dummy-data', 'landscapes', 'figures', rootLogger)

    dataset \
        .add_mutation_to_mix_with(ResizeMutation((128, 128))) \
        .add_mutation_mixing(ResizeMutation((400, 400)))

    for idx, img in enumerate(dataset.mix(4,1)):
        img.save(f'output/{idx}.png', format='png')

```

will yield to result in the `output` directory:

![output.png](output/0.png)