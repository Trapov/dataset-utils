# dataset-utils

A simple util to make your dataset flexable.

# Requirements
- Python >3.6
- pillow 6.1.0

# How to

```python

from PIL.ImageDraw import ImageDraw

from datasetutils.datasets import MixInDataset
from datasetutils.mutations import ResizeMutation
from datasetutils.pasting import LeftCornerPastingRule, RandomPastingRule

dataset = \
    MixInDataset(root='dummy-data', mixing='landscapes',to_mix_with='figures', logger=rootLogger) \
        .add_mutation_mixing(ResizeMutation((250, 250))) \
        .add_mutation_to_mix_with(ResizeMutation((128, 128))) \
        .paste_as(RandomPastingRule(250))

for idx, (image, box) in enumerate(dataset.mix(2,2)):
    draw = ImageDraw(image)
    draw.rectangle([box.minx, box.miny, box.width+box.minx, box.height+box.miny], width=6, outline="red")

    image.show('s')
    image.save(f'output/{idx}.png', format='png')
```

will yield to result in the `output` directory:

![output.png](output/0.png) ![output.png](output/1.png) ![output.png](output/2.png)