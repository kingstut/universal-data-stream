import json
from pydub import AudioSegment
import numpy as np

def mp3_to_json(input_file, out_file):
    # Load the MP3
    song = AudioSegment.from_mp3(input_file)

    # Extract samples
    samples = np.array(song.get_array_of_samples())

    # Use the samples to populate our custom JSON structure
    data_entries = []

    for i, sample in enumerate(samples):
        data_entry = {
            "timestamp": i, 
            "values": [float(sample)]
        }
        data_entries.append(data_entry)

    # Create the JSON data structure
    data = {
        "header": {
            "format" : "UDS",
            "version": 1,
            "sensorName": "audio",
            "sensorModel": "MP3 Decompressed",
            "dataUnit": "amplitude",
            "frequency": song.frame_rate,
            "metadata": {
                "channels": song.channels,
                "bit_depth": song.sample_width * 8,
                "duration": len(song)
            }
        },
        "data": data_entries
    }

    # Save to a JSON file (before binary conversion)
    with open(out_file, "w") as f:
        json.dump(data, f, indent=4)

    print("Converted MP3 to JSON format.")
