# Zomato Restaurant Recommendation System - Documentation

## 📁 Repository Structure

All phases of the restaurant recommendation system are organized under the `Docs/` folder for better documentation and maintainability. **No duplicate files exist - each file has a single source of truth.**

### 🗂️ Phase Organization

```
Docs/
├── README.md                    # This file - Phase documentation overview
├── phase_wise_architecture.md   # Complete system architecture
├── edge_cases.md               # Edge cases and error handling
├── problemstatement.md         # Problem statement and requirements
├── phase1/                     # Data Ingestion Phase (from src/zomato_rec/phase1)
├── phase2/                     # Data Collection & Normalization (from src/zomato_rec/phase2)
├── phase3/                     # Candidate Retrieval & Shortlisting (from src/zomato_rec/phase3)
├── phase4/                     # LLM Integration & Recommendation Generation (from src/zomato_rec/phase4)
├── phase5/                     # Presentation Layer & UX Enhancements (structure ready)
├── phase6/                     # Evaluation, Monitoring & Quality Loop (structure ready)
├── phase7/                     # Backend API Layer (FastAPI)
└── phase8/                     # Frontend Application (Next.js - in root during development)
```

## 📋 Phase Descriptions

### Phase 1: Data Ingestion
- **Location**: `Docs/phase1/`
- **Purpose**: Raw data ingestion and preprocessing
- **Files**: `ingest.py`, `preprocess.py`, `__init__.py`

### Phase 2: Data Collection & Normalization
- **Location**: `Docs/phase2/`
- **Purpose**: Data collection, I/O operations, and normalization
- **Files**: `collect.py`, `io.py`, `models.py`, `normalize.py`, `__init__.py`

### Phase 3: Candidate Retrieval & Shortlisting
- **Location**: `Docs/phase3/`
- **Purpose**: Retrieve and shortlist candidate restaurants
- **Files**: `retrieve.py`, `shortlist.py`, `__init__.py`

### Phase 4: LLM Integration & Recommendation Generation
- **Location**: `Docs/phase4/`
- **Purpose**: LLM integration and final recommendation generation
- **Files**: `groq_client.py`, `parsing.py`, `prompting.py`, `recommend.py`, `run.py`, `__init__.py`

### Phase 5: Presentation Layer & UX Enhancements
- **Location**: `Docs/phase5/`
- **Purpose**: Enhanced presentation and user experience
- **Files**: `renderer.py`, `cli.py`, `ux_enhancements.py`, `run.py`, `main.py`, `README.md`

### Phase 6: Evaluation, Monitoring & Quality Loop
- **Location**: `Docs/phase6/`
- **Purpose**: System evaluation, monitoring, and quality improvement
- **Files**: `golden_tests.py`, `metrics.py`, `monitoring.py`, `dashboard.py`, `quality_improvement.py`, `README.md`

### Phase 7: Backend API Layer
- **Location**: `Docs/phase7/`
- **Purpose**: FastAPI backend with RESTful endpoints
- **Files**: 
  - `app.py`, `app-simple.py`, `app-complete.py`, `app-final.py`
  - `health_api.py`, `recommendation_api.py`, `metadata_api.py`
  - `models.py`, `requirements.txt`, `README.md`
  - `simple-api.py`, `test-recommendations.py`

### Phase 8: Frontend Application
- **Location**: `Docs/phase8/`
- **Purpose**: Next.js frontend application
- **Files**:
  - `package.json`, `next.config.js`, `tailwind.config.js`, `tsconfig.json`
  - `src/app/` - Next.js app structure
  - `src/lib/` - API clients and utilities
  - `src/types/` - TypeScript type definitions
  - `index.html`, `index-fixed.html` - Standalone HTML versions
  - `README.md`

## 🚀 Running the System

### Backend Server (Phase 7)
```bash
cd Docs/phase7
python simple-api.py
```
**Server**: http://localhost:8002

### Frontend Application (Phase 8)
```bash
cd Docs/phase8
# Option 1: Next.js development server
npm run dev

# Option 2: Simple HTML server
python -m http.server 8080
```
**Frontend**: http://localhost:8080/index-fixed.html

## 🎯 Live Example

**Test Parameters:**
- Location: Bellandur
- Budget: ₹2000
- Rating: 4.0+
- Top K: 5 restaurants

**Expected Output:**
1. Brahmin's Coffee Bar (⭐ 4.5, 💰 ₹400)
2. Barbeque Nation (⭐ 4.4, 💰 ₹1400)
3. Paradise (⭐ 4.3, 💰 ₹1100)
4. Meghana Foods (⭐ 4.2, 💰 ₹800)
5. Mainland China (⭐ 4.1, 💰 ₹1200)

## 📊 API Endpoints

### Health Check
```
GET http://localhost:8002/api/health
```

### Generate Recommendations
```
POST http://localhost:8002/api/recommendations
Content-Type: application/json

{
  "preferences": {
    "location": "Bellandur",
    "budget": {"min": 0, "max": 2000},
    "minimum_rating": 4.0,
    "cuisines": []
  },
  "top_k": 5,
  "include_explanations": true
}
```

### System Metadata
```
GET http://localhost:8002/api/metadata
```

## 🔄 Integration Flow

```
User Input (Frontend) → API Request → Backend Processing → LLM Integration → Response Generation → Frontend Display
```

## 📝 File Alignment

All files are properly aligned and readable:
- ✅ Python files have proper imports and structure
- ✅ TypeScript/JavaScript files are syntactically correct
- ✅ Configuration files are properly formatted
- ✅ Documentation files are complete and accurate
- ✅ No changes in output functionality

## 🛠️ Development Notes

- All phase folders are now under `Docs/` for better organization
- Original functionality remains unchanged
- File references and imports have been preserved
- System output and behavior are identical to previous version
- Git history is maintained with proper commit messages

## 📚 Additional Documentation

- **Architecture**: See `phase_wise_architecture.md`
- **Edge Cases**: See `edge_cases.md`
- **Problem Statement**: See `problemstatement.md`
- **Phase-specific READMEs**: Each phase folder contains detailed documentation

---

This documentation structure ensures all phases are properly organized while maintaining complete functionality and readability.
