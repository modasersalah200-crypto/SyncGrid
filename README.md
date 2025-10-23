# 🌐 SyncGrid 

A real-time IoT monitoring pipeline for power grid simulation and visualization
<img width="1854" height="960" alt="Image" src="https://github.com/user-attachments/assets/8ebce91d-18a3-4e45-93dd-bed50e57feeb" />

## 📋 Overview

SyncGrid is a complete, real-time IoT monitoring pipeline designed to simulate and visualize power grid data. This project demonstrates the integration of modern IoT technologies to create a scalable, portable monitoring system for power grid health analysis.

## 🎯 Objectives & Goals

The main objective of this project is to build a comprehensive real-time IoT monitoring pipeline with the following key goals:

- **Simulate** a realistic power grid using the Pandapower library in Python
- **Transmit** data using the standard IoT messaging protocol (MQTT)
- **Collect and Parse** data using a robust agent (Telegraf)
- **Store** time-series data efficiently in a specialized database (InfluxDB)
- **Visualize** the grid's health on a live, auto-refreshing dashboard (Grafana)
- **Package** the entire system using Docker for full portability and ease of deployment


## 📁 Project Structure

```
syncgrid/
├── docker-compose.yml
├── device_simulator.py
├── Grafana_Dashboard.js
├── README.md
├── requirements.txt
└── telegraf.conf
```


## 🏗️ Architecture

The system follows a streamlined data pipeline:

```
  Publisher        Broker        Subscriber          time-seriesDB       Visualizer
┌──────────┐      ┌──────┐      ┌──────────┐         ┌──────────┐       ┌─────────┐
│  Python  │─────▶│ EMQX │─────▶│ Telegraf │────────▶│ InfluxDB │──────▶│ Grafana │
│Simulator │ MQTT │Broker│ MQTT │          │ struct  │          │ Query │         │
└──────────┘      └──────┘      └──────────┘ data    └──────────┘       └─────────┘
```

### Components

1. **Python (Data Producer)**
   - Generates power grid data using Pandapower
   - Publishes MQTT messages to the EMQX broker
   - Simulates realistic load variations over time

2. **EMQX (Message Broker)**
   - Acts as the central messaging hub
   - Receives data from the Python simulator
   - Routes messages to Telegraf

3. **Telegraf (Collector & Processor)**
   - Subscribes to MQTT topics
   - parses the incoming JSON messages into structured format
   - Writes processed data into InfluxDB

4. **InfluxDB (Time-Series Database)**
   - Stores structured time-series data from Telegraf
   - Optimized for high-throughput data ingestion
   - Provides efficient querying capabilities

5. **Grafana (Visualizer)**
   - Queries InfluxDB for stored data
   - Visualizes data as live graphs, charts, and maps
   - Auto-refreshing dashboard for real-time monitoring
   
  
   
### Data Pipeline Flow

- **Publish**: A Python simulator publishes sensor telemetry to the EMQX broker over MQTT.

- **Collect & Process**: Telegraf subscribes to the broker, consumes the messages, and parses the data into a structured format.

- **Store**: The processed time-series data is ingested and persistently stored in InfluxDB.

- **Visualize**: Grafana queries InfluxDB to display the data on real-time dashboards for monitoring and analysis.



## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

- [Docker](version 20.10)
- [Docker Compose](version 2.0)
- [Python](version 3.12)
- [Git](optional)

### Installation & Running

1. Clone the repository (or download and extract the ZIP file):

```bash
git clone https://github.com/yourusername/syncgrid.git
cd syncgrid
```

2. Create Virtual-Evironement

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Start the Docker containers:

```bash
docker-compose up -d
```

5. Run the Python data simulator:
```bash
python simulator.py
```
-----------------------------------------------------------------------------------------------------
Now the simulator will generate power grid data with varying loads to simulate real-world conditions.
-----------------------------------------------------------------------------------------------------

## 🔧 Configuration

### Accessing Services

After starting the services, access the web interfaces:

- **InfluxDB**: http://localhost:8086
  - Username: `admin`
  - Password: `password`

- **Grafana**: http://localhost:3000
  - Username: `admin`
  - Password: `password`
  
### Setting Up Grafana

1. **Connect to InfluxDB**
   - Log in to Grafana at http://localhost:3000
   - Navigate to Configuration → Data Sources
   - Add InfluxDB as a data source
   - Configure the connection with these settings:

```
Query Language: Flux
URL: http://influxdb:8086
Organization: my_iot_org
Token: my_super_secret_token
Default Bucket: iot_bucket
```

2. **Import Dashboard**
   - Go to Dashboards → Import
   - Copy the entire content from `Grafana_Dashboard.js`
   - Paste it into the import box
   - Click Import

3. **Activate Dashboard**
   - Hover over the dashboard and from the 3points select edit
   - click Refresh On the upper-right side or select Auto
   - The dashboard should now be active and displaying live data

## 📊 Features

- **Real-time Monitoring**: Live visualization of power grid metrics
- **Scalable Load Simulation**: Dynamic load variations to simulate realistic conditions
- **Time-Series Analysis**: Historical data storage and analysis capabilities
- **Auto-Refreshing Dashboard**: Continuously updated visualizations
- **Fully Dockerized**: Portable and easy to deploy on any system
- **Industry-Standard Protocols**: Uses MQTT for reliable IoT messaging

## 🛠️ Technology Stack

- **Python** - Data simulation and generation
- **Pandapower** - Power grid modeling
- **MQTT** - IoT messaging protocol
- **EMQX** - MQTT broker
- **Telegraf** - Data collection and processing
- **InfluxDB** - Time-series database
- **Grafana** - Data visualization
- **Docker** - Containerization and orchestration

## 🔍 Monitoring

Once everything is set up, you can:

- Monitor real-time power grid metrics on the Grafana dashboard
- Analyze historical trends using InfluxDB queries
- Observe load variations and grid health indicators
- Create custom visualizations and alerts

## 📝 Notes

- Ensure all Docker containers are running before starting the Python simulator
- The system automatically handles data flow from simulation to visualization
- Dashboard settings can be customized according to your monitoring needs
------------------------------------------------------------------------------------------
## Troubleshooting

### Services Not Starting

If Docker containers fail to start:

```bash
# Check container logs
docker-compose logs [service-name]

# Restart all services
docker-compose restart

# Stop and remove all containers, then start fresh
docker-compose down -v
docker-compose up -d
```

### No Data in InfluxDB

If data is not appearing in InfluxDB:

1. Check that the Python simulator is running
2. Verify EMQX is receiving messages:
   ```bash
   docker-compose logs emqx
   ```
3. Check Telegraf logs for parsing errors:
   ```bash
   docker-compose logs telegraf
   ```

### Grafana Cannot Connect to InfluxDB

If Grafana cannot connect to InfluxDB:

1. Verify the token is correct: `my_super_secret_token`
2. Check that InfluxDB container is healthy:
   ```bash
   docker-compose ps influxdb
   ```
3. Ensure you're using the container name `http://influxdb:8086` (not `localhost`)

### Port Conflicts

If you get port binding errors:

1. Check if ports 1883, 3000, or 8086 are already in use
2. Stop conflicting services or modify ports in `docker-compose.yml`
------------------------------------------------------------------------------------------

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Acknowledgments

- [Pandapower](https://www.pandapower.org/) - Power system analysis
- [EMQX](https://www.emqx.io/) - MQTT broker
- [InfluxData](https://www.influxdata.com/) - Time-series platform
- [Grafana Labs](https://grafana.com/) - Visualization platform

---
