# Sutter's BeCPP keynote: C++ added more developers in 4 years than any other language

## Body
Herb Sutter's BeCPP Symposium keynote (March 30 2026, Howest, Belgium) opened with a SlashData chart that has been quietly travelling through C++ Slack channels for the past six weeks: **C++ developer population grew 72% from Q1 2022 to Q1 2025 (9.5M -> 16.3M)**. The headline line: "There are more C++ developers today than the #1 language had four years ago."

Two honest reads of the data, both true:
- **Rust grew fastest in percentage**: 137% over three years, from 2.1M to 5.1M. Strong signal of language health on a smaller base.
- **C++ grew fastest in absolute developer count among the perf/Watt-honest languages**: +6.8M added, more than C and Rust combined. JavaScript and Java added similar absolute numbers but started 13M and 7M ahead.

Sutter's framing: the languages targeting durable perf-per-Watt are short (C, C++, Rust). (DSLs/ASICs/FPGAs always at the leading edge.) Compute demand has outstripped supply for 80 years; he sees no reason that changes in the next 80. The population data is downstream of that thesis: languages that map onto perf-per-Watt get a steady tailwind.

What the chart does NOT say:
- C++ did not overtake JavaScript / Java / Python; the gap closed, none was passed
- Rust is not shrinking or in trouble; the two stories are complementary
- SlashData polls the developer population (do you write C++ at least sometimes), not lines of code or new project starts

For anyone arguing internally that C++ is dying: 6.8M developers added in three years is a hard rebuttal. For anyone picking C++ for a new system: the talent pool is growing, not shrinking. For anyone building tooling, libraries, or training in this space: the demand signal is favourable.

The full talk is 60 minutes and worth it. Cover the safety story, the AI story, the C++26 wins, and where the standard goes next.

Watch: https://www.youtube.com/watch?v=QWqfJtjTAdw

Read the wro.cpp write-up with the chart broken into a table and the slides annotated:
https://wrocpp.github.io/posts/cpp-fastest-growing-2025/

## Hashtags
#cpp #cpp26 #moderncpp #rust #slashdata #becpp #herbsutter #wrocpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "C++ added more developers in 4 years than any other language". Subhead: SlashData Q1 2025 -- 9.5M to 16.3M (+72%); Rust +137% on smaller base; both stories true. Citation: wro.cpp 2026-05-19.

## Suggested post time
Tuesday 2026-05-19, 10:00 CET
Reason: Tuesday morning EU C++ audience; news short between post 11 (Mon 5/18) and post 12 (Fri 5/22).
