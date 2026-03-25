# Tabela Tokenów

| Kategoria | Kod tokena | Wzorzec / Opis | Kolor CSS |
|---|---|---|---|
| **Słowa kluczowe** | `KEYWORD` | `fun`, `let`, `if`, `else`, `while`, `for`, `return`, `print`, `true`, `false`, `null`, `and`, `or`, `not` | `#c678dd` (fioletowy) |
| **Identyfikatory** | `IDENT` | Litera lub `_`, potem litery, cyfry, `_` | `#e06c75` (czerwony) |
| **Liczby całkowite** | `INT` | Ciąg cyfr: `0-9+` | `#d19a66` (pomarańczowy) |
| **Liczby zmiennoprzecinkowe** | `FLOAT` | Cyfry + `.` + cyfry: `0-9+.0-9+` | `#d19a66` (pomarańczowy) |
| **Łańcuchy znaków** | `STRING` | Tekst w cudzysłowach: `"..."` | `#98c379` (zielony) |
| **Komentarz liniowy** | `COMMENT` | Od `#` do końca linii | `#5c6370` (szary) |
| **Komentarz blokowy** | `COMMENT` | Od `/*` do `*/` | `#5c6370` (szary) |
| **Operator arytmetyczny** | `OPERATOR` | `+`, `-`, `*`, `/`, `%` | `#56b6c2` (cyjan) |
| **Operator porównania** | `OPERATOR` | `==`, `!=`, `<`, `>`, `<=`, `>=` | `#56b6c2` (cyjan) |
| **Operator przypisania** | `OPERATOR` | `=` | `#56b6c2` (cyjan) |
| **Strzałka** | `ARROW` | `->` | `#56b6c2` (cyjan) |
| **Ograniczniki** | `DELIMITER` | `(`, `)`, `{`, `}`, `[`, `]`, `,`, `;`, `:` | `#abb2bf` (jasny szary) |
| **Białe znaki** | `WHITESPACE` | Spacje, tabulatory, nowe linie | — (zachowane bez koloru) |
| **Błąd** | `ERROR` | Nierozpoznany znak | `#ff0000` (czerwony tło) |