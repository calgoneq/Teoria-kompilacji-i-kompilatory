class Token:
    def __init__(self, kod, wartosc, kolumna):
        self.kod = kod
        self.wartosc = wartosc
        self.kolumna = kolumna

    def __repr__(self):
        return f"(Kod: {self.kod:^6}, Wartość: '{self.wartosc}')"


class Skaner:
    def __init__(self, kod_zrodlowy):
        self.tekst = kod_zrodlowy
        self.dlugosc = len(kod_zrodlowy)
        self.pozycja = 0
        self.kolumna = 1

    def pobierz_znak(self):
        if self.pozycja < self.dlugosc:
            znak = self.tekst[self.pozycja]
            self.pozycja += 1
            self.kolumna += 1
            return znak
        return None

    def pomin_biale_znaki(self):
        while self.pozycja < self.dlugosc and self.tekst[self.pozycja].isspace():
            znak = self.tekst[self.pozycja]
            self.pozycja += 1
            if znak == '\n':
                self.kolumna = 1
            else:
                self.kolumna += 1

    def skaner(self):
        self.pomin_biale_znaki()

        if self.pozycja >= self.dlugosc:
            return Token("EOF", "", self.kolumna)

        start_kolumna = self.kolumna
        znak = self.pobierz_znak()

        if znak.isalpha():
            wartosc = znak
            while self.pozycja < self.dlugosc and self.tekst[self.pozycja].isalnum():
                wartosc += self.pobierz_znak()
            return Token("ID", wartosc, start_kolumna)

        if znak.isdigit():
            wartosc = znak
            while self.pozycja < self.dlugosc and self.tekst[self.pozycja].isdigit():
                wartosc += self.pobierz_znak()
            return Token("INT", wartosc, start_kolumna)

        if znak == '+':
            return Token("PLUS", znak, start_kolumna)
        elif znak == '-':
            return Token("MINUS", znak, start_kolumna)
        elif znak == '*':
            return Token("MUL", znak, start_kolumna)
        elif znak == '/':
            return Token("DIV", znak, start_kolumna)
        elif znak == '(':
            return Token("LPAREN", znak, start_kolumna)
        elif znak == ')':
            return Token("RPAREN", znak, start_kolumna)

        return Token("ERROR", znak, start_kolumna)


def uruchom_test():
    wyrazenie_matematyczne = "2+3*(76+8/3)+ 3*(9-3) + abc $ 5"
    
    print(f"Skanowane wyrażenie: {wyrazenie_matematyczne}")
    print("-" * 50)
    
    moj_skaner = Skaner(wyrazenie_matematyczne)
    
    while True:
        token = moj_skaner.skaner()
        
        if token.kod == "EOF":
            print("--- KONIEC SKANOWANIA (Osiągnięto EOF) ---")
            break
            
        elif token.kod == "ERROR":
            print(f"[!] BŁĄD LEKSYKALNY: Nierozpoznany znak '{token.wartosc}' w kolumnie {token.kolumna}.")
            
        else:
            print(f"Znaleziono token: {token} -> Zaczyna się w kolumnie: {token.kolumna}")

if __name__ == '__main__':
    uruchom_test()