# A real GoogleTest suite runs in your browser

## Body
New series: assembling a C++ verification setup, one layer at a time, from the cheapest and most universal outward. We have already shown sanitizers and Google Benchmark running live in the browser. This is the layer underneath them.

GoogleTest is a Compiler Explorer library. Add it from the libraries panel, turn on the execution pane, and a real test binary builds and runs on CE's servers, printing the familiar RUN and OK report back to you.

The useful property is not that the test passes. It is that the whole thing is a URL. When a colleague claims a function behaves a certain way, or an answer online disagrees with your intuition about overload resolution, you settle it with a link anyone can fork. No toolchain to install before the conversation can start.

On picking a framework: it matters less than the arguing suggests. GoogleTest is the default in large codebases and the one FuzzTest builds on. Catch2 v3 is a compiled library now with GENERATE for light property testing. doctest compiles fastest and stays header-only. snitch is the newer C++20 entrant that needs no exceptions or heap, which matters on embedded targets.

Pick one and spend the saved energy on the layers above. A suite tells you the cases you thought of still work. It says nothing about the ones you did not.

Episode 1: https://wrocpp.github.io/posts/verification-unit-tests-live/

Which framework does your team use, and would you pick it again?

## Hashtags
#cpp #cplusplus #testing #googletest #softwareengineering #programming

## Alt-text
A cream wro.cpp social card reading "Your test suite, running in a browser tab", about GoogleTest running on Compiler Explorer.

## Suggested post time
Sunday 2026-08-16, 10:00 CET
Reason: post lands on its pubDate; mid-morning CET for the EU C++ audience.
