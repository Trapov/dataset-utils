from PIL.Image import Image
from PIL import Image as ImageFactory

from random import randint
from typing import List

from os import walk
from os.path import join, exists

from logging import Logger

from mutations import MutationProcessor

class MixInDataset(object):

    def __init__(self, root: str, mixing : str, to_mix_with : str, logger : Logger = None):

        if not all([root, mixing, to_mix_with]):
            raise ValueError(f"Some of the arguments were set to null or empty (root, mixing, to_mix_with):{(root, mixing, to_mix_with)}. They all should be filled!")

        if not exists(root):
            raise ValueError(f"Directory {repr(root)} doesn't exist")
        
        mixing_path = join(root, mixing) 
        to_mix_with_path = join(root, to_mix_with)

        if not exists(mixing_path):
            raise ValueError(f"Directory {repr(mixing_path)} doesn't exist")

        if not exists(to_mix_with_path):
            raise ValueError(f"Directory {repr(to_mix_with_path)} doesn't exist")

        self.__mixing : List[Image] = list()
        self.__to_mix_with : List[Image] = list()
        self.__logger : Logger = logger
        self.__mixing_mutations : List[MutationProcessor] = list()
        self.__to_mix_with_mutations : List[MutationProcessor] = list()

        for path, _, files in walk(root):
            if path == mixing_path:
                self.__mixing.extend([ImageFactory.open(join(mixing_path, f)) for f in files])
            elif path == to_mix_with_path:
                self.__to_mix_with.extend([ImageFactory.open(join(to_mix_with_path, f)) for f in files])
    
        if len(self.__mixing) == 0 or len(self.__to_mix_with) == 0:
            raise ValueError(f'Mixing or to mix with collections were empty. Both catalogs {mixing_path}, {to_mix_with_path} should be filled')

    def mix(self, mixing_samples: int, to_mix_with_samples: int) -> List[Image]:
        mixed : List[Image] = list()
        for _ in range(mixing_samples):
            mixing_idx = randint(0, len(self.__mixing)-1)

            for _ in range(to_mix_with_samples):

                to_mix_with_idx = randint(0, len(self.__to_mix_with)-1)
                
                if self.__logger:
                    self.__logger.debug(f"Mixing '{self.__mixing[mixing_idx].filename}' with '{self.__to_mix_with[to_mix_with_idx].filename}'")
                
                to_mix_with_copied_image : Image = self.__to_mix_with[to_mix_with_idx]
                mixing_copied_image : Image = self.__mixing[mixing_idx]

                for mut in self.__to_mix_with_mutations:
                    to_mix_with_copied_image = mut.mutate(to_mix_with_copied_image)

                for mut in self.__mixing_mutations:
                    mixing_copied_image = mut.mutate(mixing_copied_image)

                mixing_copied_image.paste(to_mix_with_copied_image, (150, 150))
                mixed.append(mixing_copied_image)
        
        return mixed


    def add_mutation_mixing(self, mutation_processor : MutationProcessor) -> 'MixInDataset':
        self.__mixing_mutations.append(mutation_processor)
        return self

    def add_mutation_to_mix_with(self, mutation_processor : MutationProcessor) -> 'MixInDataset':
        self.__to_mix_with_mutations.append(mutation_processor)
        return self

    def __str__(self) -> str:
        return f'''
            Mixing [{len(self.__mixing)}] : {[f.filename.split('/')[-1:] for f in self.__mixing[:1]]} ... {[f.filename.split('/')[-1:] for f in self.__mixing[-1:]]}
            To mix with [{len(self.__to_mix_with)}] : {[f.filename.split('/')[-1:] for f in self.__to_mix_with[:1]]} ... {[f.filename.split('/')[-1:] for f in self.__to_mix_with[-1:]]}
        '''
    
if __name__ == "__main__":
    from sys import stdout
    from logging import StreamHandler, getLogger, DEBUG

    from mutations import ResizeMutation
    
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
        .add_mutation_mixing(ResizeMutation((400, 400)))

    for idx, img in enumerate(dataset.mix(4,1)):
        img.save(f'output/{idx}.png', format='png')
