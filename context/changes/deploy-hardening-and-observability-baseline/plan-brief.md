# Deploy hardening and observability baseline — Plan Brief

> Full plan: `context/changes/deploy-hardening-and-observability-baseline/plan.md`

## What & Why

Ten plan domyka pierwszy produkcyjny baseline dla MVP: automatyczny deploy na Railway, minimalna obserwowalnosc oparta o health check i logi bledow oraz prosty pipeline GitHub Actions uruchamiany na kazdy push do `main`. Celem nie jest rozbudowana platforma operacyjna, tylko tani i szybki safety-net, ktory zmniejszy ryzyko blokad podczas kolejnych slice'ow produktowych.

## Starting Point

Aplikacja ma juz env-driven konfiguracje Django i podstawowy endpoint `/health/`, ale repo nie ma zadnego workflow CI/CD, automatycznego deployu ani centralnej konfiguracji logowania. Railway zostal juz wybrany jako docelowy provider MVP, wiec ten plan nie robi kolejnego researchu platformowego, tylko materializuje ta decyzje w kodzie i procesie.

## Desired End State

Push do `main` uruchamia testy jednostkowe i automatyczny deploy na Railway. Produkcja odpowiada pod publicznym URL, endpoint `/health/` sluzy jako smoke test po wdrozeniu, a bledy aplikacji sa widoczne w Railway logs bez dodatkowych integracji typu Sentry. Po wdrozeniu kolejny slice roadmapy nie powinien juz byc blokowany przez brak powtarzalnego deployu.

## Key Decisions Made

| Decision | Choice | Why (1 sentence) | Source |
| --- | --- | --- | --- |
| Provider runtime | Railway | Jest juz wybrany jako najlepszy kompromis dla Django MVP i celu speed. | Research |
| Zakres planu | Scalony S-00 + S-00A | Deploy i CI/CD tworza jeden przeplyw operacyjny, wiec rozdzielenie tylko zwiekszyloby zaleznosci. | Plan |
| Error tracking | Brak zewnetrznego error trackingu | Na MVP wystarcza logi Railway; dodatkowa integracja zwiekszylaby koszt i scope. | Plan |
| Logging | Tylko bledy | To najmniejszy uzyteczny sygnal operacyjny przy niskim halasie w logach. | Plan |
| Trigger deployu | Kazdy push do `main` | Priorytetem jest szybka iteracja, a nie konserwatywny release train. | Plan |
| Bramka testowa | Tylko testy jednostkowe | Aktualny stan repo i tempo MVP nie uzasadnia ciezszej bramki przed deployem. | Plan |
| Monitoring startowy | Observe first | Alerting zostaje odlozony, bo najpierw trzeba zobaczyc realny ruch i wzorce bledow. | Plan |

## Scope

**In scope:**
- produkcyjny kontrakt runtime i env vars
- minimalne logowanie bledow w Django
- workflow GitHub Actions dla testu i deployu
- automatyczny deploy na Railway
- smoke test po deployu i aktualizacja instrukcji operacyjnych

**Out of scope:**
- Sentry, Prometheus, alerting
- preview environments i release tags
- Dockerizacja
- zaawansowany tuning wydajnosci i kosztow

## Architecture / Approach

Podejscie jest liniowe: najpierw domkniecie kontraktu runtime w Django, potem dodanie prostego `LOGGING`, nastepnie workflow GitHub Actions uruchamianego na push do `main`, a na koncu spiecie pipeline z Railway i post-deploy smoke testem pod `/health/`. Railway logs sa jedynym zrodlem obserwowalnosci na start.

## Phases at a Glance

| Phase | What it delivers | Key risk |
| --- | --- | --- |
| 1. Runtime i env | Zamkniety kontrakt produkcyjny i komendy uruchomieniowe | Niejasny podzial odpowiedzialnosci miedzy CI a Railway |
| 2. Observability minimum | Logi bledow i stabilny health check | Zbyt glosne albo zbyt ubogie logi |
| 3. GitHub Actions | Automatyczny test i deploy pipeline | Pipeline oparty na zlych sekretach lub dublujacy migracje |
| 4. Railway deploy | Publiczny deploy i smoke test po wdrozeniu | Pierwszy deploy ujawni brakujace env vars albo zle komendy startowe |
| 5. Domkniecie operacyjne | Spojne instrukcje i finalna walidacja | Niedomkniete notatki po pierwszym wdrozeniu |

**Prerequisites:** Dostep do Railway projektu, mozliwosc ustawienia GitHub Secrets i gotowa baza PostgreSQL dla produkcji.
**Estimated effort:** ~2-3 sesje pracy rozlozone na 5 faz, z reczna weryfikacja po pierwszym deployu.

## Open Risks & Assumptions

- Release flow dla migracji i `collectstatic` musi miec jedno zrodlo prawdy; podwojenie tych krokow grozi niestabilnym deployem.
- Brak alertingu oznacza, ze pierwsze dni po wdrozeniu wymagaja recznego przegladu logow Railway.
- Health check musi pozostac lekki; jesli zacznie sprawdzac zaleznosci zewnetrzne, stanie sie falszywym sygnalem gotowosci.

## Success Criteria (Summary)

- Push do `main` przechodzi przez testy jednostkowe i automatycznie wdraza aplikacje na Railway.
- Publiczny `/health/` odpowiada `200`, a aplikacja otwiera sie po deployu pod stabilnym URL.
- Bledy runtime sa widoczne w Railway logs, a instrukcje deployu i walidacji sa spojne z rzeczywistym procesem.