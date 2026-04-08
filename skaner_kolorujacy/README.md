# Skaner z kolorowaniem składni

## Dokumentacja i Specyfikacja Formatu MiniScript

**Autorzy:** Wojciech Caldzudis, Radosław Kiełkowski

---

### 1. Cel zadania

Celem zadania było zaprojektowanie własnego formatu tekstowego (języka MiniScript) oraz implementacja analizatora leksykalnego, który przetworzy plik źródłowy na format HTML z zachowaniem kolorowania składni oraz oryginalnego układu znaków (spacje, tabulacje, nowe linie).

### 2. Specyfikacja formatu MiniScript

Język MiniScript to uproszczony język programowania obsługujący:

* **Słowa kluczowe:** `fun`, `let`, `if`, `else`, `while`, `for`, `return`, `print` itd.
* **Typy danych:** Liczby całkowite (INT), zmiennoprzecinkowe (FLOAT), łańcuchy znaków w cudzysłowach (STRING).
* **Komentarze:** Jednoliniowe (zaczynające się od `#`) oraz blokowe (pomiędzy `/*` a `*/`).
* **Operatory:** Arytmetyczne (`+`, `-`, `*`, `/`, `%`), porównania (`==`, `!=`, `<=`, `>=`) oraz strzałkę funkcyjną (`->`).

### 3. Tabela Tokenów

| Kategoria                 | Kod tokena               | Wzorzec (RegEx)                          | Kolor w HTML  |
| :------------------------ | :----------------------- | :--------------------------------------- | :------------ |
| **Słowa kluczowe** | `KEYWORD`              | `fun`, `let`, `if`, `else`...    | Fioletowy     |
| **Identyfikatory**  | `IDENT`                | `[a-zA-Z_][a-zA-Z0-9_]*`               | Czerwony      |
| **Liczby**          | `INT` / `FLOAT`      | `[0-9]+(\.[0-9]+)?`                    | Pomarańczowy |
| **Łańcuchy**      | `STRING`               | `".*?"`                                | Zielony       |
| **Komentarze**      | `COMMENT`              | `#...` lub `/*...*/`                 | Szary         |
| **Operatory**       | `OPERATOR` / `ARROW` | `+`, `-`, `==`, `->` ...         | Cyjan         |
| **Ograniczniki**    | `DELIMITER`            | `(`, `)`, `{`, `}`, `,`, `;` | Jasny Szary   |
| **Błąd**          | `ERROR`                | Każdy inny znak (np.`@`)              | Czerwone tło |

### 4. Implementacja Skanera

Analizator leksykalny został zaimplementowany jako **automat skończony** (klasa `AutomatSkanera`). Skaner czyta tekst znak po znaku i przechodzi między stanami (np. `STAN_LICZBA`, `STAN_LANCUCH`).

* **Ważna cecha:** Skaner nie ignoruje białych znaków, lecz pakuje je do specjalnego tokena `WHITESPACE`, co pozwala na wierne odtworzenie struktury pliku w formacie wyjściowym.

### 5. Instrukcja obsługi

Program uruchamiany jest z linii komend, przyjmując ścieżkę do pliku wejściowego oraz nazwę generowanego pliku HTML.

**Uruchomienie:**

```bash
python kolorowanie.py przyklad.ms wynik.html
```

### 6. Zawartość folderu

* `kolorowanie.py` - Główny skrypt skanera i generatora HTML.
* `przyklad.ms` - Przykładowy plik źródłowy MiniScript.
* `wynik.html` - Wygenerowany raport z pokolorowaną składnią.
* 
* `.png` - (Należy dołączyć) Schemat graficzny automatu stanów.
