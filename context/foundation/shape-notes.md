---
project: null
context_type: greenfield
created: 2026-05-22
updated: 2026-05-22
checkpoint:
  current_phase: 8
  phases_completed: [1, 2, 3, 4, 5, 6, 7]
  gray_areas_resolved:
    - topic: pain category
      decision: workflow friction
    - topic: primary persona scope
      decision: jedna konkretna rola
    - topic: insight
      decision: obecne narzedzia wymagaja manualnego zaangazowania
    - topic: access strategy
      decision: login
    - topic: role model
      decision: jedna rola
    - topic: timeline budget
      decision: 3 tygodnie po godzinach
    - topic: socrates round resolution
      decision: wszystkie FR pozostaja must-have
    - topic: business logic rule
      decision: priorytetyzacja fiszek do powtorek na podstawie historii odpowiedzi i czasu
    - topic: nfr latency
      decision: UI p95 < 300 ms, generacja AI p95 < 10 s
    - topic: nfr privacy
      decision: dane prywatne per konto, bez udostepniania miedzy uzytkownikami
    - topic: nfr compatibility
      decision: 2 ostatnie wersje Chrome, Edge, Firefox, Safari
    - topic: srs requirement
      decision: zaakceptowana fiszka uruchamialna w algorytmie powtorek w tej samej sesji
    - topic: product type
      decision: web-app
    - topic: target scale users
      decision: small
    - topic: scale 100x probe
      decision: reguly pozostaja per-user i musza byc stabilne przy wiekszym wolumenie
    - topic: hard deadline
      decision: no deadline
    - topic: after-hours only
      decision: tak
    - topic: non-goals
      decision: zaawansowany algorytm, importy, wspoldzielenie, integracje zewnetrzne i mobile poza MVP
  frs_drafted: 7
  quality_check_status: accepted
---

## Seed Input

### Source
@file:idea-notes.md

### Notes (verbatim)
### Główny problem
Manualne tworzenie wysokiej jakości fiszek edukacyjnych jest czasochłonne, co zniechęca do korzystania z efektywnej metody nauki jaką jest spaced repetition.

### Najmniejszy zestaw funkcjonalności
- Generowanie fiszek przez AI na podstawie wprowadzonego tekstu (kopiuj-wklej)
- Manualne tworzenie fiszek
- Przeglądanie, edycja i usuwanie fiszek
- Prosty system kont użytkowników do przechowywania fiszek
- Integracja fiszek z gotowym algorytmem powtórek

### Co NIE wchodzi w zakres MVP
- Własny, zaawansowany algorytm powtórek (jak SuperMemo, Anki)
- Import wielu formatów (PDF, DOCX, itp.)
- Współdzielenie zestawów fiszek między użytkownikami
- Integracje z innymi platformami edukacyjnymi
- Aplikacje mobilne (na początek tylko web)

### Kryteria sukcesu
- 75% fiszek wygenerowanych przez AI jest akceptowane przez użytkownika
- Użytkownicy tworzą 75% fiszek z wykorzystaniem AI

## Vision & Problem Statement

Manualne tworzenie wysokiej jakosci fiszek edukacyjnych jest czasochlonne, co zniecheca do korzystania z metody spaced repetition.

Problem pojawia sie, gdy osoba uczaca sie jezykow chce szybko zamienic material do nauki na zestaw fiszek i musi wykonac duzo recznej pracy.

## User & Persona

### Primary persona

- Rola: osoba uczaca sie jezykow
- Zakres: jedna konkretna rola

### Phase 1 lock

Pain: manualne tworzenie fiszek jest czasochlonne i zniecheca do spaced repetition.
Person: osoba uczaca sie jezykow.
Moment: podczas zamiany materialu do nauki na fiszki.
Cost today: wysokie reczne zaangazowanie.
Pain category: workflow friction.
Insight: obecne narzedzia wymagaja manualnego zaangazowania.

## Access Control

- Wejscie do aplikacji: login.
- Model dostepu: jedna rola uzytkownika w MVP.

## Success Criteria

### Primary

1. Uzytkownik przechodzi standardowe logowanie.
2. Uzytkownik wprowadza tekst zrodlowy do wygenerowania fiszek.
3. System wywoluje LLM API i generuje fiszki.
4. Uzytkownik przechodzi review wygenerowanych fiszek (accept/edit/reject).
5. Uzytkownik moze recznie dodac fiszki.
6. Uzytkownik zarzadza fiszkami (przegladanie, edycja, usuwanie).
7. Zestaw trafia do gotowego algorytmu powtorek i uzytkownik wykonuje pierwsza powtorke.

### Secondary

- Obie metryki sukcesu sa spelnione lacznie.

### Guardrails

- Prywatnosc danych uzytkownika musi byc zachowana.

## Timeline Budget

- mvp_weeks: 3
- hard_deadline: brak
- after_hours_only: tak

## Product Framing

- Product type: web-app.
- Target scale users: small (just me, or a handful).
- Scale probe (100x): regula priorytetyzacji pozostaje per-user i musi byc stabilna przy wiekszym wolumenie.
- Hard deadline: no deadline.
- Delivery mode: po godzinach.

## Non-Goals

- Nie budujemy wlasnego zaawansowanego algorytmu powtorek (uzywamy gotowego algorytmu).
- Brak importu PDF, DOCX i innych formatow poza kopiuj-wklej tekstu.
- Brak wspoldzielenia zestawow fiszek miedzy uzytkownikami.
- Brak integracji z innymi platformami edukacyjnymi.
- Brak aplikacji mobilnej w MVP (zakres: web).

## Quality cross-check

- Access Control: present.
- Business Logic: present.
- Project artifacts: present.
- Timeline-cost ack: present (mvp_weeks = 3).
- Non-Goals: present.
- Preserved behavior: n/a (greenfield).

## Functional Requirements

- FR-001: Osoba uczaca sie jezykow moze wkleic tekst zrodlowy do generowania fiszek. Priority: must-have
  > Socrates: Kontrargument: import tekstu moze byc zbedny w MVP przy podejsciu tylko manualnym. Rozstrzygniecie: kept; import tekstu jest rdzeniem wartosci AI.
- FR-002: Osoba uczaca sie jezykow moze wygenerowac fiszki przez AI na podstawie tekstu zrodlowego. Priority: must-have
  > Socrates: Kontrargument: jakosc generacji moze byc za slaba bez dopracowanego promptu. Rozstrzygniecie: kept; ryzyko jakosci jest akceptowane i bedzie ograniczane iteracyjnie.
- FR-003: Osoba uczaca sie jezykow moze zaakceptowac, edytowac lub odrzucic wygenerowane fiszki. Priority: must-have
  > Socrates: Kontrargument: review moze byc zbyt czasochlonne i niwelowac zysk z AI. Rozstrzygniecie: kept; kontrola jakosci przez uzytkownika jest wymagana w MVP.
- FR-004: Osoba uczaca sie jezykow moze tworzyc fiszki manualnie. Priority: must-have
  > Socrates: Kontrargument: manualne tworzenie mozna odlozyc, by skupic sie na AI. Rozstrzygniecie: kept; manualna sciezka jest potrzebna jako fallback i uzupelnienie.
- FR-005: Osoba uczaca sie jezykow moze przegladac, edytowac i usuwac fiszki. Priority: must-have
  > Socrates: Kontrargument: pelna edycja moze byc za szeroka na MVP. Rozstrzygniecie: kept; podstawowe zarzadzanie fiszkami pozostaje wymagane.
- FR-006: Osoba uczaca sie jezykow moze zapisac fiszki na swoim koncie uzytkownika. Priority: must-have
  > Socrates: Kontrargument: na start mozna dzialac lokalnie bez trwalego konta. Rozstrzygniecie: kept; zapis na koncie pozostaje elementem MVP.
- FR-007: Osoba uczaca sie jezykow moze uruchomic powtorki fiszek przez gotowy algorytm powtorek. Priority: must-have
  > Socrates: Kontrargument: powtorki mozna odlozyc po samym tworzeniu i zapisie fiszek. Rozstrzygniecie: kept; pierwsza powtorka jest kluczowa dla dowiezienia wartosci produktu.

## User Stories

### US-01: Generowanie i pierwsza powtorka fiszek

- **Given** zalogowana osoba uczaca sie jezykow ma tekst zrodlowy do nauki.
- **When** wkleja tekst, uruchamia generowanie AI i przechodzi review fiszek (accept/edit/reject).
- **Then** zapisuje zestaw fiszek i uruchamia pierwsza powtorke w gotowym algorytmie.

## Business Logic

Aplikacja priorytetyzuje fiszki do powtorki na podstawie historii odpowiedzi i czasu od ostatniej powtorki, aby zwiekszyc skutecznosc zapamietywania.

Wejscia reguly: historia odpowiedzi uzytkownika oraz czas od ostatniej powtorki.

Wynik reguly: kolejnosc fiszek do powtorki.

Uzytkownik widzi wynik reguly podczas uruchamiania sesji powtorek.

## Non-Functional Requirements

- Responsywnosc interfejsu: p95 < 300 ms dla interakcji UI.
- Czas generacji AI: p95 < 10 s dla generowania fiszek.
- Prywatnosc: tekst zrodlowy i fiszki sa prywatne per konto; brak udostepniania miedzy uzytkownikami.
- Kompatybilnosc: wsparcie dla 2 ostatnich wersji Chrome, Edge, Firefox i Safari.
- Integracja powtorek: kazda zaakceptowana fiszka jest uruchamialna w gotowym algorytmie powtorek w tej samej sesji.
