# Plan: auth-ownership-foundation

## 1. Cel i wynik

Celem jest minimalny foundation dla Django zgodny z PRD i roadmapą:
1. użytkownik może założyć konto i zalogować się,
2. każda fiszka jest przypisana do właściciela,
3. API fiszek nie ujawnia danych między użytkownikami.

Wynik ma odblokować implementację `S-01`, `S-02`, `S-04`, `S-06`.

## 2. Stan obecny (baseline)

1. `cards/models.py` ma model `Flashcard` bez relacji do użytkownika.
2. `cards/views.py` ma publiczne endpointy (`@csrf_exempt`) i operuje na wszystkich fiszkach.
3. Brak endpointów auth (register/login/logout).
4. `django.contrib.auth` i middleware auth są już włączone w `tenx_cards/settings.py`.

## 3. Założenia implementacyjne (minimalne)

1. Jedna rola użytkownika (zgodnie z PRD `Access Control`).
2. Sesyjna autoryzacja Django (cookie session) jako najprostsza ścieżka MVP.
3. Brak recovery flow na tym etapie.
4. Zakres auth dla MVP jest potwierdzony: `register / login / logout / me`, bez resetu hasła i bez weryfikacji email.
4. JSON API zachowuje obecny format odpowiedzi i kody błędów tam, gdzie to możliwe.

## 4. Zakres zmian

## 4.1 Migracje i model

1. W `cards/models.py` dodać pole właściciela:
   - `owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="flashcards")`
2. Przygotować migrację dodającą `owner`.
3. Strategia dla istniejących rekordów (lokalna baza dev):
   - jeśli brak danych produkcyjnych: migracja może wymagać wyczyszczenia lokalnych danych dev,
   - alternatywnie: data migration przypisująca rekordy do użytkownika technicznego (tylko jeśli potrzebne).

## 4.2 Endpointy auth (minimalny flow)

Dodać nowe endpointy w app `cards` (żeby zachować konwencję repo):
1. `POST /api/cards/auth/register/`
   - input: `username`, `password`
   - output: sukces + podstawowe dane usera
2. `POST /api/cards/auth/login/`
   - input: `username`, `password`
   - efekt: utworzenie sesji Django
3. `POST /api/cards/auth/logout/`
   - wymaga zalogowania
   - efekt: zamknięcie sesji
4. `GET /api/cards/auth/me/`
   - zwraca bieżącego użytkownika lub 401

## 4.3 Zmiany istniejącego API fiszek

1. `GET /api/cards/flashcards/`:
   - zwraca tylko fiszki `owner=request.user`.
2. `POST /api/cards/flashcards/`:
   - tworzy fiszkę z `owner=request.user`.
3. `GET /api/cards/flashcards/<id>/` i `DELETE ...`:
   - operacje tylko na rekordach właściciela,
   - obcy rekord traktowany jak `NOT_FOUND` (nie ujawniamy istnienia).
4. Endpointy fiszek wymagają zalogowania (`@login_required` lub równoważny check w widoku JSON).

## 4.4 Routing

1. W `cards/urls.py` dodać ścieżki auth.
2. W `tenx_cards/urls.py` pozostawić include do `cards.urls` bez zmian architektonicznych.

## 4.5 Konfiguracja i bezpieczeństwo

1. Pozostawić auth sesyjne Django jako mechanizm MVP.
2. Dla środowisk produkcyjnych upewnić się, że ustawienia cookie/session są bezpieczne (w kolejnym kroku hardeningu, jeśli nie ma jeszcze env-driven DEBUG/CSRF).

## 5. Plan testów (must-have)

## 5.1 Pozytywne

1. Rejestracja użytkownika działa (201/200).
2. Logowanie użytkownika działa i utrzymuje sesję.
3. Użytkownik A tworzy fiszkę i widzi ją na liście.
4. Użytkownik A może pobrać i usunąć własną fiszkę.

## 5.2 Negatywne autoryzacyjne

1. Niezalogowany użytkownik dostaje 401 przy endpointach fiszek.
2. Logowanie z błędnym hasłem zwraca kontrolowany błąd.
3. `GET /auth/me` bez sesji zwraca 401.

## 5.3 Izolacja danych

1. Użytkownik B nie widzi fiszek użytkownika A na liście.
2. Użytkownik B nie może pobrać fiszki A po ID (404).
3. Użytkownik B nie może usunąć fiszki A po ID (404).

## 5.4 Regresja

1. Zachować istniejące struktury błędów (`INVALID_JSON`, `VALIDATION_ERROR`, `METHOD_NOT_ALLOWED`, `NOT_FOUND`) tam, gdzie dotyczą.
2. Zaktualizować testy metod niedozwolonych, jeśli któraś metoda stanie się dozwolona.

## 6. Kolejność implementacji

1. Dodać relację `owner` do modelu + migracja.
2. Dodać minimalne endpointy auth i ich testy.
3. Ograniczyć zapytania i operacje fiszek do `request.user`.
4. Zmienić create fiszki tak, by zapisywał ownera.
5. Dodać/uzupełnić testy izolacji danych i autoryzacji.
6. Uruchomić walidację repo:
   - `.venv/Scripts/python.exe manage.py check`
   - `.venv/Scripts/python.exe manage.py migrate`
   - `.venv/Scripts/python.exe manage.py test cards`

## 7. Deploy plan

1. Deploy na Preview.
2. Smoke test auth:
   - register -> login -> me -> logout.
3. Smoke test ownership:
   - user A tworzy fiszkę,
   - user B nie widzi/nie usuwa fiszki A.
4. Jeśli smoke testy przechodzą: manual approval do production.

## 8. Rollback strategy

1. Jeśli po deployu auth/ownership blokuje podstawowe flow, rollback do poprzedniej rewizji Railway.
2. Jeśli migracja modelu powoduje błąd runtime:
   - natychmiast rollback aplikacji,
   - przywrócenie kompatybilnej wersji kodu z poprzednią migracją.
3. Dla bezpieczeństwa rolloutu:
   - nie wykonywać destrukcyjnych zmian schema w tej iteracji,
   - w razie problemu przywrócić poprzednią wersję aplikacji i zweryfikować integralność danych.

## 9. Definition of Done

1. Endpointy register/login/logout/me działają i są pokryte testami.
2. Wszystkie operacje na fiszkach są właścicielskie (per user).
3. Brak wycieku danych między użytkownikami w testach.
4. Walidacja repo z AGENTS.md przechodzi.
5. Preview smoke test przechodzi i zmiana jest gotowa do ręcznej promocji.

## 10. Ryzyka i decyzje

1. Ryzyko: niedoprecyzowany recovery flow.
   - Decyzja: poza zakresem foundation, zostaje do późniejszego slice'a.
2. Ryzyko: lokalne dane dev bez ownera.
   - Decyzja: potraktować jako dane nieprodukcyjne i uprościć migrację pod MVP.
3. Ryzyko: obecne endpointy bazują na `csrf_exempt`.
   - Decyzja: dla foundation skupić się na ownership + auth; CSRF hardening potraktować jako kolejny krok bezpieczeństwa.
