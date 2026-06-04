## Plan: Pierwsze wdrozenie MVP na Railway

Celem jest bezpieczne pierwsze wdrozenie aplikacji Django na Railway zgodnie z kontraktami z [context/foundation/infrastructure.md](context/foundation/infrastructure.md) i [context/foundation/tech-stack.md](context/foundation/tech-stack.md). Zakres obejmuje tylko pierwsze wdrozenie MVP, bez przebudowy kodu, CI/CD ani architektury produkcyjnej poza potrzebnym minimum.

**Steps**
1. Faza 1: Walidacja kontraktu wdrozeniowego.
2. Potwierdzic Railway jako platforme docelowa i manualny gate przed produkcja.
3. Potwierdzic zakres MVP: Django, Supabase i OpenRouter, bez rozszerzania architektury.
4. Faza 2: Przygotowanie srodowiska Railway.
5. Utworzyc projekt Railway i polaczyc repozytorium GitHub.
6. Skonfigurowac preview i production jako osobne srodowiska.
7. Ustawic komplet sekretow aplikacji w Railway Variables i potwierdzic brak sekretow w repo.
8. Skonfigurowac baze danych Supabase jako jedyne zrodlo danych produkcyjnych, bez Railway DB.
9. Ustawic DATABASE_URL z Supabase oraz potwierdzic poprawnosc polaczenia.
10. Wykonac migracje na bazie Supabase i potwierdzic brak bledow runtime po migracjach.
11. Faza 3: Konfiguracja uruchamiania aplikacji.
12. Ustawic startup i polityke migracji bazy dla deployu.
13. Potwierdzic dostepnosc endpointu zdrowia do smoke-check.
14. Faza 4: Deploy preview i walidacja jakosci.
15. Uruchomic deploy preview i potwierdzic zielony status.
16. Wykonac smoke testy: logowanie, endpoint fiszek, Supabase, OpenRouter, logi.
17. Zweryfikowac hosty i CSRF dla domen preview.
18. Faza 5: Publikacja produkcyjna.
19. Wykonac manualny approval i dopiero wtedy promowac rewizje do produkcji.
20. Uruchomic first-day monitoring logow, auth errors, bledow danych i opoznien.
21. Potwierdzic rollback readiness z historii deploymentow.
22. Faza 6: Stabilizacja kosztowo-operacyjna.
23. Ustawic limity i alerty kosztowe OpenRouter.
24. Wprowadzic cykliczny przeglad kosztow, wydajnosci i driftu environmentow.

**Verification**
1. Preview deployment ma status green i aplikacja odpowiada.
2. Smoke testy funkcjonalne przechodza: auth, fiszki, baza i AI.
3. DEBUG jest wylaczony na produkcji, a hosty i CSRF sa zgodne z domenami runtime.
4. Rollback da sie wykonac do poprzedniej zdrowej rewizji.
5. Alerty kosztowe OpenRouter sa aktywne.
6. Polaczenie z Supabase dziala stabilnie, a logi nie pokazuja bledow polaczenia do bazy.

**Mini-checklista logowania (auth)**
1. Login poprawny: uzytkownik z prawidlowym e-mailem i haslem loguje sie i dostaje dostep do chronionego endpointu.
2. Login bledny: nieprawidlowe haslo zwraca kontrolowany blad 401 lub 403 bez ujawniania szczegolow.
3. Sesja lub token: po zalogowaniu sesja albo token jest ustawiony, a kolejne zadanie do endpointu chronionego przechodzi.
4. Wylogowanie: po wylogowaniu dostep do endpointu chronionego jest blokowany.
5. Guard endpointow: endpointy wymagajace auth odrzucaja niezalogowanego uzytkownika.
6. Integracja Supabase auth: poprawny przeplyw dla kluczy srodowiskowych i brak bledow autoryzacji w logach.
7. Monitoring auth: brak powtarzalnych auth errors po deployu preview i po promocji na production.

**Deploy Commands**
1. Local preflight:
   - .venv/Scripts/python.exe manage.py check
   - .venv/Scripts/python.exe manage.py migrate --check
   - .venv/Scripts/python.exe manage.py test cards
2. Railway setup:
   - railway login
   - railway link
   - railway variables set DJANGO_SECRET_KEY=... DATABASE_URL=... SUPABASE_URL=... SUPABASE_KEY=... SUPABASE_SERVICE_ROLE_KEY=... OPENROUTER_API_KEY=... OPENROUTER_MODEL=... DEBUG=False ALLOWED_HOSTS=... CSRF_TRUSTED_ORIGINS=...
3. Preview deploy:
   - deploy through Railway GitHub integration after merge to the preview branch
   - railway up if using Railway CLI for manual deploys
4. Post-deploy verification:
   - railway logs
   - smoke test login, database read/write and OpenRouter path
5. Production deploy:
   - merge only after manual approval
   - deploy via Railway production environment
   - verify logs and health endpoint immediately after release

**Env Matrix**

| Variable | Source | Required for | Notes |
|---|---|---|---|
| DJANGO_SECRET_KEY | Railway secret | Django runtime | Must be unique and never committed |
| DATABASE_URL | Supabase | Database connection | Must point to Supabase PostgreSQL |
| SUPABASE_URL | Supabase | Auth and API integration | Required for Supabase-backed flows |
| SUPABASE_KEY | Supabase | Client-side or app auth flow | Use the appropriate key for the app path |
| SUPABASE_SERVICE_ROLE_KEY | Supabase | Server-only privileged access | Keep secret, never expose to frontend |
| OPENROUTER_API_KEY | OpenRouter | AI generation | Primary AI secret |
| OPENROUTER_MODEL | Config | AI generation | Pick the approved model for MVP |
| DEBUG | Railway env | Production safety | Must be False in production |
| ALLOWED_HOSTS | Railway env | Django security | Include Railway and custom domain hosts |
| CSRF_TRUSTED_ORIGINS | Railway env | Django security | Include preview and production origins |

**Rollback Criteria**
1. Roll back immediately if the health endpoint fails after deploy.
2. Roll back if login, database read/write or OpenRouter smoke tests fail.
3. Roll back if logs show repeated auth, DB or app startup errors.
4. Roll back if the app is up but critical requests return 5xx responses.
5. Roll back if production config drift is detected, especially missing env vars or wrong host settings.
6. Roll back to the last known healthy Railway revision, then re-run the smoke tests.

**Decisions**
- In scope: pierwsze wdrozenie MVP na Railway, preview i production, manualny approval.
- In scope: sekrety, rollback, logi i baseline kosztowy.
- Out of scope: przebudowa CI/CD, HA/DR, refaktory kodu.
- Zalozenie: Supabase i OpenRouter pozostaja uslugami zewnetrznymi.

**Checklist**
1. Railway projekt utworzony i repo podlaczone.
2. Preview i production sa rozdzielone.
3. Sekrety ustawione w Railway Variables i nieobecne w repo.
4. Startup i migracje potwierdzone.
5. DATABASE_URL wskazuje na Supabase PostgreSQL, nie lokalna baze i nie Railway DB.
6. Migracje na Supabase wykonane poprawnie.
7. Test zapisu i odczytu danych po deployu zakonczony sukcesem.
8. Preview deploy przeszedl i smoke testy sa OK.
9. Manualny approval produkcyjny wykonany.
10. Monitoring dnia 1 uruchomiony.
11. Rollback plan zweryfikowany.
12. Limity kosztowe OpenRouter ustawione.

**Punkty manualne**
1. Utworzenie projektu na Railway i polaczenie z GitHub.
2. Wprowadzenie i rotacja sekretow.
3. Decyzja approval albo no-approval przed produkcja.
4. Wszystkie operacje destrukcyjne na bazie danych.
5. Decyzja o rollbacku przy incydencie.
