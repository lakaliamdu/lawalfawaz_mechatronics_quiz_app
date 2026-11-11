import random
import time

# The high-score file is created in the same folder where this program runs.
HIGH_SCORE_FILE = "mechatronics_highscores.txt"

# The eight topics used by the topic picker and the report card.
TOPICS = [
    "Electronics Basics",
    "Sensors",
    "Actuators and Motors",
    "Microcontrollers and PLCs",
    "Control Systems",
    "Pneumatics and Hydraulics",
    "Robotics and Mechanisms",
    "Safety and Units"
]

# The four game modes shown in the main menu.
MODES = ["Practice", "Exam", "Survival", "Speed Run"]

# Short fun facts shown at the start and at the end of a game.
FUN_FACTS = [
    "The word robot comes from the Czech word robota, which means forced labour.",
    "Unimate, the first industrial robot, started work at General Motors in 1961.",
    "A typical hobby servo motor turns only about 180 degrees.",
    "A PLC repeats a scan cycle: read inputs, run the program, then update outputs.",
    "The Arduino Uno uses the ATmega328P microcontroller.",
    "A stepper motor often moves 1.8 degrees per step, so 200 steps make one turn.",
    "The pascal (Pa) is the SI unit of pressure, and 1 bar equals 100 kPa.",
    "Gears trade speed for torque: a slower output can push with more force.",
    "Lockout/tagout (LOTO) keeps a machine switched off while it is being repaired.",
    "A piezoelectric sensor can turn a knock or vibration into a small voltage."
]

# The ASCII robot banner. It uses only plain keyboard characters.
BANNER = """
        [ M E C H A ]
        [   Q U I Z   ]
   MECHATRONICS QUIZ APP  -  CTE213
"""

# ----------------------------------------------------------------------------
QUESTION_BANK = [
    # ---------------------------- Electronics Basics -------------------------
    [
        "Which formula is Ohm's law?",
        ["V = I x R", "V = I / R", "R = V x I", "I = V x R"],
        0, "Electronics Basics", "Easy",
        "Ohm's law says voltage equals current multiplied by resistance (V = I x R)."
    ],
    [
        "What is the unit of electrical resistance?",
        ["Volt", "Ohm", "Ampere", "Watt"],
        1, "Electronics Basics", "Easy",
        "Resistance is measured in ohms, named after Georg Simon Ohm."
    ],
    [
        "A resistor has colour bands brown, black and red. What is its value?",
        ["10 ohm", "100 ohm", "1,000 ohm", "10,000 ohm"],
        2, "Electronics Basics", "Medium",
        "Brown = 1, black = 0 and red = x100, so the value is 10 x 100 = 1,000 ohm."
    ],
    [
        "Two 100 ohm resistors are connected in parallel. What is the total resistance?",
        ["200 ohm", "100 ohm", "25 ohm", "50 ohm"],
        3, "Electronics Basics", "Hard",
        "For two equal resistors in parallel, the total is half of one resistor: 100 / 2 = 50 ohm."
    ],
    [
        "Which formula gives electrical power?",
        ["P = V / I", "P = V x I", "P = I / V", "P = V + I"],
        1, "Electronics Basics", "Easy",
        "Electrical power in watts equals voltage in volts multiplied by current in amps."
    ],
    [
        "In a series circuit, what is true about the current?",
        ["It is different in every component.", "It is always zero.",
         "It is the same through every component.", "It is divided equally between components."],
        2, "Electronics Basics", "Medium",
        "A series circuit has only one path, so the same current flows through every component."
    ],
    [
        "A 12 V supply is connected across a 4 ohm resistor. What current flows?",
        ["0.33 A", "16 A", "48 A", "3 A"],
        3, "Electronics Basics", "Medium",
        "Using Ohm's law, I = V / R = 12 / 4 = 3 amps."
    ],

    # ------------------------------- Sensors ---------------------------------
    [
        "Which sensor changes its resistance when the light level changes?",
        ["LDR", "Thermistor", "Strain gauge", "Ultrasonic sensor"],
        0, "Sensors", "Easy",
        "An LDR (light dependent resistor) lowers its resistance as the light level rises."
    ],
    [
        "A thermistor is mainly used to sense...",
        ["light", "pressure", "temperature", "magnetic field"],
        2, "Sensors", "Easy",
        "A thermistor changes resistance with temperature, so it is used for temperature sensing."
    ],
    [
        "Which sensor measures distance by sending out sound waves and listening for the echo?",
        ["Infrared sensor", "Potentiometer", "Photodiode", "Ultrasonic sensor"],
        3, "Sensors", "Easy",
        "An ultrasonic sensor times the echo of a sound pulse to work out distance."
    ],
    [
        "A photodiode is designed to convert light into...",
        ["electrical current", "heat", "sound", "mechanical force"],
        0, "Sensors", "Medium",
        "A photodiode produces a small current when light falls on its junction."
    ],
    [
        "What does a strain gauge measure?",
        ["Colour of an object", "Deformation of a material", "Sound level", "Humidity"],
        1, "Sensors", "Hard",
        "A strain gauge stretches with the material and changes resistance, showing how much it deforms."
    ],
    [
        "Which of these is a simple digital (on/off) sensor?",
        ["LDR", "Thermistor", "Strain gauge", "Limit switch"],
        3, "Sensors", "Easy",
        "A limit switch is either open or closed, which makes it a simple digital on/off sensor."
    ],

   
]
 
 # SECTION: Helper functions for input, menus, scoring and display.

def show_banner():
    print(BANNER)


# Facts are shown at the start and end of a game to make it more fun.
def show_fun_fact():
    fact = random.choice(FUN_FACTS)
    print("\nFUN FACT: " + fact)

# Show the user's score at the end of a game.
def get_text(prompt, max_length):
    while True:
        raw = input(prompt).strip()

        # Empty input is not allowed.
        if raw == "":
            print("Input cannot be empty. Please type something.")
            continue

        clean = raw.replace("|", "-").replace(",", " ")
        clean = clean[:max_length]

        # After cleaning there may be only spaces left.
        if clean.strip() == "":
            print("Please use at least one letter or number.")
            continue

        return clean.strip()
    
# Show the user's score at the end of a game.

def show_score(score):
    print("\n------------------------------ FINAL SCORE -----------------------------")
    print("Points: " + str(score[0]) + "  Correct: " + str(score[1]) + "/" + str(score[2]) +
          "  Time: " + format_time(score[3]))
    print("-----------------------------------------------------------------------")


# Get valid integer input from the user
def get_valid_int(prompt, low, high):
    while True:
        raw = input(prompt).strip()
        if raw == "":
            print("Input cannot be empty. Please type a whole number.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("'" + raw + "' is not a whole number. Please type digits only, for example 2.")
            continue

        if value < low or value > high:
            print("Please choose a number from " + str(low) + " to " + str(high) + ".")
            continue

        return value


# Get valid float input from the user
def get_valid_float(prompt):
    while True:
        raw = input(prompt).strip()

        if raw == "":
            print("Input cannot be empty. Please type a number.")
            continue
        try:
            value = float(raw)
        except ValueError:
            print("'" + raw + "' is not a number. Please type a decimal number, for example 12.5.")
            continue

        if value != value or value > 1000000000 or value < -1000000000:
            print("Please enter a normal number.")
            continue

        return value


# Get yes/no input from the user
def get_yes_no(prompt):
    while True:
        raw = input(prompt).strip().upper()

        if raw == "Y" or raw == "YES":
            return True
        if raw == "N" or raw == "NO":
            return False

        print("Please type Y for yes or N for no.")


# ----------------------------------------------------------------------------
# Contains functions for the main menu, topic and difficulty selection, and filtering questions.
# ----------------------------------------------------------------------------

def choose_mode():
    print("\n------------------------------ MAIN MENU ------------------------------")
    print("1. Practice  - see the explanation after every question")
    print("2. Exam      - no feedback until the final report")
    print("3. Survival  - 3 lives; the game ends when they are gone")
    print("4. Speed Run - extra points for fast answers")
    print("5. High Scores")
    print("6. Quit")
    print("-----------------------------------------------------------------------")
    return get_valid_int("Choose 1-6: ", 1, 6)


def choose_topic():
    print("\n------------------------------ TOPIC ----------------------------------")
    print("0. Mixed (all topics)")
    for number in range(len(TOPICS)):
        print(str(number + 1) + ". " + TOPICS[number])
    print("-----------------------------------------------------------------------")

    choice = get_valid_int("Choose 0-" + str(len(TOPICS)) + ": ", 0, len(TOPICS))
    if choice == 0:
        return "Mixed"
    return TOPICS[choice - 1]


# Choose the difficulty level for the quiz
def choose_difficulty():
    print("\n---------------------------- DIFFICULTY -------------------------------")
    print("0. Mixed")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("-----------------------------------------------------------------------")

    choice = get_valid_int("Choose 0-3: ", 0, 3)
    if choice == 0:
        return "Mixed"
    if choice == 1:
        return "Easy"
    if choice == 2:
        return "Medium"
    return "Hard"


#  Build a new list containing only the questions that match the chosen topic and difficulty.
#  'Mixed' means every value is accepted.
def filter_questions(topic, difficulty):
    result = []
    for question in QUESTION_BANK:
        topic_ok = (topic == "Mixed" or question[3] == topic)
        difficulty_ok = (difficulty == "Mixed" or question[4] == difficulty)
        if topic_ok and difficulty_ok:
            result.append(question)
    return result


def choose_question_count(maximum):
    if maximum >= 5:
        return get_valid_int("How many questions? (5-" + str(maximum) + "): ", 5, maximum)

    print("Only " + str(maximum) + " question(s) match that filter, so all of them will be used.")
    return maximum


# Create a new list of questions by shuffling the pool and taking the first 'count' items.
def make_question_set(pool, count):
    copy_of_pool = list(pool)
    random.shuffle(copy_of_pool)
    return copy_of_pool[:count]


# Shuffle options
def shuffle_options(question):
    pairs = []
    for index in range(4):
        pairs.append([question[1][index], index])

    random.shuffle(pairs)

    new_options = []
    new_correct_index = 0
    for position in range(4):
        new_options.append(pairs[position][0])
        if pairs[position][1] == question[2]:
            new_correct_index = position

    return [new_options, new_correct_index]


# ----------------------------------------------------------------------------
# SCORING AND DISPLAY HELPERS
# ----------------------------------------------------------------------------

def letter(index):
    """Turn an option index (0-3) into a letter A-D. Returns the letter."""
    return chr(ord("A") + index)


def answer_text(index, options):
    """Describe a chosen answer. Returns 'Skipped' or 'A. option text'."""
    if index == -1:
        return "Skipped"
    return letter(index) + ". " + options[index]


def format_time(seconds):
    """Turn seconds into a short string such as '4.2s'. Returns the string."""
    return str(round(seconds, 1)) + "s"


def percentage_of(correct, total):
    """Return correct / total x 100. Returns 0.0 when total is zero."""
    if total == 0:
        return 0.0
    return correct * 100.0 / total


def speed_bonus(seconds, mode):
    """
    Return extra points for a fast correct answer.
    Speed Run gives a bigger bonus than the other modes.
    """
    if mode == "Speed Run":
        if seconds <= 5:
            return 10
        if seconds <= 10:
            return 6
        if seconds <= 20:
            return 3
        return 0

    if seconds <= 5:
        return 5
    if seconds <= 10:
        return 3
    if seconds <= 20:
        return 1
    return 0


def streak_bonus(streak):
    if streak == 3:
        return 5
    if streak == 5:
        return 10
    if streak == 10:
        return 20
    return 0


def calculate_points(seconds, mode, streak):
    return 10 + speed_bonus(seconds, mode) + streak_bonus(streak)


def print_options(options, hidden):
    for index in range(4):
        if index in hidden:
            print("  " + letter(index) + ". --- removed by 50/50 ---")
        else:
            print("  " + letter(index) + ". " + options[index])


def print_progress(current, total, streak, points, lives, mode):
    filled = int(current * 20 / total)
    if filled < 0:
        filled = 0
    if filled > 20:
        filled = 20
    bar = "#" * filled + "-" * (20 - filled)

    line = "Question " + str(current) + "/" + str(total) + " [" + bar + "]"

    # In Exam mode we hide live points and streak so nothing hints at the result.
    if mode != "Exam":
        line = line + "  Points: " + str(points) + "  Streak: " + str(streak)

    if mode == "Survival":
        line = line + "  Lives: " + str(lives)

    print("\n" + line)
    print("-" * 70)


def update_topic_stats(topic_stats, topic, is_correct):
    for entry in topic_stats:
        if entry[0] == topic:
            entry[2] = entry[2] + 1
            if is_correct:
                entry[1] = entry[1] + 1
            return topic_stats

    # Topic not seen before, so create a new row.
    if is_correct:
        topic_stats.append([topic, 1, 1])
    else:
        topic_stats.append([topic, 0, 1])
    return topic_stats

# ----------------------------------------------------------------------------
# ASKING ONE QUESTION (including lifelines)
# ----------------------------------------------------------------------------

def choose_lifeline(lifelines):
    print("\nLIFELINES (one use each per game):")

    if lifelines[0]:
        status_50 = "(USED)"
    else:
        status_50 = "(available)"

    if lifelines[1]:
        status_skip = "(USED)"
    else:
        status_skip = "(available)"

    if lifelines[2]:
        status_hint = "(USED)"
    else:
        status_hint = "(available)"

    print(" 1. 50/50 - remove two wrong options " + status_50)
    print(" 2. Skip  - miss this question, no life lost " + status_skip)
    print(" 3. Hint  - show the topic and difficulty " + status_hint)
    print(" 0. Back to the question")
    return get_valid_int("Pick a lifeline: ", 0, 3)


def ask_question(question, options, correct_index, lifelines):
 
    print("\n" + question[0])
    print("")

    hidden = []          # option indexes hidden by the 50/50 lifeline
    print_options(options, hidden)

    # Only advertise the lifeline key while at least one lifeline is unused.
    if not (lifelines[0] and lifelines[1] and lifelines[2]):
        print("(Type L for a lifeline.)")

    start_time = time.time()

    # This loop is the "never crash" part for answers A-D.
    while True:
        raw = input("Your answer (A-D): ").strip().upper()

        # Empty input.
        if raw == "":
            print("Please type a letter from A to D.")
            continue

        # The user wants a lifeline.
        if raw == "L":
            choice = choose_lifeline(lifelines)

            if choice == 0:
                continue

            elif choice == 1:
                if lifelines[0]:
                    print("50/50 has already been used.")
                elif len(hidden) >= 2:
                    print("50/50 is already active for this question.")
                else:
                    # Find the indexes of the wrong options that are still visible.
                    wrong_indexes = []
                    for index in range(4):
                        if index != correct_index and index not in hidden:
                            wrong_indexes.append(index)
                    random.shuffle(wrong_indexes)

                    # Keep only two of them visible; hide the other two.
                    hidden.extend(wrong_indexes[:2])
                    lifelines[0] = True
                    print("\n50/50 used! Two wrong options are removed:")
                    print_options(options, hidden)
                continue

            elif choice == 2:
                if lifelines[1]:
                    print("Skip has already been used.")
                else:
                    lifelines[1] = True
                    elapsed = time.time() - start_time
                    print("Question skipped. It will appear in your revision sheet.")
                    return [False, True, -1, elapsed]
                continue

            elif choice == 3:
                if lifelines[2]:
                    print("Hint has already been used.")
                else:
                    lifelines[2] = True
                    print("HINT: Topic = " + question[3] + " | Difficulty = " + question[4])
                continue

        # Anything that is not exactly one letter from A to D is rejected.
        if len(raw) != 1 or raw < "A" or raw > "D":
            print("'" + raw + "' is not a valid option. Please type A, B, C or D (or L).")
            continue

        index = ord(raw) - ord("A")

        # A letter removed by 50/50 is not a valid choice.
        if index in hidden:
            print("Option " + raw + " was removed by 50/50. Please choose another letter.")
            continue

        elapsed = time.time() - start_time
        is_correct = (index == correct_index)
        return [is_correct, False, index, elapsed]


# ----------------------------------------------------------------------------
# REPORT CARD, GRADES AND REVISION SHEET
# ----------------------------------------------------------------------------

def grade_and_message(percentage, name):
    """
    Turn a percentage into a letter grade and a personal message.
    Returns [grade, message].
    This function shows a clear if / elif / else chain.
    """
    if percentage >= 70:
        return ["A", "Excellent work, " + name + "! You have a strong grasp of mechatronics."]
    elif percentage >= 60:
        return ["B", "Very good, " + name + "! A little more revision will take you to the top."]
    elif percentage >= 50:
        return ["C", "Good effort, " + name + ". Revise the weak topics and try again."]
    elif percentage >= 45:
        return ["D", "You passed, " + name + ", but the basics need more practice."]
    elif percentage >= 40:
        return ["E", "Close, " + name + ". Go through the revision sheet carefully."]
    else:
        return ["F", "Do not give up, " + name + ". Start with the revision sheet and practise daily."]


def rank_title(percentage):
    """Return a fun rank title based on the percentage."""
    if percentage >= 90:
        return "Chief Mechatronics Engineer"
    elif percentage >= 80:
        return "Senior Mechatronics Engineer"
    elif percentage >= 70:
        return "Mechatronics Engineer"
    elif percentage >= 60:
        return "Junior Mechatronics Engineer"
    elif percentage >= 50:
        return "Apprentice Technician"
    elif percentage >= 40:
        return "Workshop Trainee"
    else:
        return "Rookie Tinkerer"


def topic_revision_tip(topic):
    """Return one short revision tip for a topic."""
    if topic == "Electronics Basics":
        return "Revise Ohm's law, the power formula, and series/parallel resistors."
    elif topic == "Sensors":
        return "Make a table matching each sensor to the quantity it measures."
    elif topic == "Actuators and Motors":
        return "Compare DC, servo and stepper motors, and learn what a relay does."
    elif topic == "Microcontrollers and PLCs":
        return "Revise Arduino pins, RAM vs ROM, PWM and the PLC scan cycle."
    elif topic == "Control Systems":
        return "Learn open-loop vs closed-loop, feedback, PID and overshoot."
    elif topic == "Pneumatics and Hydraulics":
        return "Revise pressure, valves, FRL units and F = p x A for cylinders."
    elif topic == "Robotics and Mechanisms":
        return "Practise degrees of freedom, gear ratios and linkage mechanisms."
    elif topic == "Safety and Units":
        return "Revise SI prefixes, unit conversions, LOTO and PPE."
    elif topic == "Calculations":
        return "Practise Ohm's law, P = V x I, and the series/parallel formulas."
    else:
        return "Read the revision sheet again and explain each answer out loud."


def show_topic_breakdown(topic_stats):
    """
    Print a simple text bar for every topic.
    Returns the name of the weakest topic.
    """
    if len(topic_stats) == 0:
        return ""

    print("\nPER-TOPIC BREAKDOWN")
    weakest_topic = ""
    lowest_percentage = 101.0

    for entry in topic_stats:
        topic = entry[0]
        correct = entry[1]
        total = entry[2]
        percent = percentage_of(correct, total)

        # Convert the percentage to 0-20 hash marks.
        filled = int(round(percent / 100.0 * 20))
        if filled < 0:
            filled = 0
        if filled > 20:
            filled = 20
        bar = "#" * filled + "-" * (20 - filled)

        print(topic + " [" + bar + "] " + str(correct) + "/"
              + str(total) + " (" + str(round(percent, 1)) + "%)")

        if percent < lowest_percentage:
            lowest_percentage = percent
            weakest_topic = topic

    return weakest_topic


def show_report_card(name, percentage, points, correct, total, best_streak,
                     topic_stats, mode, ended_early):
    """Print the complete final report card. Returns nothing."""
    print("\n" + "=" * 70)
    print("FINAL REPORT CARD")
    print("=" * 70)
    print("Player: " + name)
    print("Mode:   " + mode)

    if ended_early:
        print("Survival ended early because all 3 lives were used.")

    print("Correct answers: " + str(correct) + " / " + str(total))
    print("Percentage: " + str(round(percentage, 1)) + "%")

    grade_result = grade_and_message(percentage, name)
    print("Grade: " + grade_result[0])
    print("Message: " + grade_result[1])
    print("Rank: " + rank_title(percentage))
    print("Points: " + str(points) + "   (best streak: " + str(best_streak) + ")")

    weakest = show_topic_breakdown(topic_stats)

    if weakest != "":
        print("\nWeakest topic: " + weakest)
        print("Revision tip: " + topic_revision_tip(weakest))
    else:
        print("\nNo topic data to show.")

    print("=" * 70)


def show_revision_sheet(wrong_list):
    """
    List every multiple-choice question the player missed, with the correct
    answer and the explanation. Returns nothing.
    """
    print("\n" + "=" * 70)
    print("REVISION SHEET - QUESTIONS TO REVIEW")
    print("=" * 70)

    if len(wrong_list) == 0:
        print("Perfect! You have nothing to revise from this game.")
        return

    number = 1
    for entry in wrong_list:
        question = entry[0]
        options = entry[1]
        correct_index = entry[2]
        chosen_index = entry[3]

        print("\n" + str(number) + ". " + question[0])
        print("   Topic: " + question[3] + "  |  Difficulty: " + question[4])
        print("   Your answer:   " + answer_text(chosen_index, options))
        print("   Correct answer: " + letter(correct_index) + ". " + options[correct_index])
        print("   Why: " + question[5])
        number = number + 1


def show_replay_summary(replay_result):
    """Print a short summary after replaying only the missed questions."""
    correct = replay_result[1]
    total = replay_result[2]
    percentage = percentage_of(correct, total)

    print("\n" + "=" * 70)
    print("REPLAY RESULT")
    print("=" * 70)
    print("Correct answers: " + str(correct) + " / " + str(total))
    print("Percentage: " + str(round(percentage, 1)) + "%")
    print("Points earned in the replay: " + str(replay_result[0]))

    if correct == total:
        print("Excellent! You have mastered every question you missed.")
    else:
        print("Keep going through the explanations, then try those questions again.")
    print("=" * 70)


# ----------------------------------------------------------------------------
# HIGH SCORES
# The file is plain text, one result per line: nickname|percentage|points
# ----------------------------------------------------------------------------

def save_high_score(name, percentage, points):
    """
    Append one result to the high-score text file.
    A missing file is fine: opening in append mode creates it.
    File errors are caught so the quiz never crashes. Returns nothing.
    """
    line = name + "|" + str(round(percentage, 1)) + "|" + str(points) + "\n"

    try:
        file = open(HIGH_SCORE_FILE, "a")
        file.write(line)
        file.close()
        print("\nHigh score saved to " + HIGH_SCORE_FILE + ".")
    except OSError:
        print("\nCould not save the high score (the file may be read-only).")


def load_high_scores():
    """
    Read the high-score file and return the top 5 results.
    Each result is [percentage, points, name].
    A missing or damaged file returns an empty list, never an error.
    """
    scores = []

    try:
        file = open(HIGH_SCORE_FILE, "r")
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        # This is normal on the very first game.
        return scores
    except OSError:
        print("Could not read the high-score file.")
        return scores

    for line in lines:
        parts = line.strip().split("|")

        # Skip damaged lines quietly.
        if len(parts) != 3:
            continue

        try:
            percentage = float(parts[1])
            points = int(parts[2])
        except ValueError:
            continue

        name = parts[0].strip()
        if name == "":
            continue

        scores.append([percentage, points, name])

    # Sorting a list of lists compares percentage first, then points, then name.
    scores.sort(reverse=True)
    return scores[:5]


def show_high_scores():
    """Load and print the top 5 high scores. Returns nothing."""
    print("\n" + "=" * 70)
    print("TOP 5 HIGH SCORES")
    print("=" * 70)

    scores = load_high_scores()

    if len(scores) == 0:
        print("No scores saved yet. Be the first on the board!")
    else:
        position = 1
        for entry in scores:
            print(str(position) + ". " + entry[2]
                  + "   " + str(round(entry[0], 1)) + "%"
                  + "   " + str(entry[1]) + " points")
            position = position + 1

    print("=" * 70)

# ----------------------------------------------------------------------------
# MAIN PROGRAM
# This function ties all the smaller functions together.
# ----------------------------------------------------------------------------

def main():
    """Run the whole quiz application. Returns nothing."""
    show_banner()
    print("Welcome to the Mechatronics Quiz App!")
    print("Test your CTE213 knowledge, earn points and climb the ranks.")
    show_fun_fact()

    # Ask for a nickname only. No real names, phone numbers or addresses.
    player_name = get_text("\nEnter a nickname (no personal details): ", 20)

    # The outer loop returns to the main menu after every game.
    while True:
        mode_choice = choose_mode()

        # Menu choice 5 is not a game mode: show high scores and show the menu again.
        if mode_choice == 5:
            show_high_scores()
            continue

        # Menu choice 6 quits the program.
        if mode_choice == 6:
            print("\nGoodbye, " + player_name + "! Keep building and stay safe.")
            break

        # Choices 1-4 map to the MODES list.
        mode = MODES[mode_choice - 1]

        topic = choose_topic()
        difficulty = choose_difficulty()

        pool = filter_questions(topic, difficulty)

        # Defensive check in case a filter ever produces nothing.
        if len(pool) == 0:
            print("\nNo questions match that topic and difficulty. Please try Mixed.")
            continue

        count = choose_question_count(len(pool))
        questions = make_question_set(pool, count)

        print("\nReady, " + player_name + "!")
        print("Mode: " + mode + "  |  Topic: " + topic
              + "  |  Difficulty: " + difficulty
              + "  |  Questions: " + str(count))
        input("Press Enter to start...")

        # Lifelines are fresh for every new game.
        # [50/50 used?, Skip used?, Hint used?]
        lifelines = [False, False, False]

        # Per-topic statistics for the report card.
        topic_stats = []

        quiz_result = run_quiz(questions, mode, lifelines, topic_stats)

        # ------------------------- Calculation round -------------------------
        if quiz_result[5] and mode == "Survival":
            print("\nSurvival ended early, so the calculation round is skipped.")
            calc_score = 0
            calc_correct = 0
            calc_total = 0
            calc_details = []
        else:
            # In Exam mode the worked solutions wait until after the report.
            show_calc_feedback = (mode != "Exam")
            calc_result = run_calculation_round(3, mode, show_calc_feedback)

            calc_score = calc_result[0]
            calc_correct = calc_result[1]
            calc_total = calc_result[2]
            calc_details = calc_result[3]

            # Add each calculation result to the topic statistics.
            for item in calc_details:
                update_topic_stats(topic_stats, "Calculations", item[4])

        # --------------------------- Final results ---------------------------
        total_correct = quiz_result[1] + calc_correct
        total_answered = quiz_result[2] + calc_total
        total_points = quiz_result[0] + calc_score
        percentage = percentage_of(total_correct, total_answered)

        show_report_card(player_name, percentage, total_points, total_correct,
                         total_answered, quiz_result[3], topic_stats, mode,
                         quiz_result[5])

        show_revision_sheet(quiz_result[4])

        # Calculation mistakes are part of the revision too. In Exam mode this
        # is the first time the user sees the worked solutions.
        show_calculation_review(calc_details, True)

        # --------------------------- High scores -----------------------------
        save_high_score(player_name, percentage, total_points)
        show_high_scores()
        show_fun_fact()

        # --------------------- Optional replay of misses ---------------------
        missed_questions = []
        for entry in quiz_result[4]:
            missed_questions.append(entry[0])

        if len(missed_questions) > 0:
            print("\nYou missed " + str(len(missed_questions)) + " multiple-choice question(s).")
            if get_yes_no("Replay ONLY the missed questions now? (Y/N): "):
                print("\nREPLAY MODE: the missed questions only.")
                replay_result = run_quiz(missed_questions, "Practice",
                                         [False, False, False], [])
                show_replay_summary(replay_result)

        # ------------------------- Play again? -------------------------------
        if not get_yes_no("\nPlay another game? (Y/N): "):
            print("\nGoodbye, " + player_name + "! Keep building and stay safe.")
            break


# ----------------------------------------------------------------------------
# PROGRAM ENTRY POINT
# Python runs main() only when this file is executed directly.
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or a closed input stream ends the program politely.
        print("\n\nInput closed. Goodbye!")
