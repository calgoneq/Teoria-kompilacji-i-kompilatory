# Program przykładowy w MiniScript
# Demonstruje wszystkie kategorie tokenów

/* Funkcja obliczająca silnię
   z wykorzystaniem pętli while */
fun silnia(n) {
    let wynik = 1;
    let i = 1;
    while (i <= n) {
        wynik = wynik * i;
        i = i + 1;
    }
    return wynik;
}

# Funkcja ze strzałką i warunkami
fun sprawdz(x) -> {
    if (x > 0 and x != 100) {
        print("Liczba dodatnia");
        return true;
    } else {
        print("Liczba niedodatnia lub równa 100");
        return false;
    }
}

# Operacje arytmetyczne
let a = 42;
let b = 3.14;
let suma = a + b;
let roznica = a - b;
let iloczyn = a * b;
let iloraz = a / b;
let reszta = a % 7;

# Tablice i pętla for
let tab = [1, 2, 3, 4, 5];
for (let j = 0; j < 5; j = j + 1) {
    print(tab[j]);
}

# Wartości specjalne
let nic = null;
let flaga = not false;

/* Wywołanie funkcji */
let wynik_silni = silnia(10);
print(wynik_silni);
sprawdz(wynik_silni);

# Test: nierozpoznany znak → błąd leksykalny
let test = 5 @ 3;
