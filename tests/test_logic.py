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

