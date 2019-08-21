if __name__ == "__main__":
    from sys import stdout
    from logging import StreamHandler, getLogger, DEBUG

    from datasetutils.datasets import MixInDataset
    from datasetutils.mutations import ResizeMutation
    from datasetutils.pasting import LeftCornerPaddingRule, RandomPaddingRule
    
    # logging routine, don't mind
    handler = StreamHandler(stdout)
    rootLogger = getLogger()
    rootLogger.addHandler(handler)
    rootLogger.setLevel(DEBUG)
    # ---------------------------

    dataset = MixInDataset('dummy-data', 'landscapes', 'figures', rootLogger)
    print(dataset)

    dataset \
        .add_mutation_to_mix_with(ResizeMutation((128, 128))) \
        .add_mutation_mixing(ResizeMutation((400, 400))) \
        .paste_as(RandomPaddingRule(400))

    for idx, img in enumerate(dataset.mix(4,1)):
        img.save(f'output/{idx}.png', format='png')
        # img.show('s')
