import importlib
import pytest
from fastapi.testclient import TestClient
from tests.conftest import ROOT


def test_existing_server_and_routes(monkeypatch, tmp_path):
    monkeypatch.setenv('NETGUARD_LEGACY_MEMORY_PATH', str(tmp_path / 'legacy.json'))
    import demo.server as server
    server = importlib.reload(server)
    with TestClient(server.app) as client:
        assert client.get('/').status_code == 200
        for path in ['/api/stream/next', '/api/inject/normal', '/api/inject/neptune',
                     '/api/inject/apache_back', '/api/inject/portsweep']:
            response = client.get(path)
            assert response.status_code == 200, response.text
            assert 'event_id' in response.json()
        assert client.get('/api/memory').status_code == 200
        assert client.post('/api/memory/reset').json()['status'] == 'cleared'
        assert client.post('/api/memory/seed').status_code == 200
        custom = client.post('/api/analyze', json=dict(protocol_type='tcp', service='http',
            flag='SF', src_bytes=100, dst_bytes=200, mock_history_count=0))
        assert custom.status_code == 200
