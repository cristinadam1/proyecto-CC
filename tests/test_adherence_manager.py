import pytest
import sys
sys.path.append('src')
from adherence_manager import AdherenceManager

@pytest.fixture
def setup_adherence_manager():
    return AdherenceManager()

def test_log_medication(setup_adherence_manager):
    manager = setup_adherence_manager
    manager.log_medication(1, "2025-01-22 09:00:00", True)
    logs = manager.medication_logs[1]
    assert len(logs) == 1
    assert logs[0]["timestamp"] == "2025-01-22 09:00:00"
    assert logs[0]["taken"] is True

def test_calculate_adherence(setup_adherence_manager):
    manager = setup_adherence_manager
    manager.log_medication(1, "2025-01-22 09:00:00", True)
    manager.log_medication(1, "2025-01-23 09:00:00", False)
    adherence = manager.calculate_adherence(1)
    assert adherence == 50.0  # 1 taken, 1 missed

def test_generate_alerts(setup_adherence_manager):
    manager = setup_adherence_manager
    manager.log_medication(1, "2025-01-22 09:00:00", False)
    alerts = manager.generate_alerts(1)
    assert len(alerts) == 1
    assert alerts[0]["message"] == "El residente ha omitido su medicación."
