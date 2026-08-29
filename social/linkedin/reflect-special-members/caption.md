# The most expensive no-op in C++

## Body
Write this and you have quietly given up move semantics:

  struct Widget {
      int x{};
      int y{};
      ~Widget() = default;    // looks free, is not
  };

Most C++ programmers know the rule in the abstract. Declaring a destructor suppresses the implicit move operations, so Widget copies where it used to move. Knowing it and checking it are different things.

C++26 reflection lets you check it. members_of returns every member the compiler produced, including the ones it generated for you; is_function picks out the methods and is_deleted separates those that exist only to be deleted. Count them and Howard Hinnant's table stops being something you remember and becomes something you print:

  Row1  nothing                6/6
  Row2  some constructor       5/6
  Row3  default constructor    6/6
  Row4  ~T() = default         4/6
  Row5  copy constructor       3/6
  Row6  copy assignment        4/6
  Row7  move constructor       2/6, 2 deleted
  Row8  move assignment        3/6, 2 deleted

Row 4 is the trap. The most innocent looking line in the language takes you from six special members to four.

Rows 7 and 8 are worth a second look too: declare a move operation and the copies do not disappear, they are generated as deleted. That is the better outcome of the two, because a deleted function gives a diagnostic that names it while a missing one is just a lookup failure.

The approach comes from Lieven de Cock's article in the August Overload, which deserves the credit. What I added is a link you can click and all eight rows.

One mistake is in the post on purpose: my first version counted Row 2's own constructor as a special member and reported 6/6, contradicting the very table the program was checking. A verification program that is wrong in a way that confirms your expectation is worse than none.

All eight rows, running: https://wrocpp.github.io/posts/reflect-special-members/

## Hashtags
#cpp #cplusplus #cpp26 #reflection #softwareengineering

## Alt-text
A wro.cpp card reading "The most expensive no-op in C++", about a defaulted destructor removing move operations.

## Suggested post time
Wednesday 2026-10-28, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
