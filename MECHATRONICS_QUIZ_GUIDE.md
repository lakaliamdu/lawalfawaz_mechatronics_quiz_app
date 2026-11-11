# Mechatronics Quiz App - Student Guide

**File:** `mechatronics_quiz.py`  
**Course:** CTE213 - Mechatronics Engineering  
**Level:** ND2, Yaba College of Technology

---

## 1. How to run

```text
python mechatronics_quiz.py
```

It also runs in IDLE, a normal console, and Pydroid 3 on Android.  
Only `random` and `time` are imported. There are no classes, colours, screen clears or external libraries.

The high-score file `mechatronics_highscores.txt` is created in the folder where the program runs. If that folder is read-only, the program prints a friendly message and continues.

---

## 2. Real sample run (trimmed)

This is real output from a run where the user typed bad menu choices, a bad answer letter, and bad numbers.

```text
------------------------------ MAIN MENU ------------------------------
1. Practice  - see the explanation after every question
2. Exam      - no feedback until the final report
3. Survival  - 3 lives; the game ends when they are gone
4. Speed Run - extra points for fast answers
5. High Scores
6. Quit
-----------------------------------------------------------------------
Choose 1-6: 'hello' is not a whole number. Please type digits only, for example 2.
Choose 1-6: Please choose a number from 1 to 6.
Choose 1-6: 1

... topic and difficulty menus ...

Choose 0-3: Input cannot be empty. Please type a whole number.
Choose 0-3: Please choose a number from 0 to 3.
Choose 0-3: How many questions? (5-50): Please choose a number from 5 to 50.
How many questions? (5-50): 'abc' is not a whole number. Please type digits only, for example 2.
How many questions? (5-50): 5

Ready, Tunde!
Mode: Practice  |  Topic: Mixed  |  Difficulty: Mixed  |  Questions: 5
Press Enter to start...

Question 1/5 [####----------------]  Points: 0  Streak: 0
----------------------------------------------------------------------

A rack and pinion mechanism converts...

  A. rotary motion into linear motion
  B. pressure into voltage
  C. electrical energy into light
  D. linear motion into heat
(Type L for a lifeline.)
Your answer (A-D): 'Z' is not a valid option. Please type A, B, C or D (or L).
Your answer (A-D):

>> CORRECT! +15 points (answered in 0.0s).
   Speed bonus: +5
   Current streak: 1
   Why: The pinion gear turns and pushes the rack in a straight line, changing rotary motion into linear motion.

...

======================================================================
FINAL REPORT CARD
======================================================================
Player: Tunde
Mode:   Practice
Correct answers: 1 / 8
Percentage: 12.5%
Grade: F
Message: Do not give up, Tunde. Start with the revision sheet and practise daily.
Rank: Rookie Tinkerer
Points: 15   (best streak: 1)

PER-TOPIC BREAKDOWN
Robotics and Mechanisms [####################] 1/1 (100.0%)
Actuators and Motors [--------------------] 0/1 (0.0%)
Sensors [--------------------] 0/1 (0.0%)
Electronics Basics [--------------------] 0/1 (0.0%)
Pneumatics and Hydraulics [--------------------] 0/1 (0.0%)
Calculations [--------------------] 0/3 (0.0%)

Weakest topic: Actuators and Motors
Revision tip: Compare DC, servo and stepper motors, and learn what a relay does.
======================================================================
```

The real report also prints a revision sheet, a high-score table, a fun fact, and offers to replay the missed questions.

---

## 3. Testing that was done

| Check | Result |
|---|---|
| `python -m py_compile mechatronics_quiz.py` | compile OK |
| Automated unit checks (62 checks) | 0 failures |
| Practice mode with bad inputs | exit code 0 |
| Exam mode (no feedback during quiz) | exit code 0 |
| Survival mode (3 lives) | ended after 3 wrong answers, exit code 0 |
| Speed Run mode | speed bonuses awarded, exit code 0 |
| Replay of missed questions | replay ran, exit code 0 |
| Narrow filter with fewer than 5 questions | handled, exit code 0 |
| High scores with missing file | friendly message, exit code 0 |
| Closed input stream (EOF / Ctrl+C) | friendly goodbye, exit code 0 |

The automated checks covered: 50 unique questions, four unique options each, valid correct indexes, topic and difficulty values, even A-D answer spread, option shuffling, empty input, letters instead of numbers, out-of-range numbers, `nan`, hidden 50/50 letters, all three lifelines, grade boundaries, survival lives, exam silence, 1% calculation tolerance, missing/corrupt high-score files, and top-5 sorting.

---

## 4. Function-by-function walkthrough (simple English)

### Display and input

- **`show_banner()`** - prints the ASCII robot and the title. Returns nothing.
- **`show_fun_fact()`** - picks one fact from `FUN_FACTS` with `random.choice()` and prints it. Returns nothing.
- **`get_text(prompt, max_length)`** - asks for a nickname until the user types something. Empty input gets a friendly message. It removes `|` and `,` so the score file stays valid, cuts the name to 20 characters, and returns the clean name.
- **`get_valid_int(prompt, low, high)`** - the main number guard. It loops forever until the text converts with `int()`, is not empty, and is inside `low..high`. `try/except ValueError` catches letters and decimals. Returns the integer.
- **`get_valid_float(prompt)`** - the same idea for decimal answers. It uses `float()`, rejects empty input, rejects `nan` (`value != value`), and rejects huge values. Returns the float.
- **`get_yes_no(prompt)`** - loops until the user types Y/YES or N/NO. Returns `True` or `False`.

### Menus and question selection

- **`choose_mode()`** - prints the six menu choices and returns a number from 1 to 6. 5 means high scores and 6 means quit; `main()` handles those.
- **`choose_topic()`** - prints the eight topics plus 0 for Mixed. Returns the topic name or `"Mixed"`.
- **`choose_difficulty()`** - prints 0 Mixed, 1 Easy, 2 Medium, 3 Hard. Returns the matching word.
- **`filter_questions(topic, difficulty)`** - builds a new list containing only questions that match. `"Mixed"` accepts everything. Returns the filtered list.
- **`choose_question_count(maximum)`** - asks for 5 to `maximum`. If the filter has fewer than 5 questions, it says so and uses all of them. Returns the count.
- **`make_question_set(pool, count)`** - copies the pool, shuffles the copy, and returns the first `count` questions. The original bank is never changed, and no question repeats.
- **`shuffle_options(question)`** - makes four `[option, original index]` pairs, shuffles them, and rebuilds the option list. It records where the correct original index landed. Returns `[new options, new correct index]`, so the program still knows the right answer.

### Scoring and small helpers

- **`letter(index)`** - turns 0,1,2,3 into A,B,C,D using `chr(ord("A") + index)`.
- **`answer_text(index, options)`** - returns `"Skipped"` or a string like `"B. Ohm"`.
- **`format_time(seconds)`** - returns a short string like `"4.2s"`.
- **`percentage_of(correct, total)`** - returns `correct / total * 100`, or 0.0 if total is 0, so there is never a divide-by-zero crash.
- **`speed_bonus(seconds, mode)`** - returns extra points for a fast answer. Speed Run gives 10/6/3 for 5/10/20 seconds; other modes give 5/3/1.
- **`streak_bonus(streak)`** - returns 5 at 3 in a row, 10 at 5, 20 at 10, otherwise 0.
- **`calculate_points(seconds, mode, streak)`** - returns 10 base points plus the speed bonus plus the streak bonus.
- **`print_options(options, hidden)`** - prints A-D. Any index in `hidden` (from 50/50) is shown as removed.
- **`print_progress(current, total, streak, points, lives, mode)`** - prints `Question 7/20 [#######-------]` and the live stats. In Exam mode it hides points and streak so the display gives nothing away.
- **`update_topic_stats(topic_stats, topic, is_correct)`** - finds the topic row `[name, correct, total]` and adds one result. If the topic is new, it creates a row. Returns the same list.

### Asking and running questions

- **`choose_lifeline(lifelines)`** - prints 50/50, Skip and Hint with `(available)` or `(USED)`. Returns 0-3. `lifelines` is `[False, False, False]` at the start of each game.
- **`ask_question(question, options, correct_index, lifelines)`** - prints the question and options, starts the timer, and loops until the answer is valid. It handles empty input, non-A-D text, and letters removed by 50/50. `L` opens the lifeline menu:
  - 50/50 hides two wrong indexes and marks that lifeline used.
  - Skip marks the question skipped and returns immediately.
  - Hint reveals the topic and difficulty.
  It returns `[is_correct, skipped, chosen_index, seconds]`.
- **`run_quiz(questions, mode, lifelines, topic_stats)`** - the engine. For every question it prints the progress, shuffles options, calls `ask_question`, updates streaks and points, tracks lives in Survival, prints feedback unless the mode is Exam, and saves wrong answers for revision. It returns six results: points, correct count, attempted count, best streak, revision list, and an "ended early" flag.

### Calculation round

- **`make_calculation_problem(kind)`** - creates one of four problems:
  1. Ohm's law `V = I x R`
  2. Power `P = V x I`
  3. Series resistors `R = R1 + R2 + R3`
  4. Parallel resistors `R = (R1 x R2) / (R1 + R2)`
  It returns `[question text, exact answer, worked solution]`.
- **`run_calculation_round(number_of_problems, mode, show_feedback)`** - shuffles the four kinds so the round uses different types, asks for each answer with `get_valid_float()`, and checks `abs(user - exact) <= 1% of exact`. Correct answers earn 10 points plus a speed bonus. In Exam mode it stores the results and shows nothing yet. Returns `[points, correct, total, details]`.
- **`show_calculation_review(details, only_wrong)`** - prints the user's answer, exact answer, formula working, and CORRECT/WRONG. If `only_wrong` is true, it prints only mistakes. Returns nothing.

### Report card, revision and replay

- **`grade_and_message(percentage, name)`** - uses a clear `if/elif/else` chain to return `[grade, message]`: A 70+, B 60+, C 50+, D 45+, E 40+, F below 40. The message includes the nickname.
- **`rank_title(percentage)`** - returns a fun rank from `Rookie Tinkerer` up to `Chief Mechatronics Engineer`.
- **`topic_revision_tip(topic)`** - returns one revision tip for each topic, including Calculations.
- **`show_topic_breakdown(topic_stats)`** - prints one 20-character bar per topic, e.g. `Sensors [#####---------------] 5/20 (25.0%)`. It also finds and returns the weakest topic.
- **`show_report_card(...)`** - prints player, mode, correct/total, percentage, grade, message, rank, points, best streak, the topic bars, and the weakest topic with its tip.
- **`show_revision_sheet(wrong_list)`** - lists every missed multiple-choice question with the user's answer, the correct answer and the explanation.
- **`show_replay_summary(replay_result)`** - prints the score and percentage for the replay of missed questions.

### High scores

- **`save_high_score(name, percentage, points)`** - appends `name|percentage|points` to the file. `try/except OSError` handles a read-only or missing folder.
- **`load_high_scores()`** - reads the file, skips damaged lines, converts the numbers with `float()` and `int()`, sorts the results, and returns the top 5. A missing file (`FileNotFoundError`) simply returns an empty list.
- **`show_high_scores()`** - prints the top 5 or a friendly "no scores yet" message.

### Main program

- **`main()`** - shows the banner and fun fact, asks for a nickname, then loops: menu, topic, difficulty, count, quiz, calculation round, report, revision, save score, show top 5, offer replay, offer another game.
- **`if __name__ == "__main__":`** - starts `main()` only when the file is run directly. `try/except (KeyboardInterrupt, EOFError)` ends politely if the user presses Ctrl+C or closes the input stream.

---

## 5. Eight questions a lecturer might ask (with answers)

### Q1. Why did you store the questions in a list of lists instead of separate variables?

Because the program needs to loop over them, filter them, shuffle them and count them. One list of 50 question lists makes all of that easy. Each inner list has a fixed pattern: question text, four options, correct index, topic, difficulty, explanation. To add a question, I copy one entry and change the words; no other part of the program needs editing.

### Q2. After shuffling the options, how does the program still know which one is correct?

In `shuffle_options()` I do not shuffle only the text. I build pairs of `[option text, original index]`, shuffle the pairs, then rebuild the text list. While rebuilding, I check which pair holds the original correct index and save its new position in `new_correct_index`. That new index is what `ask_question()` compares against. I tested this on all 50 questions, 40 shuffles each.

### Q3. The program must never crash. Show two places where you prevent that.

First, every numeric input goes through `get_valid_int()` or `get_valid_float()`. They use `try/except ValueError`, check empty input, check the range, and loop until the value is good. Second, the high-score loader catches `FileNotFoundError`, `OSError` and `ValueError`, so a missing or damaged file cannot stop the quiz. I also guard the percentage against division by zero, and `main()` catches `KeyboardInterrupt` and `EOFError`.

### Q4. How is the final percentage calculated, and why are Points separate?

The percentage is:

```text
percentage = (correct multiple-choice + correct calculations)
             / (attempted multiple-choice + calculation questions) x 100
```

That is pure accuracy, so it is fair. Points are a separate game reward: 10 base points for a correct multiple-choice answer, plus a speed bonus, plus a streak bonus. A player can have a low percentage but still collect points for the ones they got right quickly. The grade uses the percentage, not the points.

### Q5. How does the 50/50 lifeline work, and how do you stop it being used twice?

`lifelines` is a list of three Booleans: `[50/50 used, Skip used, Hint used]`. When the player chooses 50/50, the program collects the indexes of the wrong options, shuffles them with `random.shuffle()`, and hides two of them in the `hidden` list. The display shows "removed by 50/50" for those letters, and the answer loop rejects a hidden letter with a friendly message. The program sets `lifelines[0] = True`. If the player tries 50/50 again, the menu shows `(USED)` and the program prints "50/50 has already been used."

### Q6. How does Survival mode work, and why is the report based on attempted questions?

Survival starts with `lives = 3`. A wrong answer subtracts one life; a skip does not. After each question the program checks `lives <= 0`, prints "No lives left", sets `ended_early = True` and breaks out of the loop. The player may have chosen 10 questions but only answered 5, so the report uses `answered_count` as the total. The percentage is correct answers divided by questions actually attempted. Using the planned total would punish the player for questions they never saw.

### Q7. How do the speed and streak bonuses work?

The timer starts with `time.time()` just before the answer loop and stops when a valid answer is accepted. `speed_bonus()` gives more points for quick answers, and Speed Run gives the biggest bonus. `streak_bonus()` gives 5 points at 3 correct in a row, 10 at 5, and 20 at 10. `calculate_points()` adds the 10 base points, the speed bonus and the streak bonus. The report shows the best streak. The percentage is not changed by bonuses, so it still shows real accuracy.

### Q8. How are the high scores saved and loaded safely?

`save_high_score()` appends one line in the form `nickname|percentage|points` and catches `OSError` if the file cannot be written. `load_high_scores()` opens the file inside `try/except FileNotFoundError` and `try/except OSError`. For each line it splits on `|`, checks that there are three parts, converts the numbers with `float()` and `int()` inside `try/except ValueError`, and skips damaged lines. It then sorts the list in reverse order and returns only the top 5. On the very first game the file does not exist, so the program simply shows "No scores saved yet."

---

## 6. How to add or edit a question

Open `mechatronics_quiz.py` and find `QUESTION_BANK` at the top. Copy one entry and keep the same six items:

```python
[
    "Your question text?",
    ["Option A", "Option B", "Option C", "Option D"],
    0,                      # 0=A, 1=B, 2=C, 3=D
    "Sensors",              # must match one of TOPICS
    "Medium",               # Easy, Medium or Hard
    "One sentence explaining the correct answer."
],
```

Then run the file again. The topic picker, filters, report card and revision sheet pick up the new question automatically.

---

## 7. Quick requirement checklist

| Requirement | Where it is |
|---|---|
| Function that returns a value | `get_valid_int`, `filter_questions`, `run_quiz`, many more |
| Questions in lists | `QUESTION_BANK` (list of 50 lists) |
| Loop | every input function, `run_quiz`, `main` |
| if / elif / else | `grade_and_message`, menus, lifelines |
| `int()` / `float()` input | `get_valid_int`, `get_valid_float` |
| Friendly bad-input messages | all input functions, `ask_question` |
| Score, percentage, grade, message | `run_quiz`, `show_report_card` |
| Practice / Exam / Survival / Speed Run | `MODES`, `run_quiz` |
| Topic and difficulty picker | `choose_topic`, `choose_difficulty`, `filter_questions` |
| 5-50 count with validation | `choose_question_count`, `get_valid_int` |
| No repeated questions | `make_question_set` shuffles a copy |
| Shuffled options | `shuffle_options` |
| 50/50, Skip, Hint | `choose_lifeline`, `ask_question` |
| Streak bonus | `streak_bonus`, `calculate_points` |
| Speed bonus with `time` | `speed_bonus`, `ask_question` |
| Calculation round, 1% tolerance | `make_calculation_problem`, `run_calculation_round` |
| Report card and bars | `show_report_card`, `show_topic_breakdown` |
| Weakest topic and tip | `show_topic_breakdown`, `topic_revision_tip` |
| Revision sheet and replay | `show_revision_sheet`, `main` |
| High scores in a text file | `save_high_score`, `load_high_scores` |
| ASCII banner, progress bar, facts | `BANNER`, `print_progress`, `show_fun_fact` |
| `main()` + `__main__` guard | bottom of the file |

