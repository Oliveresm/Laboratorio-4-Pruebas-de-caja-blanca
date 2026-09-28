import pytest
import process_grades

# =====================================================================
# ACTIVIDAD 1 & 2: Cobertura de Sentencias y Decisiones
# =====================================================================

@pytest.mark.parametrize(
    'students, expected_passed, expected_failed, expected_recovery_log, expected_no_grades_log',
    [
        # Rama 1: Aprobado (average > 70)
        (
            [{'name': 'Ana', 'grades': [80, 85, 90]}],
            ['Ana'], [], False, False
        ),
        # Rama 2: Recuperación (50 <= average <= 70)
        (
            [{'name': 'Carlos', 'grades': [60, 60, 60]}],
            [], [], True, False
        ),
        # Rama 3: Reprobado (average < 50)
        (
            [{'name': 'Luis', 'grades': [40, 30, 40]}],
            [], ['Luis'], False, False
        ),
        # Rama 4: Sin notas (grades == None, tal como lo tiene implementado el if)
        (
            [{'name': 'Sofia', 'grades': None}],
            [], [], False, True
        ),
    ]
)
@pytest.mark.branch_coverage
def test_branches(students, expected_passed, expected_failed, expected_recovery_log, expected_no_grades_log, capsys):
    result = process_grades.process_grades(students)
    captured = capsys.readouterr()

    assert result['passed'] == expected_passed
    assert result['failed'] == expected_failed

    if expected_recovery_log:
        assert "is in recovery" in captured.out

    if expected_no_grades_log:
        assert "has no grades" in captured.out


# =====================================================================
# ACTIVIDAD 3: Cobertura de Caminos (Path Coverage)
# =====================================================================

@pytest.mark.parametrize(
    'students, expected_result, expected_printed_logs',
    [
        # Camino completo con flujo múltiple
        (
            [
                {'name': 'Ana', 'grades': [80, 90, 85]},    # > 70 (Aprobada)
                {'name': 'Luis', 'grades': [60, 65, 55]},   # >= 50 (Recuperación en print)
                {'name': 'Marta', 'grades': [40, 35, 30]},   # < 50 (Reprobada)
                {'name': 'Jorge', 'grades': None}           # grades == None (Omitido)
            ],
            {
                'passed': ['Ana'],
                'failed': ['Marta'],
                'overall_average': 0  # Da 0 debido a que # counter += 1 está comentado
            },
            ['Luis is in recovery', 'Student Jorge has no grades']
        ),
        # Camino: Lista vacía
        (
            [],
            {
                'passed': [],
                'failed': [],
                'overall_average': 0
            },
            []
        )
    ]
)
@pytest.mark.path_coverage
def test_full_paths(students, expected_result, expected_printed_logs, capsys):
    result = process_grades.process_grades(students)
    captured = capsys.readouterr()

    assert result == expected_result
    for log in expected_printed_logs:
        assert log in captured.out


# =====================================================================
# TEST DE DETECCIÓN DE DEFECTO (Objetivo 4 de la práctica)
# =====================================================================
def test_bug_empty_list_causes_zero_division():
    """Valida la falla encontrada: grades=[] provoca ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        process_grades.process_grades([{'name': 'Jorge', 'grades': []}])