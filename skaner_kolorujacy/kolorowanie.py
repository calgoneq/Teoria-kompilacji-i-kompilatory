"""
Kolorowanie składni dla języka MiniScript.
Program wczytuje plik źródłowy, tokenizuje go za pomocą automatu stanów
i generuje plik HTML z pokolorowaną składnią, zachowując układ tekstu.

Użycie:
    python3 kolorowanie.py <plik_wejściowy> <plik_wyjściowy.html>

Autor: Student TKIK
"""

import sys


# ============================================================
#  Definicje tokenów i kolorów
# ============================================================

SLOWA_KLUCZOWE = {
    "fun", "let", "if", "else", "while", "for",
    "return", "print", "true", "false", "null",
    "and", "or", "not"
}

KOLORY_CSS = {
    "KEYWORD":   "color: #c678dd; font-weight: bold;",   # fioletowy
    "IDENT":     "color: #e06c75;",                       # czerwony
    "INT":       "color: #d19a66;",                       # pomarańczowy
    "FLOAT":     "color: #d19a66;",                       # pomarańczowy
    "STRING":    "color: #98c379;",                       # zielony
    "COMMENT":   "color: #5c6370; font-style: italic;",   # szary kursywą
    "OPERATOR":  "color: #56b6c2;",                       # cyjan
    "ARROW":     "color: #56b6c2;",                       # cyjan
    "DELIMITER": "color: #abb2bf;",                       # jasny szary
    "ERROR":     "color: #ff0000; background: #3e1111;",  # czerwony z tłem
}

OPERATORY_POJEDYNCZE = set("+-*%")
OGRANICZNIKI = set("(){}[],;:")


# ============================================================
#  Klasa Token
# ============================================================

class Token:
    """Przechowuje informacje o jednym tokenie."""

    __slots__ = ("typ", "tresc")

    def __init__(self, typ: str, tresc: str):
        self.typ = typ
        self.tresc = tresc

    def __repr__(self):
        return f"Token({self.typ}, {self.tresc!r})"


# ============================================================
#  Automat skanujący (state machine)
# ============================================================

class AutomatSkanera:
    """
    Analizator leksykalny oparty na automacie stanów.
    Przetwarza tekst źródłowy na listę tokenów,
    zachowując białe znaki w celu odtworzenia układu.
    """

    # Stany automatu
    STAN_START = "START"
    STAN_IDENTYFIKATOR = "IDENTYFIKATOR"
    STAN_LICZBA = "LICZBA"
    STAN_LICZBA_ULAMEK = "LICZBA_ULAMEK"
    STAN_LANCUCH = "LANCUCH"
    STAN_KOMENTARZ_LINIOWY = "KOMENTARZ_LINIOWY"
    STAN_KOMENTARZ_BLOKOWY = "KOMENTARZ_BLOKOWY"

    def __init__(self, kod_zrodlowy: str):
        self.zrodlo = kod_zrodlowy
        self.dlug = len(kod_zrodlowy)
        self.poz = 0

    # --- metody pomocnicze ---

    def _obecny(self) -> str | None:
        """Zwraca bieżący znak bez przesuwania wskaźnika."""
        if self.poz < self.dlug:
            return self.zrodlo[self.poz]
        return None

    def _nastepny(self) -> str | None:
        """Podgląda następny znak (poz + 1)."""
        idx = self.poz + 1
        if idx < self.dlug:
            return self.zrodlo[idx]
        return None

    def _konsumuj(self) -> str:
        """Pobiera bieżący znak i przesuwa wskaźnik."""
        zn = self.zrodlo[self.poz]
        self.poz += 1
        return zn

    # --- główna pętla automatu ---

    def skanuj(self) -> list[Token]:
        """Przetwarza cały tekst i zwraca listę tokenów."""
        tokeny: list[Token] = []

        while self.poz < self.dlug:
            zn = self._obecny()

            # ── Białe znaki (zachowujemy) ──
            if zn in (" ", "\t", "\n", "\r"):
                bufor = self._konsumuj()
                while self._obecny() in (" ", "\t", "\n", "\r"):
                    bufor += self._konsumuj()
                tokeny.append(Token("WHITESPACE", bufor))
                continue

            # ── Komentarz liniowy (#) ──
            if zn == "#":
                bufor = self._konsumuj()
                while self._obecny() is not None and self._obecny() != "\n":
                    bufor += self._konsumuj()
                tokeny.append(Token("COMMENT", bufor))
                continue

            # ── Możliwy komentarz blokowy lub operator / ──
            if zn == "/":
                if self._nastepny() == "*":
                    tokeny.append(self._skanuj_komentarz_blokowy())
                else:
                    self._konsumuj()
                    tokeny.append(Token("OPERATOR", "/"))
                continue

            # ── Identyfikator / słowo kluczowe ──
            if zn.isalpha() or zn == "_":
                tokeny.append(self._skanuj_identyfikator())
                continue

            # ── Liczba ──
            if zn.isdigit():
                tokeny.append(self._skanuj_liczbe())
                continue

            # ── Łańcuch znaków ──
            if zn == '"':
                tokeny.append(self._skanuj_lancuch())
                continue

            # ── Strzałka -> lub minus ──
            if zn == "-":
                if self._nastepny() == ">":
                    self._konsumuj()
                    self._konsumuj()
                    tokeny.append(Token("ARROW", "->"))
                else:
                    self._konsumuj()
                    tokeny.append(Token("OPERATOR", "-"))
                continue

            # ── Operatory dwuznakowe (==, !=, <=, >=) ──
            if zn in ("=", "!", "<", ">"):
                tokeny.append(self._skanuj_operator_porownania())
                continue

            # ── Operatory pojedyncze ──
            if zn in OPERATORY_POJEDYNCZE:
                self._konsumuj()
                tokeny.append(Token("OPERATOR", zn))
                continue

            # ── Ograniczniki ──
            if zn in OGRANICZNIKI:
                self._konsumuj()
                tokeny.append(Token("DELIMITER", zn))
                continue

            # ── Nierozpoznany znak → BŁĄD ──
            self._konsumuj()
            tokeny.append(Token("ERROR", zn))

        return tokeny

    # --- metody stanów automatu ---

    def _skanuj_identyfikator(self) -> Token:
        """Stan IDENTYFIKATOR: litery, cyfry, podkreślenia."""
        bufor = self._konsumuj()
        while self._obecny() is not None and (
            self._obecny().isalnum() or self._obecny() == "_"
        ):
            bufor += self._konsumuj()

        if bufor in SLOWA_KLUCZOWE:
            return Token("KEYWORD", bufor)
        return Token("IDENT", bufor)

    def _skanuj_liczbe(self) -> Token:
        """Stan LICZBA → ewentualnie stan LICZBA_ULAMEK."""
        bufor = self._konsumuj()
        while self._obecny() is not None and self._obecny().isdigit():
            bufor += self._konsumuj()

        # Sprawdzenie części ułamkowej
        if self._obecny() == "." and (
            self._nastepny() is not None and self._nastepny().isdigit()
        ):
            bufor += self._konsumuj()  # kropka
            while self._obecny() is not None and self._obecny().isdigit():
                bufor += self._konsumuj()
            return Token("FLOAT", bufor)

        return Token("INT", bufor)

    def _skanuj_lancuch(self) -> Token:
        """Stan LANCUCH: od cudzysłowu do cudzysłowu."""
        bufor = self._konsumuj()  # otwierający "
        while self._obecny() is not None and self._obecny() != '"':
            if self._obecny() == "\n":
                break  # łańcuch nie może przechodzić przez nową linię
            bufor += self._konsumuj()

        if self._obecny() == '"':
            bufor += self._konsumuj()  # zamykający "
        # Jeśli nie zamknięty, i tak zwracamy to co mamy
        return Token("STRING", bufor)

    def _skanuj_komentarz_blokowy(self) -> Token:
        """Stan KOMENTARZ_BLOKOWY: od /* do */."""
        bufor = self._konsumuj()  # /
        bufor += self._konsumuj()  # *

        while self.poz < self.dlug:
            if self._obecny() == "*" and self._nastepny() == "/":
                bufor += self._konsumuj()  # *
                bufor += self._konsumuj()  # /
                return Token("COMMENT", bufor)
            bufor += self._konsumuj()

        # Niezamknięty komentarz blokowy
        return Token("COMMENT", bufor)

    def _skanuj_operator_porownania(self) -> Token:
        """Operatory porównania: ==, !=, <=, >=, <, >, ="""
        zn = self._konsumuj()
        if self._obecny() == "=":
            drugi = self._konsumuj()
            return Token("OPERATOR", zn + drugi)
        return Token("OPERATOR", zn)


# ============================================================
#  Generator HTML
# ============================================================

class GeneratorHTML:
    """Tworzy dokument HTML z pokolorowanym kodem na podstawie listy tokenów."""

    @staticmethod
    def eskejpuj(tekst: str) -> str:
        """Zamienia znaki specjalne na encje HTML."""
        tekst = tekst.replace("&", "&amp;")
        tekst = tekst.replace("<", "&lt;")
        tekst = tekst.replace(">", "&gt;")
        tekst = tekst.replace('"', "&quot;")
        return tekst

    def generuj(self, tokeny: list[Token], tytul: str = "MiniScript") -> str:
        """Składa pełny dokument HTML."""
        fragmenty_kodu = []

        for tk in tokeny:
            tresc_html = self.eskejpuj(tk.tresc)

            if tk.typ == "WHITESPACE":
                # Białe znaki wstawiamy bez spana
                fragmenty_kodu.append(tresc_html)
            elif tk.typ in KOLORY_CSS:
                styl = KOLORY_CSS[tk.typ]
                fragmenty_kodu.append(
                    f'<span style="{styl}" title="{tk.typ}">{tresc_html}</span>'
                )
            else:
                fragmenty_kodu.append(tresc_html)

        zawartosc = "".join(fragmenty_kodu)

        return f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kolorowanie składni – {self.eskejpuj(tytul)}</title>
    <style>
        body {{
            background-color: #282c34;
            color: #abb2bf;
            font-family: 'Fira Code', 'Cascadia Code', 'Consolas', monospace;
            padding: 24px;
            margin: 0;
        }}
        h1 {{
            color: #61afef;
            font-size: 18px;
            margin-bottom: 16px;
            font-weight: 400;
        }}
        .kod-zrodlowy {{
            background-color: #21252b;
            border: 1px solid #3e4451;
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
            font-size: 14px;
            line-height: 1.6;
            tab-size: 4;
        }}
        .legenda {{
            margin-top: 24px;
            padding: 16px;
            background-color: #21252b;
            border: 1px solid #3e4451;
            border-radius: 8px;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .legenda-element {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
        }}
        .legenda-kolor {{
            width: 14px;
            height: 14px;
            border-radius: 3px;
            border: 1px solid #3e4451;
        }}
    </style>
</head>
<body>
    <h1>Kolorowanie składni &mdash; {self.eskejpuj(tytul)}</h1>
    <pre class="kod-zrodlowy">{zawartosc}</pre>
    <div class="legenda">
        <div class="legenda-element">
            <div class="legenda-kolor" style="background:#c678dd;"></div>
            Słowo kluczowe
        </div>
        <div class="legenda-element">
            <div class="legenda-kolor" style="background:#e06c75;"></div>
            Identyfikator
        </div>
        <div class="legenda-element">
            <div class="legenda-kolor" style="background:#d19a66;"></div>
            Liczba
        </div>
        <div class="legenda-element">
            <div class="legenda-kolor" style="background:#98c379;"></div>
            Łańcuch znaków
        </div>
        <div class="legenda-element">
            <div class="legenda-kolor" style="background:#5c6370;"></div>
            Komentarz
        </div>
        <div class="legenda-element">
            <div class="legenda-kolor" style="background:#56b6c2;"></div>
            Operator
        </div>
        <div class="legenda-element">
            <div class="legenda-kolor" style="background:#abb2bf;"></div>
            Ogranicznik
        </div>
        <div class="legenda-element">
            <div class="legenda-kolor" style="background:#ff0000;"></div>
            Błąd
        </div>
    </div>
</body>
</html>"""


# ============================================================
#  Funkcja główna
# ============================================================

def main():
    if len(sys.argv) < 3:
        print("Użycie: python3 kolorowanie.py <plik_wejściowy> <plik_wyjściowy.html>")
        print("Przykład: python3 kolorowanie.py przyklad.ms wynik.html")
        sys.exit(1)

    sciezka_wejscie = sys.argv[1]
    sciezka_wyjscie = sys.argv[2]

    # Wczytanie pliku źródłowego
    try:
        with open(sciezka_wejscie, "r", encoding="utf-8") as plik:
            kod_zrodlowy = plik.read()
    except FileNotFoundError:
        print(f"Błąd: plik '{sciezka_wejscie}' nie istnieje.")
        sys.exit(1)

    # Analiza leksykalna (skanowanie)
    automat = AutomatSkanera(kod_zrodlowy)
    tokeny = automat.skanuj()

    # Wypisanie tokenów na konsolę
    print(f"Przeskanowano plik: {sciezka_wejscie}")
    print(f"Znaleziono {len(tokeny)} tokenów:")
    print("-" * 50)
    for tk in tokeny:
        if tk.typ != "WHITESPACE":
            print(f"  {tk.typ:12s}  │  {tk.tresc!r}")
    print("-" * 50)

    # Generowanie HTML
    generator = GeneratorHTML()
    nazwa_pliku = sciezka_wejscie.rsplit("/", 1)[-1]
    html = generator.generuj(tokeny, tytul=nazwa_pliku)

    with open(sciezka_wyjscie, "w", encoding="utf-8") as plik:
        plik.write(html)

    print(f"Zapisano pokolorowany kod do: {sciezka_wyjscie}")


if __name__ == "__main__":
    main()
