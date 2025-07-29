# API Authentication Guide

## 🔐 **API Keys and Authentication**

### **1. Required API Keys**

Your Bajaj Policy Query System uses multiple layers of security:

#### **Primary API Key** (Required)

- **Environment Variable**: `BAJAJ_API_KEY`
- **Purpose**: Secure your API endpoints
- **Current Value**: `bajaj_hack_2024_super_secure_api_key_12345`
- **Usage**: Include in `Authorization: Bearer <API_KEY>` header

#### **JWT Secret** (Required)

- **Environment Variable**: `JWT_SECRET_KEY`
- **Purpose**: Sign and verify JWT tokens
- **Generate Strong Key**: Use online JWT secret generator

### **2. Optional Third-Party API Keys**

#### **OpenAI API Key** (For Enhanced AI)

```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```

- Get from: https://platform.openai.com/api-keys
- Purpose: Enhanced natural language responses

#### **Hugging Face API Key** (For Advanced Models)

```bash
HUGGINGFACE_API_KEY=hf_your-huggingface-token-here
```

- Get from: https://huggingface.co/settings/tokens
- Purpose: Access premium models and faster inference

#### **Azure OpenAI** (Alternative to OpenAI)

```bash
AZURE_OPENAI_API_KEY=your-azure-openai-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

### **3. How to Use Authentication**

#### **Step 1: Get Access Token** (Optional JWT)

```bash
POST /auth/token
Authorization: Bearer bajaj_hack_2024_super_secure_api_key_12345
Content-Type: application/json

{
    "user_id": "user123"
}
```

#### **Step 2: Query with API Key**

```bash
POST /query/
Authorization: Bearer bajaj_hack_2024_super_secure_api_key_12345
Content-Type: multipart/form-data

file: [PDF_FILE]
query: "Does my policy cover pre-existing conditions?"
age: 35
policy_duration: 45
existing_conditions: true
```

### **4. Response Format**

```json
{
  "status": "success",
  "data": {
    "claim_allowed": false,
    "reason": "Claim rejected due to pre-existing conditions clause.",
    "reference_clause": "claims for pre-existing medical conditions are excluded...",
    "confidence_score": 0.89,
    "processing_time_ms": 1250
  }
}
```

### **5. Security Best Practices**

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Use strong API keys** - At least 32 characters
3. **Rotate keys regularly** - Change them monthly
4. **Use HTTPS in production** - Never send keys over HTTP
5. **Monitor API usage** - Check logs for suspicious activity

### **6. Environment Setup**

1. Copy `.env.example` to `.env`
2. Fill in your actual API keys
3. Never share or commit the `.env` file
4. Use different keys for development/production

### **7. Rate Limiting**

- Default: 60 requests per minute per API key
- Configurable via `RATE_LIMIT_PER_MINUTE`
- Returns `429 Too Many Requests` when exceeded

### **8. Error Codes**

- `401`: Invalid or missing API key
- `429`: Rate limit exceeded
- `400`: Invalid request format
- `500`: Internal server error
