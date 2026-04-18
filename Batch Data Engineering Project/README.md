# Mandera Analytics Pipeline

```
███╗░░░███╗░█████╗░███╗░░██╗██████╗░███████╗██████╗░░█████╗░
████╗░████║██╔══██╗████╗░██║██╔══██╗██╔════╝██╔══██╗██╔══██╗
██╔████╔██║███████║██╔██╗██║██║░░██║█████╗░░██████╔╝███████║
██║╚██╔╝██║██╔══██║██║╚████║██║░░██║██╔══╝░░██╔══██╗██╔══██║
██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝███████╗██║░░██║██║░░██║
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝

░█████╗░███╗░░██╗░█████╗░██╗░░░░░██╗░░░██╗████████╗██╗░█████╗░██████╗░░██████╗
██╔══██╗████╗░██║██╔══██╗██║░░░░░██║░░░██║╚══██╔══╝██║██╔══██╗██╔══██╗██╔════╝
███████║██╔██╗██║███████║██║░░░░░██║░░░██║░░░██║░░░██║██║░░╚═╝██████╔╝╚█████╗░
██╔══██║██║╚████║██╔══██║██║░░░░░██║░░░██║░░░██║░░░██║██║░░██╗██╔══██╗░╚═══██╗
██║░░██║██║░╚███║██║░░██║███████╗╚██████╔╝░░░██║░░░██║╚█████╔╝██║░░██║██████╔╝
╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝╚══════╝░╚═════╝░░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚═╝╚═════╝░
```

A comprehensive batch data engineering pipeline for processing customer analytics data. This project implements a complete ETL (Extract, Transform, Load) pipeline that generates synthetic data, processes it through various stages, and provides analytics-ready datasets.

## 🏗️ Architecture

```
MongoDB → PostgreSQL → Transformation → Analytics
   ↓           ↓             ↓
Faker     Raw Tables    Clean Data
Data      (Landing)     (Staging)
```

### Components

- **Data Generation**: Synthetic customer, product, and order data generation using Faker
- **Source Storage**: MongoDB for initial data storage
- **Data Warehouse**: PostgreSQL with raw and staging schemas
- **Object Storage**: MinIO S3-compatible storage for files and backups
- **Orchestration**: Apache Airflow for workflow management
- **Transformation**: Jupyter notebooks for data cleaning and processing

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.14+
- Git

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd batch-data-engineering-project
   ```

2. **Start all services**
   ```bash
   docker-compose up -d postgres minio mongo redis pgadmin
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requiremeents.txt
   ```

4. **Generate sample data**
   ```bash
   python -m generator.data_generator
   ```

5. **Run extraction pipeline**
   ```bash
   python extraction/extract_mongo_to_postgres.py
   ```

6. **Run transformation**
   ```bash
   jupyter notebook transformation/
   ```

## 📁 Project Structure

```
├── airflow/                 # Airflow DAGs and configurations
├── config/                  # Configuration files and settings
├── extraction/              # ETL extraction scripts
│   ├── extract_mongo_to_minio.py
│   └── extract_mongo_to_postgres.py
├── generator/               # Synthetic data generation
│   ├── data_generator.py
│   ├── fake_customers.py
│   ├── fake_orders.py
│   └── fake_products.py
├── sql/                     # Database schema and migration scripts
├── transformation/          # Data transformation notebooks
├── validation/              # Data quality validation scripts
├── workflow/                # CI/CD and automation workflows
├── docker-compose.yml       # Container orchestration
├── Dockerfile              # Custom container definitions
└── .env                    # Environment variables
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# MongoDB
MONGO_URI=mongodb://admin:password@mongo:27017/mandera_source?authSource=admin
MONGO_DB=mandera_source

# PostgreSQL
POSTGRES_USER=pipeline
POSTGRES_PASSWORD=pipeline_secret
POSTGRES_DB=mandera_warehouse
POSTGRES_HOST=localhost
POSTGRES_PORT=5435

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123
MINIO_ENDPOINT=http://minio:9000

# Airflow
AIRFLOW__CORE__EXECUTOR=CeleryExecutor
```

### Database Schemas

- **Raw Schema**: Landing tables for extracted data
- **Staging Schema**: Cleaned and transformed data
- **Monitoring Schema**: Pipeline metadata and logs

## 🏃‍♂️ Usage

### Data Generation

Generate synthetic data and store in MongoDB:

```bash
python -m generator.data_generator
```

### Data Extraction

Extract data from MongoDB to PostgreSQL:

```bash
python extraction/extract_mongo_to_postgres.py
```

### Data Transformation

Run transformation notebooks in `transformation/` directory:

```bash
jupyter notebook transformation/
```

### Airflow Orchestration

Start Airflow services:

```bash
docker-compose up airflow-webserver airflow-scheduler
```

Access Airflow UI at: http://localhost:8080

## 🌐 Services

| Service | URL | Purpose |
|---------|-----|---------|
| PostgreSQL | localhost:5435 | Data warehouse |
| MinIO API | localhost:9000 | Object storage API |
| MinIO Console | localhost:9001 | Web UI for MinIO |
| pgAdmin | localhost:5050 | PostgreSQL admin interface |
| Airflow Webserver | localhost:8080 | Workflow orchestration |
| MongoDB | localhost:27017 | Source data storage |

## 📊 Data Flow

1. **Generate**: Faker creates synthetic customer/product/order data
2. **Store**: Data inserted into MongoDB collections
3. **Extract**: Data extracted from MongoDB to PostgreSQL raw tables
4. **Transform**: Raw data cleaned and transformed in staging tables
5. **Load**: Analytics-ready data available for reporting

## 🔍 Monitoring & Logging

- **Logs**: Available in `logs/` directory
- **Health Checks**: Built into Docker services
- **Monitoring Tables**: Pipeline execution metadata in PostgreSQL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

- **Port conflicts**: Ensure ports 5435, 9000-9001, 8080, 5050 are available
- **MongoDB connection**: Check MongoDB service is running and credentials are correct
- **PostgreSQL connection**: Verify PostgreSQL health check passes
- **Python dependencies**: Install requirements with `pip install -r requiremeents.txt`

### Logs

Check service logs:
```bash
docker-compose logs <service-name>
```

### Reset Environment

To reset all data and start fresh:
```bash
docker-compose down -v  # Remove containers and volumes
docker-compose up -d    # Restart services
```</content>
<parameter name="filePath">/Users/mac1/Batch Data Engineering Project/README.md