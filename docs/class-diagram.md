# Mars Rover UML class diagram

The diagram below describes the principal classes, enums, and relationships in
the `mars_rover/src` package. It reflects the current implementation,
including the console and Pygame adapters.

```mermaid
classDiagram
    direction LR

    class LayerCoordinator {
        -InputParser _input_layer
        -Plateau _plateau
        -OutputWriter _output_layer
        -ProgramState _state
        +run()
        -_setup() ProgramState
        -_run()
        -_get_next_instruction(expected_instruction_type) ProgramState
        -_cleanup()
    }

    class InputParser {
        <<abstract>>
        +get_next_instruction(expected_instruction_type) InputInstruction
        +setup()
        +cleanup()
        +logic_error_raised(exception)
        #_parse_plateau_size(data)$ InputInstruction
        #_parse_rover_start(data)$ InputInstruction
        #_parse_rover_instruction(data)$ InputInstruction
    }

    class ConsoleInputParser {
        +get_next_instruction(expected_instruction_type) InputInstruction
    }

    class FileInputParser {
        -str _file_path
        -TextIOWrapper _file
        +setup()
        +cleanup()
        +get_next_instruction(expected_instruction_type) InputInstruction
        +ensure_file_open() TextIOWrapper
    }

    class PygameInputParser {
        -list~InputInstruction~ _gui_input_buffer
        +get_next_instruction(expected_instruction_type) InputInstruction
        +gui_callback(button_type, data)
        +logic_error_raised(exception)
    }

    class Plateau {
        -list~Rover~ _rovers
        -PlateauSize _size
        +set_dimensions(size)
        +add_rover(rover_start)
        +move_rover(instruction)
        +to_output_data() OutputData
        -_is_within_bounds(position) bool
    }

    class Rover {
        +Position position
        +CompassDirection direction
        +act(instruction)
        +to_output_data() RoverData
        -_move()
        -_turn_left()
        -_turn_right()
    }

    class OutputWriter {
        <<abstract>>
        +write(data)
        +setup()
        +cleanup()
    }

    class ConsoleOutputWriter {
        +write(data)
    }

    class PygameOutputWriter {
        -OutputData _previous_output_data
        -Surface _canvas
        -TextInput _plateau_size_input
        +setup()
        +write(data)
        +handle_event(event)
        +button_click_callback(click_position) ButtonData
        -_write_create_plateau_screen()
        -_write_plateau_grid(data)
    }

    class PygameObject {
        <<abstract>>
        +is_clicked(click_position) bool
        +draw(canvas)
        +handle_event(event)
    }

    class Button {
        +Rect shape
        +str label
        +is_clicked(click_position) bool
        +draw(canvas)
        +handle_event(event)
    }

    class TextInput {
        +Rect rect
        +str text
        +is_clicked(click_position) bool
        +draw(canvas)
        +handle_event(event)
    }

    class InputInstruction {
        +InstructionType type
        +Any data
    }

    class OutputData {
        +PlateauSize plateau_size
        +list~RoverData~ rovers
    }

    class RoverData {
        +Position position
        +CompassDirection direction
    }

    class Position {
        +int x
        +int y
        +copy() Position
    }

    class Size {
        +int width
        +int height
    }

    class PlateauSize

    class CompassDirection {
        <<enumeration>>
        NORTH
        EAST
        SOUTH
        WEST
    }

    class RoverInstruction {
        <<enumeration>>
        MOVE_FORWARD
        TURN_LEFT
        TURN_RIGHT
        STAY
    }

    class InstructionType {
        <<enumeration>>
        ROVER_START
        PLATEAU_SIZE
        ROVER_INSTRUCTION
        QUIT
        NEXT_ROVER
        NONE
    }

    class ProgramState {
        <<enumeration>>
        INITIALIZING
        GET_PLATEAU_SIZE
        GET_ROVER_START
        GET_ROVER_INSTRUCTION
        ERROR
        EXIT
    }

    class ButtonData {
        +ButtonType type
        +Any data
    }

    class ButtonType {
        <<enumeration>>
        PLATEAU_SIZE
        NEW_ROVER
    }

    class MarsRoverException {
        <<exception>>
    }

    class RoverLeftPlateauException {
        +PlateauSize plateau_size
        +Position position
    }

    class ProgramEndException {
        <<exception>>
    }

    class InvalidInputException {
        <<exception>>
    }

    class InvalidPlateauInputException {
        <<exception>>
    }

    class InvalidRoverInputException {
        <<exception>>
    }

    class InvalidMovementInputException {
        <<exception>>
    }

    LayerCoordinator --> InputParser : reads instructions from
    LayerCoordinator *-- Plateau : owns
    LayerCoordinator --> OutputWriter : sends output to
    LayerCoordinator --> ProgramState : controls state with

    InputParser <|-- ConsoleInputParser
    InputParser <|-- FileInputParser
    InputParser <|-- PygameInputParser
    InputParser --> InputInstruction : produces
    InputParser --> PlateauSize : parses
    InputParser --> RoverData : parses
    InputParser --> RoverInstruction : parses

    Plateau *-- "0..*" Rover : contains
    Plateau *-- PlateauSize : has dimensions
    Plateau --> RoverInstruction : applies
    Plateau --> OutputData : creates
    Plateau ..> RoverLeftPlateauException : raises

    Rover *-- Position : has
    Rover --> CompassDirection : faces
    Rover --> RoverInstruction : executes
    Rover --> RoverData : creates

    OutputWriter <|-- ConsoleOutputWriter
    OutputWriter <|-- PygameOutputWriter
    OutputWriter --> OutputData : writes
    PygameOutputWriter *-- TextInput : owns
    PygameOutputWriter *-- Button : owns
    PygameOutputWriter --> ButtonData : returns

    PygameObject <|.. Button
    PygameObject <|.. TextInput
    Button --> ButtonType : represents
    ButtonData --> ButtonType : identifies
    ButtonData --> PlateauSize : may contain
    PygameInputParser --> ButtonType : handles

    InputInstruction --> InstructionType : identifies
    InputInstruction --> RoverData : may contain
    InputInstruction --> PlateauSize : may contain
    InputInstruction --> RoverInstruction : may contain

    OutputData *-- PlateauSize
    OutputData *-- "0..*" RoverData
    RoverData *-- Position
    RoverData --> CompassDirection

    PlateauSize --|> Size

    RoverLeftPlateauException --|> MarsRoverException
    ProgramEndException --|> MarsRoverException
    InvalidInputException --|> MarsRoverException
    InvalidPlateauInputException --|> InvalidInputException
    InvalidRoverInputException --|> InvalidInputException
    InvalidMovementInputException --|> InvalidInputException
```

## Layer overview

- **Coordinator:** `LayerCoordinator` drives the state machine and connects
  input, domain logic, and output.
- **Input layer:** `InputParser` defines the adapter contract; console, file,
  and Pygame implementations convert external input into `InputInstruction`.
- **Logic layer:** `Plateau` owns the active rovers and enforces bounds and
  collision rules; `Rover` applies movement instructions.
- **Output layer:** `OutputWriter` defines the rendering contract. The console
  and Pygame writers consume `OutputData`.
- **Common model:** value/data objects (`Position`, `Size`, `PlateauSize`,
  `RoverData`, `InputInstruction`, `OutputData`) and enums are shared across
  layers.
