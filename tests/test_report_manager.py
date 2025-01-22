import pytest
import sys
sys.path.append('src')
from report_manager import ReportManager
from adherence_manager import AdherenceManager
from resident_manager import ResidentManager
from medication_manager import MedicationManager

@pytest.fixture
def setup_report_manager():
    resident_manager = ResidentManager()
    medication_manager = MedicationManager()
    adherence_manager = AdherenceManager()
    report_manager = ReportManager(adherence_manager, resident_manager)
    return report_manager, resident_manager, adherence_manager

def test_generate_resident_report(setup_report_manager):
    report_manager, resident_manager, adherence_manager = setup_report_manager
    resident_id = resident_manager.add_resident("Maria Sanchez", 80, "123-456-789")
    adherence_manager.log_medication(resident_id, "2025-01-22 09:00:00", True)
    adherence_manager.log_medication(resident_id, "2025-01-23 09:00:00", False)
    report = report_manager.generate_resident_report(resident_id)
    assert report["adherencia"] == 50.0

def test_generate_global_report(setup_report_manager):
    report_manager, resident_manager, adherence_manager = setup_report_manager
    resident_id_1 = resident_manager.add_resident("Maria Sanchez", 80, "123-456-789")
    resident_id_2 = resident_manager.add_resident("Juan Perez", 70, "987-654-321")
    adherence_manager.log_medication(resident_id_1, "2025-01-22 09:00:00", True)
    adherence_manager.log_medication(resident_id_1, "2025-01-23 09:00:00", False)
    adherence_manager.log_medication(resident_id_2, "2025-01-22 09:00:00", True)
    reports = report_manager.generate_global_report()
    assert len(reports) == 2
    assert reports[0]["adherencia"] == 50.0
    assert reports[1]["adherencia"] == 100.0
