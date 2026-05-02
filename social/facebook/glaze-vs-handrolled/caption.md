# Glaze v7.2 vs your hand-rolled JSON: a 30-line benchmark

## Body
Glaze v7.2 (announced 28 April) is the first JSON library whose reflection backend is standard C++26 -- not __PRETTY_FUNCTION__ string-scraping. The 128-member cap is gone, private members serialize without friends, and enums round-trip for free.

So: is your own 30-line writer still worth owning? Yes, when the schema is small and you want to understand reflection. Glaze wins by an order of magnitude on real payloads -- C++ JSON writers now cross gigabytes/sec, past serde_json.

Full post: https://wrocpp.github.io/posts/glaze-vs-handrolled/

## Hashtags
#cpp #cpp26 #json #glaze #wrocpp

## Alt-text
Light-themed wro.cpp social card titled "Glaze v7.2 vs your hand-rolled JSON" with a one-line summary about P2996 reflection retiring __PRETTY_FUNCTION__ tricks.

## Suggested post time
Wednesday 2026-05-06, 10:00 CET
Reason: aligns with pubDate; midweek morning fits the EU technical reader window.
