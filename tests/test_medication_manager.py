import pytest
import sys
sys.path.append('src')
from medication_manager import MedicationManager

@pytest.fixture
def setup_medication_manager():
    return MedicationManager()

def test_add_medication(setup_medication_manager):
    manager = setup_medication_manager
    medication_id = manager.add_medication("Aspirina", "Alivia dolores", True)
    medications = manager.get_medications()
    assert len(medications) == 1
    assert medications[0]["name"] == "Aspirina"
    assert medications[0]["description"] == "Alivia dolores"
    assert medications[0]["available_online"] is True

def test_update_medication(setup_medication_manager):
    manager = setup_medication_manager
    medication_id = manager.add_medication("Aspirina", "Alivia dolores", True)
    manager.update_medication(medication_id, name="Ibuprofeno", description="Alivia inflamaciones")
    medication = manager.medications[medication_id]
    assert medication["name"] == "Ibuprofeno"
    assert medication["description"] == "Alivia inflamaciones"

def test_remove_medication(setup_medication_manager):
    manager = setup_medication_manager
    medication_id = manager.add_medication("Aspirina", "Alivia dolores", True)
    manager.remove_medication(medication_id)
    assert len(manager.medications) == 0

def test_medication_not_found(setup_medication_manager):
    manager = setup_medication_manager
    try:
        manager.remove_medication(999)  # Trying to remove a non-existing medication
    except ValueError as e:
        assert str(e) == "Medication with ID 999 does not exist."
