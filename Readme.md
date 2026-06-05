# Riddler

Riddler to aplikacja konsolowa napisana w Pythonie, która wykorzystuje embeddingi językowe oraz model Sentence Transformers do wyszukiwania, rozwiązywania i odgadywania zagadek.

## Funkcje

- Rozwiązywanie zagadek podanych przez użytkownika.
- Wyszukiwanie zagadek na podstawie słowa kluczowego.
- Gra z systemem punktów i statystykami użytkowników.
- Ocena podobieństwa odpowiedzi z wykorzystaniem embeddingów semantycznych.
- Lokalne działanie bez połączenia z API.

## Wymagania

- Python 3.10+
- NumPy
- sentence-transformers

## Instalacja

```bash
pip install -r requirements.txt
```

## Uruchomienie

W katalogu projektu uruchom:

```bash
python main.py
```

## Dostępne tryby

### 1. Rozwiązywanie zagadek
Użytkownik podaje treść zagadki, a program:
- wyszukuje podobne zagadki w bazie,
- proponuje najbardziej pasujące odpowiedzi ze słownika.

### 2. Wyszukiwanie zagadek
Użytkownik podaje słowo, a program wyszukuje pasujące zagadki.

### 3. Gra
- logowanie użytkownika,
- pojedyncza zagadka,
- runda 5 zagadek,
- statystyki i rekordy.

## Źródła danych

Baza zawiera 354 zagadki pochodzące z dwóch zbiorów. Program korzysta również ze słownika zawierającego ponad 5000 rzeczowników.

## Model językowy

Program wykorzystuje lokalnie uruchamiany model:

`paraphrase-multilingual-MiniLM-L12-v2`

dzięki któremu możliwe jest rozpoznawanie odpowiedzi podobnych znaczeniowo, a nie tylko identycznych tekstowo.
