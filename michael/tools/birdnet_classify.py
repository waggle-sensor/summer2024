# For classifying separated bird sources
# Requires python >= 3.9 and the birdnet package, which are NOT included by the Dockerfile.
# https://github.com/kahst/BirdNET

from pathlib import Path
from birdnet.models import ModelV2M4
import argparse


def main(path):
    # create model instance for v2.4
    model = ModelV2M4()

    # predict species within the whole audio file
    species_in_area = model.predict_species_at_location_and_time(42.5, -76.45, week=4)
    predictions = model.predict_species_within_audio_file(
    Path(path),
    filter_species=set(species_in_area.keys())
    )

    # get most probable prediction at time interval 0s-3s
    prediction, confidence = list(predictions[(0.0, 3.0)].items())[0]
    print(f"predicted '{prediction}' with a confidence of {confidence:.6f}")


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Path to target file')
    args = parser.parse_args()

    main(args.f)  
