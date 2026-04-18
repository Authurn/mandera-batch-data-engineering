# Mandera Analytics Pipeline - Architecture Documentation

## 📊 Complete Data Pipeline Overview

This document provides comprehensive visual architecture diagrams for the Mandera Analytics Pipeline, showing how data flows through each component of the system.

---

## 🔄 1. End-to-End Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MANDERA ANALYTICS PIPELINE                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  🔄 CI/CD                📊 Generation         🗄️ Raw Store            │
│  ┌──────────────┐        ┌─────────────────┐  ┌─────────────────┐      │
│  │   GitHub     │───────▶│  Python Faker   │─▶│  MongoDB Atlas  │      │
│  │   Actions    │        │  • Customers    │  │  • Collections  │      │
│  │ • Automated  │        │  • Orders       │  │  • Documents    │      │
│  │ • Scheduled  │        │  • Products     │  │  • Backup       │      │
│  │ • Triggers   │        │  • Realistic    │  │  • Scalable     │      │
│  └──────────────┘        └─────────────────┘  └─────────────────┘      │
│                                                        │                 │
│                                                        ▼                 │
│         📦 Data Lake              Landing Zone        Data Warehouse    │
│      ┌─────────────────┐      ┌────────────────┐  ┌──────────────────┐ │
│      │   MinIO (S3)    │◀─────│  PostgreSQL    │  │   PostgreSQL     │ │
│      │ • Parquet files │      │  raw schema    │  │  staging schema  │ │
│      │ • Backup        │      │  • Load        │──▶│  • Deduplicate   │ │
│      │ • Cost-effective│      │  • Unmodified  │  │  • Validate      │ │
│      │ • Distributed   │      │  • Normalized  │  │  • Transform     │ │
│      └─────────────────┘      └────────────────┘  └──────────────────┘ │
│                                                        │                 │
│                                                        ▼                 │
│                                          ┌──────────────────────────┐   │
│                                          │   PostgreSQL             │   │
│                                          │   analytics schema       │   │
│                                          │ • dim_customers          │   │
│                                          │ • dim_products           │   │
│                                          │ • fact_orders            │   │
│                                          │ • Aggregations           │   │
│                                          │ • Ready for BI           │   │
│                                          └──────────────────────────┘   │
│                                                        │                 │
│                                                        ▼                 │
│                                          ┌──────────────────────────┐   │
│                                          │   📊 Analytics & BI      │   │
│                                          │  • Dashboards            │   │
│                                          │  • Reports               │   │
│                                          │  • Insights              │   │
│                                          └──────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📈 2. Data Transformation Stages

### Stage 1: Data Generation & Ingestion
- **Tool**: Python 3.14+ with Faker Library
- **Output**: Realistic synthetic data
- **Entities**: Customers, Orders, Products
- **Features**:
  - Random but realistic data
  - Batch processing capabilities
  - Customizable schemas

### Stage 2: Raw Data Store
- **Tool**: MongoDB Atlas
- **Collections**:
  - `customers` - Customer documents
  - `orders` - Order documents
  - `products` - Product catalog
- **Characteristics**:
  - NoSQL document storage
  - Flexible schemas
  - Real-time ingestion

### Stage 3: Data Lake & Backup
- **Tool**: MinIO (S3-compatible object storage)
- **Structure**:
  ```
  raw/
  ├── customers.parquet
  ├── orders.parquet
  └── products.parquet
  ```
- **Purpose**:
  - Cost-effective backup storage
  - Distributed access
  - Archival capabilities

### Stage 4: Landing Zone
- **Tool**: PostgreSQL (raw schema)
- **Tables**:
  ```sql
  raw.customers_raw
  raw.orders_raw
  raw.products_raw
  ```
- **Properties**:
  - 1:1 copy from source
  - Minimal transformations
  - Audit trail via batch_id

### Stage 5: Staging & Transformation
- **Tool**: PostgreSQL (staging schema)
- **Tables**:
  ```sql
  staging.customers_staging
  staging.orders_staging
  staging.products_staging
  ```
- **Transformations**:
  - ✅ Deduplication
  - ✅ Type conversion
  - ✅ NULL handling
  - ✅ Data validation
  - ✅ Schema standardization

### Stage 6: Curated Data
- **Tool**: PostgreSQL (analytics schema)
- **Dimension Tables**:
  - `dim_customers` - Customer attributes
  - `dim_products` - Product attributes
  - `dim_dates` - Date dimensions
- **Fact Tables**:
  - `fact_orders` - Order transactions
  - `fact_order_items` - Line items
- **Features**:
  - Star schema design
  - Pre-aggregated metrics
  - Ready for BI tools
  - Performance optimized

---

## 🔄 3. GitHub Actions Automated Workflow

### Trigger Events
| Event | Description |
|-------|-------------|
| 📤 **Push** | Triggered on push to main/develop branch |
| 🔀 **Pull Request** | Triggered on PR creation/update |
| ⏰ **Scheduled** | Daily/Hourly scheduled runs |

### Workflow Steps

#### Phase 1: Setup & Validation
```
1️⃣  Checkout Code
     └─ Clone repository
     
2️⃣  Setup Python
     └─ Python 3.14+
     
3️⃣  Install Dependencies
     └─ pip install -r requirements.txt
     
4️⃣  Lint & Code Quality
     └─ pylint, black, flake8
     
5️⃣  Run Unit Tests
     └─ pytest, coverage reports
```

#### Phase 2: Data Pipeline Execution
```
6️⃣  Generate Data
     └─ faker library → synthetic data
     
7️⃣  Ingest to MongoDB Atlas
     └─ pymongo → collections
     
8️⃣  Extract to MinIO
     └─ parquet format → S3-compatible storage
     
9️⃣  Load to PostgreSQL (raw)
     └─ psycopg2 → raw schema
     
🔟 Transform to Staging
     └─ SQL transformations → staging schema
     
1️⃣1️⃣ Curate Analytics
     └─ SQL aggregations → analytics schema
```

#### Phase 3: Validation & Notification
```
✅ Data Quality Checks
   ├─ Row count validation
   ├─ Schema validation
   └─ NULL value checks
   
📧 Notifications
   ├─ Success email
   └─ Failure alerts
```

### Workflow YAML Example
```yaml
name: Mandera Analytics Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  data-pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.14'
      - run: pip install -r requirements.txt
      - run: python generator/data_generator.py
      - run: python config/extraction/extract_mongo_to_postgres.py
```

---

## 🛠️ 4. Technology Stack

```
┌────────────────────────────────────────────────────┐
│         ORCHESTRATION & CI/CD LAYER               │
├────────────────────────────────────────────────────┤
│  • GitHub Actions - Automated workflow            │
│  • Apache Airflow - DAG orchestration             │
│  • cron schedules - Scheduled jobs                │
└────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│           DATA GENERATION LAYER                   │
├────────────────────────────────────────────────────┤
│  • Python 3.14+ - Core language                  │
│  • Faker - Realistic data generation             │
│  • Pandas - Data manipulation                    │
└────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│        DATA INGESTION & STORAGE LAYER             │
├────────────────────────────────────────────────────┤
│  • MongoDB Atlas - NoSQL raw data store           │
│  • Redis - Caching & message queue                │
│  • MinIO - S3-compatible object storage           │
└────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│      DATA WAREHOUSE & TRANSFORMATION LAYER        │
├────────────────────────────────────────────────────┤
│  • PostgreSQL 15 - Relational warehouse           │
│  • SQLAlchemy - ORM framework                    │
│  • SQL - ETL transformations                     │
│  • psycopg2 - PostgreSQL adapter                 │
└────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│      DEPLOYMENT & OPERATIONS LAYER               │
├────────────────────────────────────────────────────┤
│  • Docker - Containerization                     │
│  • Docker Compose - Container orchestration      │
│  • pgAdmin - PostgreSQL GUI management           │
└────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│      MONITORING & OBSERVABILITY LAYER             │
├────────────────────────────────────────────────────┤
│  • Logging - Error tracking & debugging          │
│  • Metrics - Performance monitoring               │
│  • Alerts - Failure notifications                │
└────────────────────────────────────────────────────┘
```

---

## 📊 5. Database Schema Architecture

### PostgreSQL Schema Hierarchy

```
mandera_warehouse/
│
├── raw schema (Landing Zone)
│   ├── customers_raw
│   │   ├── customer_id (PK)
│   │   ├── name
│   │   ├── email
│   │   ├── phone
│   │   ├── city
│   │   ├── batch_id
│   │   └── created_at
│   │
│   ├── orders_raw
│   │   ├── order_id (PK)
│   │   ├── customer_id (FK)
│   │   ├── order_date
│   │   ├── total_amount
│   │   ├── batch_id
│   │   └── created_at
│   │
│   └── products_raw
│       ├── product_id (PK)
│       ├── name
│       ├── category
│       ├── price
│       ├── batch_id
│       └── created_at
│
├── staging schema (Transformation)
│   ├── customers_staging
│   │   └── [Deduplicated, validated customers]
│   │
│   ├── orders_staging
│   │   └── [Validated orders with error flags]
│   │
│   └── products_staging
│       └── [Enriched product data]
│
└── analytics schema (Curated Data)
    ├── dim_customers
    │   ├── customer_key (PK)
    │   ├── customer_id
    │   ├── customer_name
    │   ├── email
    │   ├── phone
    │   ├── city
    │   ├── country
    │   ├── created_date
    │   ├── is_active
    │   └── dw_insert_date
    │
    ├── dim_products
    │   ├── product_key (PK)
    │   ├── product_id
    │   ├── product_name
    │   ├── category
    │   ├── price
    │   ├── cost
    │   ├── margin_pct
    │   └── dw_insert_date
    │
    ├── fact_orders
    │   ├── order_key (PK)
    │   ├── order_id
    │   ├── customer_key (FK)
    │   ├── order_date_key (FK)
    │   ├── order_amount
    │   ├── order_quantity
    │   ├── status
    │   └── dw_insert_date
    │
    └── fact_order_items
        ├── order_item_key (PK)
        ├── order_key (FK)
        ├── product_key (FK)
        ├── quantity
        ├── unit_price
        ├── line_total
        └── dw_insert_date
```

---

## 🔐 6. Data Flow Security

### MongoDB Atlas (Raw Data)
- ✅ Cloud-managed MongoDB
- ✅ Encryption at rest & in transit
- ✅ Network access controls
- ✅ Backup & recovery

### MinIO Data Lake
- ✅ S3-compatible access control
- ✅ Versioning enabled
- ✅ Lifecycle policies
- ✅ Encryption support

### PostgreSQL Warehouse
- ✅ Role-based access control
- ✅ Row-level security policies
- ✅ Connection pooling
- ✅ Audit logging

### GitHub Actions
- ✅ Secrets management
- ✅ Encrypted environment variables
- ✅ Branch protection rules
- ✅ Action approval workflows

---

## 📈 7. Performance Characteristics

| Component | Throughput | Latency | Scalability |
|-----------|-----------|---------|-------------|
| Data Generation | 10K-100K rows/min | <100ms | Linear |
| MongoDB Atlas | 10K-50K ops/sec | 10-50ms | Horizontal |
| MinIO | 100MB+/sec | <10ms | Horizontal |
| PostgreSQL (raw→staging) | 50K-500K rows/min | 100-500ms | Vertical |
| PostgreSQL (staging→analytics) | 10K-100K rows/min | 500ms-1s | Vertical |

---

## 🚀 8. Deployment Architecture

### Local Development
```bash
docker-compose up -d
# Starts all services locally
```

### Services
- **PostgreSQL**: `localhost:5432`
- **MongoDB**: `localhost:27017`
- **MinIO**: `localhost:9000`
- **Redis**: `localhost:6379`
- **Airflow**: `localhost:8080`
- **pgAdmin**: `localhost:5050`

### Cloud Deployment
- **MongoDB Atlas**: Cloud-managed MongoDB
- **PostgreSQL RDS/Aurora**: Cloud-managed PostgreSQL
- **S3/MinIO**: Cloud object storage
- **GitHub Actions**: CI/CD orchestration

---

## 📝 9. Key Design Patterns

### 1. Lambda Architecture (Speed + Batch Layers)
- **Batch Layer**: nightly data loads via GitHub Actions
- **Speed Layer**: Redis cache for real-time access

### 2. Star Schema (Analytics)
- **Dimension tables**: dim_customers, dim_products
- **Fact tables**: fact_orders, fact_order_items
- **Benefits**: Fast aggregations, easy joins

### 3. Extract-Load-Transform (ELT)
- Extract: MongoDB → MinIO → PostgreSQL raw
- Load: Parallel loading into staging
- Transform: SQL-based transformations

### 4. Medallion Architecture
- **Bronze (raw)**: Raw data from sources
- **Silver (staging)**: Cleaned, validated data
- **Gold (analytics)**: Curated, aggregated data

---

## 🔧 10. Configuration & Customization

### Environment Variables
```
MONGO_URI=mongodb+srv://...
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=...
MINIO_SECRET_KEY=...
```

### Docker Compose Services
- Modify `docker-compose.yml` for service configuration
- Add environment variables in `.env` file
- Scale services with `--scale` flag

### Transformation Queries
- Located in `sql/` directory
- Execute via Python ETL scripts
- Version control all changes

---

## 📊 11. Monitoring & Troubleshooting

### Health Checks
```bash
# PostgreSQL
psql -h localhost -d mandera_warehouse -U pipeline

# MongoDB
mongosh --host localhost

# MinIO
aws s3 --endpoint-url http://localhost:9000 ls

# Redis
redis-cli ping
```

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection refused | Service not running | `docker-compose up -d` |
| Schema not found | Migration not run | `python setup_data.py` |
| Data not appearing | ETL failed silently | Check GitHub Actions logs |
| Slow queries | Missing indexes | Run `ANALYZE` on tables |

---

## 📚 Related Documentation

- **[README.md](README.md)** - Project overview & quick start
- **[run.md](run.md)** - Step-by-step run instructions
- **[requirements.txt](requirements.txt)** - Python dependencies
- **[docker-compose.yml](docker-compose.yml)** - Service definitions
- **[config/settings.py](config/settings.py)** - Configuration management

---

**Last Updated**: April 2026  
**Version**: 1.0  
**Architecture Owner**: Data Engineering Team