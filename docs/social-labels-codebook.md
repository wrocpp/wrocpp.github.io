# Codebook for labelling wro.cpp posts

You label posts for a review of what makes a LinkedIn card work. You do not see any numbers about how a post
performed, and you must not look them up. Judge only the text in front of you.

The hook labels (`hook_number`, `hook_reframe`) were set from four fields: the **title**, the **card headline**,
the **caption lead** (first sentence) and the **summary**. The `person_role` label is set from those four plus
the **full caption** as it was posted and the **opening of the post** (about its first 200 words), because a
person is often named later than the first sentence.

Label every post for the three fields below. Use only the listed values. When a text is borderline, choose
the stricter value (`no`, `none`) and write the reason in the `note` column.

## hook_number: `yes` or `no`

Does the **card headline** state a quantity the reader could check? A count, a ratio, a duration or a
measurement written as a number or a number word.

| Yes | No |
|---|---|
| "A lookup that got 40 times faster" | "C++26 contracts" (a standard name) |
| "Four editors, one config" | "GCC 16.2 adds a flag" (a compiler version) |
| "193 microseconds became 320 nanoseconds" | "The 2026 survey" (a year) |
| "Cuts three allocations to none" | "Until 12 October" (a date) |
| | "One struct" used only as a figure of speech with no checkable count |

Version numbers, standard names, paper numbers (P2795R5), years, dates, clock times, prices and ticket
numbers never count on their own. A number that counts or measures something does. You are shown no
script flag or hint: read the headline yourself.

Only the headline decides. A number that appears only in the caption lead does not make this `yes`.

## hook_reframe: `yes` or `no`

Both conditions must hold, or the label is `no`.

1. The headline or lead names an **everyday construct or habit** that readers write or do without a second
   thought (an uninitialised `int x;`, `std::endl`, `push_back` in a loop, a moved-from object, a default
   compiler flag).
2. It **claims that construct is the bug, the cost or the danger.**

| Yes | No |
|---|---|
| "The harmless `int x;` is the bug" | "A new container arrives in C++26" (nothing familiar is blamed) |
| "Your default `-O2` hides the slow part" | "How `std::endl` works" (names the habit, makes no claim against it) |

## person_role: `answer`, `credit` or `none`

Does the post name a person from outside the project as part of its reason to exist?

- `answer`: it replies to a named reader's comment, question, spec or wishlist.
- `credit`: it builds on a named author's article, talk, paper or library, and names them.
- `none`: anything else. A bare mention in passing is `none`. Naming only a company, a committee or a
  project is `none`. Naming the site's own author is `none`.

The name may appear anywhere in what you are shown for this label: the title, headline, lead, summary, the full
caption or the opening of the post. Naming is not enough: the person must be part of why the post exists (a reply,
or a piece built on their work), not just cited as a source for one fact. If no person is named anywhere in what
you are shown, the label is `none`, even if you suspect the post is about someone's work.

## Output

One row per post, in the file you are given, with exactly the columns the file asks for (the first pass asked
for `slug,hook_reframe,hook_number,person_role,note`; the person_role pass asks for `slug,person_role,note`).
Do not add columns, do not reorder rows, and do not change any other file.
