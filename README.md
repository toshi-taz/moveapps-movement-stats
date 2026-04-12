# Wildlife Movement Statistics

MoveApps Python App  
Github repository: github.com/toshi-taz/moveapps-movement-stats

## Description
Calculates movement statistics per individual from animal tracking data. Outputs a CSV summary and a bar chart of total distance traveled per individual.

## Documentation

### Application scope
#### Generality of App usability
This App was developed for any taxonomic group with GPS tracking data.

#### Required data properties
The App should work for any kind of location data with a minimum of 2 fixes per individual.

### Input type
`MovingPandas.TrajectoryCollection`

### Output type
`MovingPandas.TrajectoryCollection`

### Artifacts
- `movement_stats.csv` — summary table with records, total distance, and time range per individual
- `distance_plot.png` — bar chart of total distance per individual

### Parameters
None required.

## Author
Alexander Toshiro Bataz López  
Ingeniería en Sistemas Energéticos y Redes Inteligentes — UPIEM–IPN  
Conservation Technology | Wildlife Telemetry | IoT Sensor Networks
