import pytest
from unittest.mock import patch, Mock
from my_cat import CatFactProcessor, APIError  # Импортируем из твоего основного файла

# Позитивный тест получения факта
@patch('my_cat.requests.get')
def test_get_fact_success(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"fact": "Cats sleep 70% of their lives"}
    mock_get.return_value = mock_response

    processor = CatFactProcessor()
    fact = processor.get_fact()

    assert fact == "Cats sleep 70% of their lives"
    assert processor.last_fact == "Cats sleep 70% of their lives"

# Негативный тест получения факта (ошибка запроса)
import requests

@patch('my_cat.requests.get')
def test_get_fact_failure(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Network error")  

    processor = CatFactProcessor()
    with pytest.raises(APIError) as exc_info:
        processor.get_fact()

    assert "Ошибка при запросе к API" in str(exc_info.value)


# Позитивный тест анализа факта
def test_get_fact_analysis_with_fact():
    processor = CatFactProcessor()
    processor.last_fact = "Cat"
    analysis = processor.get_fact_analysis()

    assert analysis["length"] == 3
    assert analysis["letter_frequencies"] == {"c": 1, "a": 1, "t": 1}

# Негативный тест анализа факта (факт отсутствует)
def test_get_fact_analysis_without_fact():
    processor = CatFactProcessor()
    analysis = processor.get_fact_analysis()

    assert analysis["length"] == 0
    assert analysis["letter_frequencies"] == {}
