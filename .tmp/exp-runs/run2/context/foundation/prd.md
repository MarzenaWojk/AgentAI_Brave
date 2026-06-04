---
project: "# TODO: project — see Open Questions"
version: 1
status: draft
created: 2026-05-22
context_type: greenfield
product_type: web-app
target_scale:
  users: small
  qps: "# TODO: qps — see Open Questions"
  data_volume: "# TODO: data_volume — see Open Questions"
timeline_budget:
  mvp_weeks: 3
  hard_deadline: null
  after_hours_only: true
---

## Vision & Problem Statement

Manualne tworzenie wysokiej jakości fiszek edukacyjnych jest czasochłonne, co zniechęca do korzystania z efektywnej metody nauki opartej o spaced repetition.

Problem pojawia się, gdy osoba ucząca się języków chce szybko zamienić materiał do nauki na zestaw fiszek i musi wykonać dużo ręcznej pracy. Obecne narzędzia wymagają manualnego zaangażowania, przez co tarcie w pracy z materiałem jest zbyt wysokie.

## User & Persona

### Primary persona

- Rola: osoba ucząca się języków
- Kontekst: korzysta z materiału do nauki, który chce szybko zamienić na fiszki
- Moment użycia: sięga po produkt, gdy chce przejść od tekstu źródłowego do gotowych fiszek i pierwszej powtórki

## Success Criteria

### Primary

- 75% fiszek wygenerowanych przez AI jest akceptowane przez użytkownika.
- Użytkownicy tworzą 75% fiszek z wykorzystaniem AI.

### Secondary

- Obie metryki sukcesu są spełnione łącznie.

### Guardrails

- Prywatność danych użytkownika musi być zachowana.

## User Stories

### US-01: Generowanie i pierwsza powtórka fiszek

- **Given** zalogowana osoba ucząca się języków ma tekst źródłowy do nauki.
- **When** wkleja tekst, uruchamia generowanie AI i przechodzi review fiszek (accept/edit/reject).
- **Then** zapisuje zestaw fiszek i uruchamia pierwszą powtórkę w gotowym algorytmie.

#### Acceptance Criteria

# TODO: acceptance criteria for US-01 — see Open Questions

## Functional Requirements

- FR-001: Osoba ucząca się języków może wkleić tekst źródłowy do generowania fiszek. Priority: must-have
  > Socrates: Kontrargument: import tekstu może być zbędny w MVP przy podejściu tylko manualnym. Rozstrzygnięcie: kept; import tekstu jest rdzeniem wartości AI.
- FR-002: Osoba ucząca się języków może wygenerować fiszki przez AI na podstawie tekstu źródłowego. Priority: must-have
  > Socrates: Kontrargument: jakość generacji może być za słaba bez dopracowanego promptu. Rozstrzygnięcie: kept; ryzyko jakości jest akceptowane i będzie ograniczane iteracyjnie.
- FR-003: Osoba ucząca się języków może zaakceptować, edytować lub odrzucić wygenerowane fiszki. Priority: must-have
  > Socrates: Kontrargument: review może być zbyt czasochłonne i niwelować zysk z AI. Rozstrzygnięcie: kept; kontrola jakości przez użytkownika jest wymagana w MVP.
- FR-004: Osoba ucząca się języków może tworzyć fiszki manualnie. Priority: must-have
  > Socrates: Kontrargument: manualne tworzenie można odłożyć, by skupić się na AI. Rozstrzygnięcie: kept; manualna ścieżka jest potrzebna jako fallback i uzupełnienie.
- FR-005: Osoba ucząca się języków może przeglądać, edytować i usuwać fiszki. Priority: must-have
  > Socrates: Kontrargument: pełna edycja może być za szeroka na MVP. Rozstrzygnięcie: kept; podstawowe zarządzanie fiszkami pozostaje wymagane.
- FR-006: Osoba ucząca się języków może zapisać fiszki na swoim koncie użytkownika. Priority: must-have
  > Socrates: Kontrargument: na start można działać lokalnie bez trwałego konta. Rozstrzygnięcie: kept; zapis na koncie pozostaje elementem MVP.
- FR-007: Osoba ucząca się języków może uruchomić powtórki fiszek przez gotowy algorytm powtórek. Priority: must-have
  > Socrates: Kontrargument: powtórki można odłożyć po samym tworzeniu i zapisie fiszek. Rozstrzygnięcie: kept; pierwsza powtórka jest kluczowa dla dowiezienia wartości produktu.

## Non-Functional Requirements

- Responsywność interfejsu: p95 < 300 ms dla interakcji UI.
- Czas generacji AI: p95 < 10 s dla generowania fiszek.
- Prywatność: tekst źródłowy i fiszki są prywatne per konto; brak udostępniania między użytkownikami.
- Kompatybilność: wsparcie dla 2 ostatnich wersji Chrome, Edge, Firefox i Safari.
- Integracja powtórek: każda zaakceptowana fiszka jest uruchamialna w gotowym algorytmie powtórek w tej samej sesji.

## Business Logic

Aplikacja priorytetyzuje fiszki do powtórki na podstawie historii odpowiedzi i czasu od ostatniej powtórki, aby zwiększyć skuteczność zapamiętywania.

Wejścia reguły to historia odpowiedzi użytkownika oraz czas od ostatniej powtórki.

Wynikiem reguły jest kolejność fiszek do powtórki.

Użytkownik widzi wynik reguły podczas uruchamiania sesji powtórek.

## Access Control

- Dostęp do produktu wymaga logowania.
- MVP zakłada jedną rolę użytkownika.
- Zapisane fiszki są powiązane z kontem użytkownika.

## Non-Goals

- Nie budujemy własnego zaawansowanego algorytmu powtórek; produkt korzysta z gotowego algorytmu.
- MVP nie obsługuje importu PDF, DOCX ani innych formatów poza kopiuj-wklej tekstu.
- MVP nie wspiera współdzielenia zestawów fiszek między użytkownikami.
- MVP nie integruje się z innymi platformami edukacyjnymi.
- MVP nie obejmuje aplikacji mobilnej; zakres pierwszej wersji to web.

## Open Questions

1. **Jaka jest właściwa nazwa projektu?** — TBD by user. Block: no.
2. **Jaki jest docelowy poziom qps?** — TBD by user. Block: no.
3. **Jaki jest docelowy wolumen danych?** — TBD by user. Block: no.
4. **Jakie są acceptance criteria dla US-01?** — TBD by user. Block: no.
