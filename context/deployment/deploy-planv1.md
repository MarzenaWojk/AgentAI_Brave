## Plan: Pierwsze wdrożenie MVP na Railway

Celem jest bezpieczne pierwsze wdrożenie aplikacji Django na Railway zgodnie z kontraktami z [context/foundation/infrastructure.md](context/foundation/infrastructure.md) i [context/foundation/tech-stack.md](context/foundation/tech-stack.md), bez zmian w kodzie na tym etapie.

**Steps**
1. Faza 1: Walidacja kontraktu wdrożeniowego.
2. Potwierdzić Railway jako platformę docelową i manualny gate przed produkcją.
3. Potwierdzić zakres MVP: Django + Supabase + OpenRouter, bez rozszerzania architektury.
4. Faza 2: Przygotowanie środowiska Railway (manual).
5. Utworzyć projekt Railway i połączyć repozytorium GitHub.
6. Skonfigurować preview i production jako osobne środowiska.
7. Ustawić komplet sekretów aplikacji w Railway Variables i potwierdzić brak sekretów w repo.
8. Faza 3: Konfiguracja uruchamiania aplikacji.
9. Ustawić startup i politykę migracji bazy dla deployu.
10. Potwierdzić dostępność endpointu zdrowia do smoke-check.
11. Faza 4: Deploy preview i walidacja jakości.
12. Uruchomić deploy preview i potwierdzić zielony status.
13. Wykonać smoke testy: logowanie, endpoint fiszek, Supabase, OpenRouter, logi.
14. Zweryfikować hosty i CSRF dla domen preview.
15. Faza 5: Publikacja produkcyjna.
16. Wykonać manualny approval i dopiero wtedy promować rewizję do produkcji.
17. Uruchomić first-day monitoring logów, auth/data errors i opóźnień.
18. Potwierdzić rollback readiness z historii deploymentów.
19. Faza 6: Stabilizacja kosztowo-operacyjna.
20. Ustawić limity i alerty kosztowe OpenRouter.
21. Wprowadzić cykliczny przegląd kosztów, wydajności i driftu env.

**Relevant files**
- [context/foundation/infrastructure.md](context/foundation/infrastructure.md) — decyzja platformowa, ryzyka, rollback, manual gates.
- [context/foundation/tech-stack.md](context/foundation/tech-stack.md) — stack wykonawczy i założenia CI flow.
- [AGENTS.md](AGENTS.md) — reguły repo i proces walidacji.
- [manage.py](manage.py) — wejście operacyjne Django.
- [tenx_cards/settings.py](tenx_cards/settings.py) — konfiguracja środowiskowa runtime.

**Verification**
1. Preview deployment ma status green i aplikacja odpowiada.
2. Smoke testy funkcjonalne przechodzą: auth, fiszki, baza, AI.
3. DEBUG wyłączony na produkcji, hosty i CSRF zgodne z domenami runtime.
4. Rollback da się wykonać do poprzedniej zdrowej rewizji.
5. Alerty kosztowe OpenRouter są aktywne.

**Decisions**
- In scope: pierwsze wdrożenie MVP na Railway, preview + production, manualny approval.
- In scope: sekrety, rollback, logi i baseline kosztowy.
- Out of scope: przebudowa CI/CD, HA/DR, refaktory kodu.
- Założenie: Supabase i OpenRouter pozostają usługami zewnętrznymi.

**Checklist**
1. Railway projekt utworzony i repo podłączone.
2. Preview i production są rozdzielone.
3. Sekrety ustawione w Railway Variables i nieobecne w repo.
4. Startup i migracje potwierdzone.
5. Preview deploy przeszedł i smoke testy są OK.
6. Manualny approval produkcyjny wykonany.
7. Monitoring dnia 1 uruchomiony.
8. Rollback plan zweryfikowany.
9. Limity kosztowe OpenRouter ustawione.

**Punkty manualne**
1. Utworzenie projektu na Railway i połączenie z GitHub.
2. Wprowadzenie i rotacja sekretów.
3. Decyzja approval/no-approval przed produkcją.
4. Wszystkie operacje destrukcyjne na bazie danych.
5. Decyzja o rollbacku przy incydencie.