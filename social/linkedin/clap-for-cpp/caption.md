# Clap for C++: struct -> argv parser via reflection

## Body
Rust's `clap` crate is one of the best CLI parser stories in any language. You write a struct, mark fields with `#[arg(short, long, default_value = "...")]`, and the parser, help text, and error messages all derive from the type. The C++ version has historically been Boost.Program_options + glue, or one of fifty smaller libraries each with their own DSL.

C++26 reflection collapses this. Walk a struct at compile time, generate the argv parser at compile time, generate `--help` at compile time. Add a field, the parser grows. Annotate it, the parser respects the annotation. No registration step, no DSL.

```cpp
struct Args {
    [[=cli::flag{"-v", "--verbose"}]]              bool verbose = false;
    [[=cli::option{"-n", "--count"},
      =cli::default_value{1}]]                     int count;
    [[=cli::positional{0}]]                        std::string input;
};

int main(int argc, char** argv) {
    auto args = cli::parse<Args>(argc, argv).value();
    std::println("verbose={} count={} input={}",
                 args.verbose, args.count, args.input);
}

// ./demo --verbose --count 5 input.txt
// verbose=true count=5 input=input.txt
```

What the post covers: the per-field annotation taxonomy (`flag`, `option`, `positional`, `default_value`, `description`), the help-text generation walker, the std::expected error path with field-name + expected-type-aware messages, integration with subcommands (one struct per subcommand, dispatch via type-erased variant).

What this does NOT replace: CLI11 (mature ecosystem, polished error messages, completion scripts for bash/zsh), Boost.Program_options (broad compatibility), argparse (header-only, popular). The reflection version is for codebases that prefer schema-as-spec -- the same struct annotations may already drive your JSON serializer + ORM + REST API definitions.

Series post 12 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/clap-for-cpp/

## Hashtags
#cpp #cpp26 #reflection #cli #clap #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Clap for C++: struct to argv parser". Subhead: Per-field annotations drive the parser, the help text, the error messages -- one source of truth for the CLI surface. Citation: wro.cpp 2026-05-22.

## Suggested post time
Friday 2026-05-22, 10:00 CET
Reason: Friday morning slot reaches EU C++ engineers; reflection-arc post 12 continues the 2-day cadence with the first non-text-format use case.
