# First Gated Generation — Plan Brief

> Full plan: `context/changes/first-gated-generation/plan.md`

## What & Why

Budujemy pierwszy endpoint generacji AI, ktory dziala tylko dla zalogowanego uzytkownika i zapisuje fiszki jako dane wlasciciela. To domyka krytyczny krok roadmapy po auth foundation i przygotowuje grunt pod review oraz zapis/repetition flow. Priorytetem tej zmiany jest bezpieczenstwo i izolacja danych, nie maksymalna rozbudowa funkcji.

## Starting Point

Obecnie API ma publiczne endpointy fiszek i brak endpointu generacji. Model `Flashcard` nie ma ownership, a PRD wymaga logowania i prywatnosci danych per konto.

## Desired End State

Zalogowany user wysyla tekst, dostaje wygenerowane drafty i ma je zapisane na swoim koncie. Niezalogowany user nie moze uruchomic generacji, a drugi user nie widzi cudzych danych. API zwraca stabilne kody bledow dla walidacji, limitow i problemow providera.

## Key Decisions Made

| Decision | Choice | Why (1 sentence) | Source |
| --- | --- | --- | --- |
| Scope | Generate + save owned drafts | Daje wartosc produktu i od razu zgodnosc z ownership. | Plan |
| Priority | Security and ownership first | Ogranicza ryzyko wycieku i koszt pozniejszego reworku. | Plan |
| Auth mechanism | Session auth required | Jest zgodny z aktualnym stackiem Django i MVP. | Plan |
| Data model | GenerationBatch + owned Flashcards | Umozliwia audyt, retry i przyszly review per partia. | Plan |
| Errors | Classified errors with stable codes | Zapewnia przewidywalny kontrakt dla klienta i testow. | Plan |
| Testing bar | Full auth+ownership matrix | Potwierdza brak wyciekow i stabilnosc kontraktu API. | Plan |
| Performance guard | Soft limits + timeout budget | Trzyma koszt i czas odpowiedzi w granicach MVP. | Plan |

## Scope

**In scope:**
- endpoint `POST /api/cards/generation/generate/` za auth,
- zapis wygenerowanych fiszek jako owned records,
- encja partii generacji,
- klasyfikacja bledow 400/401/429/502,
- testy auth/ownership/error matrix,
- smoke test preview dla gated generation.

**Out of scope:**
- review accept/edit/reject,
- JWT migration,
- zaawansowany prompt engineering,
- nowe role,
- mobile i inne formaty importu.

## Architecture / Approach

Plan jest etapowy: najpierw kontrakty gate (auth + ownership), potem endpoint i warstwa serwisowa generacji, nastepnie persystencja per owner i izolacja danych, na koncu walidacja preview. Ten uklad minimalizuje ryzyko uruchomienia publicznej generacji bez ochrony danych.

## Phases at a Glance

| Phase | What it delivers | Key risk |
| --- | --- | --- |
| 1. Gate Contracts Readiness | Ownership schema i gotowe kontrakty auth | Niespojne dane dev przy migracji |
| 2. Gated Generation Endpoint | Endpoint generacji z walidacja, timeout i kodami bledow | Niepelna klasyfikacja bledow providera |
| 3. Owned Persistence and Isolation | Zapis generated cards pod ownerem i twarda izolacja | Wyciek danych przy detail/delete |
| 4. Preview Validation and Rollout | Smoke test i gotowosc do promocji | Roznice miedzy local i preview runtime |

**Prerequisites:** dostepny foundation auth/ownership (lub jego domkniecie na poczatku tej zmiany), skonfigurowane srodowisko Django i deploy preview.  
**Estimated effort:** ~2-3 sesje implementacyjne przez 4 fazy.

## Open Risks & Assumptions

- Zakladamy session auth jako docelowy mechanizm MVP.
- Zakladamy, ze mozna bezpiecznie ograniczyc dane dev podczas migracji ownera.
- Zakladamy, ze provider AI moze byc opakowany prostym adapterem serwisowym.

## Success Criteria (Summary)

- Zalogowany user moze wygenerowac i zapisac drafty fiszek na swoim koncie.
- Niezalogowany user nie uruchomi generacji, a drugi user nie widzi cudzych danych.
- Testy API oraz smoke test preview potwierdzaja brak regresji i stabilny kontrakt bledow.
