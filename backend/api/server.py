"""
API Server for React Frontend
Place this file at: api/server.py
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from services.orchestrator import MultiAgentOrchestrator
from config import Config

# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title="Multi-Agent News API",
    description="AI-powered news with 6 specialized agents",
    version="1.0.0"
)

# CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator
orchestrator = None


# ============================================
# MODELS
# ============================================

class NewsQueryRequest(BaseModel):
    query: str
    max_results: Optional[int] = 5
    enrich: Optional[bool] = True
    parallel: Optional[bool] = True


# ============================================
# STARTUP
# ============================================

@app.on_event("startup")
async def startup():
    global orchestrator
    print("🚀 Initializing Multi-Agent System...")
    orchestrator = MultiAgentOrchestrator(
        api_key=Config.GOOGLE_AI_STUDIO_KEY,
        show_loading=False  # No terminal animations for API
    )
    print("✅ API Server Ready!\n")


# ============================================
# ENDPOINTS
# ============================================

@app.get("/")
async def root():
    return {
        "service": "Multi-Agent News API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check"""
    if not orchestrator:
        raise HTTPException(503, "Service not initialized")
    
    health = orchestrator.health_check()
    return {
        "status": health['system'],
        "agents": health['agents']
    }


@app.post("/api/news/search")
async def search_news(request: NewsQueryRequest):
    """
    Main search endpoint
    
    Frontend sends:
    {
        "query": "AI news in India",
        "max_results": 5,
        "enrich": true,
        "parallel": true
    }
    
    Returns:
    {
        "success": true,
        "articles": [...],
        "metrics": {...}
    }
    """
    if not orchestrator:
        raise HTTPException(503, "Service not initialized")
    
    try:
        response = orchestrator.fetch_news(
            query=request.query,
            max_results=request.max_results,
            enrich=request.enrich,
            parallel=request.parallel
        )
        
        if not response['success']:
            raise HTTPException(400, response['message'])
        
        return {
            "success": True,
            "message": response['message'],
            "articles": response['data'],
            "metrics": response['metrics']
        }
    
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/news/preview")
async def get_preview(url: str):
    """
    Get article preview with image + text
    
    Frontend calls: /api/news/preview?url=https://...
    
    Returns:
    {
        "url": "...",
        "title": "...",
        "image": "https://...",
        "preview_text": "First paragraphs...",
        "author": "...",
        "source_domain": "..."
    }
    """
    if not url:
        raise HTTPException(400, "URL required")
    
    try:
        from newspaper import Article
        from urllib.parse import urlparse
        
        article = Article(url)
        article.download()
        article.parse()
        
        # First 500 chars as preview
        preview = article.text[:500] + "..." if len(article.text) > 500 else article.text
        
        return {
            "url": url,
            "title": article.title,
            "image": article.top_image,
            "preview_text": preview,
            "author": ", ".join(article.authors) if article.authors else None,
            "published": str(article.publish_date) if article.publish_date else None,
            "source_domain": urlparse(url).netloc
        }
    
    except Exception as e:
        return {
            "url": url,
            "title": "Preview unavailable",
            "image": None,
            "preview_text": "Could not extract preview.",
            "error": str(e)
        }


@app.get("/api/stats")
async def get_stats():
    """System statistics"""
    if not orchestrator:
        raise HTTPException(503, "Service not initialized")
    
    return {
        "system": orchestrator.get_system_metrics(),
        "agents": orchestrator.get_agent_metrics()
    }


# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*80)
    print("🚀 MULTI-AGENT NEWS API SERVER")
    print("="*80)
    print("📡 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("🔧 Health: http://localhost:8000/health")
    print("="*80 + "\n")
    
    uvicorn.run(
        "api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )