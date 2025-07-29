# Data Setup Guide

## 📂 **Sample Data Files Added**

### **1. `data/sample_policy_clauses.json`**

- 10 realistic insurance policy clauses
- Covers exclusions, conditions, coverage, and benefits
- Includes health insurance scenarios like:
  - Pre-existing conditions
  - Dental treatment
  - Mental health coverage
  - Maternity benefits
  - Alternative medicine

### **2. `data/test_queries.json`**

- 5 test queries with expected results
- Includes user metadata (age, policy duration, existing conditions)
- Tests various scenarios:
  - Diabetes treatment (pre-existing condition)
  - Dental coverage
  - Mental health treatment
  - Plastic surgery
  - Hospitalization

### **3. `scripts/populate_database.py`**

- Generates real embeddings for policy clauses
- Populates PostgreSQL database
- Creates FAISS vector index
- **MUST RUN** before using the system

### **4. `scripts/test_queries.py`**

- Tests the complete pipeline with sample queries
- Validates system responses
- Checks expected vs actual decisions

## 🚀 **How to Set Up Sample Data**

### **Step 1: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 2: Set Up Database**

```bash
# Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE bajaj_policy_db;"

# Run schema creation
psql -U postgres -d bajaj_policy_db -f database/schema.sql
```

### **Step 3: Populate with Real Data**

```bash
# Generate embeddings and populate database
python scripts/populate_database.py
```

### **Step 4: Test the System**

```bash
# Run test queries
python scripts/test_queries.py
```

### **Step 5: Start the API**

```bash
python run.py
```

## 🎯 **What This Solves**

### **Before (Empty Embeddings)**

```sql
embedding: '[]'  -- Won't work with FAISS search
```

### **After (Real Embeddings)**

```sql
embedding: '[0.1234, -0.5678, 0.9012, ...]'  -- 384-dimensional vector
```

## 📊 **Sample Data Structure**

### **Policy Clause Example:**

```json
{
  "clause_text": "Dental treatment is covered up to Rs. 50,000 per policy year after 6 months waiting period.",
  "section": "Benefits",
  "code": "Code-Cover03",
  "clause_type": "coverage",
  "policy_type": "health"
}
```

### **Test Query Example:**

```json
{
  "query": "Can I claim for my diabetes treatment?",
  "expected_match": "Claims for pre-existing medical conditions are excluded",
  "user_metadata": {
    "age": 45,
    "policy_duration": 60,
    "existing_conditions": true
  },
  "expected_decision": false,
  "expected_reason": "pre-existing condition"
}
```

## ⚡ **Quick Start (One Command)**

After setting up the database:

```bash
python scripts/populate_database.py && python scripts/test_queries.py
```

This will populate your system with working sample data and test it immediately!
