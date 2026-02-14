# Vector Search - Quick Start

## 1️⃣ Build Index

```bash
# Test with 3 papers first
python build_index.py --summaries temp_summaries.jsonl

# Build full index
python build_index.py --summaries summaries.jsonl

# Incremental update (auto-resume if failed)
python build_index.py --summaries summaries.jsonl

# Force rebuild from scratch
python build_index.py --summaries summaries.jsonl --force-rebuild
```

### Build Parameters
```bash
python build_index.py \
  --summaries PATH          # JSONL file (default: summaries.jsonl)
  --chunk-size INT          # Text chunk size (default: 2500)
  --chunk-overlap INT       # Chunk overlap (default: 300)
  --embedding-model STR     # Ollama model (default: embeddinggemma:300m)
  --batch-size INT          # Papers per save (default: 3)
  --force-rebuild           # Rebuild from scratch
```

**Index Location:** `vector_indices/chunk{size}_overlap{overlap}_model_{model}/`

---

## 2️⃣ Serve API

```bash
# Find your index directory
ls vector_indices/

# Start server
python serve_search.py --index-dir vector_indices/chunk2500_overlap300_model_embeddinggemma_300m
```

### Serve Parameters
```bash
python serve_search.py \
  --index-dir PATH          # Required: index directory path
  --host STR                # Bind host (default: 0.0.0.0)
  --port INT                # Bind port (default: 5001)
```

---

## 3️⃣ API Usage

### Search
```python
import requests

response = requests.post('http://localhost:5001/search', json={
    'query': 'transformer architecture',
    'k': 5,                                      # optional, default 5
    'return_fields': ['title', 'url'],           # optional, all if not specified
    'return_scores': True                        # optional, default true
})

results = response.json()
```

### Endpoints
- `GET /health` - Health check
- `GET /metadata_fields` - List all available metadata fields
- `GET /stats` - Index statistics
- `POST /search` - Search (see above)

---

## ⚡ Key Features

- **Incremental updates** - Only processes new papers
- **Auto-resume** - Saves every N papers (default: 3)
- **Dual indexing** - Both PDF original text + AI summary
- **Hybrid search** - Vector (FAISS) + Keyword (BM25)
- **Flexible metadata** - Handles missing fields gracefully
