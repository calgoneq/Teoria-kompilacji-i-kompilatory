# Teoria Kompilacji i Kompilatory (TKiK)

Repozytorium zawiera realizację zadań laboratoryjnych oraz projekt semestralny z przedmiotu "Teoria kompilacji i kompilatory" prowadzonego przez **dr inż. Jacka Piwowarczyka**.

---

## Autorzy

* **Wojciech Caldzudis: email - wcaldzudis@student.agh.edu.pl**
* **Radosław Kiełkowski: email - radusiekk@student.agh.edu.pl**

---

## Zawartość Repozytorium

### 1. [Skaner Matematyczny (Zadanie 2)](./skaner_prosty/)

Prosty analizator leksykalny wyrażeń matematycznych zaimplementowany jako automat stanów w języku Python.

* **Zakres:** Tokenizacja liczb, identyfikatorów i operatorów, obsługa błędów, lokalizacja kolumny.

### 2. [Kolorowanie Składni (Zadanie 3)](./skaner_kolorujacy/)

Skaner zaimplementowany jako automat skończony, generujący plik HTML z pokolorowaną składnią autorskiego formatu `MiniScript`.

* **Zakres:** Diagram przejść (DFA), tabela tokenów, zachowanie układu tekstu wejściowego.

### 3. [Projekt: PVG Compiler (Projekt Semestralny)](./pvg_compiler/)

Główny projekt przedmiotu: Kompilator proceduralnego języka opisu grafiki wektorowej (**PVG**) do formatu **SVG**.

* **Technologia:** Python 3.x, generator parserów **SLY** (Sly Lex-Yacc).
* **Status:** W trakcie rozwoju (Etap: Implementacja gramatyki i parsera - Temat 7)

---

## Technologie i Narzędzia

* **Język:** Python 3.13+
* **Biblioteki:** SLY (Sly Lex-Yacc)
* **Dokumentacja:** Markdown, LaTeX, Mermaid (diagramy)

---

## Jak uruchomić skanery?

Szczegółowe instrukcje dotyczące uruchamiania poszczególnych modułów znajdują się w ich dedykowanych folderach.

```bash
# Przykład dla skanera kolorującego:
python skaner_kolorujacy/kolorowanie.py przyklad.ms wynik.html
```
