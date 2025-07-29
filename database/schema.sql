-- database/schema.sql

-- Main table for storing policy clauses with embeddings
CREATE TABLE IF NOT EXISTS policy_clauses (
    id SERIAL PRIMARY KEY,
    clause_text TEXT NOT NULL,
    embedding TEXT NOT NULL, -- JSON or base64 of vector
    section TEXT,
    code TEXT UNIQUE, -- E.g., "Code-Excl03", "Code-Cover01"
    clause_type VARCHAR(50), -- 'exclusion', 'coverage', 'condition', 'benefit'
    policy_type VARCHAR(50), -- 'health', 'life', 'auto', 'travel'
    confidence_threshold FLOAT DEFAULT 0.75,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing user queries and their results (for analytics/learning)
CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    user_query TEXT NOT NULL,
    matched_clause_id INTEGER REFERENCES policy_clauses(id),
    confidence_score FLOAT,
    claim_decision BOOLEAN, -- TRUE if allowed, FALSE if rejected
    decision_reason TEXT,
    user_metadata JSONB, -- Store age, policy_duration, conditions, etc.
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for different policy documents
CREATE TABLE IF NOT EXISTS policy_documents (
    id SERIAL PRIMARY KEY,
    document_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(50), -- 'health_policy', 'terms_conditions', etc.
    file_path TEXT,
    version VARCHAR(20),
    effective_date DATE,
    expiry_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Junction table to link clauses to specific documents
CREATE TABLE IF NOT EXISTS document_clauses (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES policy_documents(id),
    clause_id INTEGER REFERENCES policy_clauses(id),
    page_number INTEGER,
    line_number INTEGER,
    UNIQUE(document_id, clause_id)
);

-- Table for storing user sessions and feedback
CREATE TABLE IF NOT EXISTS user_feedback (
    id SERIAL PRIMARY KEY,
    query_log_id INTEGER REFERENCES query_logs(id),
    user_rating INTEGER CHECK (user_rating >= 1 AND user_rating <= 5),
    was_helpful BOOLEAN,
    feedback_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_policy_clauses_type ON policy_clauses(clause_type);
CREATE INDEX IF NOT EXISTS idx_policy_clauses_policy_type ON policy_clauses(policy_type);
CREATE INDEX IF NOT EXISTS idx_policy_clauses_active ON policy_clauses(is_active);
CREATE INDEX IF NOT EXISTS idx_query_logs_created_at ON query_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_query_logs_decision ON query_logs(claim_decision);

-- Sample data for testing (will be replaced by proper embeddings via populate_database.py)
-- Note: Run 'python scripts/populate_database.py' to populate with real embeddings
INSERT INTO policy_clauses (clause_text, section, code, clause_type, policy_type, embedding) VALUES
('Claims for pre-existing medical conditions are excluded from coverage unless specifically declared and accepted by the insurer.', 'Exclusions', 'Code-Excl01', 'exclusion', 'health', '[]'),
('The policy has a 30-day waiting period for all claims except emergency treatments.', 'Conditions', 'Code-Cond01', 'condition', 'health', '[]'),
('Coverage includes hospitalization expenses up to the sum insured amount.', 'Benefits', 'Code-Cover01', 'coverage', 'health', '[]'),
('Maternity benefits are covered after 36 months of continuous policy tenure.', 'Benefits', 'Code-Cover02', 'coverage', 'health', '[]'),
('Claims arising from self-inflicted injuries or suicide attempts are not covered.', 'Exclusions', 'Code-Excl02', 'exclusion', 'health', '[]')
ON CONFLICT (code) DO NOTHING;
