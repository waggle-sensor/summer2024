import tensorflow_datasets as tfds
from morton_arboretum import MortonArboretum


tfds.builder_cls('morton_arboretum')(data_dir='/home/msz/tensorflow_datasets/downloads/manual/morton_arboretum')

print("Registered datasets:")
print(tfds.list_builders())

try:
    dataset = tfds.load('morton_arboretum', split='train')
    print("Dataset loaded successfully")
except Exception as e:
    print(f"Error loading dataset: {e}")
