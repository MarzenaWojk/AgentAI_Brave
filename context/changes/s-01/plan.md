# S-01 Account Access Flow Implementation Plan

## Overview

W tej zmianie dostarczamy minimalny, produkcyjnie uzywalny flow dostepu do konta: rejestracja, logowanie, wylogowanie i endpoint me. Celem jest domkniecie warstwy dostepu użytkownika wymaganej przez roadmape i odblokowanie dalszego lancucha AI generation.

## Current State Analysis

Obecny backend ma API JSON i routing Django, ale brak dedykowanego flow auth dla konta na poziomie slice S-01. Kontrakt auth/ownership zostal zaplanowany jako foundation F-01 i stanowi bezposrednia zaleznosc tej zmiany.

### Key Discoveries:

- S-01 ma twarda zaleznosc od F-01: context/foundation/roadmap.md:103
- Zakres S-01 to konto i logowanie, bez recovery flow: context/foundation/roadmap.md:109
- PRD wymaga logowania i prywatnosci danych per konto: context/foundation/prd.md:92
- Foundation plan juz ustalil minimalny zakres auth register/login/logout/me: context/changes/auth-ownership-foundation/plan.md:23

## Desired End State

Uzytkownik moze zalozyc konto i zalogowac sie przez API JSON, utrzymac sesje, odczytac swoj stan przez me i bezpiecznie sie wylogowac. Negatywne scenariusze zwracaja kontrolowane bledy, a flow jest gotowy jako bramka dla kolejnych endpointow wymagajacych zalogowania. S-01 nie jest oznaczane jako completed, dopoki testy izolacji ownership z foundation F-01 nie przechodza.

## What We're NOT Doing

- Password reset i email verification.
- JWT/token auth migration.
- Rozbudowane role i uprawnienia poza jedna rola MVP.
- Zmiany w AI generation i review (to kolejne slice'y).

## Implementation Approach

S-01 implementujemy jako cienka warstwe kontraktu konta oparta o session auth Django i JSON API. Trzymamy istniejacy styl odpowiedzi bledow, unikamy zmian architektonicznych w routingach i skupiamy sie na stabilnym, testowalnym flow register/login/logout/me.

## Phase 0: Foundation Gate

### Overview

Potwierdzic, ze zaleznosc F-01 jest zamknieta przed startem implementacji S-01.

### Changes Required:

#### 1. Prerequisite verification

**File**: context/changes/auth-ownership-foundation/change.md

**Intent**: Potwierdzic, ze foundation auth/ownership jest zakonczone i nie wymaga domykania podczas S-01.

**Contract**:
- Status F-01 to completed, nie planned.
- W kodzie istnieje ownership contract wymagany przez roadmape dla dalszych slice'ow.

### Success Criteria:

#### Automated Verification:

- F-01 ma status completed w change metadata.
- Cards test suite przechodzi na branchu z wdrozonym F-01.

#### Manual Verification:

- Potwierdzone, ze S-01 startuje bez luki zaleznosci wobec F-01.

## Phase 1: Account Endpoint Contract

### Overview

Zdefiniowac i wdrozyc endpointy auth dla konta uzytkownika zgodnie z minimalnym zakresem MVP.

### Changes Required:

#### 1. Auth handlers

**File**: cards/views.py

**Intent**: Dodac endpointy register/login/logout/me i utrzymac spojnosc JSON API.

**Contract**:
- POST /api/cards/auth/register/
- POST /api/cards/auth/login/
- POST /api/cards/auth/logout/
- GET /api/cards/auth/me/
- Stabilny kontrakt bledow dla walidacji i nieudanej autoryzacji.

#### 2. Auth routes

**File**: cards/urls.py

**Intent**: Podlaczyc endpointy auth w module app routes.

**Contract**:
- Trasy auth sa obslugiwane w cards/urls.py
- Glowny include w tenx_cards/urls.py pozostaje bez zmian.

### Success Criteria:

#### Automated Verification:

- .venv/Scripts/python.exe manage.py test cards przechodzi dla testow auth happy path.
- .venv/Scripts/python.exe manage.py check przechodzi bez nowych bledow.

#### Manual Verification:

- Uzytkownik moze zarejestrowac konto i zalogowac sie przez API.
- Endpoint me zwraca zalogowanego usera i 401 bez sesji.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 2: Failure Modes and API Consistency

### Overview

Domknac scenariusze bledow i spojnosc odpowiedzi, aby klienci API dostali przewidywalne zachowanie.

### Changes Required:

#### 1. Error mapping

**File**: cards/views.py

**Intent**: Ustandaryzowac odpowiedzi bledow dla brakow danych, zlych danych logowania i metod niedozwolonych.

**Contract**:
- Bledy walidacji zwracaja 400.
- Bledy auth zwracaja 401.
- Niedozwolone metody zwracaja 405.
- Odpowiedz bledow utrzymuje format error.code/error.message/error.context.

#### 2. Auth API tests

**File**: cards/tests.py

**Intent**: Pokryc testami happy path i negatywne scenariusze auth.

**Contract**:
- Testy register/login/logout/me dla poprawnych danych.
- Testy dla zlych danych logowania i brakujacych pol.
- Testy 405 na nieobslugiwanych metodach endpointow auth.

### Success Criteria:

#### Automated Verification:

- .venv/Scripts/python.exe manage.py test cards przechodzi z testami negatywnymi auth.
- Wszystkie testy METHOD_NOT_ALLOWED sprawdzaja nadal nieobslugiwane metody.

#### Manual Verification:

- Bledne logowanie zwraca kontrolowany blad bez traceback.
- Niepelne payloady register/login zwracaja czytelny blad walidacji.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 3: Slice Readiness for Downstream Work

### Overview

Potwierdzic, ze S-01 rzeczywiscie odblokowuje S-02 i S-06 bez dodatkowych niespodzianek kontraktowych.

### Changes Required:

#### 1. Readiness checks

**File**: cards/tests.py

**Intent**: Dodac lekki zestaw testow integracyjnych potwierdzajacych, ze zalogowany user ma aktywna sesje dostepna dla kolejnych endpointow.

**Contract**:
- Po login me zwraca ten sam user identity.
- Po logout me zwraca 401.

### Success Criteria:

#### Automated Verification:

- .venv/Scripts/python.exe manage.py check przechodzi.
- .venv/Scripts/python.exe manage.py migrate przechodzi.
- .venv/Scripts/python.exe manage.py test cards przechodzi.
- Testy izolacji ownership (foundation F-01) przechodza jako gate zamkniecia S-01.

#### Manual Verification:

- Preview smoke flow auth przechodzi na URL deploymentu.
- Brak regresji na endpointach homepage i health.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

## Testing Strategy

### Unit Tests:

- Walidacja payloadu register/login.
- Mapa kodow bledow auth.

### Integration Tests:

- Register -> login -> me -> logout flow.
- Brak sesji -> me = 401.

### Manual Testing Steps:

1. Utworz konto nowego usera przez endpoint register.
2. Zaloguj usera i sprawdz endpoint me.
3. Wyloguj usera i potwierdz brak sesji.
4. Zweryfikuj bledy przy zlym hasle i brakujacych polach.

## Performance Considerations

- Endpointy auth sa lekkie i nie wymagaja osobnych optymalizacji wydajnosci na etapie S-01.
- Kluczowe jest utrzymanie stabilnosci i przewidywalnych kodow odpowiedzi.

## Migration Notes

- S-01 nie wymaga nowych migracji, jesli F-01 jest juz wdrozone.
- Jesli F-01 nie jest wdrozone, implementacja S-01 musi byc wykonywana razem z foundation.

## References

- context/foundation/roadmap.md
- context/foundation/prd.md
- context/changes/auth-ownership-foundation/plan.md
- cards/views.py
- cards/urls.py
- cards/tests.py

## Progress

> Convention: - [ ] pending, - [x] done. Append — <commit sha> when a step lands. Do not rename step titles.

### Phase 0: Foundation Gate

#### Automated

- [ ] 0.1 F-01 change metadata shows completed status
- [ ] 0.2 Cards tests pass on branch with F-01 implemented

#### Manual

- [ ] 0.3 Dependency gate confirmation recorded before S-01 implementation

### Phase 1: Account Endpoint Contract

#### Automated

- [x] 1.1 Auth happy-path tests pass in cards suite
- [x] 1.2 Django check passes without new errors

#### Manual

- [ ] 1.3 Register and login work via API
- [ ] 1.4 Endpoint me returns user in-session and 401 out-of-session

### Phase 2: Failure Modes and API Consistency

#### Automated

- [ ] 2.1 Auth negative-path tests pass
- [ ] 2.2 METHOD_NOT_ALLOWED tests validate unsupported methods

#### Manual

- [ ] 2.3 Wrong credentials return controlled auth error
- [ ] 2.4 Invalid payload returns validation error without traceback

### Phase 3: Slice Readiness for Downstream Work

#### Automated

- [ ] 3.1 Check, migrate, and cards tests pass
- [ ] 3.2 Session continuity tests pass for me before and after logout
- [ ] 3.3 Ownership isolation tests from F-01 pass as S-01 close gate

#### Manual

- [ ] 3.4 Preview smoke flow register-login-me-logout-me401 passes
- [ ] 3.5 Homepage and health endpoints remain stable
