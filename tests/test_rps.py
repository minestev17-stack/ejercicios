import sys
from pathlib import Path
from importlib import util

import pytest

# Cargar el módulo `rps` directamente desde src/rps.py usando importlib.
# Esto evita potenciales efectos secundarios si el archivo se ejecuta como
# script (protección: if __name__ == "__main__": main()).
module_path = Path(__file__).resolve().parents[1] / "src" / "rps.py"
spec = util.spec_from_file_location("rps_module_for_test", str(module_path))
rps = util.module_from_spec(spec)
spec.loader.exec_module(rps)
import random


def test_determine_result_all_combinations():
    """Comprueba todas las combinaciones posibles y compara contra la regla del juego."""
    wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    for user in rps.VALID_CHOICES:
        for cpu in rps.VALID_CHOICES:
            expected = (
                "draw" if user == cpu else ("win" if wins[user] == cpu else "lose")
            )
            assert rps.determine_result(user, cpu) == expected


def test_determine_result_case_insensitive():
    assert rps.determine_result("Rock", "SCISSORS") == "win"
    assert rps.determine_result("PAPER", "rock") == "win"
    assert rps.determine_result("scissors", "PAPER") == "win"


def test_play_valid_and_monkeypatched_random(monkeypatch):
    # Fuerza la CPU a elegir "scissors"
    monkeypatch.setattr(rps.random, "choice", lambda choices: "scissors")

    cpu_choice, result = rps.play("rock")
    assert cpu_choice == "scissors"
    assert result == "win"

    # Entrada con espacios y mayúsculas -> debe normalizar y funcionar
    cpu_choice2, result2 = rps.play("  Rock  ")
    assert cpu_choice2 == "scissors"
    assert result2 == "win"


def test_play_invalid_choice_raises():
    with pytest.raises(ValueError):
        rps.play("lizard")

    # cadena vacía tras strip -> inválida
    with pytest.raises(ValueError):
        rps.play("   ")


def test_play_cpu_choice_in_valid_choices(monkeypatch):
    # Asegurar que aunque elijo aleatoriamente, el valor retornado está en VALID_CHOICES
    monkeypatch.setattr(rps.random, "choice", lambda choices: "paper")
    cpu_choice, result = rps.play("scissors")
    assert cpu_choice in rps.VALID_CHOICES
    assert result in {"win", "lose", "draw"}
