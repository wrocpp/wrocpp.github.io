# The fastest JVM is the C++26 compiler

## Body
Koen Samyn's BeCPP talk (May 13) uses std::meta::substitute to transform Java bytecode into executable C++ at compile time.

The four-step pipeline: reflect the execute template, lift constants via reflect_constant, substitute template arguments, splice back into code. Each Java opcode becomes a template specialization. The bytecode stream becomes a variadic expansion. With -O2, the compiler constant-folds the entire program.

Samyn: "The loop doesn't just run faster. It doesn't exist."

This is reflection used not for serialization or enum-to-string, but as a compile-time metaprogramming substrate for building language interpreters.

https://wrocpp.github.io/posts/fastest-jvm-is-cpp26/

## Hashtags
#cpp #cpp26 #reflection #p2996 #becpp #java #jvm #metaprogramming #wrocpp

## Alt-text
Editorial card: "The fastest JVM is the C++26 compiler". Java bytecode compiled at compile time via std::meta::substitute.

## Suggested post time
Monday 2026-06-08, 10:00 CET
