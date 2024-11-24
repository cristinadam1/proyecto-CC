# tests/test_logic.py

import pytest
from logic import Resident, generate_care_report

# Test para verificar la creación de un residente
def test_resident_creation():
    # Crear un residente y verificar sus atributos
    resident = Resident(name="Maria Sanchez", age=80)
    assert resident.name == "Maria Sanchez"
    assert resident.age == 80
    assert resident.medication_schedule == []

# Test para verificar que se puede añadir un medicamento a un residente
def test_add_medication():
    # Crear un residente y añadir medicamento
    resident = Resident(name="Juan Gonzalez", age=75)
    resident.add_medication("Ibuprofeno")
    assert "Ibuprofeno" in resident.medication_schedule

# Test para generar un reporte de cuidado con múltiples residentes
def test_generate_care_report():
    # Crear residentes con diferentes horarios de medicamentos
    resident1 = Resident(name="Maria Sanchez", age=80, medication_schedule=["Aspirina"])
    resident2 = Resident(name="Juan Gonzalez", age=75, medication_schedule=["Ibuprofeno"])
    
    # Generar el reporte de cuidado
    report = generate_care_report([resident1, resident2])
    
    # Verificaciones para asegurar que el reporte es correcto
    assert len(report) == 2  # Debe haber 2 residentes en el reporte
    assert report[0]["name"] == "Maria Sanchez"  # Verificar nombre del primer residente
    assert report[0]["medications"] == ["Aspirina"]  # Verificar medicamentos del primer residente
    assert report[1]["name"] == "Juan Gonzalez"  # Verificar nombre del segundo residente
    assert report[1]["medications"] == ["Ibuprofeno"]  # Verificar medicamentos del segundo residente

#Test para un residente sin medicamentos
def test_empty_medication_schedule():
    resident = Resident(name="Sonia Ruiz", age=65)
    assert resident.medication_schedule == [], "Medication schedule should be empty when no medications are added"

#Test para evitar añadir medicamentos duplicados
def test_adding_duplicate_medication():
    resident = Resident(name="Maria Sanchez", age=80)
    resident.add_medication("Aspirina")
    resident.add_medication("Aspirina")  # Duplicado
    assert resident.medication_schedule == ["Aspirina"], "Medication schedule should not have duplicates"

# Test para generar reporte de cuidado de un residente sin medicamentos
def test_care_report_for_resident_without_medications():
    resident = Resident(name="Alicia", age=70)
    report = generate_care_report([resident])
    assert len(report) == 1, "There should be one resident in the care report"
    assert report[0]["medications"] == [], "The medication list should be empty for a resident without medications"

# Test para manejar residentes con atributos inválidos
def test_resident_with_invalid_age():
    with pytest.raises(ValueError, match="Age cannot be negative"):
        Resident(name="Invalid Resident", age=-5)

