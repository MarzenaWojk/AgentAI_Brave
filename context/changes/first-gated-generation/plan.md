# First Gated Generation Implementation Plan

## Overview

Implementujemy pierwszy bezpieczny endpoint generacji AI dla fiszek. Endpoint ma byc dostepny tylko dla zalogowanych uzytkownikow, zapisywac wynik jako owned records i zwracac stabilny kontrakt bledow, zgodny z istniejacym stylem API JSON.

## Current State Analysis

Kod bazowy ma publiczne endpointy CRUD fiszek i nie posiada endpointu generacji.
Obecny model fiszki nie ma ownership, a endpointy nie wymagaja auth.
W repo istnieje juz plan foundation auth/ownership, ale brak potwierdzonej implementacji kodu.

## Desired End State

Zalogowany uzytkownik moze wyslac tekst zrodlowy, otrzymac i zapisac wygenerowane drafty fiszek, a dane pozostaja prywatne per konto. API zwraca przewidywalne kody bledow dla walidacji, auth, limitow i problemow providera.

### Key Discoveries:

- Model fiszki nie ma ownera: `cards/models.py:1`
- Endpointy API fiszek sa publiczne i `csrf_exempt`: `cards/views.py:39`
- Routing app pozwala rozszerzyc API bez zmian architektury projektu: `cards/urls.py:1`, `tenx_cards/urls.py:14`
- PRD wymaga logowania i prywatnosci danych per konto: `context/foundation/prd.md:92`
- Wymaganie generacji AI jest must-have: `context/foundation/prd.md:57`

## What We're NOT Doing

- Nie implementujemy review accept/edit/reject.
- Nie wprowadzamy JWT ani przebudowy auth poza session auth.
- Nie budujemy nowego, zaawansowanego algorytmu powtorek.
- Nie dodajemy importu innych formatow niz tekst.
- Nie optymalizujemy zaawansowanie promptow poza MVP-safe kontrakt.

## Implementation Approach

Podejscie jest incremental i bezpieczne:
1. Ustabilizowac kontrakt ownership/auth jako gate (lub zweryfikowac i dopelnic, jesli foundation nie jest jeszcze zakodowany).
2. Dodac endpoint generacji z jasno zdefiniowanym payloadem, timeout budget i klasyfikacja bledow.
3. Zapisywac wyniki jako owned flashcards i utrzymac izolacje danych miedzy uzytkownikami.
4. Potwierdzic macierza testow API oraz smoke testem preview.

## Critical Implementation Details

### Timing & lifecycle

Ta zmiana zalezy od kontraktow auth/ownership z foundation. Jesli w momencie implementacji nadal ich nie ma w kodzie, trzeba je dowiezc na poczatku tej zmiany jako warunek uruchomienia endpointu generacji. Nie wolno uruchamiac generacji jako endpointu publicznego.

## Phase 1: Gate Contracts Readiness

### Overview

Zapewnic lub zweryfikowac minimalne kontrakty auth i ownership wymagane przez bramkowana generacje.

### Changes Required:

#### 1. Ownership and generation schema

**File**: `cards/models.py`

**Intent**: Rozszerzyc model danych tak, by wygenerowane fiszki byly zawsze powiazane z wlascicielem i mozna bylo grupowac wynik pojedynczego wywolania generacji.

**Contract**:
- `Flashcard` ma `owner` wskazujacego `settings.AUTH_USER_MODEL`.
- Dodana encja `GenerationBatch` z minimalnymi metadanymi (owner, source_text, requested_count, created_at).
- `Flashcard` moze miec relacje do `GenerationBatch` (nullable dla kompatybilnosci z danymi historycznymi).

#### 2. Migrations

**File**: `cards/migrations/*.py`

**Intent**: Dodac migracje dla ownership i GenerationBatch z bezpiecznym przejsciem dla lokalnych danych dev.

**Contract**:
- Migracje sa deterministyczne i przechodza na czystej i istniejacej bazie.
- Strategia danych dev jest jawna (cleanup lub przypisanie techniczne) i opisana w migration notes.

#### 3. Auth gate verification

**File**: `cards/views.py`, `cards/urls.py`

**Intent**: Zweryfikowac, ze endpointy wymagane przez session auth sa dostepne i gotowe jako podstawa dla gate generation.

**Contract**:
- Dostepny jest minimalny flow `register/login/logout/me`.
- Brak dostepu do endpointow wymagajacych ownership bez sesji.

### Success Criteria:

#### Automated Verification:

- `.venv/Scripts/python.exe manage.py makemigrations` tworzy poprawne migracje bez konfliktow.
- `.venv/Scripts/python.exe manage.py migrate` przechodzi lokalnie bez bledow.
- `.venv/Scripts/python.exe manage.py test cards` przechodzi dla testow auth/ownership baseline.

#### Manual Verification:

- Rejestracja i logowanie dzialaja end-to-end przez API.
- Niezalogowany klient nie ma dostepu do endpointow protected.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 2: Gated Generation Endpoint and Error Contract

### Overview

Dostarczyc endpoint generacji fiszek, ktory jest dostepny tylko dla zalogowanych i zwraca stabilny kontrakt odpowiedzi oraz bledow.

### Changes Required:

#### 1. Generation API handler

**File**: `cards/views.py`

**Intent**: Dodac endpoint POST dla generacji draftow fiszek z tekstu, z walidacja wejscia i timeout budget.

**Contract**:
- Nowy endpoint: `POST /api/cards/generation/generate/`
- Wejscie JSON:
  - `source_text` (required, non-empty string)
  - `requested_count` (optional integer, domyslnie 5)
- Limity MVP:
  - `source_text` max length (np. 5000 znakow)
  - `requested_count` range (np. 1..20)
  - timeout budget dla providera (np. 10 sekund)
- Auth: endpoint wymaga aktywnej sesji.
- Bledy sa klasyfikowane:
  - 400 `VALIDATION_ERROR`
  - 401 `AUTH_REQUIRED`
  - 429 `RATE_LIMITED` lub `LIMIT_EXCEEDED`
  - 502 `PROVIDER_ERROR`
- Sukces zwraca `batch_id` i liste draftow.

#### 2. Generation service boundary

**File**: `cards/services/generation.py` (new)

**Intent**: Odseparowac logike wywolania providera AI od warstwy HTTP, aby uproscic testy i przyszla podmiane providerow.

**Contract**:
- Publiczna funkcja przyjmuje `source_text`, `requested_count`, `timeout_s`.
- Zwraca liste draftow w postaci kontraktu domenowego (`front`, `back`).
- Wyjatki domenowe mapuja sie jednoznacznie na kody bledow API.

#### 3. Routing

**File**: `cards/urls.py`

**Intent**: Dodac trase endpointu generacji w module app routes.

**Contract**:
- Endpoint jest pod namespace `api/cards/generation/`.
- Glowny routing projektu pozostaje bez zmian architektonicznych.

### Success Criteria:

#### Automated Verification:

- Testy endpointu generacji pokrywaja happy path i bledy klasyfikowane.
- Testy walidacji limitow przechodza (dlugosc tekstu, requested_count, timeout mapping).
- `.venv/Scripts/python.exe manage.py test cards` przechodzi bez regresji istniejacego API.

#### Manual Verification:

- Zalogowany uzytkownik moze wygenerowac drafty z poprawnego tekstu.
- Niezalogowany uzytkownik dostaje 401 na endpoint generacji.
- Przy sztucznie zasymulowanym bledzie providera API zwraca kontrolowany blad, a nie traceback.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 3: Owned Persistence and Isolation Guarantees

### Overview

Zapisywac wygenerowane fiszki jako dane wlasciciela i potwierdzic izolacje per user dla odczytu i operacji po ID.

### Changes Required:

#### 1. Persist generated drafts as owned flashcards

**File**: `cards/views.py`, `cards/models.py`

**Intent**: Zapewnic, by kazdy draft wygenerowany przez endpoint byl zapisywany jako rekord wlasciciela i przypiety do batcha.

**Contract**:
- `Flashcard.owner` zawsze ustawiane na `request.user`.
- `Flashcard.generation_batch` ustawiane dla rekordow z generacji.
- Brak mozliwosci utworzenia anonimowej fiszki przez endpoint generacji.

#### 2. Retrieval and detail isolation

**File**: `cards/views.py`

**Intent**: Zweryfikowac lub dopelnic filtrowanie listy i detaili tak, by endpointy zwracaly wyłącznie rekordy wlasciciela.

**Contract**:
- Lista fiszek filtruje po ownerze.
- Dostep do cudzego rekordu po ID zwraca 404.
- Usuniecie cudzego rekordu po ID zwraca 404.

#### 3. Tests matrix for ownership and failures

**File**: `cards/tests.py`

**Intent**: Dodac pelna macierz testowa auth+ownership+error contract dla endpointu generacji i operacji na fiszkach.

**Contract**:
- Testy obejmuja minimum:
  - auth required,
  - two-user isolation,
  - walidacje inputu,
  - timeout/provider failure mapping,
  - regresje kodow bledow.

### Success Criteria:

#### Automated Verification:

- Testy dwoch uzytkownikow potwierdzaja brak wycieku danych miedzy kontami.
- Testy endpointu detail/delete dla cudzego ID zwracaja 404.
- `.venv/Scripts/python.exe manage.py check` i `.venv/Scripts/python.exe manage.py test cards` przechodza.

#### Manual Verification:

- User A generuje fiszki i widzi je na swojej liscie.
- User B po zalogowaniu nie widzi fiszek usera A.
- Usuniecie wlasnej fiszki dziala, usuniecie cudzej nie jest mozliwe.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 4: Preview Validation and Rollout Readiness

### Overview

Zamknac zmiane przez smoke test preview i przygotowanie bezpiecznej promocji na production.

### Changes Required:

#### 1. Deploy smoke procedure update

**File**: `context/deployment/deploy-plan-v2.md` (if maintained), `context/changes/first-gated-generation/plan.md`

**Intent**: Zaktualizowac i wykonac smoke flow specyficzny dla gated generation.

**Contract**:
- Smoke flow obejmuje:
  - register -> login -> generation -> list -> logout
  - negative auth test bez sesji
  - two-user isolation check

#### 2. Runtime configuration checks

**File**: `tenx_cards/settings.py`, Railway environment

**Intent**: Potwierdzic, ze limity i timeout sa zgodne z budgetem MVP i nie prowadza do silent failure.

**Contract**:
- Timeout i limity sa konfigurowalne przez env (tam gdzie to uzasadnione).
- Blad konfiguracji nie prowadzi do niesprawdzalnego zachowania endpointu.

### Success Criteria:

#### Automated Verification:

- `.venv/Scripts/python.exe manage.py check` przechodzi.
- `.venv/Scripts/python.exe manage.py migrate` przechodzi na preview.
- `.venv/Scripts/python.exe manage.py test cards` przechodzi po deployu preview.

#### Manual Verification:

- Smoke flow gated generation dziala na preview URL.
- Czas odpowiedzi endpointu generacji jest akceptowalny w granicach MVP.
- Regressions na homepage i health endpoint nie wystepuja.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

## Testing Strategy

### Unit Tests:

- Walidacja payloadu `source_text` i `requested_count`.
- Mapowanie wyjatkow serwisu generacji na stabilne kody bledow.
- Testy helperow odpowiedzi bledow i struktury JSON.

### Integration Tests:

- End-to-end API: register/login/generate/list/detail/delete/logout.
- Izolacja danych: User A vs User B na liscie i detailu.
- Scenariusze bledow providera i timeout.

### Manual Testing Steps:

1. Zaloguj User A, wygeneruj zestaw, potwierdz zapis i widocznosc.
2. Zaloguj User B, potwierdz brak dostepu do danych User A.
3. Wykonaj request bez sesji i potwierdz 401.
4. Wymus timeout providera i potwierdz kontrolowany blad API.

## Performance Considerations

- Przyjac MVP budget: p95 dla endpointu generacji <= 10s, zgodnie z PRD.
- Ograniczyc rozmiar `source_text` i `requested_count`, by unikac niekontrolowanego kosztu i czasu.
- Dla timeoutow i limitów zwracac jawny kod bledu, bez silent retry wydluzajacego request.

## Migration Notes

- Migracje ownership i GenerationBatch musza byc kompatybilne z lokalna baza deweloperska.
- Jesli dane dev sa niespojne z nowym kontraktem ownera, preferowany jest kontrolowany cleanup lokalny przed migracja.
- W razie problemow na preview, rollback do poprzedniej rewizji i ponowne przejscie migracji na czystej bazie.

## References

- PRD: `context/foundation/prd.md`
- Roadmap slice S-02: `context/foundation/roadmap.md`
- Foundation plan: `context/changes/auth-ownership-foundation/plan.md`
- Existing API endpoints: `cards/views.py:39`, `cards/views.py:103`
- Existing tests baseline: `cards/tests.py:6`

## Progress

> Convention: `- [ ]` pending, `- [x]` done. Append ` — <commit sha>` when a step lands. Do not rename step titles.

### Phase 1: Gate Contracts Readiness

#### Automated

- [ ] 1.1 Schema migrations for owner and GenerationBatch apply cleanly
- [ ] 1.2 Auth and ownership baseline tests pass in cards suite

#### Manual

- [ ] 1.3 Register/login flow verified via API
- [ ] 1.4 Protected endpoints reject unauthenticated requests

### Phase 2: Gated Generation Endpoint and Error Contract

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
