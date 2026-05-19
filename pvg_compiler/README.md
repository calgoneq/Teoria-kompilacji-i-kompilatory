
# Procedural Vector Graphics (PVG) Compiler


## 1. Temat projektu

Kompilator autorskiego, proceduralnego języka opisu grafiki wektorowej (PVG) do formatu SVG.

## 2. Dane studentów

* **Wojciech Caldzudis: email - wcaldzudis@student.agh.edu.pl**
* **Radosław Kiełkowski: email - radusiekk@student.agh.edu.pl**

## 3. Założenia programu

### Ogólne cele programu

Celem projektu jest stworzenie kompilatora dla autorskiego, proceduralnego języka programowania służącego do generowania grafiki wektorowej. Język będzie dostarczał intuicyjnych instrukcji do rysowania kształtów geometrycznych na wirtualnym płótnie.

Dodatkowo język będzie w pełni proceduralny – przewidujemy implementację obsługi podstawowych operacji matematycznych, pętli sterujących (np. `for`, `while`) oraz możliwość definiowania i wywoływania własnych procedur z parametrami. Istotnym elementem projektu będzie również zaimplementowanie czytelnej obsługi błędów leksykalnych i składniowych, ułatwiającej użytkownikowi debugowanie kodu.

### Rodzaj translatora

Kompilator (kod źródłowy PVG -> Drzewo Składniowe AST -> kod docelowy SVG).

### Planowany wynik działania programu

Wynikiem działania kompilatora będzie wygenerowany, poprawny plik tekstowy w formacie **XML/SVG**, który można bezpośrednio otworzyć i wyrenderować w dowolnej przeglądarce internetowej lub programie graficznym.

### Planowany język implementacji

Python 3.x

### Sposób realizacji skanera i parsera

Analizator leksykalny (skaner) oraz analizator składniowy (parser) zostaną zaimplementowane przy użyciu zewnętrznego narzędzia: generatora **SLY** (Sly Lex-Yacc) dla języka Python.

---

## 4. Przykład użycia (Wstępny draft koncepcyjny)

**Kod wejściowy w języku PVG (`rysunek.pvg`):**

```text
canvas(800, 600);
background("#ffffff");

def rysuj_wzorzec(x, y, promien) {
    color("#ff0000");
    circle(x, y, promien);
    color("#000000");
    rect(x - promien, y - promien, promien * 2, promien * 2);
}

for (let i = 0; i < 5; i = i + 1) {
    rysuj_wzorzec(100 + i * 120, 300, 50);
}
```

**Spodziewany wynik (fragment pliku `rysunek.svg`):**

```xml
<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#ffffff" />
    <!-- Iteracja 1 -->
    <circle cx="100" cy="300" r="50" fill="#ff0000" />
    <rect x="50" y="250" width="100" height="100" fill="#000000" />
    <!-- Iteracja 2 -->
    <circle cx="220" cy="300" r="50" fill="#ff0000" />
    <!-- ... -->
</svg>
```

---

## 5. Gramatyka formatu (EBNF)

Obecna wersja gramatyki wspiera ponad 15 głównych produkcji, umożliwiając tworzenie zaawansowanych algorytmicznie grafik.

```ebnf
<program>       ::= <statements>
<statements>    ::= <statement> | <statements> <statement>
<statement>     ::= <simple_stmt> ";" | <compound_stmt>

<simple_stmt>   ::= <canvas_cmd> | <attr_cmd> | <shape_cmd> | <assign_stmt> | <print_stmt> | <call_stmt>
<compound_stmt> ::= <if_stmt> | <while_stmt> | <for_stmt> | <def_stmt>

<canvas_cmd>    ::= "canvas" "(" <expr> "," <expr> ")"
<attr_cmd>      ::= "background" "(" STR ")" | "color" "(" STR ")" | "stroke_width" "(" <expr> ")" | "opacity" "(" <expr> ")"
<shape_cmd>     ::= "circle" "(" <expr> "," <expr> "," <expr> ")"
                  | "rect" "(" <expr> "," <expr> "," <expr> "," <expr> ")"
                  | "line" "(" <expr> "," <expr> "," <expr> "," <expr> ")"
                  | "ellipse" "(" <expr> "," <expr> "," <expr> "," <expr> ")"

<if_stmt>       ::= "if" "(" <expr> ")" "{" <statements> "}" [ "else" "{" <statements> "}" ]
<while_stmt>    ::= "while" "(" <expr> ")" "{" <statements> "}"
<for_stmt>      ::= "for" "(" <simple_stmt> ";" <expr> ";" <simple_stmt> ")" "{" <statements> "}"
<def_stmt>      ::= "def" IDENT "(" <params> ")" "{" <statements> "}"

<expr>          ::= <expr> <op> <expr> | <math_func> "(" <expr> ")" | IDENT | NUMBER
<math_func>     ::= "sin" | "cos" | "sqrt"
```

---

## 6. PVG Studio (Webowe IDE / GUI)

**PVG Studio** to nowoczesne, interaktywne środowisko programistyczne (IDE) uruchamiane w przeglądarce, dedykowane do pracy z językiem PVG. Umożliwia pisanie kodu z natychmiastowym podglądem generowanej grafiki wektorowej oraz inspekcją wnętrza kompilatora.

### Główne cechy środowiska:
* **Edytor Kodu (Monaco Editor):** Posiada pełne podświetlanie składni PVG, inteligentne autouzupełnianie instrukcji (IntelliSense) oraz zaawansowany ciemny motyw.
* **Podgląd SVG na Żywo:** Natychmiastowe renderowanie wynikowego obrazu po kliknięciu przycisku *Compile*.
* **Inspektor Drzewa AST:** Graficzna, interaktywna wizualizacja drzewa składniowego generowanego przez parser.
* **Inspektor Tokenów:** Podgląd tabeli tokenów wygenerowanych przez lekser (wraz z ich klasyfikacją).
* **Galeria Przykładów:** Wbudowane, gotowe do uruchomienia programy demonstrujące możliwości języka (pętle, rekurencję, fraktale).

---
<img width="1908" height="947" alt="1" src="https://github.com/user-attachments/assets/734e3c0f-13aa-421f-bb32-248b30c113b9" />|<img width="1906" height="945" alt="image" src="https://github.com/user-attachments/assets/abb28a84-aded-473f-b1db-d48434ffa624" />
<img width="1909" height="940" alt="image" src="https://github.com/user-attachments/assets/8716768d-04a9-4517-b69f-fb07ee3de508" />|<img width="1914" height="946" alt="image" src="https://github.com/user-attachments/assets/e7f33d34-a27e-47e3-a004-93c7f46e159e" />



## 7. Jak uruchomić projekt (Instrukcja)

Projekt składa się z dwóch niezależnych części: backendu (FastAPI w Pythonie) oraz frontendu (Vite + React w Node.js).

### Krok 1: Uruchomienie Backend API (Python)

Backend odpowiada za tokenizację, parsowanie oraz kompilację kodu PVG do formatu SVG.

1. Przejdź do katalogu głównego projektu i zainstaluj wymagane pakiety Pythona:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Przejdź do katalogu `backend`:
   ```bash
   cd backend
   ```
3. Uruchom serwer FastAPI (domyślnie pod adresem `http://localhost:8000`):
   ```bash
   python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

### Krok 2: Uruchomienie Frontend (Vite + React)

Interfejs użytkownika (webowe IDE) komunikuje się z backendem w celu kompilacji kodu na żywo.

1. Przejdź do katalogu `frontend`:
   ```bash
   cd frontend
   ```
2. Zainstaluj wymagane zależności Node.js:
   ```bash
   npm install
   ```
3. Uruchom deweloperski serwer lokalny (domyślnie pod adresem `http://localhost:3000`):
   ```bash
   npm run dev
   ```
4. Otwórz przeglądarkę i wejdź na: **[http://localhost:3000](http://localhost:3000)**.
