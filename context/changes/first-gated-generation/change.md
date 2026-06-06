---
change_id: first-gated-generation
title: First gated generation for owned flashcards
status: planned
created: 2026-06-06
updated: 2026-06-06
roadmap_ref: S-02
owner: user
---

## Context

Zmiana realizuje pierwszy bezpieczny krok AI generation po foundation auth/ownership. Celem jest dostarczenie endpointu generacji, który dziala tylko dla zalogowanego uzytkownika i zapisuje wynik jako dane wlasciciela.

## Goal

1. Udostepnic endpoint generacji fiszek z tekstu dla zalogowanych uzytkownikow.
2. Zapisywac wygenerowane fiszki jako owned records per konto.
3. Zwrocic stabilny kontrakt bledow i limity MVP dla przewidywalnego zachowania.

## Out of Scope

1. Review accept/edit/reject (to kolejny slice).
2. Wlasny algorytm powtorek.
3. Rozbudowane role i token/JWT migration.
4. Zaawansowana optymalizacja prompt engineering poza MVP-safe defaults.
