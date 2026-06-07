# S-01B UI Shell and Auth Pages Implementation Plan

## Overview

W tej zmianie dostarczamy minimalny web UI, ktory pozwala uzytkownikowi korzystac z MVP bez recznego odpalania endpointow JSON. Zakres obejmuje strony auth (register/login), chroniony dashboard oraz podstawowa obsluge listy i tworzenia fiszek, oparta na juz istniejacych endpointach backendu.

## Current State Analysis

Kod aktualnie dziala jako API-only backend. Root URL zwraca JsonResponse, a w repo brak warstwy templates/static i frontendowego runtime. To powoduje, ze produkt jest funkcjonalny technicznie, ale nieuzywalny dla docelowego usera bez klienta HTTP.

### Key Discoveries:

- Root routing prowadzi do endpointu JSON homepage.
- Brak katalogow templates i static dla UI shell.
- Session auth endpointy sa juz dostepne i moga byc wykorzystane przez formularze HTML.
- Roadmapa ma nowy slice S-01B jako warstwe UX enablement.

## Desired End State

Uzytkownik moze wejsc na strone glowna, przejsc do register/login, po zalogowaniu zobaczyc dashboard z lista swoich fiszek i formularzem dodawania nowej fiszki. Wylogowanie konczy sesje i przekierowuje do ekranu logowania. Brak dostepu do dashboardu bez aktywnej sesji.

## What We're NOT Doing

- Nie budujemy SPA i nie dodajemy osobnego frontend frameworka.
- Nie implementujemy generacji AI ani review cards w UI (to kolejne slice'y).
- Nie robimy rozbudowanego systemu komponentow ani themingu.
- Nie zmieniamy kontraktow backend API poza ewentualnymi drobnymi poprawkami integracyjnymi.

## Implementation Approach

Podejscie server-rendered, minimalne i szybkie: Django templates + klasyczne formularze POST + session auth. Pozwala to dostarczyc wartosc UI bez dodatkowego toolchainu, przy zachowaniu zgodnosci z obecnym stackiem i harmonogramem MVP.

## Phase 1: UI Foundation and Routing

### Overview

Stworzyc szkielat warstwy HTML i routing public/protected dla podstawowego UI.

### Changes Required:

#### 1. Template and static scaffold

**File**: `templates/base.html` (new), `templates/home.html` (new), `cards/templates/cards/*.html` (new), `static/css/app.css` (new)

**Intent**: Dodac minimalny, czytelny layout i styl, bez zmiany backend domain logic.

**Contract**:
- Globalny layout z prostym headerem i sekcja content.
- Ekrany: home, register, login, dashboard.
- Styl responsywny desktop/mobile dla podstawowych widokow.

#### 2. UI routes

**File**: `cards/ui_urls.py` (new), `tenx_cards/urls.py`

**Intent**: Rozdzielic trasy UI od API i podpiac je pod root.

**Contract**:
- Root (`/`) renderuje strone HTML, nie JSON.
- API pozostaje pod `/api/cards/` bez zmian.
- Healthcheck pozostaje dostepny pod `/health/`.

### Success Criteria:

#### Automated Verification:

- `.venv/Scripts/python.exe manage.py check` przechodzi.
- Smoke test renderowania stron przechodzi w `cards/tests.py`.

#### Manual Verification:

- `/` wyswietla HTML shell.
- `/login/` i `/register/` renderuja formularze.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 2: Auth UI Flow

### Overview

Podlaczyc formularze UI do session auth i dopiac przekierowania.

### Changes Required:

#### 1. Auth form handlers

**File**: `cards/ui_views.py` (new)

**Intent**: Wdrozyc register/login/logout po stronie server-rendered views.

**Contract**:
- GET renderuje formularz, POST obsluguje walidacje i sesje.
- Sukces register/login przekierowuje na dashboard.
- Logout konczy sesje i przekierowuje na login.
- Bledy formularza sa widoczne na stronie bez tracebacka.

#### 2. Auth tests for UI

**File**: `cards/tests.py`

**Intent**: Dodac testy scenariuszy auth przez warstwe HTML.

**Contract**:
- Test register page + successful submit.
- Test login page + successful submit.
- Test protected dashboard redirect for anonymous user.

### Success Criteria:

#### Automated Verification:

- `.venv/Scripts/python.exe manage.py test cards` przechodzi.
- Testy auth API nie maja regresji.

#### Manual Verification:

- User moze zalozyc konto z poziomu formularza.
- User moze zalogowac i wylogowac sie z poziomu UI.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 3: Dashboard and Flashcards Basics

### Overview

Dostarczyc minimum wartosci po zalogowaniu: lista fiszek i dodawanie nowej fiszki.

### Changes Required:

#### 1. Dashboard data/actions

**File**: `cards/ui_views.py`, `cards/templates/cards/dashboard.html`

**Intent**: Pokazac userowi jego fiszki i pozwolic na szybkie dodanie nowej.

**Contract**:
- Dashboard pobiera tylko fiszki zalogowanego usera.
- Formularz dodawania wymaga front/back i pokazuje bledy walidacji.
- Sukces dodania odswieza liste przez redirect GET.

#### 2. Optional delete action

**File**: `cards/ui_views.py`, `cards/templates/cards/dashboard.html`

**Intent**: Dodac prosty mechanizm usuwania fiszki, jesli mieci sie w czasie MVP.

**Contract**:
- Delete dziala tylko dla wlasnych rekordow.
- Nieautoryzowany dostep jest blokowany.

### Success Criteria:

#### Automated Verification:

- Test list/create (i opcjonalnie delete) przez UI przechodzi.
- `.venv/Scripts/python.exe manage.py check` i `.venv/Scripts/python.exe manage.py test cards` przechodza.

#### Manual Verification:

- Po login user widzi swoje fiszki.
- User dodaje nowa fiszke i widzi ja na liscie.
- (Jesli wdrozone) user usuwa swoja fiszke z dashboardu.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 4: UX Hardening and Preview Readiness

### Overview

Podniesc jakosc UX na tyle, by preview bylo czytelne i testowalne przez uzytkownika.

### Changes Required:

#### 1. UX polish

**File**: `static/css/app.css`, `templates/base.html`

**Intent**: Poprawic czytelnosc i ergonomie podstawowych ekranow.

**Contract**:
- Jednolity styl formularzy, przyciskow i alertow.
- Widoczne komunikaty sukcesu i bledu.
- Uklad poprawny na mobile i desktop.

#### 2. Preview smoke checklist

**File**: `context/changes/ui-shell-and-auth-pages/plan.md`

**Intent**: Spisac i wykonac manualny smoke flow dla UI.

**Contract**:
- Smoke flow: home -> register -> login -> dashboard -> create card -> logout.
- Potwierdzona blokada dashboardu dla niezalogowanego usera.

### Success Criteria:

#### Automated Verification:

- `.venv/Scripts/python.exe manage.py check` przechodzi.
- `.venv/Scripts/python.exe manage.py test cards` przechodzi.

#### Manual Verification:

- Pelny smoke flow UI przechodzi lokalnie i na preview.
- Nie ma regresji endpointow API i healthcheck.

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

## Testing Strategy

### Unit Tests:

- Walidacja formularzy auth i create card.

### Integration Tests:

- Register -> login -> dashboard -> create -> logout przez HTML views.
- Anon user redirect na dashboard protected.

### Manual Testing Steps:

1. Otworz `/` i przejdz do register.
2. Zaloz konto i potwierdz wejscie na dashboard.
3. Dodaj fiszke i potwierdz jej widocznosc.
4. Wyloguj i potwierdz, ze dashboard wymaga logowania.

## Performance Considerations

- Server-rendered strony sa lekkie i powinny miescic sie w wymaganiach responsywnosci MVP dla prostych interakcji.
- Brak dodatkowego bundlera frontend ogranicza narzut runtime i deployment.

## Migration Notes

- Zmiana UI nie wymaga nowych migracji danych, o ile model fiszek i auth sa juz wdrozone.

## References

- `context/foundation/roadmap.md`
- `context/foundation/prd.md`
- `tenx_cards/urls.py`
- `cards/views.py`
- `cards/urls.py`

## Progress

> Convention: `- [ ]` pending, `- [x]` done. Append ` — <commit sha>` when a step lands. Do not rename step titles.

### Phase 1: UI Foundation and Routing

#### Automated

- [ ] 1.1 HTML template scaffold and UI routing wired
- [ ] 1.2 Project checks and UI render tests pass

#### Manual

- [ ] 1.3 Home/login/register pages render correctly
- [ ] 1.4 Root URL shows HTML shell instead of JSON

### Phase 2: Auth UI Flow

#### Automated

- [ ] 2.1 UI auth handlers pass register/login/logout tests
- [ ] 2.2 Existing cards API tests pass without regressions

#### Manual

- [ ] 2.3 User can register and login from UI
- [ ] 2.4 Logout ends session and redirects to login

### Phase 3: Dashboard and Flashcards Basics

#### Automated

- [ ] 3.1 Dashboard list/create (and optional delete) tests pass
- [ ] 3.2 Project checks and cards test suite pass

#### Manual

- [ ] 3.3 User sees only own cards on dashboard
- [ ] 3.4 User can create a card from dashboard form

### Phase 4: UX Hardening and Preview Readiness

#### Automated

- [ ] 4.1 Final checks and tests pass on preview config
- [ ] 4.2 No API/health regressions after UI wiring

#### Manual

- [ ] 4.3 End-to-end smoke flow passes on browser
- [ ] 4.4 Anonymous user cannot access dashboard directly
