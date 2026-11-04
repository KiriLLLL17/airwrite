# Wymagania — Projekt z Pythona (Programming with Python, Fall 2026)

## Terminy

| Co | Kiedy |
|---|---|
| **Raport (deadline)** | **13 listopada 2026, 23:59** |
| Prezentacja ustna | Tygodnie 9–11, 10 minut |

---

## Skład grupy

- [ ] Maksymalnie **4 studentów** w grupie
- [ ] Maksymalnie 36 grup na kursie
- [ ] Kryteria oceny nie zależą od wielkości grupy, ale **wkład każdego studenta jest brany pod uwagę**
- [ ] Wszyscy członkowie grupy muszą być obecni na scenie podczas prezentacji

---

## Trzy obowiązkowe elementy

1. [ ] Raport projektowy
2. [ ] Kod
3. [ ] Prezentacja ustna na zajęciach (10 minut)

---

## Wymagania techniczne wobec kodu

- [ ] Minimum **100 linii kodu**
- [ ] Minimum **2 biblioteki** do AI / data mining / analizy danych
  - np. scikit-learn, NumPy, pandas, Matplotlib, Seaborn, TensorFlow, PyTorch
- [ ] **Wystarczająco dużo komentarzy** — kod musi być czytelny
- [ ] Kod **musi się uruchamiać poprawnie**
- [ ] Wyniki muszą być **reprodukowalne**
- [ ] ⚠️ Fabrykowanie lub modyfikowanie wyników eksperymentalnych jest **surowo zabronione**

## Wymagania wobec zawartości projektu

- [ ] Zastosowanie AI / data mining / analizy danych **do własnej dziedziny studiów**
- [ ] Samodzielny wybór funkcjonalności i **jasno określony cel programu**
- [ ] Wystarczająco dużo **analizy danych**
- [ ] Wystarczająco dużo **wizualizacji danych**
- [ ] Wykazanie **pewnego stopnia innowacyjności**
- [ ] **Real-world dataset** (zbiór danych z rzeczywistego świata)

---

## Sposób złożenia projektu

Projekt trzeba złożyć w **dwóch miejscach**:

### 1. python123.io
- [ ] Odpowiednia jednostka kursu
- [ ] Tylko **raport i kod**
- [ ] ⚠️ **NIE wysyłać danych** na tę platformę

### 2. Email: `python_projects@163.com`
- [ ] Tylko **jeden email na grupę**
- [ ] Załączniki: raport, kod, dane — **spakowane osobno**

#### Format tematu emaila

```
CourseProjectFall2026-Name1-StudentID1-Name2-StudentID2-Name3-StudentID3-Name4-StudentID4
```

#### Treść emaila musi zawierać

- [ ] Tytuł projektu
- [ ] Imiona i nazwiska wszystkich członków grupy
- [ ] Numery studenckie
- [ ] Klasy (classes)
- [ ] Zakres odpowiedzialności każdej osoby
- [ ] Wkład każdej osoby

---

## Struktura raportu (obowiązkowy szablon)

Raport może być w **Word** lub **LaTeX**. Pisz zwięźle, unikaj powtórzeń.

### Nagłówek
- Tytuł raportu
- Imiona i nazwiska studentów, numery studenckie, klasy

### 1. Introduction
- [ ] Przedstawienie problemu i jego znaczenia
- [ ] Krótkie podsumowanie podejścia
- [ ] Główne wnioski

### 2. Method
- [ ] **Uzasadnienie wyboru modeli/algorytmów** w odniesieniu do state-of-the-art i powszechnie stosowanych metod
- [ ] Opis implementacji
- [ ] Opis własnych ulepszeń
- [ ] Diagramy lub zarysy algorytmów, gdzie to pomocne

### 3. Experimental Results and Analysis
- [ ] Opis zbiorów danych
- [ ] Kryteria ewaluacji
- [ ] Prezentacja i **interpretacja** wyników — czytelne tabele i wykresy
- [ ] Dodatkowe analizy, np.:
  - robustness hiperparametrów
  - badania ablacyjne (ablation studies)

### 4. Discussion and Conclusion
- [ ] Podsumowanie wyników
- [ ] **Własny, oryginalny wkład**
- [ ] Mocne strony
- [ ] Ograniczenia
- [ ] Wnioski i wyciągnięte lekcje
- [ ] Możliwe przyszłe usprawnienia

### 5. References
- [ ] Wszystkie zewnętrzne źródła: teorie, algorytmy, modele, dane, rysunki
- [ ] **Spójny format** cytowania

---

## Uczciwość akademicka

> Nie przedstawiaj cudzej pracy jako własnej. **Plagiat = ocena zero z projektu.**

- [ ] Cytuj ponownie wykorzystany kod
- [ ] Wyjaśnij, co jest Twoim własnym wkładem

---

## Źródła danych polecane przez prowadzącego

| Źródło | Opis |
|---|---|
| UCI Machine Learning Repository | Dane tabelaryczne, tekstowe, szeregi czasowe |
| Kaggle Datasets | Dane społecznościowe — sprawdź jakość źródła i warunki dostępu |
| Hugging Face Datasets | Język, wizja i inne — część wymaga zgody na dostęp |
| World Bank Open Data / Data.gov | Wskaźniki rozwoju, otwarte dane rządowe |
| Google Dataset Search / Awesome Public Datasets | Wyszukiwanie — potwierdź dostęp u pierwotnego dostawcy |

### Przed wyborem zbioru sprawdź
- [ ] Dostępność pobrania
- [ ] Jakość danych
- [ ] Licencję
- [ ] Warunki redystrybucji
- [ ] Czy projekt da się ukończyć i zreprodukować w dostępnym czasie

---

## Sugerowane kierunki projektu (przykłady od prowadzącego)

| Kierunek | Przykładowy zbiór | Możliwy projekt |
|---|---|---|
| Dane tabelaryczne | UCI Wine Quality | Predykcja jakości wina, porównanie modeli, analiza błędów |
| Analiza tekstu | UCI SMS Spam Collection | Porównanie klasyfikatorów spamu i reprezentacji tekstu |
| Computer vision | Fashion-MNIST | Klasyfikacja ubrań, analiza typowych pomyłek |
| Rekomendacje | MovieLens 100K | Porównanie rekomendacji popularnościowych i kolaboratywnych |
| Szeregi czasowe | UCI Bike Sharing | Prognoza popytu z chronologicznym podziałem train/test |
| Analiza sieci | SNAP Facebook | Badanie społeczności, porównanie miar centralności |
| Dane medyczne | UCI Breast Cancer Wisconsin | Porównanie klasyfikatorów i selekcji cech (cel edukacyjny) |

Dla zaawansowanych projektów: małe podzbiory ImageNet, COCO lub Open Images.

### Materiały pomocnicze
- Oficjalne przykłady scikit-learn
- Tutoriale pandas
- Tutoriale PyTorch
- Hugging Face Papers (szukanie pomysłów badawczych)

---

## Checklista przed wysłaniem

- [ ] Kod ma ≥100 linii i działa bez błędów
- [ ] Użyte ≥2 biblioteki z listy
- [ ] Kod ma komentarze
- [ ] Ustawione ziarna losowe (reprodukowalność)
- [ ] Raport zawiera wszystkie 5 sekcji
- [ ] Wszystkie źródła zacytowane
- [ ] Raport + kod wrzucone na python123.io (bez danych!)
- [ ] Email na python_projects@163.com z poprawnym tematem
- [ ] W treści emaila: tytuł, dane wszystkich członków, odpowiedzialności, wkład
- [ ] Raport, kod i dane spakowane **osobno**
- [ ] Prezentacja na 10 minut przygotowana, wszyscy członkowie wiedzą, co mówią
