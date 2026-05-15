# C++ supply chain in 2026

## Body
Shipping C++ in 2026 means vcpkg or Conan, a CycloneDX SBOM on every build, grype `--fail-on critical` as a CI gate, in-toto attestations, sigstore signing. The conventional SBOM workflow leaks because the YAML manifest drifts from the code. C++26 reflection closes the gap: components as P3394 annotations on their integration type; consteval walker emits the CycloneDX fragment AND refuses to compile if a vendored member lacks the annotation. SBOM cannot drift from source.

https://wrocpp.github.io/toolset/cpp-supply-chain-2026/

## Hashtags
#cpp #cpp26 #supplychain #sbom #vcpkg #reflection #wrocpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "C++ supply chain in 2026". Subhead: vcpkg + SBOM + CVE feeds + reflection-driven manifest. Citation: wro.cpp 2026-06-09.

## Suggested post time
Tuesday 2026-06-09, 10:00 CET
Reason: Tuesday morning EU audience.
