# Minimalny kontrakt auth i ownership dla MVP — Plan Brief

> Full plan: `context/changes/auth-ownership-foundation/plan.md`

## What & Why

Wprowadzamy minimalny foundation auth + ownership dla MVP: użytkownik ma móc założyć konto, zalogować się i korzystać z fiszek przypisanych wyłącznie do własnego konta. To jest potrzebne, żeby kolejne kroki roadmapy mogły bezpiecznie budować generację AI, review i zapis bez ryzyka wycieku danych między użytkownikami.

## Starting Point

Obecnie aplikacja ma publiczne endpointy JSON dla fiszek, bez ochrony logowania i bez powiązania rekordów z właścicielem. Model `Flashcard` nie ma relacji do użytkownika, więc każdy widzi i modyfikuje wszystkie rekordy. Django auth middleware jest już dostępny w settings, ale flow auth nie jest jeszcze zaimplementowany.

## Desired End State

Po zakończeniu planu użytkownik będzie mógł zarejestrować konto, zalogować się, wylogować i sprawdzić własną sesję przez `me`. Każda fiszka będzie przypisana do konkretnego użytkownika, a endpointy fiszek będą działać wyłącznie na danych właściciela. Testy mają potwierdzić zarówno poprawny dostęp, jak i brak dostępu do cudzych danych.

## Key Decisions Made

| Decision | Choice | Why (1 sentence) | Source |
| --- | --- | --- | --- |
| Auth scope | register / login / logout / me | To najszybszy MVP-owy zakres bez recovery flow i weryfikacji email. | Plan |
| Auth mechanism | Django session auth | Najprostsza ścieżka dla obecnego stacku i testów backendowych. | Plan |
| Data ownership | Flashcard przypisany do `request.user` | Zapewnia izolację danych między użytkownikami. | Plan |
| API shape | Minimalne zmiany w istniejących endpointach cards | Chroni obecny kontrakt JSON i ogranicza zakres zmian. | Plan |

## Scope

**In scope:**
- dodanie minimalnego flow auth,
- dodanie ownera do fiszek,
- ograniczenie odczytu i modyfikacji do własnych rekordów,
- testy autoryzacji i izolacji danych,
- preview deploy i smoke test przed produkcją.

**Out of scope:**
- reset hasła,
- weryfikacja email,
- social login,
- rozbudowane role,
- przebudowa UI poza konieczne endpointy,
- zaawansowany hardening security poza foundation.

## Architecture / Approach

Podejście jest zachowawcze: rozszerzamy istniejące endpointy `cards` o minimalny kontrakt auth i ownership, zamiast budować nową warstwę aplikacji. Sesyjna autoryzacja Django i ForeignKey do użytkownika dają najmniejszy koszt zmiany przy zachowaniu pełnej izolacji danych.

## Phases at a Glance

| Phase | What it delivers | Key risk |
| --- | --- | --- |
| 1. Data ownership foundation | Model fiszki ma właściciela i migrację bezpiecznie przechodzi | Migracja i istniejące rekordy |
| 2. Auth endpoints | register/login/logout/me działają na sesjach Django | Niejasny kontrakt loginu |
| 3. Ownership-gated cards API | Lista, create, detail i delete działają tylko na własnych danych | Wycieki danych lub błędne 404 |
| 4. Test & deploy hardening | Testy i smoke test potwierdzają brak regresji | Niespójność auth/csrf/ownership |

**Prerequisites:** istniejąca baza Django, gotowy roadmap F-01, gotowy repo workflow preview->production.  
**Estimated effort:** kilka sesji implementacyjnych w ramach jednej zmiany.

## Open Risks & Assumptions

- Zakładamy, że MVP nie potrzebuje resetu hasła ani weryfikacji email.
- Zakładamy, że dane dev mogą zostać uproszczone przy migracji ownera.
- Zakładamy, że sesyjny auth Django wystarczy na ten etap produktu.

## Success Criteria (Summary)

- Użytkownik może założyć konto i zalogować się.
- Fiszki są widoczne i modyfikowalne tylko przez właściciela.
- Testy i smoke testy przechodzą bez wycieków między użytkownikami.
