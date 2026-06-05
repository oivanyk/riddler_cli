# Dokumentacja projektu Riddler

## Opis projektu

Riddler jest aplikacją konsolową wykorzystującą embeddingi semantyczne do pracy z zagadkami. Program umożliwia:

1. Rozwiązywanie zagadek podanych przez użytkownika.
2. Wyszukiwanie zagadek dla podanego słowa.
3. Grę z punktacją i statystykami użytkowników.

Podstawą działania jest model Sentence Transformers, który zamienia tekst na wektory embeddingów. Dzięki temu możliwe jest porównywanie znaczenia tekstów za pomocą podobieństwa cosinusowego.

---

# Architektura projektu

## Struktura katalogów

```text
│   main.py
│   Readme.md
│   requirements.txt
│
├── baza_zagadek
├── models
├── slownik
└── user_data
```

---

# Dane

## Baza zagadek

Źródło 1:
- 66 zagadek

Źródło 2:
- 288 zagadek

Łącznie:
- 354 zagadki

Każda zagadka posiada:
- odpowiedź,
- treść zagadki,
- embedding odpowiedzi,
- embedding treści.

## Słownik

Zawiera około 5152 rzeczowników wraz z embeddingami.

## Dane użytkowników

Przechowywane są:

- liczba rozwiązanych zagadek,
- liczba nierozwiązanych zagadek,
- najlepszy wynik rundy,
- całkowita liczba punktów.

---

# Model NLP

Wykorzystany model:

paraphrase-multilingual-MiniLM-L12-v2

Model działa lokalnie i generuje embeddingi dla:

- zagadek,
- odpowiedzi,
- słownika,
- odpowiedzi użytkownika.

---

# Główne funkcje

## cos_similarity()

Oblicza podobieństwo cosinusowe pomiędzy dwoma wektorami.

Zastosowanie:
- porównywanie odpowiedzi,
- wyszukiwanie podobnych zagadek,
- wyszukiwanie podobnych słów.

## delete_dublic_matrix()

Usuwa duplikaty na podstawie wskazanej kolumny.

## solver()

Tryb rozwiązywania zagadek.

Działanie:
1. Użytkownik wpisuje zagadkę.
2. Tworzony jest embedding.
3. Program wyszukuje podobne zagadki.
4. Program wyszukuje podobne odpowiedzi.
5. Wyniki są sortowane według podobieństwa.

## finder()

Tryb wyszukiwania zagadek.

Działanie:
1. Użytkownik podaje słowo.
2. Tworzony jest embedding.
3. Program wyszukuje najbardziej podobne odpowiedzi.
4. Wyświetlane są odpowiadające im zagadki.

## one_game()

Obsługuje pojedynczą rozgrywkę.

Punktacja:

- 1 próba: +5 pkt
- 2 próba: +3 pkt
- 3 próba: +1 pkt
- brak odpowiedzi: -1 pkt

Próg poprawnej odpowiedzi:

SIM_THRESHOLD = 0.92

## game()

Obsługuje:
- logowanie,
- tworzenie kont,
- statystyki,
- rundy,
- zapisywanie wyników.

---

# Algorytm oceny odpowiedzi

1. Odpowiedź użytkownika zamieniana jest na embedding.
2. Pobierany jest embedding poprawnej odpowiedzi.
3. Liczone jest podobieństwo cosinusowe.
4. Jeśli wynik >= 0.92 odpowiedź uznawana jest za poprawną.

Dzięki temu akceptowane są odpowiedzi bliskoznaczne.

---

# Mocne strony projektu

- wykorzystanie NLP zamiast zwykłego porównania tekstów,
- lokalne działanie,
- własna baza zagadek,
- system użytkowników,
- statystyki i rekordy,
- obsługa wielu poprawnych odpowiedzi.

---

# Co można poprawić

## Optymalizacja

Obecnie wiele operacji wykonywanych jest w pętlach Pythonowych.

Można:
- wykorzystać wektoryzację NumPy,
- znormalizować embeddingi,
- użyć FAISS do wyszukiwania najbliższych sąsiadów.

## Architektura

Podzielić projekt na moduły:

```text
main.py
game.py
finder.py
solver.py
utils.py
database.py
```

## Funkcjonalności

- ranking użytkowników,
- poziomy trudności,
- podpowiedzi,
- panel administratora,
- dodawanie własnych zagadek,
- eksport statystyk,
- GUI (Tkinter lub PyQt),
- aplikacja webowa (Flask/FastAPI),
- API REST.

## Jakość kodu

Warto:
- dodać type hints,
- napisać testy jednostkowe,
- użyć loggera zamiast printów,
- zastąpić pliki .npy bazą SQLite.

