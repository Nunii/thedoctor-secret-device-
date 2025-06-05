from app.router.health import router

def test_router_contains_health():
    assert any(r.path == "/health" for r in router.routes)
