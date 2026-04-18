# Mandera Analytics Pipeline - Visual Architecture Guide

## 🎯 Quick Navigation

This document contains visual representations of the complete Mandera Analytics Pipeline architecture:

1. **[End-to-End Data Flow](#1-end-to-end-data-flow)** - How data moves through the system
2. **[Data Transformation Stages](#2-data-transformation-stages)** - Six-stage data pipeline
3. **[GitHub Actions Workflow](#3-github-actions-automated-workflow)** - CI/CD automation
4. **[Technology Stack](#4-complete-technology-stack)** - All tools and services

---

## 1. End-to-End Data Flow

This diagram shows the complete journey of data from generation to analytics:

```
GitHub Actions (CI/CD)
        ↓
   Python + Faker
   (Generate Data)
        ↓
   MongoDB Atlas
   (Raw Data Store)
       ↙  ↘
  MinIO    PostgreSQL (raw schema)
  (Data      (Landing Zone)
   Lake)         ↓
        PostgreSQL (staging schema)
        (Transform & Validate)
           ↓
        PostgreSQL (analytics schema)
        (Curated & Cleaned Data)
           ↓
        📊 Analytics & BI
        (Dashboards & Reports)
```

### Data Flow Components:

| Component | Role | Purpose |
|-----------|------|---------|
| **GitHub Actions** | Orchestrator | Triggers automated workflows on events |
| **Python + Faker** | Generator | Creates realistic synthetic data |
| **MongoDB Atlas** | Raw Store | Stores unstructured data documents |
| **MinIO** | Data Lake | Cost-effective backup storage (S3-compatible) |
| **PostgreSQL (raw)** | Landing Zone | Initial load of structured data |
| **PostgreSQL (staging)** | Transformation | Clean, deduplicate, validate data |
| **PostgreSQL (analytics)** | Curated | Star schema, aggregations for BI |

---

## 2. Data Transformation Stages

### Stage 1: Data Generation & Ingestion
**Tool**: Python 3.14+ with Faker Library

```
┌─────────────────────────────────────┐
│  Faker Library (Python)             │
├─────────────────────────────────────┤
│ ✓ Customers (names, emails)         │
│ ✓ Orders (transactions, dates)      │
│ ✓ Products (catalog, prices)        │
│ ✓ Realistic but synthetic data      │
└─────────────────────────────────────┘
```

**Features**:
- Random but realistic data generation
- Customizable batch sizes
- Reproducible with seed values
- Supports multiple locales

---

### Stage 2: Raw Data Store
**Tool**: MongoDB Atlas (Cloud NoSQL)

```
┌─────────────────────────────────────┐
│  MongoDB Atlas                      │
├─────────────────────────────────────┤
│ Collections:                        │
│ • customers { ... }                 │
│ • orders { ... }                    │
│ • products { ... }                  │
│                                     │
│ Features:                           │
│ ✓ Flexible schemas                  │
│ ✓ Real-time ingestion               │
│ ✓ Cloud-managed                     │
│ ✓ Automated backups                 │
└─────────────────────────────────────┘
```

---

### Stage 3: Data Lake & Backup
**Tool**: MinIO (S3-Compatible Object Storage)

```
┌─────────────────────────────────────┐
│  MinIO Data Lake                    │
├─────────────────────────────────────┤
│ raw/                                │
│ ├── customers.parquet               │
│ ├── orders.parquet                  │
│ └── products.parquet                │
│                                     │
│ Features:                           │
│ ✓ Parquet format (columnar)         │
│ ✓ Cost-effective storage            │
│ ✓ Distributed access                │
│ ✓ Versioning enabled                │
└─────────────────────────────────────┘
```

**When to use MinIO:**
- 💾 Long-term archival
- 📦 Data backups
- 🔄 Disaster recovery
- 💰 Cost optimization

---

### Stage 4: Landing Zone
**Tool**: PostgreSQL (raw schema)

```
┌──────────────────────────────────────────┐
│  PostgreSQL - raw schema                 │
├──────────────────────────────────────────┤
│ TABLE: raw.customers_raw                 │
│ ├── customer_id (PK)                     │
│ ├── name                                 │
│ ├── email                                │
│ ├── phone                                │
│ ├── city                                 │
│ ├── batch_id (for tracking)              │
│ └── created_at                           │
│                                          │
│ Similar tables:                          │
│ • orders_raw                             │
│ • products_raw                           │
│                                          │
│ Characteristics:                         │
│ ✓ 1:1 copy from source                   │
│ ✓ Minimal transformation                 │
│ ✓ Audit trail via batch_id               │
│ ✓ Historical tracking                    │
└──────────────────────────────────────────┘
```

---

### Stage 5: Staging & Transformation
**Tool**: PostgreSQL (staging schema)

```
┌──────────────────────────────────────────┐
│  PostgreSQL - staging schema             │
├──────────────────────────────────────────┤
│ TABLE: staging.customers_staging         │
│                                          │
│ Applied Transformations:                 │
│ ✅ Deduplication (DISTINCT ON)           │
│ ✅ Type Conversion (CAST)                │
│ ✅ NULL Handling (COALESCE)              │
│ ✅ Data Validation (CHECK)               │
│ ✅ Schema Standardization                │
│                                          │
│ Example Query:                           │
│ SELECT                                   │
│   DISTINCT ON (customer_id)              │
│   customer_id,                           │
│   LOWER(TRIM(name)) as name,             │
│   LOWER(email) as email,                 │
│   created_at                             │
│ FROM raw.customers_raw                   │
│ ORDER BY customer_id, created_at DESC;   │
└──────────────────────────────────────────┘
```

---

### Stage 6: Curated Data
**Tool**: PostgreSQL (analytics schema)

```
┌──────────────────────────────────────────┐
│  PostgreSQL - analytics schema           │
├──────────────────────────────────────────┤
│                                          │
│ DIMENSION TABLES:                        │
│ ┌────────────────────────────────────┐   │
│ │ dim_customers                      │   │
│ ├────────────────────────────────────┤   │
│ │ • customer_key (PK)                │   │
│ │ • customer_id (Business Key)       │   │
│ │ • customer_name                    │   │
│ │ • email, phone                     │   │
│ │ • city, country                    │   │
│ │ • is_active                        │   │
│ │ • dw_insert_date                   │   │
│ └────────────────────────────────────┘   │
│                                          │
│ ┌────────────────────────────────────┐   │
│ │ dim_products                       │   │
│ ├────────────────────────────────────┤   │
│ │ • product_key (PK)                 │   │
│ │ • product_id (Business Key)        │   │
│ │ • product_name, category           │   │
│ │ • price, cost, margin_pct          │   │
│ │ • dw_insert_date                   │   │
│ └────────────────────────────────────┘   │
│                                          │
│ FACT TABLES:                             │
│ ┌────────────────────────────────────┐   │
│ │ fact_orders                        │   │
│ ├────────────────────────────────────┤   │
│ │ • order_key (PK)                   │   │
│ │ • order_id (Business Key)          │   │
│ │ • customer_key (FK)                │   │
│ │ • order_date_key (FK)              │   │
│ │ • order_amount, quantity           │   │
│ │ • status, dw_insert_date           │   │
│ └────────────────────────────────────┘   │
│                                          │
│ ┌────────────────────────────────────┐   │
│ │ fact_order_items                   │   │
│ ├────────────────────────────────────┤   │
│ │ • order_item_key (PK)              │   │
│ │ • order_key (FK)                   │   │
│ │ • product_key (FK)                 │   │
│ │ • quantity, unit_price, line_total │   │
│ │ • dw_insert_date                   │   │
│ └────────────────────────────────────┘   │
│                                          │
│ BENEFITS:                                │
│ ✓ Star schema for fast queries           │
│ ✓ Pre-aggregated metrics                 │
│ ✓ Optimized for analytics tools          │
│ ✓ Ready for BI dashboards                │
└──────────────────────────────────────────┘
```

---

## 3. GitHub Actions Automated Workflow

### Trigger Events

```
Events that trigger the pipeline:
├── 📤 Git Push (to main/develop)
├── 🔀 Pull Request (created/updated)
└── ⏰ Scheduled (cron: daily at 2 AM)
```

### Workflow Execution Flow

```
Start Workflow
      │
      ▼
┌─────────────────────────┐
│ 1️⃣  CHECKOUT CODE      │
│ └─ git clone           │
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ 2️⃣  SETUP PYTHON       │
│ └─ Python 3.14+        │
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ 3️⃣  INSTALL DEPS       │
│ └─ pip install -r req  │
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ 4️⃣  LINT & QA          │
│ └─ pylint, black       │
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ 5️⃣  RUN TESTS          │
│ └─ pytest, coverage    │
└─────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ 6️⃣  GENERATE DATA              │
│ └─ faker library → CSV/JSON     │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ 7️⃣  INGEST TO MONGODB          │
│ └─ pymongo → collections        │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ 8️⃣  EXTRACT TO MINIO           │
│ └─ S3 API → parquet files       │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ 9️⃣  LOAD TO PG (raw)           │
│ └─ psycopg2 → raw schema        │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ 🔟 TRANSFORM TO STAGING        │
│ └─ SQL transforms → staging sch │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ 1️⃣1️⃣ CURATE TO ANALYTICS       │
│ └─ Star schema → analytics sch  │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ ✅ DATA QUALITY CHECKS          │
│ ├─ Row count validation         │
│ ├─ Schema validation            │
│ └─ NULL checks                  │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ 📧 SEND NOTIFICATIONS           │
│ ├─ Success email                │
│ └─ Failure alerts               │
└─────────────────────────────────┘
      │
      ▼
    End
```

### Workflow Configuration (workflow.yml)

```yaml
name: Mandera Analytics Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC

env:
  PYTHON_VERSION: '3.14'
  POSTGRES_HOST: localhost
  MONGODB_TIMEOUT: 30

jobs:
  data-pipeline:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: mandera_warehouse
          POSTGRES_USER: pipeline
          POSTGRES_PASSWORD: pipeline_secret
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      mongodb:
        image: mongo:latest
        options: >-
          --health-cmd mongo
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      minio:
        image: minio/minio:latest
        env:
          MINIO_ROOT_USER: minioadmin
          MINIO_ROOT_PASSWORD: minioadmin
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Lint code
        run: pylint config/ generator/ && black --check .
      
      - name: Run tests
        run: pytest tests/ --cov=.
      
      - name: Generate data
        run: python generator/data_generator.py
      
      - name: Ingest to MongoDB
        run: python config/extraction/extract_mongo_to_postgres.py
      
      - name: Extract to MinIO
        run: python scripts/export_to_minio.py
      
      - name: Load to PostgreSQL (raw)
        run: python config/extraction/extract_mongo_to_postgres.py
      
      - name: Transform to staging
        run: psql -h ${{ env.POSTGRES_HOST }} -f sql/staging_transforms.sql
      
      - name: Curate analytics
        run: psql -h ${{ env.POSTGRES_HOST }} -f sql/analytics_curated.sql
      
      - name: Data quality checks
        run: python validation/run_checks.py
      
      - name: Send notification
        if: always()
        run: |
          if [ $? -eq 0 ]; then
            echo "✅ Pipeline succeeded"
          else
            echo "❌ Pipeline failed"
          fi
```

---

## 4. Complete Technology Stack

### Layer 1: Orchestration & CI/CD
```
┌─────────────────────────────────┐
│ GitHub Actions                  │
│ • Event-driven automation       │
│ • Parallel job execution        │
│ • Artifact storage              │
│ • Matrix builds                 │
└─────────────────────────────────┘
       │
       ├─────────────────────────────────────┐
       ▼                                     ▼
┌─────────────────────────┐      ┌──────────────────────┐
│ Apache Airflow          │      │ Cron Schedules       │
│ • DAG orchestration     │      │ • Daily jobs         │
│ • Monitoring            │      │ • Hourly tasks       │
│ • Retry logic           │      │ • On-demand runs     │
└─────────────────────────┘      └──────────────────────┘
```

### Layer 2: Data Generation
```
┌───────────────────────────────────────────┐
│ Python 3.14+                              │
├───────────────────────────────────────────┤
│ • Core runtime                            │
│ • Virtual environment support             │
│ • asyncio for concurrency                 │
│ • Type hints and modern features          │
└───────────────────────────────────────────┘
       │
       ▼
┌───────────────────────────────────────────┐
│ Faker Library                             │
├───────────────────────────────────────────┤
│ • Realistic synthetic data                │
│ • Multiple locales                        │
│ • Custom providers                        │
│ • Reproducible with seeds                 │
└───────────────────────────────────────────┘
       │
       ├─────────────┬──────────────┬──────────────┐
       ▼             ▼              ▼              ▼
    Customers    Orders         Products      Additional
                                              Entities
```

### Layer 3: Data Ingestion & Storage
```
┌──────────────────────────────┐
│ MongoDB Atlas (Cloud NoSQL)  │
├──────────────────────────────┤
│ • Document storage           │
│ • Flexible schemas           │
│ • Real-time ingestion        │
│ • Automated backups          │
│ • Scaling options            │
└──────────────────────────────┘
       │
       ├──────────────────────┬──────────────────────┐
       ▼                      ▼                      ▼
┌────────────────┐    ┌────────────────┐    ┌────────────────┐
│ Redis Cache    │    │ MinIO S3       │    │ PostgreSQL     │
│ • Hot data     │    │ • Backup       │    │ • Landing zone │
│ • Sessions     │    │ • Archival     │    │ • Warehouse    │
│ • Queue        │    │ • Distribution │    │ • Analytics    │
└────────────────┘    └────────────────┘    └────────────────┘
```

### Layer 4: Data Warehouse & Transformation
```
┌───────────────────────────────────────────────┐
│ PostgreSQL 15                                 │
├───────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────┐   │
│ │ raw schema (Landing Zone)               │   │
│ │ └─ Initial load, 1:1 from source        │   │
│ └─────────────────────────────────────────┘   │
│ ┌─────────────────────────────────────────┐   │
│ │ staging schema (Transformation)         │   │
│ │ └─ Data cleansing, validation           │   │
│ └─────────────────────────────────────────┘   │
│ ┌─────────────────────────────────────────┐   │
│ │ analytics schema (Curated)              │   │
│ │ └─ Star schema, aggregations            │   │
│ └─────────────────────────────────────────┘   │
└───────────────────────────────────────────────┘
       │
       ├──────────────┬──────────────────┐
       ▼              ▼                  ▼
    SQLAlchemy    psycopg2           Pandas
    (ORM)         (Driver)        (Data manip)
```

### Layer 5: Deployment & Operations
```
┌──────────────────────────────────────┐
│ Docker & Docker Compose              │
├──────────────────────────────────────┤
│ • Container images                   │
│ • Service orchestration              │
│ • Network isolation                  │
│ • Volume management                  │
│ • Environment configuration          │
└──────────────────────────────────────┘
       │
       ├─────────────────┬─────────────────┐
       ▼                 ▼                 ▼
   Development      Production       Testing
   Deployment       Deployment      Environment
```

### Layer 6: Monitoring & Observability
```
┌──────────────────────────────────┐
│ Logging & Error Tracking         │
├──────────────────────────────────┤
│ • Application logs               │
│ • Error stack traces             │
│ • Audit logs                     │
│ • Performance metrics            │
└──────────────────────────────────┘
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
   File Logs    CloudWatch       DataDog
   (Local)      (AWS)            (SaaS)
```

---

## 📊 Component Relationships

```
GitHub Actions
      │
      ├─ Triggers ─────────────────────────► Python + Faker
      │
      └─ Monitors ─────────────────┐
                                   │
                         ┌─────────▼──────────┐
                         │   Data Pipeline    │
                         ├────────────────────┤
                         │                    │
MongoDB Atlas ◄──────────┤  (6 Stages)       │
   │                     │                    │
   ├─────────────────────┤                    │
   │                     │                    │
MinIO ◄──────────────────┤                    │
   │                     │                    │
   ├─────────────────────┤                    │
   │                     │                    │
PostgreSQL ◄─────────────┤                    │
(raw→staging→analytics)  │                    │
   │                     │                    │
   └─────────────────────┤                    │
                         │                    │
                         └────────────────────┘
                              │
                              ▼
                        ✅ Quality Checks
                        📧 Notifications
                        📊 Dashboards
```

---

## 🎓 Key Takeaways

### Data Flow Path
```
Generate → Store → Extract → Load → Transform → Curate → Analyze
(Faker)   (Mongo)  (MinIO)  (PG)   (PG)        (PG)     (BI)
```

### Schema Progression
```
raw schema (Landing)
    ↓
staging schema (Transformation)
    ↓
analytics schema (Curated)
    ↓
Dimension & Fact Tables (Star Schema)
```

### Automation via GitHub Actions
```
Event Trigger → Code Checkout → Setup Environment → Run Pipeline → Validate → Notify
```

---

## 📞 Getting Help

For detailed information, refer to:
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical deep dive
- **[README.md](README.md)** - Project overview
- **[run.md](run.md)** - Quick start guide

---

**Created**: April 2026  
**Architecture Version**: 1.0  
**Last Updated**: April 2026