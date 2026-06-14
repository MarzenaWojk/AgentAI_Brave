# ci-cd-deploy Implementation Plan

## Overview

Ten plan realizuje S-00A: automatyczny pipeline CI/CD uruchamiany na kazdy push do `main`. Po zielonych testach GitHub Actions wyzwala deploy na Railway przez CLI, a po deployu wykonuje smoke test na `/health/`. Migracje i collectstatic pozostaja w Railway release command — jedno zrodlo prawdy, bez duplikacji w CI.

## Current State Analysis

- Repo nie ma `.github/workflows/*.yml` — brak jakiegokolwiek CI.
- `tenx_cards/settings.py` ma production hardening (S-00 Phase 1 dostarczone).
- `cards/views.py` i `cards/public_urls.py` dostarczaja istniejacy endpoint `/health/`.
- `cards/tests.py` ma 19 testow, wszystkie zielone.
- `.env.example` dokumentuje kontrakt env; Railway release command jest opisany w komentarzu: `python manage.py migrate ; python manage.py collectstatic --noinput`.
- Brak pliku `runtime.txt` — Railway i GH Actions nie wiedza jakiej wersji Pythona uzyc.
- Brak `railway.json` — Railway dziala na buildpack autodetect; nie blokuje, ale warto miec.

## Desired End State

Push do `main` uruchamia automatycznie:
1. Testy jednostkowe na SQLite (izolowane od Supabase).
2. Deploy na Railway przez `railway deploy`.
3. Smoke test `curl --fail <RAILWAY_URL>/health/` — pipeline czerwony jezeli app nie odpowiada 200.

Migracje i collectstatic sa uruchamiane przez Railway release command — nie przez CI.

Python version jest zadeklarowana w `runtime.txt` i uzywana wspolnie przez Railway i GH Actions runner.

Wymagane GitHub Secrets (RAILWAY_TOKEN, RAILWAY_PUBLIC_URL) sa udokumentowane w komentarzach `deploy.yml`.

## What We're NOT Doing

- Nie konfigurujemy PR checks — pipeline odpala sie tylko na push do `main`.
- Nie robimy migracji w CI — Railway release command jest jedynym wlascicielem migrate.
- Nie dodajemy preview environments ani staging environment.
- Nie wdrazamy sentry, alertingu ani zaawansowanego observability (to S-00 Phases 2-5).
- Nie dodajemy `railway.json` — Railway buildpack autodetect wystarcza dla MVP.

## Implementation Approach

Jedna faza, dwa pliki do stworzenia, zerowe zmiany w kodzie aplikacji:

1. `runtime.txt` — deklaracja wersji Pythona dla Railway buildpack i GH Actions.
2. `.github/workflows/deploy.yml` — jeden workflow z dwoma jobami: `test` i `deploy`.

Job `test` uruchamia testy z SQLite (brak DATABASE_URL = SQLite fallback w settings.py). Job `deploy` zalezy od `test` i uruchamia `railway deploy`. Po deployu wykonuje curl na `/health/` jako smoke test.

## Critical Implementation Details

- **Brak DATABASE_URL w CI** — settings.py ma SQLite fallback gdy DATABASE_URL jest pusty. Nie ustawiamy DATABASE_URL w CI env, zeby testy nie dosiegaly Supabase.
- **SECRET_KEY w CI** — testy Django wymagaja SECRET_KEY. Ustawiamy statyczna wartosc testowa jako `env:` w jobie test (nie wchodzi na produkcje, nie jest prawdziwym secretem).
- **RAILWAY_TOKEN** — wymaga Railway Personal Token z prawem do deploy tego projektu. Tworzysz go w Railway Dashboard → Account → API Tokens.
- **RAILWAY_PUBLIC_URL** — publiczny URL serwisu na Railway (np. `https://tenx-cards.up.railway.app`). Ustawiasz jako GitHub Secret.
- **Kolejnosc jobów**: `test` → `deploy` (needs: [test]) → smoke test w tym samym jobie deploy po railway deploy.
- **Python version**: `runtime.txt` musi zawierac `python-3.12` (Railway buildpack format) i ten sam numer trafi do `python-version:` w GH Actions jako odczyt z pliku.

---

## Phase 1: runtime.txt i .github/workflows/deploy.yml

### Overview

Jedyna faza tego planu. Tworzymy dwa pliki i nie dotykamy kodu aplikacji.

### Changes Required:

#### 1. Deklaracja wersji Pythona

**File**: `runtime.txt`

**Intent**: Jawna deklaracja wersji Pythona dla Railway buildpack i GitHub Actions, zeby obydwa srodowiska uzywaly tej samej wersji bez zgadywania.

**Contract**: Plik zawiera jeden wiersz w formacie wymaganym przez Railway buildpack: `python-X.Y`. Nie zawiera microversion (np. `python-3.12` a nie `python-3.12.3`).

**Content**:
```
python-3.12
```

#### 2. GitHub Actions workflow — testy i deploy

**File**: `.github/workflows/deploy.yml`

**Intent**: Automatyczny pipeline uruchamiany na push do `main`. Dwa sequential jobs: `test` (uruchamia 19 testow Django na SQLite) i `deploy` (railway CLI deploy + smoke test).

**Contract**:
- Trigger: `on: push: branches: [main]`
- Job `test`: checkout + setup-python z wersja z `runtime.txt` + pip install -r requirements.txt + `python manage.py test cards` z `SECRET_KEY=test-only-key` i pustym DATABASE_URL (SQLite fallback)
- Job `deploy`: `needs: [test]` + instalacja railway CLI + `railway deploy` z RAILWAY_TOKEN z GitHub Secrets + `curl --fail ${{ secrets.RAILWAY_PUBLIC_URL }}/health/` jako smoke test
- Komentarze w pliku dokumentuja wymagane GitHub Secrets (RAILWAY_TOKEN, RAILWAY_PUBLIC_URL) i jak je ustawic

**Content** (dokladna tresc do skopiowania przy implementacji):

```yaml
# Required GitHub Secrets:
#   RAILWAY_TOKEN      - Railway Personal Token (Railway Dashboard → Account → API Tokens)
#   RAILWAY_PUBLIC_URL - Public URL of the Railway service, e.g. https://tenx-cards.up.railway.app

name: Test and Deploy

on:
  push:
    branches:
      - main

jobs:
  test:
    name: Run Django tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Read Python version
        id: python-version
        run: echo "version=$(cat runtime.txt | sed 's/python-//')" >> $GITHUB_OUTPUT

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ steps.python-version.outputs.version }}

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        env:
          SECRET_KEY: test-only-secret-key-not-used-in-production
          DATABASE_URL: ""
          DEBUG: "True"
        run: python manage.py test cards

  deploy:
    name: Deploy to Railway
    runs-on: ubuntu-latest
    needs: [test]
    steps:
      - uses: actions/checkout@v4

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: railway deploy --detach

      - name: Smoke test
        run: |
          sleep 30
          curl --fail --retry 3 --retry-delay 10 ${{ secrets.RAILWAY_PUBLIC_URL }}/health/
```

**Note on `sleep 30`**: Railway release command (migrate + collectstatic) wykonuje sie po deployu, przed startem aplikacji. Sleep 30s daje Railway czas na zakonczenie release command i uruchomienie serwisu przed smoke testem. Wartosc moze wymagac dostosowania po pierwszym deployu.

### Success Criteria:

#### Automated Verification:

- [ ] `python manage.py check` — brak bledow
- [ ] `python manage.py test cards` — 19 testow zielonych (bez zmian w testach)
- [ ] Plik `runtime.txt` istnieje i zawiera `python-3.12`
- [ ] Plik `.github/workflows/deploy.yml` istnieje i jest poprawnym YAML
- [ ] Workflow ma trigger `push: branches: [main]`
- [ ] Job `deploy` ma `needs: [test]`
- [ ] Smoke test uzywa `secrets.RAILWAY_PUBLIC_URL`
- [ ] Komentarze w deploy.yml dokumentuja RAILWAY_TOKEN i RAILWAY_PUBLIC_URL

#### Manual Verification (po konfiguracji GitHub Secrets):

- [ ] Push do main wyzwala GH Actions workflow
- [ ] Job `test` przechodzi, job `deploy` startuje po `test`
- [ ] Railway dashboard pokazuje nowy deploy
- [ ] Smoke test w CI zwraca 200 z `/health/`
- [ ] Lokal: `python manage.py test cards` nadal zielony po zmianie

### Rollback Criteria:

- Jezeli `railway deploy` failuje w pipeline: wróc do poprzedniej rewizji przez Railway Dashboard (Deployments → rollback). Nie ma zmian w modelu danych, wiec migracje nie stanowia ryzyka.
- Jezeli smoke test failuje: sprawdz Railway logs. Moze byc potrzebne zwiekszenie `sleep` lub diagnoza bledu w release command.

---

## Progress

Completion: 8 / 13

### Phase 1: runtime.txt i .github/workflows/deploy.yml

#### Automated Verification:

- [x] 1.1 python manage.py check — brak bledow
- [x] 1.2 python manage.py test cards — 19 testow zielonych
- [x] 1.3 runtime.txt istnieje i zawiera python-3.12
- [x] 1.4 deploy.yml istnieje i jest poprawnym YAML
- [x] 1.5 Workflow ma trigger push: branches: [main]
- [x] 1.6 Job deploy ma needs: [test]
- [x] 1.7 Smoke test uzywa secrets.RAILWAY_PUBLIC_URL
- [x] 1.8 Komentarze dokumentuja RAILWAY_TOKEN i RAILWAY_PUBLIC_URL

#### Manual Verification:

- [ ] 1.9 Push do main wyzwala GH Actions workflow
- [ ] 1.10 Job test przechodzi, job deploy startuje po test
- [ ] 1.11 Railway dashboard pokazuje nowy deploy
- [ ] 1.12 Smoke test w CI zwraca 200 z /health/
- [ ] 1.13 Lokal: python manage.py test cards nadal zielony
