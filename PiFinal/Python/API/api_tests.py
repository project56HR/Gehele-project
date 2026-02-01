"""
Unit tests for the Wind Generator Stats FastAPI application.
Tests all API endpoints with various scenarios including edge cases.
"""
from datetime import datetime
from unittest.mock import Mock
import pytest
import threading
from starlette.testclient import TestClient

lock = threading.Lock()

# Import the app and dependencies
from main import app, get_db


# Mock DatabaseManager for testing
class MockDatabaseManager:
    """Mock DatabaseManager to avoid actual database connections during testing."""

    def __init__(self, *args, **kwargs):
        self.mock_query = Mock()

    def startDB(self):
        pass

    def createTables(self):
        pass

    def closeDB(self):
        pass

    def table(self, table_name):
        """Return a mock query builder."""
        self.mock_query.table_name = table_name
        return self.mock_query


@pytest.fixture
def mock_db():
    """Fixture to provide a mock database."""
    return MockDatabaseManager()


@pytest.fixture
def client(mock_db):
    """Fixture to provide a test client with mocked database."""

    def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def mock_query_builder():
    """Fixture to provide a mock query builder with chaining methods."""
    mock = Mock()

    # Make all query builder methods return self for chaining
    for method in ["select", "where", "groupBy", "orderBy", "sum", "avg", "count", "get"]:
        setattr(mock, method, Mock(return_value=mock))

    return mock

class TestVoltageEndpoints:
    """Tests for voltage-related endpoints (average)."""

    def test_get_voltage_by_hour(self, client, mock_db, mock_query_builder):
        # Setup mock data
        mock_data = [{"value": 12.5}, {"value": 15.0}, {"value": 13.0}]
        mock_query_builder.get.return_value = mock_data
        mock_db.mock_query = mock_query_builder

        response = client.get("/get/voltage/day/15-01-2024")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(isinstance(x, dict) for x in data)

    def test_get_voltage_by_hour_invalid_date(self, client):
        response = client.get("/get/voltage/day/2024-01-15")
        assert response.status_code == 400

    def test_get_voltage_by_day_of_week(self, client, mock_db, mock_query_builder):
        mock_data = [{"value": 12.5}, {"value": 15.0}]
        mock_query_builder.get.return_value = mock_data
        mock_db.mock_query = mock_query_builder

        response = client.get("/get/voltage/week/15-01-2024")
        assert response.status_code == 200

    def test_get_voltage_by_month(self, client, mock_db, mock_query_builder):
        mock_data = [{"value": 1250.5}, {"value": 1350.5}]
        mock_query_builder.get.return_value = mock_data
        mock_db.mock_query = mock_query_builder

        response = client.get("/get/voltage/year/15-01-2024")
        assert response.status_code == 200


class TestAmpEndpoints:
    """Tests for amp-related endpoints (average)."""

    def test_get_amp_by_hour(self, client, mock_db, mock_query_builder):
        mock_data = [{"value": 2.5}, {"value": 3.0}]
        mock_query_builder.get.return_value = mock_data
        mock_db.mock_query = mock_query_builder

        response = client.get("/get/amp/day/15-01-2024")
        assert response.status_code == 200

    def test_get_amp_by_day_of_week(self, client, mock_db, mock_query_builder):
        mock_data = [{"value": 2.5}, {"value": 3.0}]
        mock_query_builder.get.return_value = mock_data
        mock_db.mock_query = mock_query_builder

        response = client.get("/get/amp/week/15-01-2024")
        assert response.status_code == 200

    def test_get_amp_by_month(self, client, mock_db, mock_query_builder):
        mock_data = [{"value": 25.0}, {"value": 30.0}]
        mock_query_builder.get.return_value = mock_data
        mock_db.mock_query = mock_query_builder

        response = client.get("/get/amp/year/15-01-2024")
        assert response.status_code == 200


class TestWattEndpoints:
    """Tests for watt endpoints (kWh)."""

    def test_get_watt_by_hour(self, client, mock_db, mock_query_builder):
        mock_data = [
            {"value": 100, "created_at": datetime(2024, 1, 15, 0, 0)},
            {"value": 200, "created_at": datetime(2024, 1, 15, 0, 30)},
        ]
        mock_query_builder.get.return_value = mock_data
        mock_db.mock_query = mock_query_builder

        response = client.get("/get/watt/day/15-01-2024")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(isinstance(x, dict) for x in data)

    def test_get_watt_by_week(self, client, mock_db, mock_query_builder):
        mock_data = [
            {"value": 150, "created_at": datetime(2024, 1, 10)},
            {"value": 200, "created_at": datetime(2024, 1, 11)},
        ]
        mock_query_builder.get.return_value = mock_data
        mock_db.mock_query = mock_query_builder

        response = client.get("/get/watt/week/15-01-2024")
        assert response.status_code == 200

    def test_get_watt_by_month(self, client, mock_db, mock_query_builder):
        mock_data = [
            {"value": 150, "created_at": datetime(2024, 1, 1)},
            {"value": 200, "created_at": datetime(2024, 2, 1)},
        ]
        mock_query_builder.get.return_value = mock_data
        mock_db.mock_query = mock_query_builder

        response = client.get("/get/watt/year/15-01-2024")
        assert response.status_code == 200


class TestDateParsing:
    """Tests for date parsing edge cases."""

    def test_invalid_day_for_month(self, client):
        response = client.get("/get/voltage/day/31-02-2024")
        assert response.status_code == 400

    def test_valid_leap_year(self, client, mock_db, mock_query_builder):
        mock_query_builder.get.return_value = [{"value": 12.0}]
        mock_db.mock_query = mock_query_builder

        response = client.get("/get/voltage/day/29-02-2024")
        assert response.status_code == 200


# Run tests with: pytest test_main.py -v
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
