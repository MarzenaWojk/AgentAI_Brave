# S-01 Account Access Flow — Plan Brief

> Full plan: context/changes/s-01/plan.md

## What & Why

Ta zmiana dowozi minimalny flow dostepu do konta: register/login/logout/me. Jest to konieczny krok, aby kolejne endpointy (szczegolnie generation) mogly byc legalnie i bezpiecznie bramkowane loginem.

## Starting Point

Roadmapa oznacza S-01 jako slice zalezny od F-01. Kod ma API JSON i brak pelnego, wydzielonego flow auth dla S-01.

## Desired End State

Uzytkownik moze zalozyc konto, zalogowac sie, pobrac swoje dane sesji i wylogowac sie przez API JSON. Negatywne scenariusze maja stabilny kontrakt bledow, gotowy pod frontend i kolejne slice'y.

## Key Decisions Made

| Decision | Choice | Why (1 sentence) | Source |
| --- | --- | --- | --- |
| Auth scope | register/login/logout/me only | Najmniejszy zakres zgodny z MVP speed-first. | Plan |
| Auth method | Django session auth | Najprostszy fit do obecnego stacku i testow. | Plan |
| Error contract | Structured JSON errors | Spojnosc z istniejacym API i prostsza integracja klienta. | Plan |
| Downstream readiness | Explicit smoke flow for session continuity | Potwierdza gotowosc pod S-02 i S-06 bez zgadywania. | Plan |

## Scope

In scope:
- endpointy register/login/logout/me,
- testy happy path i negatywne auth,
- smoke flow preview dla auth.

Out of scope:
- password reset,
- email verification,
- JWT migration,
- review/generation logic.

## Architecture / Approach

Plan zaklada cienka warstwe auth API oparta o istniejace mechanizmy Django sessions i obecny kontrakt JSON. Zmiany ograniczamy do views, urls i tests, bez przebudowy architektury projektu.

## Phases at a Glance

| Phase | What it delivers | Key risk |
| --- | --- | --- |
| 1. Account Endpoint Contract | Endpointy register/login/logout/me | Niespojny kontrakt odpowiedzi przy integracji |
| 2. Failure Modes and API Consistency | Stabilne bledy i negatywne scenariusze | Niedopiete testy metod i walidacji |
| 3. Slice Readiness for Downstream Work | Potwierdzona ciaglosc sesji pod kolejne slice'y | Ukryta zaleznosc od niewdrozonego F-01 |

Prerequisites: domkniety foundation F-01 (lub realizacja razem).  
Estimated effort: ~1-2 sesje implementacyjne.

## Open Risks & Assumptions

- Zakladamy, ze F-01 bedzie wdrozone przed lub razem z S-01.
- Zakladamy brak potrzeby recovery flow w MVP.

## Success Criteria (Summary)

- Register/login/logout/me dzialaja i sa pokryte testami.
- Endpoint me poprawnie odzwierciedla stan sesji.
- Preview smoke flow auth przechodzi bez regresji systemowej.
