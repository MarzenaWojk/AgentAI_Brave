# Text to AI Draft Cards — Plan Brief

> Full plan: `context/changes/text-to-ai-draft-cards/plan.md`

## What & Why

Budujemy pierwszy bezpieczny flow generacji AI dla fiszek: zalogowany user wkleja tekst, system zwraca drafty i zapisuje je jako owned records w partii generacji. To jest krok roadmapy, ktory odblokowuje review i dalszy zapis bez wycieku danych między użytkownikami.

## Starting Point

Projekt ma już JSON API, session auth i publiczny homepage/health endpoint, ale nie ma jeszcze endpointu generacji ani warstwy AI service boundary. Model fiszki nadal nie ma ownership ani relacji do partii generacji.

## Desired End State

Uzytkownik po zalogowaniu generuje drafty z tekstu, dostaje `batch_id` plus drafty, a dane pozostają prywatne per konto. Nie ma publicznej generacji, a błędy providera, walidacji i timeoutu mają stabilny kontrakt JSON.

## Key Decisions Made

| Decision | Choice | Why (1 sentence) | Source |
| --- | --- | --- | --- |
| Scope | Save owned drafts in a generation batch | Daje stan do review i zachowuje prywatność. | Plan |
| Provider | Configurable service adapter | Ułatwia testy i późniejszą podmianę providera. | Plan |
| Output contract | batch_id plus drafts | Ułatwia audyt i dalsze kroki w flow. | Plan |
| Error strategy | Fail fast with explicit error | Przewidywalne API i brak częściowych danych. | Plan |
| Privacy | Keep minimal metadata only | Chroni tekst źródłowy i ogranicza ryzyko. | Plan |
| Auth gate | Session auth required | Zgodne z obecnym stackiem i wymaganiami PRD. | Plan |

## Scope

**In scope:**
- endpoint generacji draftów z tekstu,
- zapis owned drafts w generation batch,
- service boundary dla providera AI,
- stabilny kontrakt błędów,
- testy auth, ownership, timeout i provider failure,
- preview smoke flow.

**Out of scope:**
- accept/edit/reject review,
- JWT migration,
- zaawansowany algorytm powtórek,
- import PDF/DOCX,
- silent retry i publiczny endpoint generacji.

## Architecture / Approach

Plan zakłada cienką warstwę HTTP w `cards/views.py` i osobny service adapter dla generacji. Najpierw domykamy ownership/persistencję, potem endpoint generacji, a na końcu testy i preview, żeby nie wypuścić publicznej generacji bez właściciela i bez klas błędów.

## Phases at a Glance

| Phase | What it delivers | Key risk |
| --- | --- | --- |
| 1. Foundation Gate and Data Model | Ownership i batch schema gotowe | Migracja i zależność od F-01 |
| 2. Generation Service Boundary and API Contract | Endpoint i serwis generacji z kontraktem | Zbyt szeroki payload lub słaby error mapping |
| 3. Owned Persistence and Isolation Guarantees | Dane właściciela i izolacja per user | Wyciek danych przy list/detail/delete |
| 4. Preview Validation and Rollout Readiness | Smoke test preview i stabilny deploy | Różnice między local a preview/runtime |

**Prerequisites:** gotowy session auth i ownership gate z F-01/S-01 albo realizacja ich kontraktu na początku tej zmiany.  
**Estimated effort:** ~2-3 sesje implementacyjne przez 4 fazy.

## Open Risks & Assumptions

- Zakładamy, że generation będzie synchroniczne w obrębie jednego requestu.
- Zakładamy, że pełny source text nie musi być przechowywany długoterminowo.
- Zakładamy, że provider generacji można opakować prostym adapterem serwisowym.

## Success Criteria (Summary)

- Zalogowany user generuje i widzi tylko własne drafty w batchu.
- Niezalogowany user nie uruchomi generacji, a błędy są kontrolowane.
- Preview smoke flow potwierdza brak regresji i zgodność z PRD prywatności.
