# GoogleTest tells you not to use its releases

## Body
GoogleTest 1.18.0 shipped on 10 August 2026. Its release notes open by saying the branch will not accept patches of new features, and recommending you build from the latest commit instead.

That is not a note about this release. The same paragraph, with the version number swapped, opens 1.17.0 and 1.16.0. It is a standing position: the release exists, and the project would rather you did not use it.

Version 1.17.0 came out at the end of April 2025. Version 1.18.0 came out sixteen months later. Between them, under Notable Changes, 1.18.0 lists one item and a catch all: a macro set unconditionally because C++17 always has string_view, and many bug fixes.

Compiler Explorer makes the consequence visible. Ask its library API what GoogleTest versions it offers and you get two entries: 1.10.0, from 2019, and trunk. Nothing in between, and in particular not 1.17 or 1.18. That is Google's engineering philosophy showing up as a user interface.

The awkward part is that almost nobody outside Google lives at head. vcpkg and Conan resolve to tagged releases. Debian, Ubuntu, Fedora and Homebrew package tagged releases. Corporate build systems pin a SHA and review the bump. The whole packaging ecosystem assumes a release is the thing you consume, and these release notes politely decline that assumption in their first sentence.

In practice this is mostly fine and worth saying so plainly. GoogleTest is stable and a sixteen month old version will run your tests correctly. The cost is narrower: a bug you hit may already be fixed on trunk and will not be backported, and the documentation tracks head rather than your version.

A version number usually tells you what its maintainers support. Here it tells you which snapshot you took.

https://wrocpp.github.io/posts/googletest-live-at-head/

Do you pin a release or a commit for your test framework?

## Hashtags
#cpp #cplusplus #googletest #testing #tooling

## Alt-text
A wro.cpp social card reading "The notes say do not use the release", about GoogleTest recommending users build from trunk.

## Suggested post time
Saturday 2026-10-25, 10:00 CET
Reason: Weekend mid morning for a tooling and dependency management read.
