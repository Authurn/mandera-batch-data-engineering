# Quick Start Guide - Mandera Analytics Pipeline

This guide provides step-by-step instructions to get the pipeline running quickly.

## 🚀 Quick Start (5 minutes)

### 1. Prerequisites Check
```bash
# Check Docker
docker --version
docker-compose --version

# Check Python
python --version  # Should be 3.14+
```

### 2. Start Core Services
```bash
# Start essential services
docker-compose up -d postgres minio mongo redis pgadmin
```

### 3. Wait for Services to be Healthy
```bash
# Check service status
docker-compose ps

# Wait until all services show "healthy" or "running"
```

### 4. Install Dependencies
```bash
# Install Python packages
pip install -r requiremeents.txt
```

### 5. Generate Sample Data
```bash
# Generate synthetic data
python -m generator.data_generator
```

### 6. Run Extraction
```bash
# Extract data to PostgreSQL
python extraction/extract_mongo_to_postgres.py
```

### 7. Run Transformation
```bash
# Open Jupyter for transformation
jupyter notebook transformation/
```

## 📋 Detailed Setup

### Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd batch-data-engineering-project

# Copy environment template
cp .env.example .env  # If .env.example exists

# Edit .env with your settings
nano .env
```

### Database Setup
```bash
# Create raw tables
docker-compose run --rm db-setup

# Or manually create tables
python setup_data.py
```

### MinIO Setup
```bash
# Access MinIO console
open http://localhost:9001

# Login with:
# Username: minioadmin
# Password: minioadmin123

# Create bucket
mc alias set myminio http://localhost:9000 minioadmin minioadmin123
mc mb myminio/mandera-raw
```

## 🎯 Common Workflows

### Full Pipeline Run
```bash
# 1. Start all services
docker-compose up -d

# 2. Generate data
python -m generator.data_generator

# 3. Extract to warehouse
python extraction/extract_mongo_to_postgres.py

# 4. Transform data (via notebooks)
jupyter notebook transformation/

# 5. Start Airflow (optional)
docker-compose up airflow-webserver airflow-scheduler
```

### Development Mode
```bash
# Start only essential services
docker-compose up -d postgres minio mongo

# Run tests
python -m pytest

# Development server
python -m generator.data_generator --dev
```

### Reset Everything
```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Clean up data directories
rm -rf ~/minio-data

# Restart fresh
docker-compose up -d postgres minio mongo redis pgadmin
```

## 🔧 Service Management

### Start Services
```bash
# Core services
docker-compose up -d postgres minio mongo redis

# With monitoring
docker-compose up -d pgadmin

# Full stack with Airflow
docker-compose up -d
```

### Stop Services
```bash
# Stop all
docker-compose down

# Stop specific service
docker-compose stop minio
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f postgres

# Last 100 lines
docker-compose logs --tail=100 minio
```

### Health Checks
```bash
# Check all services
docker-compose ps

# PostgreSQL health
docker-compose exec postgres pg_isready -U pipeline

# MinIO health
curl http://localhost:9000/minio/health/live
```

## 🌐 Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **MinIO Console** | http://localhost:9001 | minioadmin / minioadmin123 |
| **pgAdmin** | http://localhost:5050 | admin@mandera.io / admin |
| **Airflow** | http://localhost:8080 | admin / admin |
| **PostgreSQL** | localhost:5435 | pipeline / pipeline_secret |
| **MongoDB** | localhost:27017 | admin / password |

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check port conflicts
lsof -i :5435,9000,9001,8080,5050

# Free up ports
docker-compose down

# Or change ports in .env
POSTGRES_EXTERNAL_PORT=5436
```

### Database Connection Issues
```bash
# Test PostgreSQL connection
psql -h localhost -p 5435 -U pipeline -d mandera_warehouse

# Test MongoDB connection
mongosh mongodb://admin:password@localhost:27017/mandera_source
```

### MinIO Issues
```bash
# Check MinIO status
curl http://localhost:9000/minio/health/live

# Restart MinIO
docker-compose restart minio
```

### Python Issues
```bash
# Check Python environment
python --version
which python

# Reinstall dependencies
pip install -r requiremeents.txt --force-reinstall
```

### Clean Restart
```bash
# Nuclear option - remove everything
docker-compose down -v --remove-orphans
docker system prune -f
docker volume prune -f

# Restart fresh
docker-compose up -d postgres minio mongo redis pgadmin
```

## 📊 Verification Steps

### Check Data Pipeline
```bash
# 1. Verify MongoDB has data
python -c "
from pymongo import MongoClient
client = MongoClient('mongodb://admin:password@localhost:27017/mandera_source')
print('Customers:', client.mandera_source.customers.count_documents({}))
print('Products:', client.mandera_source.products.count_documents({}))
print('Orders:', client.mandera_source.orders.count_documents({}))
"

# 2. Verify PostgreSQL has data
python -c "
import psycopg2
conn = psycopg2.connect('host=localhost port=5435 dbname=mandera_warehouse user=pipeline password=pipeline_secret')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM raw.customers_raw')
print('Raw customers:', cursor.fetchone()[0])
cursor.close()
conn.close()
"

# 3. Test transformation
python -c "
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('postgresql://pipeline:pipeline_secret@localhost:5435/mandera_warehouse')
df = pd.read_sql('SELECT * FROM raw.customers_raw LIMIT 5', engine)
print('Sample data:')
print(df.head())
"
```

## 🎉 Success Indicators

- ✅ All services show "healthy" in `docker-compose ps`
- ✅ Can connect to PostgreSQL on port 5435
- ✅ Can access MinIO console at http://localhost:9001
- ✅ MongoDB collections have data
- ✅ Raw tables in PostgreSQL have data
- ✅ Jupyter notebooks can connect to database

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review service logs: `docker-compose logs`
3. Verify environment variables in `.env`
4. Ensure all prerequisites are installed
5. Check GitHub Issues for similar problems

5. **Run extraction pipeline**
   ```bash
   python extraction/extract_mongo_to_postgres.py
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