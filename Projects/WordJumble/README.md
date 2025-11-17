# Word Jumble Project  ([Rubric](/Assignments/Rubric_WordJumble.pdf))

This project is a design challenge that involves both individual and partner work. The goal is for you to synthesize what you learned throughout this course by applying your knowledge of data structures and algorithms to a fun word puzzle found in many newspapers.

## Description

Below is a word jumble from a newspaper:

![jumble](Jumble-2014-11-22.png)

The challenge is to **design a way to solve this word jumble with a computer!** Use what you've learned in the course to automate solving this puzzle!

For the first 4 words, each jumble of letters is actually an anagram of a word in an English dictionary. Your first task is to rearrange them to discover the real word they represent.

Once you solve all 4 words, look at where the circles are. All of the letters within the circles should be added to a letter bank, which you'll unscramble and use to solve the final jumble, which is a hyphenated phrase that's an answer to the the punny riddle in the picture.

## Example Input

```python3
    # Create a data structure to help unscramble words (once in global scope)
    # By storing the words list in a specialized dictionary rather than a list,
    # we can look up candidate words much faster than linear searching a list.
    words_dict = create_words_dict(words_list)

`   Try these examples:
    print(words_dict['DGO'])  # --> ['DOG', 'GOD']
    print(words_dict['CDEO'])  # --> ['CODE', 'COED']
    print(words_dict['ILST'])  # --> ['LIST', 'SILT', 'SLIT']
    print(words_dict['EILNST'])  # --> ['ENLIST', 'LISTEN', 'SILENT', 'TINSEL']
```

## Expected Output

```bash
['DOG', 'GOD']
['CODE', 'COED']
['LIST', 'SILT', 'SLIT']
['ENLIST', 'LISTEN', 'SILENT', 'TINSEL']
==================== WORD JUMBLE TEST CASE 1 ====================
Jumble 1: ACOME => unscrambled into 1 words: CAMEO
Jumble 2: FEROC => unscrambled into 1 words: FORCE
Jumble 3: REDDEG => unscrambled into 2 words: DREDGE or GEDDER
Jumble 4: YURFIP => unscrambled into 1 words: PURIFY
Final Jumble: ERCDEPI => unscrambled into 1 possible phrases:
    Option 1: PIERCED

==================== WORD JUMBLE TEST CASE 2 ====================
Jumble 1: TARFD => unscrambled into 1 words: DRAFT
Jumble 2: JOBUM => unscrambled into 1 words: JUMBO
Jumble 3: TENJUK => unscrambled into 1 words: JUNKET
Jumble 4: LETHEM => unscrambled into 1 words: HELMET
Final Jumble: TUMUTHT => unscrambled into 3 possible phrases:
    Option 1: MUTH TUT
    Option 2: TUM TUTH
    Option 3: HUT MUTT

==================== WORD JUMBLE TEST CASE 3 ====================
Jumble 1: LAISA => unscrambled into 1 words: ALIAS
Jumble 2: LAURR => unscrambled into 2 words: RURAL or URLAR
Jumble 3: BUREEK => unscrambled into 1 words: REBUKE
Jumble 4: PROUOT => unscrambled into 1 words: UPROOT
Final Jumble: LIARRREROT => unscrambled into 6 possible phrases:
    Option 1: ERROR LITRA
    Option 2: ERROR TRAIL
    Option 3: ERROR TRIAL
    Option 4: RORAL TERRI
    Option 5: RORAL TIRER
    Option 6: RORAL TRIER

==================== WORD JUMBLE TEST CASE 4 ====================
Jumble 1: TEFON => unscrambled into 1 words: OFTEN
Jumble 2: SOKIK => unscrambled into 1 words: KIOSK
Jumble 3: NIUMEM => unscrambled into 1 words: IMMUNE
Jumble 4: SICONU => unscrambled into 1 words: COUSIN
Final Jumble: TNKISNSI => (no solution)
```

## Tips and Hints

- Use the English dictionary words file located at `/usr/share/dict/words` on all Mac and Linux installations.
- You first need to solve all of the 4 jumbled words to find the set of letters used in the final jumbled phrase.
- The final jumbled phrase is more challenging to solve because it's made up of multiple words, and it could even be a made-up word or phrase pun (see yesterday's solution at the bottom of the image: "furrever").

## Phases of the Activity

1. (Individual) Brainstorm ideas of data structures and algorithms you can use to solve this on your own whiteboard
2. (Pairs) Find a partner whom you don't usually work with, collaborate, share and debate ideas for your solution
3. (Individual) Write **pseudocode** to design your solution first (on whiteboard or on your computer)
4. (Individual) Start implementing your solution with real code!

For the rest of class, your goal is to accomplish the following:

1. Find a partner
2. Write pseudocode
3. Begin writing some implementations for the first and second scenarios
