# Bajaj Insurance PDF Testing Guide

## 🎯 **Testing Your System with Real Bajaj PDF**

You now have a complete testing framework for your Bajaj insurance policy document:

### 📂 **New Scripts Created:**

#### **1. `scripts/analyze_bajaj_pdf.py`**

- Extracts and analyzes the Bajaj PDF content
- Shows document statistics and key sections
- Identifies potential policy clauses
- **Run this first** to understand your PDF structure

#### **2. `scripts/extract_bajaj_clauses.py`**

- Automatically extracts policy clauses from Bajaj PDF
- Generates embeddings for the clauses
- Populates your database with real Bajaj policy data
- Updates FAISS index with Bajaj-specific vectors

#### **3. `scripts/test_bajaj_queries.py`**

- Tests your complete system with realistic insurance queries
- Uses the actual Bajaj PDF as input
- Tests various scenarios (pre-existing conditions, dental, maternity, etc.)

### 🚀 **Step-by-Step Testing Process:**

#### **Step 1: Analyze the PDF**

```bash
python scripts/analyze_bajaj_pdf.py
```

**What it does:**

- Extracts text from your Bajaj PDF
- Shows statistics (word count, sections found)
- Saves full text to `data/bajaj_pdf_analysis.txt`
- Identifies key insurance terms

#### **Step 2: Extract Real Policy Clauses**

```bash
python scripts/extract_bajaj_clauses.py
```

**What it does:**

- Intelligently extracts policy clauses from Bajaj PDF
- Categorizes them (exclusions, coverage, conditions)
- Generates real embeddings using SentenceTransformers
- Populates PostgreSQL database
- Updates FAISS vector index
- Saves clauses to `data/bajaj_extracted_clauses.json`

#### **Step 3: Test with Real Queries**

```bash
python scripts/test_bajaj_queries.py
```

**What it does:**

- Tests 6 realistic insurance queries
- Uses your actual Bajaj PDF
- Shows approve/reject decisions
- Displays confidence scores and reasoning
- Measures processing time

### 📋 **Sample Test Queries for Bajaj PDF:**

1. **"What is the waiting period for pre-existing diseases?"**

   - Tests exclusion handling
   - User with existing conditions

2. **"Are dental treatments covered?"**

   - Tests benefit coverage
   - Healthy user profile

3. **"Is maternity coverage included?"**

   - Tests specific benefits
   - Female user scenario

4. **"What about hospitalization expenses?"**

   - Tests core coverage
   - General hospitalization

5. **"Are alternative treatments like Ayurveda covered?"**

   - Tests alternative medicine coverage
   - Specific treatment inquiry

6. **"Is plastic surgery covered?"**
   - Tests cosmetic vs medical necessity
   - Exclusion scenarios

### 🎯 **Expected Test Results:**

Your system should:

- ✅ Extract real clauses from Bajaj PDF
- ✅ Generate accurate embeddings
- ✅ Match queries to relevant clauses
- ✅ Apply business logic (waiting periods, conditions)
- ✅ Return structured approve/reject decisions
- ✅ Provide confidence scores
- ✅ Process queries in under 2 seconds

### 🔧 **Troubleshooting:**

#### **If PDF extraction fails:**

- Ensure PyMuPDF is installed: `pip install PyMuPDF`
- Check PDF file permissions
- Verify PDF path is correct

#### **If database population fails:**

- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Run schema creation: `psql -d bajaj_policy_db -f database/schema.sql`

#### **If FAISS index fails:**

- Ensure `models/faiss_index/` directory exists
- Check write permissions
- Install FAISS: `pip install faiss-cpu`

### 📊 **Performance Expectations:**

With your Bajaj PDF:

- **Clause Extraction**: ~30-100 clauses (depending on PDF size)
- **Embedding Generation**: ~10-30 seconds
- **Query Processing**: <2 seconds per query
- **Accuracy**: 80-90% for clear policy questions

### 🎉 **Success Indicators:**

1. **PDF Analysis**: Shows key sections like "EXCLUSIONS", "BENEFITS"
2. **Clause Extraction**: Generates 20+ meaningful policy clauses
3. **Database Population**: Successfully inserts clauses with embeddings
4. **Query Testing**: Returns relevant approve/reject decisions
5. **Performance**: Fast response times with high confidence scores

This testing framework validates your entire system using **real Bajaj insurance policy data**!
