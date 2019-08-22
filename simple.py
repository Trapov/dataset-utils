from sys import stdout
from logging import StreamHandler, getLogger, DEBUG

from PIL.ImageDraw import ImageDraw

from datasetutils.datasets import MixInDataset
from datasetutils.mutations import ResizeMutation
from datasetutils.pasting import LeftCornerPastingRule, RandomPastingRule

# logging routine, don't mind
handler = StreamHandler(stdout)
rootLogger = getLogger()
rootLogger.addHandler(handler)
rootLogger.setLevel(DEBUG)
# ---------------------------

dataset = \
    MixInDataset(root='dummy-data', mixing='landscapes',to_mix_with='figures', logger=rootLogger) \
        .add_mutation_mixing(ResizeMutation((250, 250))) \
        .add_mutation_to_mix_with(ResizeMutation((128, 128))) \
        .paste_as(RandomPastingRule(250))

for idx, (image, box) in enumerate(dataset.mix(2,2)):
    #img.save(f'output/{idx}.png', format='png')
    draw = ImageDraw(image)
    draw.rectangle([box.minx, box.miny, box.width+box.minx, box.height+box.miny], width=6, outline="red")

    image.show('s')
    image.save(f'output/{idx}.png', format='png')
    print(box)
