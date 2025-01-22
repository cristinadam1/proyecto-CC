import pytest
from src.resident_manager import ResidentManager

@pytest.fixture
def setup_resident_manager():
    return ResidentManager()

def test_add_resident(setup_resident_manager):
    manager = setup_resident_manager
    resident_id = manager.add_resident("Maria Sanchez", 80, "123-456-789")
    residents = manager.get_residents()
    assert len(residents) == 1
    assert residents[0]["name"] == "Maria Sanchez"
    assert residents[0]["age"] == 80
    assert residents[0]["contact"] == "123-456-789"

def test_update_resident(setup_resident_manager):
    manager = setup_resident_manager
    resident_id = manager.add_resident("Maria Sanchez", 80, "123-456-789")
    manager.update_resident(resident_id, name="Maria Lopez")
    resident = manager.residents[resident_id]
    assert resident["name"] == "Maria Lopez"

def test_remove_resident(setup_resident_manager):
    manager = setup_resident_manager
    resident_id = manager.add_resident("Maria Sanchez", 80, "123-456-789")
    manager.remove_resident(resident_id)
    assert len(manager.residents) == 0

def test_resident_not_found(setup_resident_manager):
    manager = setup_resident_manager
    try:
        manager.remove_resident(999)  # Trying to remove a non-existing resident
    except ValueError as e:
        assert str(e) == "Resident with ID 999 does not exist."
