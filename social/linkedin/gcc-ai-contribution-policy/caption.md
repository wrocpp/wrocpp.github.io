# GCC will decline AI-generated contributions above the legal threshold

## Body
The GCC Steering Committee accepted its AI Policy Working Group's recommendation on 29 July, and the policy is now published. It is more carefully drawn than the headlines suggest.

The core rule: GCC declines any legally significant contribution which includes LLM-generated content or is derived from it. Everything turns on "legally significant", which is not a new term invented for this. It comes from the GNU maintainer guidelines, where the practical boundary sits at roughly fifteen lines of code or text. Below that a change is generally not copyrightable on its own, which tells you what the policy is actually about: provenance and copyright, not code quality.

The exceptions are the interesting part. Test cases are exempt, and maintainers may accept legally significant test cases generated in whole or in part by a model. Small contributions are allowed if they meet the usual bar and are clearly marked. And using a model is not the same as contributing its output: research, analysis, bug discovery, patch review and debugging are all explicitly fine, so long as nothing generated lands in the tree.

Two procedural requirements came with it. Commit messages carry an Assisted-by tag where a model helped, and only humans may submit contributions and provide sign-offs, which forecloses the agent-opens-a-pull-request workflow before it arrives.

The policy is explicitly provisional, with a review no later than the start of 2027.

Full breakdown: https://wrocpp.github.io/posts/gcc-ai-contribution-policy/

Where would you draw this line for your own project?

## Hashtags
#cpp #cplusplus #gcc #opensource #ai #softwareengineering

## Alt-text
A cream wro.cpp social card reading "GCC will not take AI-written patches", about the GCC Steering Committee's AI contribution policy.

## Suggested post time
Thursday 2026-08-06, 10:00 CET
Reason: post lands on its pubDate; mid-morning CET for the EU audience.
