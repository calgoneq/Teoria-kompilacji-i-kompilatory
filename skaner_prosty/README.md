# Skaner Leksykalny (Wyrażenia matematyczne)

## Dokumentacja i Spis Tokenów

**Autorzy:** Wojciech Caldzudis, Radosław Kiełkowski

---

### 1. Język implementacji

Skaner leksykalny został zaimplementowany w języku **Python 3.13.2**. Zgodnie z założeniami projektu, implementacja opiera się na ręcznie zbudowanym automacie skończonym (maszynie stanów), bez użycia zewnętrznych generatorów skanerów oraz bez użycia bibliotek do wyrażeń regularnych wewnątrz logiki sterującej procesem skanowania.

### 2. Spis tokenów (Legenda)

Poniższa tabela stanowi formalną specyfikację symboli leksykalnych rozpoznawanych przez skaner dla wyrażenia matematycznego (np. `2+3*(76+8/3)+ 3*(9-3)`).

| Kod tokena | Opis (znaczenie)               | Wyrażenie regularne           | Atrybuty           |
| :--------- | :----------------------------- | :----------------------------- | :----------------- |
| `INT`    | Liczba całkowita (ciąg cyfr) | `[0-9]+`                     | Wartość liczbowa |
| `ID`     | Identyfikator (zmienna, nazwa) | `[a-zA-Z][a-zA-Z0-9]*`       | Nazwa (string)     |
| `PLUS`   | Operator dodawania             | `+`                          | brak               |
| `MINUS`  | Operator odejmowania           | `-`                          | brak               |
| `MUL`    | Operator mnożenia             | `*`                          | brak               |
| `DIV`    | Operator dzielenia             | `/`                          | brak               |
| `LPAREN` | Nawias otwierający            | `(`                          | brak               |
| `RPAREN` | Nawias zamykający             | `)`                          | brak               |
| `EOF`    | Koniec strumienia wejściowego | *(End of File)*              | brak               |
| `ERROR`  | Nierozpoznany znak (błąd)    | `[^a-zA-Z0-9\+\-\*\/\(\)\s]` | Błędny znak      |

### 3. Opis struktury tokena

Każdy rozpoznany element jest reprezentowany jako obiekt klasy `Token`, przechowujący:

* **Typ (Kod):** Kategoria tokena (np. `INT`, `PLUS`).
* **Wartość:** Tekstowa reprezentacja wycięta z wejścia.
* **Lokalizacja:** Numer kolumny, na której zaczyna się dany token (kluczowe do raportowania błędów).

### 4. Znaki pomijane (Białe znaki)

Skaner ignoruje spacje, tabulacje oraz znaki nowej linii (`[ \t\n\r]+`). Przy napotkaniu tych znaków wskaźnik pozycji jest przesuwany, ale obiekt `Token` nie jest generowany.

### 5. Instrukcja uruchomienia

Aby uruchomić skaner i przetestować przykładowe wyrażenie matematyczne (zawierające błąd leksykalny dla testu lokalizacji błędu), należy wykonać polecenie:

```bash
python skaner.py
```

Program wypisze na konsoli listę znalezionych tokenów w formacie `(Kod, Wartość)` wraz z informacją o kolumnie rozpoczęcia każdego z nich.
