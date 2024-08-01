# for chirp, you will need to clone https://github.com/google-research/perch first.
from chirp.data.tfds_builder import WavDirectoryBuilder
import tensorflow_datasets as tfds


class MortonArboretum(WavDirectoryBuilder):
    VERSION = tfds.core.Version('1.0.0')
    RELEASE_NOTES = {
        '1.0.0': 'Initial release.',
    }

    def _description(self) -> str:
        return "lorem ipsum"

    def _citation(self) -> str:
        return """lorem ipsum"""
