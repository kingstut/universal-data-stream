# universal data stream
 file format for sensor datastreams

# Introduction
The Universal Data Stream (UDS) format aims to provide a standardized file format for streaming and storing data from various sensors. It offers flexibility for multiple sensor types and ensures consistency for software that processes sensor data.

# File Structure Overview
A .uds file is structured in JSON and comprises three main sections:
- Header: Contains metadata about the data stream.
- Data: Holds the actual sensor data points.
- Footer: Optional section, primarily for integrity checks and annotations.

# Detailed Specification
## 1. Header
The header provides metadata for the sensor data stream:
- format: Always set to "UDS" to identify this file format.
- version: Specifies the version of the UDS format.
- sensorName: Descriptive name of the sensor.
- sensorModel: Model or part number.
- sensorType: General category of the sensor (e.g., Temperature).
- dataUnit: Measurement units of the recorded data (int).
- frequency: Data recording rate (int).
- metadata: Additional optional details.

## 2. Data
This section is an array of data points:
- timestamp: The time when the data point was recorded (UNIX format).
- values: Sensor values, either a single value or an array for multi-dimensional sensors.

## 3 Footer
(Optional)
- checksum: A computed value for data integrity checks.
- annotations: Any additional notes about the data stream.

# UDS binary format 

Format (4 bytes): A unique identifier for the UDS format, e.g., UDS.
Version (1 byte): Format version.
Sensor Name Length (1 byte): Length of the subsequent sensor name.
Sensor Name (variable): ASCII encoded name of the sensor.
Sensor Model Length (1 byte): Length of the subsequent sensor model.
Sensor Model (variable): ASCII encoded model of the sensor.
Sensor Type (1 byte): A byte representing the type of sensor, e.g., 0x01 for Motion.
Data Unit (2 bytes): Representing the measurement units, e.g., 0x0101 for m/s^2.
Frequency (2 bytes): Data recording rate in Hz.
Metadata Length (2 bytes): Length of the subsequent metadata section.
Metadata (variable): Additional metadata.

Number of Records (4 bytes): An integer indicating how many data records follow.
Records (variable): Each record consists of:
Timestamp (8 bytes): UNIX timestamp.
Value(s) (variable): Depending on the sensor. E.g., 3x 4-byte floats for a 3-axis accelerometer.

Checksum (4 bytes): A CRC32 or similar checksum for data integrity.
Annotations Length (2 bytes): Length of the subsequent annotations.
Annotations (variable): ASCII encoded annotations.


# Create binary file for json
json_to_binary('example.json', 'example.uds')