# S-01B UI Shell and Auth Pages - Plan Brief

> Full plan: context/changes/ui-shell-and-auth-pages/plan.md

## What and Why

Ta zmiana dodaje minimalny browserowy interfejs do istniejacego API, aby produkt byl uzywalny bez recznych wywolan HTTP. Zakres jest MVP-first: auth pages + prosty dashboard z podstawowymi akcjami fiszek.

## Starting Point

Projekt dziala jako API-only backend (root zwraca JSON), bez templates i static. Session auth i endpointy cards sa juz dostepne po stronie backendu.

## Desired End State

Uzytkownik moze wejsc na strone glowna, zarejestrowac sie, zalogowac, wejsc na dashboard i dodac fiszke. Wylogowanie konczy sesje, a dashboard jest chroniony.

## Key Decisions Made

| Decision | Choice | Why | Source |
| --- | --- | --- | --- |
| UI architecture | Django server-rendered templates | Najszybsza droga do MVP bez dodatkowego toolchainu | Plan |
| Auth integration | Reuse Django sessions | Zgodnosc z obecnym backendem i testami | Plan |
| Scope | Auth + dashboard basics | Minimalna wartosc user-facing przed kolejnymi slice'ami | Roadmap |
| Routing | UI na root, API pod /api/cards/ | Jasny podzial interfejsu user vs API | Plan |

## Scope

In scope:
- strony home/register/login/dashboard,
- przekierowania auth i ochrona dashboardu,
- lista i tworzenie fiszek z dashboardu,
- podstawowy styl i smoke flow.

Out of scope:
- SPA framework,
- AI generation/review UI,
- rozbudowany design system,
- mobile app/PWA.

## Phases at a Glance

| Phase | What it delivers | Key risk |
| --- | --- | --- |
| 1. UI Foundation and Routing | Templates, static, trasy UI | Konflikt root URL miedzy JSON i HTML |
| 2. Auth UI Flow | Formularze register/login/logout | Niespojne walidacje miedzy UI i API |
| 3. Dashboard and Flashcards Basics | Lista i tworzenie fiszek | Regresja izolacji danych userow |
| 4. UX Hardening and Preview Readiness | Czytelnosc i smoke flow | Niedopiete testy manualne przed deploy |

Prerequisites: domkniete F-01 i S-01.
Estimated effort: 2-4 sesje implementacyjne.

## Success Criteria (Summary)

- Root i auth pages renderuja HTML.
- Dashboard wymaga sesji i pokazuje tylko wlasne dane.
- User tworzy fiszke z poziomu UI.
- Check i test cards przechodza bez regresji API.
