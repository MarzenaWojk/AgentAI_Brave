# Text to AI Draft Cards Implementation Plan

## Overview

W tej zmianie dostarczamy pierwszy end-to-end flow generacji draftow fiszek z tekstu: zalogowany uzytkownik wkleja tekst, system tworzy drafty AI, zapisuje je jako owned records w partii generacji i zwraca stabilny kontrakt odpowiedzi. Zmieniamy tylko to, co jest potrzebne do bezpiecznej generacji i dalszego review, bez wchodzenia jeszcze w accept/edit/reject.

## Current State Analysis

Kod bazowy ma publiczne endpointy fiszek i brak endpointu generacji AI. Model `Flashcard` nadal nie ma ownership ani relacji do partii generacji, a obecny backend nie posiada wydzielonej warstwy serwisowej dla generacji.

### Key Discoveries:

- Roadmapa definiuje S-02 jako krok po S-01 i F-01: `context/foundation/roadmap.md`.
- PRD wymaga prywatnosci danych per konto i generacji fiszek z tekstu: `context/foundation/prd.md`.
- Istniejacy plan `first-gated-generation` juz ustalil, ze review accept/edit/reject jest osobnym slice'em.
- W `cards/views.py` istnieje juz spójny kontrakt JSON error helperów i auth gate, wiec generacja moze na tym oprzec swój format odpowiedzi.

## Desired End State

Zalogowany uzytkownik moze wyslac `source_text`, otrzymac drafty fiszek wygenerowane przez AI, a te drafty sa zapisane jako owned records powiazane z partia generacji. API zwraca `batch_id` oraz liste draftow, a wszystkie bledy sa klasyfikowane i przewidywalne. Dane generacji pozostaja prywatne per konto i nie wyciekaja do innych uzytkownikow.

### Key Discoveries:

- S-02 ma twarda zaleznosc od F-01 i S-01; nie wolno uruchamiac generacji jako publicznego endpointu.
- Istniejacy wzorzec odpowiedzi w API to JSON z `_error_response(...)`.
- Najbardziej ryzykowna czesc zmiany to granica miedzy warstwa HTTP a dostawca AI, wiec plan zaklada osobny service adapter.

## What We're NOT Doing

- Nie implementujemy review accept/edit/reject.
- Nie wprowadzamy JWT ani token auth.
- Nie budujemy zaawansowanego algorytmu powtorek.
- Nie importujemy innych formatow niz tekst.
- Nie robimy silent retry na bledach providera.
- Nie przechowujemy pelnego tekstu zrodlowego dluzej niz potrzebne metadane MVP.

## Implementation Approach

Podejscie jest zachowawcze i incremental: najpierw potwierdzamy readiness foundation auth/ownership, nastepnie dodajemy model partii generacji i serwis AI, potem endpoint generacji z walidacja i klasyfikacja bledow, a na koncu potwierdzamy prywatnosc, testy i preview smoke. Ta struktura ogranicza ryzyko publicznej generacji bez ownership oraz pozwala testowac provider bez sprzatania po nieudanych requestach.

## Critical Implementation Details

### Timing & lifecycle

Ta zmiana nie moze wystartowac bez gotowego kontraktu auth/ownership z F-01. Jesli owner na fiszce lub ochrona endpointow nie sa jeszcze dostepne w kodzie, trzeba je najpierw domknac albo zatrzymac rollout tej zmiany do czasu ich wdrozenia. Generacja nie moze byc publiczna ani anonimowa.

### User experience spec

Endpoint generacji ma zwracac komplet draftow od razu, zamiast wymuszac polling albo osobny status screen. To jest MVP-owy kompromis: prostszy flow dla uzytkownika i prostszy test harness dla zespolu, kosztem synchronizacji requestu z czasem odpowiedzi providera.

### Performance constraints

Budzet czasu odpowiedzi dla generacji pozostaje ograniczony do MVP (p95 okolo 10s). Limitujemy rozmiar `source_text` i `requested_count`, a bledy timeout/provider traktujemy jako jawny failure, nie jako ukryte opóznienie.

## Phase 1: Foundation Gate and Data Model

### Overview

Zapewnic kontrakty, na ktorych opiera sie bezpieczna generacja: ownership na fiszkach, partia generacji i gotowy gate do session auth.

### Changes Required:

#### 1. Ownership and batch schema

**File**: `cards/models.py`

**Intent**: Rozszerzyc model danych tak, by wygenerowane fiszki byly zawsze powiazane z wlascicielem i partia generacji mogla przechowac kontekst jednego wywolania AI.

**Contract**:
- `Flashcard` ma `owner = ForeignKey(settings.AUTH_USER_MODEL, ...)`.
- Nowa encja `GenerationBatch` przechowuje `owner`, `source_text` albo minimalne metadata, `requested_count` i `created_at`.
- `Flashcard` moze byc powiazany z `GenerationBatch` przez relacje nullable, zeby zachowac kompatybilnosc danych.

#### 2. Migration plan

**File**: `cards/migrations/*.py`

**Intent**: Dodac migracje dla ownership i batcha tak, aby przejscie bylo deterministyczne na czystej i lokalnej bazie.

**Contract**:
- Migracje przechodza na pustej bazie oraz na obecnym db.sqlite3.
- Strategia danych dev jest jawna w migration notes i nie wymaga zgadywania przez implementera.

#### 3. Auth readiness check

**File**: `cards/views.py`, `cards/urls.py`

**Intent**: Potwierdzic, ze session auth register/login/logout/me jest juz gotowe jako gate dla generacji.

**Contract**:
- Zalogowany user jest dostepny przez sesje Django.
- Endpoint generacji nie ma trybu publicznego.

### Success Criteria:

#### Automated Verification:

- `.venv/Scripts/python.exe manage.py makemigrations` tworzy poprawne migracje bez konfliktow.
- `.venv/Scripts/python.exe manage.py migrate` przechodzi lokalnie bez bledow.
- `.venv/Scripts/python.exe manage.py test cards` przechodzi dla testow auth/ownership baseline.

#### Manual Verification:

- Rejestracja, login i `me` dzialaja jako gate dla generacji.
- Niezalogowany klient nie ma dostepu do flow generacji.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 2: Generation Service Boundary and API Contract

### Overview

Wydzielic logike generacji AI do serwisu i zdefiniowac stabilny kontrakt request/response dla endpointu draft generation.

### Changes Required:

#### 1. Generation service adapter

**File**: `cards/services/generation.py` (new)

**Intent**: Odseparowac wywolanie providera AI od warstwy HTTP, zeby testy i przyszla podmiana providera byly proste.

**Contract**:
- Publiczna funkcja przyjmuje `source_text`, `requested_count`, `timeout_s`.
- Funkcja zwraca liste draftow w kontrakcie domenowym (`front`, `back`).
- Bledy domenowe mapuja sie jednoznacznie na kody odpowiedzi API.

#### 2. Generation endpoint contract

**File**: `cards/views.py`, `cards/urls.py`

**Intent**: Dodac endpoint POST dla generacji draftow z tekstu i utrzymac spojnosc z istniejaczym JSON API.

**Contract**:
- Nowy endpoint: `POST /api/cards/generation/generate/`.
- Wejscie JSON: `source_text` oraz opcjonalnie `requested_count`.
- Odpowiedz sukcesu zwraca `batch_id` i liste draftow.
- Endpoint wymaga aktywnej sesji Django.

### Success Criteria:

#### Automated Verification:

- Testy happy path generacji przechodza.
- Testy walidacji `source_text` i `requested_count` przechodza.
- `.venv/Scripts/python.exe manage.py test cards` przechodzi bez regresji istniejacego API.

#### Manual Verification:

- Zalogowany uzytkownik moze wygenerowac drafty z poprawnego tekstu.
- Odpowiedz ma stabilny kontrakt `batch_id` plus drafty.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 3: Owned Persistence and Isolation Guarantees

### Overview

Zapisac drafty generacji jako owned records i potwierdzic, ze tylko wlasny user widzi swoje dane.

### Changes Required:

#### 1. Persist generated drafts

**File**: `cards/views.py`, `cards/models.py`

**Intent**: Zapewnic, by wynik generacji byl zapisany jako partia draftow przypisana do wlasciciela i gotowa do review.

**Contract**:
- `Flashcard.owner` zawsze wskazuje `request.user` dla wygenerowanych rekordow.
- `GenerationBatch` grupuje wygenerowane drafty.
- Brak mozliwosci utworzenia anonimowego draftu przez generation endpoint.

#### 2. Isolation on read paths

**File**: `cards/views.py`

**Intent**: Zabezpieczyc odczyt tak, aby generowane drafty i ich partia pozostaly prywatne per user.

**Contract**:
- Lista fiszek filtruje po ownerze.
- Dostep do cudzego rekordu zwraca 404.
- Usuniecie cudzego rekordu zwraca 404.

#### 3. Test matrix

**File**: `cards/tests.py`

**Intent**: Dodac pelna macierz testowa dla auth, ownership, draft generation i bledow providera.

**Contract**:
- Testy obejmuja auth required, two-user isolation, walidacje wejscia i mapowanie bledow providera.
- Testy regresji METHOD_NOT_ALLOWED pozostaja na nadal nieobslugiwanych metodach.

### Success Criteria:

#### Automated Verification:

- Testy dwoch uzytkownikow potwierdzaja brak wycieku danych miedzy kontami.
- Testy endpointu detail/delete dla cudzego ID zwracaja 404.
- `.venv/Scripts/python.exe manage.py check` i `.venv/Scripts/python.exe manage.py test cards` przechodza.

#### Manual Verification:

- User A widzi tylko wlasne wygenerowane drafty.
- User B nie widzi i nie usuwa draftow User A.
- Wlasny delete dziala, cudzy delete jest blokowany.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 4: Preview Validation and Rollout Readiness

### Overview

Domknac zmiane przez preview smoke test i potwierdzenie, ze generacja jest stabilna po deployu.

### Changes Required:

#### 1. Preview smoke flow

**File**: `context/changes/text-to-ai-draft-cards/plan.md`

**Intent**: Ustalic i wykonac smoke flow dla preview generacji.

**Contract**:
- Smoke flow obejmuje: register -> login -> generation -> list -> logout.
- Dodatkowo sprawdzany jest brak dostepu bez sesji.

#### 2. Runtime guardrails

**File**: `tenx_cards/settings.py`, Railway environment

**Intent**: Potwierdzic, ze timeout i limity inputu pozostaja zgodne z budzetem MVP i nie powoduja silent failure.

**Contract**:
- Limity i timeout sa czytelne oraz testowalne.
- Blad konfiguracji nie prowadzi do cichego sukcesu z niekompletnym wynikiem.

### Success Criteria:

#### Automated Verification:

- `.venv/Scripts/python.exe manage.py check` przechodzi.
- `.venv/Scripts/python.exe manage.py migrate` przechodzi.
- `.venv/Scripts/python.exe manage.py test cards` przechodzi po deployu preview.

#### Manual Verification:

- Preview smoke flow generation dziala na URL deploymentu.
- Czas odpowiedzi endpointu pozostaje w granicach MVP.
- Homepage i health pozostaja zdrowe po deployu.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

## Testing Strategy

### Unit Tests:

- Walidacja `source_text` i `requested_count`.
- Mapowanie bledow providera na stabilne kody odpowiedzi.
- Kontrakt odpowiedzi success i error JSON.

### Integration Tests:

- End-to-end API: register/login/generate/list/detail/delete/logout.
- Izolacja danych: User A vs User B.
- Scenariusze timeout i provider failure.

### Manual Testing Steps:

1. Zaloguj User A i wygeneruj zestaw z tekstu.
2. Potwierdz, ze drafty sa zapisane i widoczne tylko dla User A.
3. Zaloguj User B i potwierdz brak dostepu do danych User A.
4. Wymus timeout providera i potwierdz kontrolowany blad API.

## Performance Considerations

- Budzet odpowiedzi dla generation endpoint pozostaje ograniczony do MVP.
- Ograniczamy rozmiar `source_text` i `requested_count`.
- Provider failure i timeout zwracaja jawny blad, bez silent retry.

## Migration Notes

- Migracje ownership i GenerationBatch musza byc kompatybilne z lokalna baza deweloperska.
- Jesli dane dev sa niespojne z nowym kontraktem, preferowany jest kontrolowany cleanup lokalny przed migracja.
- W razie problemow na preview rollback wraca do poprzedniej rewizji i czystej bazy.

## References

- `context/foundation/prd.md`
- `context/foundation/roadmap.md`
- `context/changes/auth-ownership-foundation/plan.md`
- `context/changes/s-01/plan.md`
- `context/changes/first-gated-generation/plan.md`
- `cards/views.py`
- `cards/urls.py`
- `cards/tests.py`
- `tenx_cards/settings.py`

## Progress

> Convention: `- [ ]` pending, `- [x]` done. Append ` — <commit sha>` when a step lands. Do not rename step titles.

### Phase 1: Foundation Gate and Data Model

#### Automated

- [x] 1.1 Schema migrations for owner and GenerationBatch apply cleanly
- [x] 1.2 Auth and ownership baseline tests pass in cards suite

#### Manual

- [ ] 1.3 Register/login flow verified via API
- [ ] 1.4 Protected endpoints reject unauthenticated requests

### Phase 2: Generation Service Boundary and API Contract

#### Automated

- [ ] 2.1 Generation endpoint happy-path and validation tests pass
- [ ] 2.2 Error classification tests (400/401/429/502) pass
- [ ] 2.3 Cards test suite passes without regressions

#### Manual

- [ ] 2.4 Authenticated generation works with valid source text
- [ ] 2.5 Unauthenticated generation is blocked with 401
- [ ] 2.6 Provider failure returns controlled JSON error

### Phase 3: Owned Persistence and Isolation Guarantees

#### Automated

- [ ] 3.1 Two-user isolation tests pass for list/detail/delete
- [ ] 3.2 Generated flashcards persist with owner and batch linkage
- [ ] 3.3 Project checks and cards tests pass

#### Manual

- [ ] 3.4 User A can view only own generated cards
- [ ] 3.5 User B cannot view or delete User A cards
- [ ] 3.6 Own delete works while foreign delete is blocked

### Phase 4: Preview Validation and Rollout Readiness

#### Automated

- [ ] 4.1 Preview migration and checks pass
- [ ] 4.2 Post-deploy cards test suite passes

#### Manual

- [ ] 4.3 Preview smoke flow register-login-generate-list-logout passes
- [ ] 4.4 Preview isolation smoke test passes for two users
- [ ] 4.5 Homepage and health remain healthy after deploy
