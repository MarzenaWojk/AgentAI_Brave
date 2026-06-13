# Deploy hardening and observability baseline Implementation Plan

## Overview

Ten plan scala roadmapowe S-00 i S-00A w jeden strumien wdrozeniowy dla MVP. Celem jest postawienie aplikacji Django pod stabilnym publicznym URL na Railway, dodanie minimalnej obserwowalnosci opartej o logi bledow i health check oraz uruchomienie automatycznego CI/CD na kazdy push do `main`.

## Current State Analysis

Aplikacja ma juz podstawowy kontrakt runtime dla produkcji, ale nie ma jeszcze powtarzalnego procesu wdrozeniowego ani centralnej konfiguracji logowania. `tenx_cards/settings.py` czyta kluczowe zmienne srodowiskowe i obsluguje `DATABASE_URL`, ale nie definiuje `LOGGING` ani dodatkowych bezpiecznikow runtime dla wdrozenia. Endpoint health check juz istnieje, lecz zwraca tylko prosty status i nie jest jeszcze osadzony w szerszym procesie smoke testow i deploy verification. Repo nie ma workflow GitHub Actions, manifestu Railway ani zadnego zautomatyzowanego kroku uruchamiajacego testy, migracje i deploy.

## Desired End State

Po zakonczeniu tego planu repo ma dostarczac w pelni powtarzalny pipeline: push do `main` uruchamia testy jednostkowe, a po ich przejsciu wdraza aplikacje na Railway. Srodowisko produkcyjne ma miec jawny kontrakt zmiennych srodowiskowych, automatyczne migracje i `collectstatic`, podstawowy smoke-test po deployu oraz logowanie ograniczone do bledow, czytelne w Railway logs. Koniec planu jest osiagalny i weryfikowalny, gdy nowa rewizja przechodzi przez GitHub Actions, laduje sie na Railway, odpowiada na `/health/`, a aplikacja dalej przechodzi podstawowe testy Django.

### Key Discoveries:

- `tenx_cards/settings.py:26-34` ma juz env-driven `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` i `CSRF_TRUSTED_ORIGINS`, wiec plan nie zaczyna od przebudowy konfiguracji, tylko od jej domkniecia.
- `tenx_cards/settings.py:97-114` obsluguje `DATABASE_URL` z PostgreSQL i `sslmode=require`, co dobrze pasuje do Railway i zewnetrznej bazy.
- `cards/views.py:39` oraz `cards/public_urls.py:6` definiuja istniejacy endpoint `/health/`, a `cards/tests.py:52-56` juz sprawdza jego podstawowe zachowanie.
- `context/foundation/infrastructure.md` wskazuje Railway jako rekomendowany runtime dla MVP i podaje zalozenia operacyjne zgodne z celem speed.
- W repo nie ma `.github/workflows/*.yml`, `railway.json`, `Procfile` ani `Dockerfile`, wiec CI/CD i first deploy trzeba zaprojektowac od zera.

## What We're NOT Doing

- Nie wdrazamy Sentry, Datadog, Prometheusa ani alertingu.
- Nie przechodzimy na Docker-based deployment, o ile Railway buildpack wystarczy dla Django.
- Nie budujemy preview environments, release tags ani wieloetapowego promotion flow.
- Nie rozszerzamy zakresu o optymalizacje wydajnosciowe, cost monitoring AI ani zaawansowane security hardening poza MVP.

## Implementation Approach

Strategia jest celowo prosta: wykorzystac to, co juz istnieje w Django, i dodac tylko te warstwy, ktore realnie zmniejszaja ryzyko publikacji. Najpierw trzeba dopiac kontrakt runtime i logowanie bledow, potem zbudowac GitHub Actions jako jedyne zrodlo prawdy dla testu i deployu, a na koncu spiac to z Railway przez jawne komendy startowe, migracyjne i smoke-testowe. Plan zaklada, ze S-00A nie bedzie osobnym wdrozeniem, tylko zostanie skonsumowane przez ten jeden change, bo inaczej rozdzielilibysmy jeden przeplyw operacyjny na dwie zalezne zmiany bez zysku.

## Critical Implementation Details

Kolejnosc ma znaczenie: workflow CI/CD nie powinien powstac przed ustaleniem komend runtime i kontraktu env, bo wtedy pierwszy deploy bedzie oparty na zgadywaniu. Health check musi pozostac prosty i szybki; nie wolno zamienic go w endpoint zaleznosciowy od zewnetrznych uslug, bo wtedy przestanie byc wiarygodnym sygnalem liveness dla Railway.

## Phase 1: Domkniecie runtime i kontraktu srodowiska

### Overview

Ta faza stabilizuje lokalny i produkcyjny kontrakt uruchomieniowy, zeby pipeline mial na czym pracowac. Chodzi o jawne ustawienia produkcyjne, brakujace komendy runtime i aktualna dokumentacje env vars.

### Changes Required:

#### 1. Ustawienia Django dla produkcji

**File**: `tenx_cards/settings.py`

**Intent**: Dopiac minimalny production hardening pod Railway bez przepisywania calego settings module. Dodatkowe zmiany maja sluzyc przewidywalnemu deployowi i ograniczeniu liczby niejawnych defaultow w produkcji.

**Contract**: Modul settings nadal pozostaje oparty o zmienne srodowiskowe, ale jawnie definiuje brakujace ustawienia produkcyjne potrzebne do stabilnego runtime, logowania bledow i pracy za reverse proxy Railway.

#### 2. Kontrakt zmiennych srodowiskowych

**File**: `.env.example`

**Intent**: Utrzymac jeden czytelny kontrakt dla lokalnego developmentu, GitHub Actions i Railway. Dokument ma jednoznacznie wskazywac, ktore zmienne sa wymagane, ktore opcjonalne i jakie wartosci sa oczekiwane w produkcji.

**Contract**: `.env.example` zawiera komplet zmiennych wymaganych przez deploy, w tym runtime Django, polaczenie z baza, hosty/CSRF oraz ewentualne flagi uruchomieniowe dla komend release/start.

#### 3. Komendy uruchomieniowe dla platformy

**File**: `requirements.txt`

**Intent**: Zweryfikowac i utrzymac zaleznosci potrzebne do produkcyjnego startu aplikacji na Railway, w szczegolnosci serwer aplikacyjny i adapter bazy.

**Contract**: Zestaw zaleznosci pozostaje wystarczajacy do wykonania migracji, `collectstatic` i startu aplikacji przez produkcyjny serwer WSGI.

### Success Criteria:

#### Automated Verification:

- `python manage.py check` przechodzi z docelowymi ustawieniami deployowymi
- `python manage.py migrate --plan` dziala bez brakujacych zaleznosci runtime

#### Manual Verification:

- Lista wymaganych env vars jest zrozumiala i wystarczajaca do konfiguracji Railway
- Zespol zna docelowe komendy startowe i migracyjne dla pierwszego wdrozenia

**Implementation Note**: Po zakonczeniu tej fazy i przejsciu automatycznej weryfikacji zatrzymaj sie na krotkie sprawdzenie reczne kontraktu env przed przejsciem do CI/CD.

---

## Phase 2: Minimalna obserwowalnosc przez health check i logi bledow

### Overview

Ta faza dodaje najtanszy mozliwy safety-net operacyjny dla MVP: szybki health check, logowanie bledow i podstawowe testy chroniace to zachowanie.

### Changes Required:

#### 1. Konfiguracja logowania produkcyjnego

**File**: `tenx_cards/settings.py`

**Intent**: Dodac centralna konfiguracje `LOGGING`, ktora ogranicza sie do zdarzen bledu i kieruje je na stdout/stderr, zeby Railway mogl je zebrac bez dodatkowej infrastruktury.

**Contract**: Produkcyjne logowanie rejestruje co najmniej bledy Django/request cycle i bledy aplikacyjne na poziomie `ERROR`, bez zalewania logow wpisami `INFO` i `DEBUG`.

#### 2. Utrzymanie lekkiego endpointu health

**File**: `cards/views.py`

**Intent**: Zachowac `/health/` jako szybki, stabilny sygnal gotowosci aplikacji do obslugi requestow po deployu.

**Contract**: Endpoint health pozostaje publiczny, szybki i niezalezny od zewnetrznych providerow; moze rozszerzyc payload o podstawowe metadane runtime tylko wtedy, gdy nie komplikuje semantyki `200 OK`.

#### 3. Testy health i bledow runtime

**File**: `cards/tests.py`

**Intent**: Zamknac obserwowalnosc minimalnym zestawem testow, ktory pilnuje endpointu health i zachowania aplikacji po zmianach settings.

**Contract**: Testy nadal weryfikuja `GET /health/ == 200`, a w razie rozszerzenia payloadu sprawdzaja tylko stabilny kontrakt publiczny, nie szczegoly implementacyjne.

### Success Criteria:

#### Automated Verification:

- `python manage.py test cards` przechodzi po dodaniu konfiguracji logowania
- `python manage.py check --deploy` przechodzi dla ustawien produkcyjnych albo ma jawnie udokumentowane wyjatki MVP

#### Manual Verification:

- Bledy aplikacji pojawiaja sie w logach Railway w czytelnym formacie
- `/health/` nadaje sie do recznego smoke testu po wdrozeniu

**Implementation Note**: Po tej fazie manualnie potwierdz, ze planowane logowanie sluzy do diagnostyki, ale nie zalewa log streamu wpisami informacyjnymi.

---

## Phase 3: Workflow GitHub Actions dla testu i deployu

### Overview

Ta faza buduje powtarzalny pipeline repozytorium: push do `main` uruchamia test jednostkowy i tylko po sukcesie przechodzi do publikacji.

### Changes Required:

#### 1. Workflow CI/CD

**File**: `.github/workflows/deploy.yml`

**Intent**: Dodac pojedynczy workflow pokrywajacy checkout, setup Pythona, instalacje zaleznosci, testy jednostkowe i deploy trigger dla Railway.

**Contract**: Workflow uruchamia sie na push do `main`, zatrzymuje deploy przy bledzie testow i korzysta z GitHub Secrets do danych uwierzytelniajacych potrzebnych przez Railway.

#### 2. Dokumentacja sekretow i pipeline

**File**: `AGENTS.md`

**Intent**: Zachowac onboarding repo zgodny z faktycznym sposobem walidacji i wdrozenia po wprowadzeniu CI/CD.

**Contract**: Sekcja walidacji i/lub reguly repo jednoznacznie wskazuja minimalne komendy sprawdzajace oraz fakt, ze deploy produkcyjny idzie przez GitHub Actions + Railway.

#### 3. Wsparcie dla collectstatic i migracji

**File**: `.github/workflows/deploy.yml`

**Intent**: Zapewnic, ze pipeline nie tylko publikuje kod, ale tez uruchamia przewidywalny proces migracji i przygotowania statycznych assetow.

**Contract**: Workflow albo release command Railway uruchamia `migrate` i `collectstatic` w jednej jawnie opisanej sciezce, bez podwojnego wykonywania tych samych komend w dwoch miejscach.

### Success Criteria:

#### Automated Verification:

- Workflow przechodzi lokalna walidacje skladni YAML i ma komplet wymaganych sekretow
- Push do galezi testowej odwzorowujacej `main` wykonuje testy jednostkowe bez recznych krokow

#### Manual Verification:

- Konfiguracja GitHub Secrets dla Railway jest kompletna i zrozumiala
- Wiadomo, czy migracje i `collectstatic` dzieja sie w GitHub Actions, czy w release command Railway, bez dublowania odpowiedzialnosci

**Implementation Note**: Tu trzeba uniknac najczestszego bledu tego typu zmian: ten sam krok migracyjny nie moze byc zrodlem prawdy jednoczesnie w CI i w Railway runtime.

---

## Phase 4: Spiecie z Railway i pierwszy automatyczny deploy

### Overview

Ta faza materializuje pipeline w docelowym srodowisku. Chodzi o skonfigurowanie Railway tak, by przyjac deploy z GitHub Actions i uruchomic aplikacje zgodnie z kontraktem runtime z wczesniejszych faz.

### Changes Required:

#### 1. Konfiguracja projektu Railway

**File**: `context/deployment/deploy-plan.md`

**Intent**: Zaktualizowac istniejaca notatke deployowa tak, by odpowiadala finalnemu pipeline opisanemu w change planie, zamiast zyc obok kodu jako alternatywny scenariusz.

**Contract**: Dokument deployowy opisuje aktualny startup command, release/migration flow, wymagane zmienne Railway i podstawowy rollback dla pierwszego deployu automatycznego.

#### 2. Sekrety i zmienne srodowiskowe Railway

**File**: `.env.example`

**Intent**: Powiazac repozytoryjny kontrakt env z konfiguracja docelowego runtime w Railway, tak by nie bylo dryfu miedzy lokalnym developmentem, CI i produkcja.

**Contract**: Wszystkie zmienne wymagane przez Railway sa odzwierciedlone w repozytoryjnym kontrakcie env i da sie je ustawic bez interpretacji ukrytej w czacie czy dashboardzie.

#### 3. Smoke test po wdrozeniu

**File**: `.github/workflows/deploy.yml`

**Intent**: Dodac tani post-deploy check, ktory zweryfikuje, ze nowe wdrozenie odpowiada pod publicznym URL i przynajmniej endpoint health dziala.

**Contract**: Po zakonczeniu deployu workflow wykonuje prosty HTTP smoke test przeciw publicznemu URL i failuje pipeline, jesli aplikacja nie odpowiada `200` na uzgodnionym endpointcie.

### Success Criteria:

#### Automated Verification:

- Deploy z GitHub Actions publikuje rewizje na Railway po zielonych testach
- Smoke test po deployu potwierdza odpowiedz `200` z publicznego `/health/`

#### Manual Verification:

- Aplikacja otwiera sie pod publicznym URL Railway po pierwszym deployu
- Reczny przeglad logow Railway pozwala potwierdzic brak oczywistych bledow startowych

**Implementation Note**: Po tej fazie potrzebna jest reczna akceptacja pierwszego deployu, bo dopiero wtedy wiemy, czy kontrakt env i runtime jest rzeczywiscie zamkniety.

---

## Phase 5: Finalna weryfikacja operacyjna i porzadki dokumentacyjne

### Overview

Ostatnia faza domyka plan przez potwierdzenie, ze nowy baseline jest zrozumialy, odtwarzalny i gotowy pod kolejne zmiany produktowe.

### Changes Required:

#### 1. Weryfikacja instrukcji operacyjnych

**File**: `AGENTS.md`

**Intent**: Upewnic sie, ze onboarding repo i polecenia walidacyjne sa zgodne z nowym stanem po wdrozeniu CI/CD oraz pierwszym deployu Railway.

**Contract**: Instrukcje repo wskazuja aktualne komendy walidacyjne i nie przecza rzeczywistej sciezce deployu ani smoke testow.

#### 2. Dokumentacja zmiany

**File**: `context/changes/deploy-hardening-and-observability-baseline/change.md`

**Intent**: Zostawic czytelny slad decyzji wdrozeniowych w artefaktach zmiany, zeby kolejne fazy roadmapy nie musialy odtwarzac ustalen z rozmowy.

**Contract**: `change.md` i plan pozostaja spojne co do zakresu: S-00 zawiera tez wykonanie S-00A jako czesc jednego przeplywu operacyjnego.

### Success Criteria:

#### Automated Verification:

- `python manage.py check`
- `python manage.py migrate`
- `python manage.py test cards`

#### Manual Verification:

- Instrukcje deployu i walidacji sa wystarczajace, by inna osoba mogla powtorzyc wdrozenie
- Zespol potwierdza, ze baseline S-00/S-00A jest zamkniety i nie wymaga osobnego follow-up planu tylko dla CI/CD

**Implementation Note**: Po tej fazie mozna bezpiecznie przejsc do kolejnych slice'ow roadmapy, bo ryzyko deployowe nie powinno juz byc niewidocznym blokerem.

## Testing Strategy

### Unit Tests:

- Utrzymac i ewentualnie rozszerzyc test endpointu `/health/`
- Dodac testy chroniace oczekiwany kontrakt odpowiedzi health po zmianach obserwowalnosci
- Utrzymac zielony pakiet `cards/tests.py` jako minimalna bramka do deployu

### Integration Tests:

- Brak nowych testow integracyjnych w tej zmianie; pipeline opiera sie na testach jednostkowych i smoke tescie HTTP po deployu

### Manual Testing Steps:

1. Ustawic wszystkie wymagane zmienne w Railway i GitHub Secrets zgodnie z `.env.example`.
2. Wypchnac kontrolowana zmiane do `main` i potwierdzic, ze GitHub Actions przechodzi przez testy i deploy.
3. Otworzyc publiczny URL aplikacji i sprawdzic `/health/`, strone glowna oraz podstawowe logowanie do aplikacji.
4. W Railway logs potwierdzic, ze bledy sa widoczne, ale standardowy ruch nie generuje nadmiarowych wpisow informacyjnych.

## Performance Considerations

Plan nie wprowadza nowych funkcji obciazajacych runtime, ale health check musi pozostac bardzo tani. Wszelkie rozszerzenia payloadu health powinny unikac zapytan do bazy i integracji z zewnetrznymi providerami, bo celem jest szybki sygnal liveness, nie pelny audit dependencies.

## Migration Notes

Migracje pozostaja standardowymi migracjami Django, ale ich miejsce wykonania musi byc jednoznaczne. Jesli zostana uruchamiane w Railway jako release command, GitHub Actions nie powinien odpalac ich ponownie przeciw produkcji; jesli workflow uruchamia je zdalnie, Railway nie moze miec drugiej sciezki robiacej to samo.

## References

- Related implementation note: `context/deployment/deploy-plan.md`
- Platform decision: `context/foundation/infrastructure.md`
- Existing production config: `tenx_cards/settings.py:26-34`
- Database runtime contract: `tenx_cards/settings.py:97-114`
- Existing health endpoint: `cards/views.py:39`
- Public health route: `cards/public_urls.py:6`
- Existing health test: `cards/tests.py:52-56`

## Progress

> Convention: `- [ ]` pending, `- [x]` done. Append ` — <commit sha>` when a step lands. Do not rename step titles. See `references/progress-format.md`.

### Phase 1: Domkniecie runtime i kontraktu srodowiska

#### Automated

- [x] 1.1 `python manage.py check` przechodzi z docelowymi ustawieniami deployowymi
- [x] 1.2 `python manage.py migrate --plan` dziala bez brakujacych zaleznosci runtime

#### Manual

- [x] 1.3 Lista wymaganych env vars jest zrozumiala i wystarczajaca do konfiguracji Railway
- [x] 1.4 Zespol zna docelowe komendy startowe i migracyjne dla pierwszego wdrozenia

### Phase 2: Minimalna obserwowalnosc przez health check i logi bledow

#### Automated

- [ ] 2.1 `python manage.py test cards` przechodzi po dodaniu konfiguracji logowania
- [ ] 2.2 `python manage.py check --deploy` przechodzi dla ustawien produkcyjnych albo ma jawnie udokumentowane wyjatki MVP

#### Manual

- [ ] 2.3 Bledy aplikacji pojawiaja sie w logach Railway w czytelnym formacie
- [ ] 2.4 `/health/` nadaje sie do recznego smoke testu po wdrozeniu

### Phase 3: Workflow GitHub Actions dla testu i deployu

#### Automated

- [ ] 3.1 Workflow przechodzi lokalna walidacje skladni YAML i ma komplet wymaganych sekretow
- [ ] 3.2 Push do galezi testowej odwzorowujacej `main` wykonuje testy jednostkowe bez recznych krokow

#### Manual

- [ ] 3.3 Konfiguracja GitHub Secrets dla Railway jest kompletna i zrozumiala
- [ ] 3.4 Wiadomo, czy migracje i `collectstatic` dzieja sie w GitHub Actions, czy w release command Railway, bez dublowania odpowiedzialnosci

### Phase 4: Spiecie z Railway i pierwszy automatyczny deploy

#### Automated

- [ ] 4.1 Deploy z GitHub Actions publikuje rewizje na Railway po zielonych testach
- [ ] 4.2 Smoke test po deployu potwierdza odpowiedz `200` z publicznego `/health/`

#### Manual

- [ ] 4.3 Aplikacja otwiera sie pod publicznym URL Railway po pierwszym deployu
- [ ] 4.4 Reczny przeglad logow Railway pozwala potwierdzic brak oczywistych bledow startowych

### Phase 5: Finalna weryfikacja operacyjna i porzadki dokumentacyjne

#### Automated

- [ ] 5.1 `python manage.py check`
- [ ] 5.2 `python manage.py migrate`
- [ ] 5.3 `python manage.py test cards`

#### Manual

- [ ] 5.4 Instrukcje deployu i walidacji sa wystarczajace, by inna osoba mogla powtorzyc wdrozenie
- [ ] 5.5 Zespol potwierdza, ze baseline S-00/S-00A jest zamkniety i nie wymaga osobnego follow-up planu tylko dla CI/CD