# reflect_llmschema: emit Claude / GPT tool-use schemas from C++ functions at compile time

## Body
In the AI-agent era every C++ function you expose to Claude / GPT / any tool-using LLM needs a **JSON-Schema description**: parameter names, types, descriptions, required fields, return shape. The conventional path is hand-writing the schema next to the function and praying it stays in sync. C++26 reflection makes the schema fall out of the function declaration:

```cpp
[[=tool::doc{"Fetch weather for a city."}]]
auto get_weather(std::string city, std::string country_code) -> std::string;

std::println("{}", reflect_llmschema::tool_of<&get_weather>());
```

Output (the OpenAI / Anthropic tool-use format, both standardised on the same shape):

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Fetch weather for a city.",
    "parameters": {
      "type": "object",
      "properties": {
        "city":         { "type": "string" },
        "country_code": { "type": "string" }
      },
      "required": ["city", "country_code"]
    }
  }
}
```

The mechanic: walk `parameters_of(^^&fn)` at compile time, infer JSON Schema type from each parameter's C++ type (`std::string` -> `string`, `int` -> `integer`, `std::optional<T>` -> not-required, `bool` -> `boolean`), pull description from a P3394 `[[=tool::doc{...}]]` annotation. Add a parameter to the C++ signature, the schema follows automatically. Rename a parameter, the schema renames. Remove the function, the registration vanishes.

What this REPLACES: every hand-maintained `tools.json` file in your MCP server, every per-function `register_tool()` call with a manually-typed schema string, the test that verifies the schema matches the C++ signature.

What this does NOT replace: server transport (HTTP / stdio / WebSocket, still your choice), authentication, rate limiting, prompt-engineering for which tools to expose. The reflection layer is the schema-generation half; server framework is the other half.

The same walker pattern drives [auto std::formatter](/posts/auto-formatter/) (post 6) and the [JSON serialiser](/posts/json-naive/) (post 8). One walker, three orthogonal output formats. Add a fourth (Anthropic Computer-Use action schema, OpenAPI 3.1 endpoint definition) and the same pattern emits it.

Series post 19 of 25 in the wro.cpp C++26 reflection arc. Live demo on Godbolt with clang-p2996 (`-std=c++26 -freflection-latest -stdlib=libc++`).

https://wrocpp.github.io/posts/reflect-llmschema/

## Hashtags
#cpp #cpp26 #reflection #llm #claude #gpt #mcp #anthropic #openai #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "reflect_llmschema". Subhead: C++26 reflection emits Claude / GPT tool-use schemas at compile time from the function declaration. Citation: wro.cpp 2026-06-17.

## Suggested post time
Wednesday 2026-06-17, 10:00 CET
Reason: Mid-week morning EU C++ + AI/LLM-tooling audience; reflection-arc post 19 continues the every-2-day cadence past the headline 18-post run.
