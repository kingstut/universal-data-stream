import json
import struct

SENSOR_MAPPING = {
    'accelerometer': 1,
    'temperature': 2,
    # ... add more as required
}

def encode_header(header):
    # Magic Number, Version
    binary_data = b'UDS' + struct.pack('>B', header['version'])

    # Encode variable-length strings with prefixed length
    for key in ['sensorName', 'sensorModel']:
        value = header[key].encode('ascii')
        binary_data += struct.pack('>H', len(value)) + value

    # Sensor Type, Data Unit, Frequency
    binary_data += struct.pack('>BHH', header['sensorType'], header['dataUnit'], header['frequency'])

    # Metadata (optional)
    metadata_str = ';'.join(f"{k}={v}" for k, v in header.get('metadata', {}).items())
    metadata = metadata_str.encode('ascii')
    binary_data += struct.pack('>H', len(metadata)) + metadata

    return binary_data

def encode_data(data, data_format):
    binary_data = struct.pack('>I', len(data))

    for record in data:
        timestamp = struct.pack('>Q', record['timestamp'])
        values = struct.pack(data_format, *record['values'])
        binary_data += timestamp + values

    return binary_data

def json_to_binary(json_file, binary_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    header = data['header']
    
    # Translate sensor name to code
    sensor_name = header.get('sensorName', '').lower()
    if sensor_name not in SENSOR_MAPPING:
        raise ValueError(f"Unsupported sensor name: {sensor_name}")
    sensor_code = SENSOR_MAPPING[sensor_name]
    header['sensorType'] = sensor_code

    # Define data format based on sensor type
    if header['sensorType'] == 1:  # Assuming '1' for Motion (3-axis accelerometer)
        data_format = '>fff'
    elif header['sensorType'] == 2:  # Placeholder for other sensor types
        data_format = '>f'
    else:
        raise ValueError("Unsupported sensor type.")

    # Encode header and data
    binary_data = encode_header(header) + encode_data(data['data'], data_format)

    # Write to binary file
    with open(binary_file, 'wb') as f:
        f.write(binary_data)

    print(f"Binary data written to {binary_file}")