---
project: "# TODO: project — see Open Questions"
version: 1
status: draft
created: 2026-06-05
updated: 2026-06-05
prd_version: 1
main_goal: speed
top_blocker: time
---

# Roadmap: # TODO: project — see Open Questions

> Derived from `context/foundation/prd.md` (v1) + auto-researched codebase baseline.
> Edit-in-place; archive when superseded.
> Slices below are listed in dependency order. The "At a glance" table is the index.

## Vision recap

Produkt ma zmniejszyc tarcie w nauce jezykow: zamiast recznie budowac fiszki, uzytkownik ma przejsc od tekstu zrodlowego do gotowego zestawu i pierwszej powtorki w jednej sesji. Wersja MVP ma dzialac w warunkach solo builda po godzinach, wiec kolejnosc prac musi prowadzic do jak najszybszego uruchomienia kompletnego przeplywu wartosci. Priorytetem roadmapy jest szybkie domkniecie lancucha: rejestracja -> generacja -> review -> zapis -> pierwsza powtorka.

## North star

**S-05: Uzytkownik moze uruchomic pierwsza sesje powtorki dla zaakceptowanych fiszek.** To jest walidacyjny kamien milowy dla MVP, bo potwierdza caly lancuch wartosci od wejscia tekstu do realnego momentu nauki.

> North star w tym roadmapie to najmniejszy end-to-end wynik, ktory po dowiezieniu potwierdza, ze glowna hipoteza produktu dziala w praktyce.

## At a glance

| ID | Change ID | Outcome (user can …) | Prerequisites | PRD refs | Status |
|---|---|---|---|---|---|
| F-01 | auth-ownership-foundation | (foundation) minimalny kontrakt tozsamosci i wlasnosci danych jest gotowy | — | Access Control, NFR-privacy | ready |
| S-01 | account-access-flow | user can zarejestrowac konto i zalogowac sie do aplikacji | F-01 | FR-006, US-01 | proposed |
| S-02 | text-to-ai-draft-cards | user can wkleic tekst i wygenerowac draft fiszek przez AI | S-01 | FR-001, FR-002, US-01 | proposed |
| S-03 | review-generated-cards | user can zaakceptowac, edytowac lub odrzucic wygenerowane fiszki | S-02 | FR-003, FR-005, US-01 | proposed |
| S-04 | save-reviewed-cards | user can zapisac zaakceptowane fiszki na swoim koncie | S-03 | FR-006, US-01 | proposed |
| S-05 | first-review-session | user can uruchomic pierwsza sesje powtorki dla zapisanych fiszek | S-04 | FR-007, US-01 | proposed |
| S-06 | manual-cards-crud | user can tworzyc fiszki manualnie i zarzadzac nimi | S-01 | FR-004, FR-005 | proposed |

## Streams

Navigation aid — groups items that share a Prerequisites chain. Canonical ordering still lives in the dependency graph below; this table is the proposed reading order across parallel tracks.

| Stream | Theme | Chain | Note |
|---|---|---|---|
| A | Core value chain | `F-01` -> `S-01` -> `S-02` -> `S-03` -> `S-04` -> `S-05` | Gowny lancuch pod cel speed i walidacje hipotezy produktu. |
| B | Manual fallback | `S-06` | Rownolegly fallback po `S-01`; mozna uruchomic niezaleznie od AI chain. |

## Baseline

What's already in place in the codebase as of `2026-06-05` (auto-researched + user-confirmed).
Foundations below assume these are present and do NOT re-scaffold them.

- **Frontend:** absent — brak UI frameworka, template'ow i statycznych assetow; API tylko JSON.
- **Backend / API:** present — Django routing i endpointy JSON dla kart w `cards/views.py`, `cards/urls.py`, `tenx_cards/urls.py`.
- **Data:** present — model `Flashcard`, migracja `0001_initial`, lokalne sqlite + obsluga `DATABASE_URL` w `tenx_cards/settings.py`.
- **Auth:** absent — brak login flow, brak ochrony endpointow na poziomie routingu API.
- **Deploy / infra:** partial — Railway online + runtime dependencies, ale brak pelnej automatyzacji CI workflow jako kod.
- **Observability:** partial — endpoint `/health/` istnieje, brak centralnego LOGGING/metryk/trackingu bledow.

## Foundations

### F-01: Minimalny kontrakt tozsamosci i wlasnosci

- **Outcome:** (foundation) aplikacja ma minimalny kontrakt auth + ownership, tak aby dane fiszek byly scisle powiazane z kontem i gotowe do dalszych slice'ow.
- **Change ID:** auth-ownership-foundation
- **PRD refs:** Access Control, NFR-privacy, FR-006
- **Unlocks:** S-01, S-02, S-04, S-06
- **Prerequisites:** —
- **Parallel with:** —
- **Blockers:** —
- **Unknowns:**
  - Jakie minimalne acceptance criteria dla loginu i ownership sa wymagane w MVP? — Owner: user. Block: no.
- **Risk:** Zbyt waski kontrakt auth moze wymusic kosztowne poprawki podczas integracji zapisu i review.
- **Status:** proposed

## Slices

### S-01: Dostep do konta

- **Outcome:** Uzytkownik moze zarejestrowac konto i zalogowac sie do aplikacji.
- **Change ID:** account-access-flow
- **PRD refs:** FR-006, US-01
- **Prerequisites:** F-01
- **Parallel with:** —
- **Blockers:** —
- **Unknowns:**
  - Czy w MVP wystarczy jedna metoda logowania bez recovery flow? — Owner: user. Block: no.
- **Risk:** Rozszerzenie scope auth ponad MVP spowolni caly lancuch speed-first.
- **Status:** ready

### S-02: Generacja draftu fiszek z tekstu

- **Outcome:** Uzytkownik moze wkleic tekst i wygenerowac draft fiszek przez AI.
- **Change ID:** text-to-ai-draft-cards
- **PRD refs:** FR-001, FR-002, US-01
- **Prerequisites:** S-01
- **Parallel with:** S-06
- **Blockers:** —
- **Unknowns:**
  - Jakie acceptance criteria dla jakosci draftu uznajemy za minimum MVP? — Owner: user. Block: no.
- **Risk:** Slaba jakosc draftow obnizy wskaznik akceptacji i utrudni walidacje metryk sukcesu.
- **Status:** proposed

### S-03: Sesja review wygenerowanych fiszek

- **Outcome:** Uzytkownik moze zaakceptowac, edytowac lub odrzucic wygenerowane fiszki.
- **Change ID:** review-generated-cards
- **PRD refs:** FR-003, FR-005, US-01
- **Prerequisites:** S-02
- **Parallel with:** S-06
- **Blockers:** —
- **Unknowns:**
  - Jakie precyzyjne acceptance criteria review (accept/edit/reject) zamykaja US-01? — Owner: user. Block: no.
- **Risk:** Niedookreslone kryteria review moga spowodowac rework UI/API i opoznienie lancucha.
- **Status:** proposed

### S-04: Zapis zaakceptowanych fiszek na koncie

- **Outcome:** Uzytkownik moze zapisac zaakceptowane fiszki na swoim koncie.
- **Change ID:** save-reviewed-cards
- **PRD refs:** FR-006, US-01
- **Prerequisites:** S-03
- **Parallel with:** —
- **Blockers:** —
- **Unknowns:**
  - Czy potrzebny jest podzial na zestawy juz w MVP, czy tylko zapis listy fiszek? — Owner: user. Block: no.
- **Risk:** Nadmierne modelowanie danych w tym kroku moze zablokowac szybkie domkniecie flow.
- **Status:** proposed

### S-05: Pierwsza sesja powtorki

- **Outcome:** Uzytkownik moze uruchomic pierwsza sesje powtorki dla zapisanych fiszek.
- **Change ID:** first-review-session
- **PRD refs:** FR-007, US-01
- **Prerequisites:** S-04
- **Parallel with:** —
- **Blockers:** —
- **Unknowns:**
  - Jakie minimalne zachowanie gotowego algorytmu uznajemy za zaliczenie pierwszej powtorki? — Owner: user. Block: no.
- **Risk:** Integracja algorytmu powtorek pod koniec lancucha moze ujawnic ukryte zaleznosci danych.
- **Status:** proposed

### S-06: Manualne fiszki i CRUD

- **Outcome:** Uzytkownik moze tworzyc fiszki manualnie i nimi zarzadzac.
- **Change ID:** manual-cards-crud
- **PRD refs:** FR-004, FR-005
- **Prerequisites:** S-01
- **Parallel with:** S-02, S-03
- **Blockers:** —
- **Unknowns:**
  - Czy manualna sciezka wymaga pelnej parity z AI review juz w MVP? — Owner: user. Block: no.
- **Risk:** Rozbudowa CRUD ponad fallback moze ukrasc czas krytyczny dla north star.
- **Status:** proposed

## Backlog Handoff

| Roadmap ID | Change ID | Suggested issue title | Ready for `/10x-plan` | Notes |
|---|---|---|---|---|
| F-01 | auth-ownership-foundation | Foundation: minimalny kontrakt auth i ownership | yes | Warunek startowy dla kont i zapisu |
| S-01 | account-access-flow | User can zalozyc konto i zalogowac sie | no | Wymaga domknietego F-01 |
| S-02 | text-to-ai-draft-cards | User can wygenerowac draft fiszek z tekstu | no | Wymaga zamknietego S-01 |
| S-03 | review-generated-cards | User can przejsc sesje review (accept/edit/reject) | no | Wymaga draftu z S-02 |
| S-04 | save-reviewed-cards | User can zapisac zaakceptowane fiszki na koncie | no | Wymaga review z S-03 |
| S-05 | first-review-session | User can uruchomic pierwsza sesje powtorki | no | North star, wymaga zapisu z S-04 |
| S-06 | manual-cards-crud | User can tworzyc i zarzadzac manualnymi fiszkami | no | Mozliwe rownolegle po S-01 |

## Open Roadmap Questions

1. **Jaka jest wlasciwa nazwa projektu?** — Owner: user. Block: roadmap-wide.
2. **Jaki jest docelowy poziom qps?** — Owner: user. Block: roadmap-wide.
3. **Jaki jest docelowy wolumen danych?** — Owner: user. Block: roadmap-wide.
4. **Jakie sa acceptance criteria dla US-01?** — Owner: user. Block: S-03, S-05.

## Parked

- **Wlasny zaawansowany algorytm powtorek** — Why parked: PRD `## Non-Goals` wyklucza budowe w MVP.
- **Import PDF/DOCX i innych formatow** — Why parked: PRD `## Non-Goals` ogranicza wejscie do kopiuj-wklej tekstu.
- **Wspoldzielenie zestawow fiszek miedzy uzytkownikami** — Why parked: PRD `## Non-Goals`.
- **Integracje z innymi platformami edukacyjnymi** — Why parked: PRD `## Non-Goals`.
- **Aplikacja mobilna** — Why parked: PRD `## Non-Goals` (MVP web-only).

## Done

