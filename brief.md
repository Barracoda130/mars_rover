In this sprint, you'll launch a Rover to explore the surface of Mars!

In practical terms, you will first create a project to solve a kata using test-driven development, and then extend that project into a solid basis for a full application, using your creativity and imagination to add extra features.

> The link to the **Mars Rover Brief** appears in a later task. Follow the task guidance as usual.

---

# 1) Create the Project

In most previous sprints, you have cloned an existing project that we have provided for you. However, it's also important to practice setting up fresh projects from scratch.

## Instructions

Set up a new Python project. You'll need to:

- Create a folder with an appropriate name, perhaps `py-mars-rover`
- Set up a new `venv` with `python3 -m venv venv`
- Activate the venv: `source venv/bin/activate` on Mac/Linux
- Use `git init` in the root folder to make it a git repository
- Set up an appropriate `.gitignore` with content to avoid committing build artifacts such as `pytest_cache`
- Use `pip` to install dependencies like `pytest`

Write a quick `hello_world.py` and `test_hello_world.py` to make sure everything is working.

```py
# hello_world.py
print("Hello, World")
```

```py
# test_hello_world.py
def test_hello_world():
	assert True
```

## Create a GitHub repo + connect remote

1. Create a new GitHub repository with the same name as your folder. Make sure you **don't** add a README or similar on GitHub - you are making everything locally and pushing up. If you add on GitHub too then you will experience conflicts.
2. In the local repo root, connect to your remote repository:

```bash
git remote add origin <PASTE_GITHUB_REPO_URL>
```
## First commit + push

```bash
git add .
git commit -m "Initial solution setup"
git branch -M main
git push -u origin main
```

## Before Moving On

Make sure:

- `python3 hello_world.py` runs the console app and prints `Hello, World`
- `pytest` runs the sample test which passes
- you can commit and push changes to GitHub

---

# 2) The Input Layer: Enums

## Instructions

- Carefully read [the Mars Rover Brief](https://github.com/northcoders/mars-rover-brief)

- Once you have read the brief, think about how you might implement this as a single function, then as a whole program, then read on below.

## Cleanly Handling Input

The Mars Rover brief lends itself naturally to an OOP (Object-Oriented Programming) approach. A useful approach could be to create classes such as `Plateau` and `Rover` which together handle the logic of moving the rover around.

These classes could have methods like `Rover.move_forward()` and `Rover.rotate("left")` or `Plateau.is_within_bounds(x,y)`. By calling these methods, the logic for movement could be implemented.

However, one additional problem that the Mars Rover App has to solve is "handling input".

Recall that the input for the program is a series of strings. For example:

```
5 5
1 2 N
LMLMMLLMMMR
```

It may seem natural that your `Plateau` or your `Rover` classes would have methods or constructors that take these strings as parameters.

However, one major disadvantage of this approach is that this ***ties your input to your logic***. If the input format changes (which happens frequently in tech), then you would have to alter your entire program. For example, if the input string for the plateau size changes from `"5 5"` to `"PLATEAU5x5"` you may have to make changes in many parts of your program if you have used these strings directly in multiple classes.

Instead, it's helpful to create an ***Input Layer***: a series of classes whose job is to convert from some input (in this case, the above strings) to an appropriate data type.

You can then use these clean data types everywhere in your program. If the input changes in future, you then _only_ need to change your input layer.

### Enums - Instruction and CompassDirection

It's tempting to treat the instructions as a `string`. After all, `LMLLMMLR` looks like one. But the problem with strings is that they can be _anything_. A user could input the string `"bananaLMLL"` and your program would be happy with that because they're both strings.

Instead of passing around strings of instructions, let's create an `Instruction` type.

You _could_ make an `Instruction` class whose job is to take a string like `LMLMR` and turn it into a list of valid instructions. Perhaps it would filter out any invalid characters like `B`.

But you can also use `enums` in Python for this.

```py
from enum import Enum

class Instruction(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    MOVE = 'M'
```

This creates a special class which only allows for values `L`, `M` or `R` - exactly what you want.

## Your Task

- Create the enum for `Instruction` as above

- Create an enum for a compass direction too.

- For now, **do not** worry about converting input strings into these enums.

## Before Moving On

- Commit your changes with a clear message (e.g. `Add Instruction and CompassDirection enums`)


---

# 3) The Input Layer: Data Types

Usually we think of classes as being about a mix of data and functionality - properties and methods. However, they can be useful purely for grouping related data together, even without adding any methods. These are sometimes known as **data classes**.

## Data classes - Position and PlateauSize

Look again at the second input line:

```
1 2 N
```

This defines the position of a Rover. It would be very natural to store this on the Rover as two `int`s and a `char`. For example `Rover.X`, `Rover.Y` and `Rover.FacingDirection`, or similar.

However, instead of scattering these values around separately, it can be useful to create a `Position` class to hold this information together.

tion` class to hold this information together.

This gives you the same advantages as using an `Instruction` type instead of a raw string: your data becomes more structured, more expressive, and easier to work with.

For example, once you have a `Position` class, you can use it all over your program. Then, if the requirements change later to add a z‑axis, then it would be simple to add a `z` to your position class, and then this information is available everywhere in your program.

## Your Task

- Create a `Position` class which contains data properties for the x, y and direction you are facing. Hint: make sure you use the **appropriate** type for your direction, which you created in the last task.

- Create a class for `PlateauSize` to represent the plateau boundaries.

## Organisation

Consider where you want to keep these classes and enums on disk within your project. Do you want to create a folder to hold all of the types you are defining? What could that folder be called?

## Before Moving On

At this point, you should have created enums/data classes for:

1. The Instructions
2. The Plateau Size
3. The Compass Directions
4. The Rover Position

> Don't forget to make commits at suitable intervals, with high-quality commit messages.

---

# 4) The Input Layer: Parsers

## Domain Types & Complexity

You now have created types which match the ***domain*** you are working with.

This is often the first task when beginning a complex application, and is the most important step to get right. Starting with incorrect or poorly-designed classes leads to complexity in future, as you strain to force your not-quite-right classes to handle the actual domain of the problem.

This means that if you find yourself writing increasingly complex, confusing code, you should take a step back and reconsider if altering the design of some classes would simplify your current problem. Sometimes a well-designed class removes a problem entirely!

For example, imagine this _terrible_ design: your compass directions have been designed to ONLY have `NE`, `SE`, `SW` and `NW`. You could then add a method that calculates `N`, `S`, `E` and `W` by adding together two of your other points, so `NE + NW = N`. Every time you need a simple direction, you would have to add together two other directions to find it! Hopefully it's obvious that this design is not a wise idea as it is making compass points much more complex than they need to be.

This example illustrates that a **poor choice of underlying data types leads to logical complexity** - just using `N`, `E`, `S` and `W` is **much** simpler.

> Whenever you find yourself struggling with a problem which keeps seeming to grow in complexity, consider if there may be a simpler way to store your underlying data.

## Parsing Classes

The next task is to convert from the raw string input, such as `5 5 N` to your nice clean classes and types. Conversion from strings to custom types is known as **parsing**. Almost every program which deals with user input has to parse it at some point.

## Your Task

- Create a class (or classes) whose job is to parse the provided input strings. The class methods should return the appropriate types from those you have created up to now.

> This task is very well-suited to TDD - read on to consider how you may approach it.

### Approaches

You might choose to create a single `InputParser` class with methods for parsing each of the input strings. For example, it might have a method called `parse_instruction(rawInstruction)` which returns a list of your `Instruction` types when given a string such as `"LMRRRLMM"`.

Alternatively, you might choose to create a specific `InstructionParser` and a specific `PlateauParser` along with other specific parser classes. This approach is good when you have lots of different user inputs and you want to keep them clean and separated. Which approach you choose is up to you!

- Group these classes together in a folder with an appropriate name. This is the critical part of your **Input Layer** - the part which takes raw input and converts it into useful types.

## Testing

- Make sure each of your classes has a corresponding `test_XXXXXX.py` file with proper unit tests for your classes.

- Ensure you test that various valid inputs return the correct data.

- Include tests which pass **invalid** input to your parsing classes. Consider how this should be handled in your parsing classes, and what you should/could test for.

For example, you could decide that invalid instructions are ignored, so `LMRHAJREAJEM` becomes `LMRRM`. Or you could decide that invalid instructions lead to raising an error. These are both justifiable choices. Pick the one you think seems best.

## Before Moving On

- You should have well-tested classes which parse all of the possible user inputs defined in the brief, returning appropriate data types you defined in earlier tasks.

> Don't forget to make commits at suitable intervals, with high-quality commit messages.

---

# 5) The Benefits of Layering

You have now created a simple "input layer", whose job is to take raw string input and convert it to custom types to use in the rest of your application.

In the next few tasks you will implement the "logic layer" - the part of your app which actually moves rovers around on a plateau.

When presented with a problem, it's _so tempting_ to immediately jump to the logic layer and begin writing code to move rovers around. However, in this case you'd have ended up with all your parsing logic mixed up with your "moving rovers" logic.

> It can also be tempting to jump straight to implementing the UI! This often leads to a very over-complicated design which grows into a nightmare to work on.

Creating the input layer in advance will simplify the logic layer, because the logic layer is now independent of the input format. This input could come from a web form, from mouse clicks, from unit tests, or from a user typing `"LMMMLR"` into a terminal. But since you have cleanly separated parsing from logic, the code that processes the instructions won't care – it will just receive a list of valid `Instruction` values no matter where those instructions came from.

This has the additional advantage of being **flexible** for future changes. In real apps, requirements are constantly changing, and designing your code to be easy to change is important.

For your Mars Rover, if or when the input format changes, you will only need to change the code in your parsing functions, not everywhere in your program.

This approach of clean layering can be applied to almost every complex application you ever create.

----

# 6) Create an Entry Point

Until now, many sprints have been made up of isolated functions which you have tested via the test runner.

In real world programs, we must also consider how the program starts. Generally, there is a single "entry point" - a piece of code whose job is to do all of the required setup and start off the program.

Eventually, this file will be the main orchestrator for your program. It will do things like "request the UI layer to take in input from the user", "call the input layer to parse the input", "pass the parsed input to the logic layer" and "pass the result to the UI layer to display".

> Notice how the above paragraph is phrased. Your main entry point should not do any of those tasks itself! Its job is to **coordinate** the different layers.

Currently you have a simple "Hello world" entry point. Let's replace that with something more useful.

## Your Task

- Delete your hello world file.
- Create a `main.py` file.
- For now, make `main.py` simply pass the example input from the brief into your parser class(es) as a series of strings, receiving the data classes in return.

Later you can replace this code with more sophisticated coordination as your layers themselves become more sophisticated.

This iterative improvement is how real applications are built.

## Before Moving On

Run `python3 main.py` and observe the data classes returned from your input layer - is it all working as expected?

> Don't forget to make commits at suitable intervals, with high-quality commit messages.

---

# 7) The Logic Layer: Design

## Instructions

The next few tasks will lead you through the process of implementing the key functionality of [the Mars Rover Brief](https://github.com/northcoders/mars-rover-brief).

The end result you're aiming for is a series of classes which will act as the "logic layer" for your future application.

> At first, we won't connect the input layer to the logic layer. Consider this a separate mini-system that you're building alongside your existing input layer. Later, you will adjust `main.py` to provide the glue from the input layer to this new logic layer.

## The Rover

- Using either pen/paper or a free online whiteboard program, sketch out designs for the classes required to meet the brief. Ask yourself these questions:

1. What classes will my solution require?
2. What data should each class have?
3. What methods should each class have?

> Don't spend too long on this task - 5-10 minutes of design thinking will be useful.

### Consider the alternatives

There are many potential designs, each with different tradeoffs. Take the example of "position data for a Rover". You have already created a data class to hold this information. But which classes could/should have that data class as an attribute?

1. The `Rover` class could have a position attribute which is an instance of your `Position` class. This is the most intuitive and natural solution.
2. Alternatively, the `Plateau` class could have a list of `Position` to track all of the rovers on the plateau. Effectively we'd be transferring some responsibility from the Rover to the Plateau. Instead of each Rover knowing its position, the Plateau would know the positions of all rovers.
3. Or there could be a `MissionControl` class which holds all of the positions of Rovers on the Plateau. This class would act as an orchestrator of the Rovers, perhaps calling methods like `is_position_empty()` on the `Plateau` class to find out if a particular Rover can make a move to a new position before updating the positions.

Each of these is a plausible choice! 

The purpose of this exercise isn't to choose the "best" solution. We're aiming to feel out the design decisions required when creating any class.

**Note:** While the above are all good options, there are bad options too! For example, duplicate rover positions on the plateau, rover AND mission control. State data should always be stored only ONCE, or it may get out of sync - the Plateau thinks a Rover is at `[1,1]` but the Rover thinks it is at `[3,1]`. We always want a **single source of truth** for all data.

> If you're in doubt after thinking this over, then go with option #1 for this particular decision! It's most natural in OOP to keep the Rover position on the Rover itself.

- Complete your class diagram sketch, adding all the methods & data you think you might require to fulfil the brief.

- Once you've sketched out your first idea, try taking a fresh piece of paper and sketching a different possibility. What else do you have to change if you, say, add a `MissionControl` class, or move some functionality from one class to another?

---

# 8) The Logic Layer: First Test

## Instructions

- Pick a small piece of functionality from your design and add a series of unit tests for it.

For example, let's explore how a rover might rotate - a small, important piece of functionality. 

Perhaps you designed your `Rover` class to have a `rotate` method. This would be a typical approach. Consider all the possibilities required to test this hypothetical method:

```py
# Example code - don't worry about the details, look at what we're testing
def test_rotate_right_from_north():
        rover = Rover(0, 0, CompassDirection.NORTH)
        rover.rotate(Instruction.RIGHT)
        assert rover.facing == CompassDirection.EAST

def test_rotate_right_from_east():
        rover = Rover(0, 0, CompassDirection.EAST)
        rover.rotate(Instruction.RIGHT)
        assert rover.facing == CompassDirection.SOUTH
```

You might also wonder about testing for weird circumstances, like this:

```py
rover_facing_east.rotate(Instruction.M); # what should this do?!
```

Or perhaps your `rotate` method was designed to take two parameters, a start direction and the rotation:

```py
rover.rotate(Direction.N, Instruction.R); # output should be E
```

Again, the point here is to explore the problem space. Even a "simple" rotation method requires you to make a surprising number of design decisions!

- Once you have implemented (one or more) ***failing*** tests for your rotation method (or a similar-sized method), you're ready to move on.

---

# 9) The Logic Layer: First Implementation

## Your Task

- Using your failing tests as a guide, implement this single method.

For example, if you followed the example of testing your `Rover.rotate` method, start to implement the actual method until the test passes.

- Repeat the process, adding more tests and implementing the logic using the **RED-GREEN-REFACTOR** cycle until your chosen method is fully-tested for all possible inputs and unusual circumstances.

You've now got a single robust, well-tested, well-designed method. This is a great starting point for your logic layer. Following this TDD process also automatically builds a suite of tests to ensure your application remains stable when you make changes.

### The Plan

Remember, for now, there's no requirement to hook this up to any of your Input Layer parsing code. Your logic layer methods should receive your data classes and custom data types and return suitable data classes and custom data types.

We will hook the layers together in `main.py` once the logic layer is completed.

> Don't forget to make commits at suitable intervals, with high-quality commit messages.

---

# 10) The Logic Layer: Repeat the Process

## Instructions

- Pick another method from your logic layer. What else does it need to do? Perhaps a rover needs to move forward? Perhaps a method needs to check if you've hit the edge of a plateau? And so on...

- For that method, create a series of unit tests, considering all the possible design decisions and potential inputs. Make sure each test fails at first.

> Remember to consider different types of valid input, invalid input, and missing input.

- Implement the functionality until all the tests pass.

- Repeat the process of implementing new methods until the brief has been met.

> Don't forget to make commits at suitable intervals, with high-quality commit messages.

## Before Moving On

You should now have:

1. A series of data classes/enum types
2. Some classes that parse string inputs and return those data classes / enum types (your input layer)
2. Some classes that take your custom classes/enums as parameters and move Rovers around on a Plateau (your logic layer) according to a series of instructions

It's time to hook these things together in `main.py`.

---

# 11) Connect the layers: Integration Testing

## Instructions

- Return to `main.py` for the application.

- Add an array of strings called `input`, and hard-code it to the example input from the brief:

```
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

- Pass this sample input into your input layer in the appropriate ways to retrieve your parsed data.

- Pass the parsed data into your logic layer. It should be possible to retrieve the final position of the rovers, which should match the example from the brief:

```
1 3 N
5 1 E
```

> This is effectively a manual "integration test". You are testing that both layers of the application work when tested together.

- Create a new test file - perhaps `test_layer_integration.py` and add a test which does all of the above steps and asserts that the output is correct. This test will ensure your input and logic layers work well together even as you add new functions.

- Add a couple more tests to your integration test file. These tests should check that **other** sets of raw inputs lead to correct Rover positions after being passed through your input and logic layers.

> Don't forget to make commits at suitable intervals, with high-quality commit messages.

---

# 12) Remember the README

## Instructions

It's crucial that your project has a high quality `README.md`. This benefits:

- Other developers seeking to use your project
- Potential employers looking at your github
- Your future self

Go back to your `README.md` at the root of the project. Use [Github Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) to lay out the README contents. 

You should include:

- Headings
- A description of the project
- Instructions for running the project on a fresh machine
- Documentation for other developers regarding how to use/run the project

Ensure the README looks professional in both layout and content. If necessary, use a spell-checker to verify your spelling and grammar.

Later, once you've added a user interface (UI) it would be good to add screenshots and explanations of how to use the UI to your README.

> Don't forget to make commits at suitable intervals, with high-quality commit messages.

---

# 13) A Simple UI Layer

- First, delete your existing entry point code from `main.py`. Your integration test should still check that the whole app works and solves the kata when you run your tests.

## The Plan

It would be good to add a main loop in your entry point which uses a new layer to either a) receive information from the user, or b) display the current status of the plateau to the user. This main loop will then call your input/logic layers as necessary to process the user input, passing any results to this new layer to display.

For the above plan to work, you will need the final layer of this application: a **User Interface (UI)** layer.

## UI Design

At the moment, all of your users must input data by altering hard-coded strings. It's time to create an interface for users to work with your app.

Luckily, you've created a great foundation of clean and well-designed input/logic layers.

It's very natural when developing to **start** with the UI instead of input/logic layers. After all, as users, UI is the first thing we think of when we interact with an application. 

But beginning with the UI layer can lead to muddy code, where UI is intertwined with input parsing which is intertwined with logic. The approach you have followed will make it much easier to add all kinds of user interfaces on top of clean layers.

For example, if your UI receives input from the user, you can pass that to your input-parsing layer. To display outputs, your UI layer can ask the logic layer to calculate positions, and then show them on screen.

Let's think about possibilities...

### Options

- You could opt to add a ***file-based UI***, where you read inputs from a file named `input.txt`. This makes it much easier for users to input data to your application than altering the code itself.

- You could opt to create a ***terminal-based UI***, where you prompt the user to enter the plateau size, the rover landing coordinates, and the rover instructions. You can eventually make this more sophisticated, adding display of the rovers on the terminal and moving them around visually as instructions are entered!

- You could opt for your program to support **both** files and terminal input!

Since you already have a neat layer which handles inputs, it's easy to hook up either of these approaches (or both!) and then feed the result into your logic layer.

## UI Layer Design

The main elements you will need are:

1. A UI class
2. A method on the UI class which receives your classes which represent the current state of the world (rovers, plateaus, mission control, whatever you have!) and displays the plateau together with all rovers in the terminal.
3. Various methods on the UI class which prompt for input, e.g. `prompt_for_plateau_size()` and `prompt_for_rover_landing_position()` and `prompt_for_rover_instructions()`.

These prompting methods can return raw strings (in which case the code calling them has to immediately call your parsing classes to convert them to nice custom types), or they could call the parsing classes themselves and return the nice types directly. Both approaches can be useful. Choose whichever you prefer.

- Implement the above list of requirements in a new folder named `/ui/` in files of your choice.

### Tying it together

Once you have a UI class (or classes) which does the above, return to your empty `main.py` and add code which:

1. Displays a welcome to the user (by calling a suitable method from the UI layer)
2. Prompts the user for a plateau size (by calling a suitable method from the UI layer)
3. Creates an appropriate plateau object (input layer)
4. Prompts the user for a rover landing position (UI layer)
5. Creates appropriate data classes from the input using your parsing classes (input layer)
6. Prompts the user for movement instructions (UI layer)
7. Uses your input/logic classes to make the rover follow the instructions (logic layer)
8. Displays the end result of the plateau (UI layer)
9. Ends the program

Importantly, this code should all be simple - it is just tying together existing pieces from your input, logic and UI layers. Your `main.py` should not contain anything complicated!

## Before Moving On

Running the program should start an interactive terminal which prompts the user to enter a plateau size, rover landing coordinates, and instructions. It should display the end result of the plateau with correct position, and then the program should end.

---

# 14) To the Moon…

Usually programs like this don’t end after a single rover. The final task you need is to turn this into a **persistent rover‑management program**.

The easiest way to begin is by making sure your program can handle **invalid input**.

## Incorrect Input

One major issue with user input is that users will often get it wrong! What if a user enters an invalid plateau size, or some nonsense instructions? What does your program do?

### Your Task

- Read this entire task carefully before you begin!
- Your aim is to make it so your **input layer returns an appropriate error code** if invalid input is detected.
- If your `main.py` receives an **error rather than your custom data types**, it should **display the prompt again**.

At first, this may seem very difficult to implement! It is easy to accidentally create a tangled web of spaghetti code attempting to do this. Read on for hints...

### Hint: Finite State Machines

Look up the concept of a **finite state machine**. The idea is that your application always has a current **state**, and your program behaves differently depending on that state.

You can model this using an enum:

```python
from enum import Enum, auto

class AppState(Enum):
    WELCOME = auto()
    PROMPT_FOR_PLATEAU = auto()
    PROMPT_FOR_LANDING = auto()
    PROMPT_FOR_INSTRUCTIONS = auto()
    DISPLAY_PLATEAU = auto()
```

You can then track the current state in `main.py`:

```python
current_app_state = AppState.WELCOME
```

And drive your program using a loop and a match (or if/elif fallback):

```python
try:
    while True:
        match current_app_state:
            case AppState.WELCOME:
                # show a welcome message
                current_app_state = AppState.PROMPT_FOR_PLATEAU

            case AppState.PROMPT_FOR_PLATEAU:
                # prompt user for plateau size
                # parse input using your input layer
                # if valid → move to next state
                # if invalid → show error and stay in this state
                pass

            case AppState.PROMPT_FOR_LANDING:
                # prompt for rover landing position
                pass

            case AppState.PROMPT_FOR_INSTRUCTIONS:
                # prompt for rover movement instructions
                pass

            case AppState.DISPLAY_PLATEAU:
                # display plateau and rover positions
                pass

            case _:
                raise RuntimeError("Unknown application state")
except Exception as ex:
    print("An unexpected error occurred:", ex)
    # Optionally reset state or exit safely
```

This approach lets you:

- keep **input parsing separate from logic**
- **recover gracefully** from invalid input
- avoid messy, deeply nested conditionals
- build a **fully interactive, persistent** console app

## Error Handling

Consider what happens if an unexpected exception is thrown in any of your layers.

- Add a global `try/except` around your main state machine loop.
- What can you sensibly do in the `except`? At the very least, you should show a message to the user. Perhaps you want to reset the app state too? Does it depend?

## Before Moving On

Make sure you:

- return errors from your input layer instead of crashing
- loop back to prompts when input is invalid
- keep your state transitions clear and predictable

---

# 15) ... and Beyond!

## Instructions

It's time to get *really* creative!

You've taken a single kata and turned it into a well-structured, well-tested foundation for an application, with cleanly separated layers to handle parsing input, logic, and a user interface.

How far can you push this? What features can you add? Here are some ideas for you:

### More Commands

Add support for alternative commands, like flipping 180 degrees, or jumping forward several spaces, or taking a photo of the Martian surface, or picking up a rock sample.

Hint: if you've designed your input/logic layers well, then adding this feature will just require adding a new item to your `Instruction` enum, adding the relevant parsing code, and then adding a small piece of code to the instruction processing part of your logic layer. This is why we wanted to create a clean design in the first place - it makes changing the code and adding features much simpler.

***Don't forget to add tests for these new commands!***

### Obstacles on the Plateau

Can you add obstacles to the plateau? How would you display them on your UI? What happens when a Rover tries to move into one?

### Aliens

Are there aliens on Mars? What do they do when they come across a Rover?

### Three Dimensions

Can the plateau have hills and valleys? Can the Rover fly? How about adding a `z` co-ordinate - what needs to change to support this?

### Alternative-shaped Plateaus

Can you define input formats for other plateau shapes and sizes? How should a Rover move around on these plateaus? What problems do you have to solve? What do you have to change about your class design?

### Other features

The reason we built a strong foundation for this app is so it can support some creative ideas, so use your imagination! 

> Whatever you add, keep your code clean and ensure all your code is properly unit-tested. Ensure your README is up-to-date with everything and this can be a really impressive portfolio piece for you.

