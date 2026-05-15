# C++ supply chain in 2026: vcpkg / Conan / SBOM / CVE feeds + a reflection-driven SBOM that cannot drift

## Body
Shipping C++ in 2026 means more than picking the right compiler. It means a real package manager (`vcpkg` or `Conan`), a CycloneDX or SPDX SBOM emitted on every build, CVE feeds wired into CI, in-toto attestations for the build steps, and a story for "what do we do when the next OpenSSL CVE drops at 04:00 on a Sunday".

The 2026 stack:
- **Package manager**: vcpkg (manifest mode) or Conan (per-dep recipes). Either qualifies; mixing causes pain.
- **SBOM**: `syft` emits CycloneDX 1.5 JSON or SPDX 2.3 JSON from your source tree on every build
- **CVE scan**: `grype --fail-on critical` consumes the SBOM + NVD + GitHub Advisory + OSV. The non-zero exit is the load-bearing line -- without it, grype is a dashboard; with it, it's a gate.
- **Provenance**: in-toto attestations for build steps; SLSA Level 3 / 4 for critical pipelines.
- **Signing**: sigstore cosign, keyless via OIDC.

Where this workflow leaks: a side-channel manifest (YAML) drifts. A new dep gets vendored without a manifest entry; an old dep stays in the manifest after removal; license changes between versions; manifest holds the old one. Each drift is an audit-finding waiting to happen.

C++26 reflection closes the gap. Encode each component as a templated P3394 annotation on its integration type:

```cpp
struct VendoredComponents {
    [[=sbom::component<"nlohmann-json","3.11.3",
                       "pkg:github/nlohmann/json@v3.11.3","MIT">{}]]
    struct nlohmann_json_tag {} json;

    [[=sbom::component<"openssl","3.2.1",
                       "pkg:github/openssl/openssl@openssl-3.2.1",
                       "Apache-2.0">{}]]
    struct openssl_tag {} openssl;
};

emit_components<VendoredComponents>();  // emits CycloneDX 1.5 JSON
```

A consteval walker emits CycloneDX from the annotations AND `static_assert`s every member carries one. **The SBOM cannot drift from the source because the source is the only declaration of it.** Add a vendored type without the annotation, the build refuses with the field name in the diagnostic. Merge the in-source fragment with the toolchain SBOM (syft scans the binary + system deps) and you have a complete BOM that grype can consume.

The same `nonstatic_data_members_of` walker drives the hardened-stdlib lint, the MISRA Rule 11.0.1 lint, the lifetime borrow lint, the SoA layout transform. One walker, five orthogonal rules. The SBOM-required rule is just predicate #6.

C++29 candidate features collapse the loop further: `[[inject(sbom_component)]] using nlohmann_json = vcpkg::dep<"nlohmann-json","3.11.3">` would let the compiler read vcpkg.json + inject the wrapper struct + P3394 annotations.

https://wrocpp.github.io/toolset/cpp-supply-chain-2026/

## Hashtags
#cpp #cpp26 #supplychain #sbom #cyclonedx #vcpkg #conan #grype #syft #cve #reflection #wrocpp #moderncpp #security

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "C++ supply chain in 2026". Subhead: vcpkg / Conan / SBOM / CVE feeds + reflection-driven SBOMs that cannot drift from the source. Citation: wro.cpp 2026-06-09.

## Suggested post time
Tuesday 2026-06-09, 10:00 CET
Reason: Tuesday morning EU security + DevSecOps + production-C++ audience; toolset launch fits the off-day cadence between reflection-series posts.
