---
change_id: auth-ownership-foundation
title: Minimalny kontrakt auth i ownership dla MVP
status: planned
created: 2026-06-05
updated: 2026-06-05
roadmap_ref: F-01
owner: user
---

## Context

Zmiana realizuje foundation `F-01` z roadmapy i odblokowuje kolejne slice'y (`S-01`, `S-02`, `S-04`, `S-06`).

## Goal

Wprowadzić minimalny, implementowalny kontrakt:
1. logowanie/rejestracja dla jednej roli użytkownika,
2. własność danych fiszek per konto,
3. brak dostępu do danych innego użytkownika.

## Out of Scope

1. Zaawansowany system ról.
2. Social login.
3. Password reset / email verification (o ile nie zostanie to jawnie dopisane jako wymaganie MVP).
4. Rozbudowa UI poza konieczne endpointy i walidację API.
