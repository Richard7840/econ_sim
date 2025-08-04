# **Technical Design Document: Python Prototype**

## **1\. Core Architecture**

This section defines the high-level structure of the application. The goal is to separate the game's logic from its presentation, which makes the code easier to manage, test, and expand.  
**Decision:** A **Model-View-Controller (MVC)** architecture will be used.

* **Model:** Contains all the raw data and game logic (e.g., calculating GDP, processing turn events). It will be a collection of Python classes like Nation, Industry, Technology, etc.  
* **View:** The user interface. For this prototype, it will be a text-based command-line interface responsible for displaying data from the Model.  
* **Controller:** Acts as the intermediary. It will take user input from the command line and tell the Model what to do, then trigger the View to refresh.

## **2\. Game State Management**

The "Game State" is the complete snapshot of the game at any given moment.  
**Decision:**

* The state will be stored in a **single, large GameState object**. This object will hold all other data models (e.g., a list of Nation objects, the current turn number, etc.), making it easy to pass the entire state around and to save/load the game.  
* Changes to the state will be handled via **direct mutation** (e.g., player.treasury \-= 100). This is simple, fast, and sufficient for the prototype.

## **3\. Data Structures (Class Design)**

This defines the "nouns" of our game in code.  
**Initial Class Structure:**

* Game: The main class that holds the game state and runs the game loop.  
* Nation: Represents a player or AI faction. Holds resources, lists of industries, known technologies, etc.  
* Industry: Represents a specific industry, with attributes like level, production\_output, etc.  
* Technology: Represents a single tech in the tree, with attributes like name, rp\_cost, and is\_researched.  
* ComponentDesign: Represents a piece of equipment, storing its stats and any woven runes.  
* Rune: A simple data class for AethericWeaving and CivicGlyphs.  
* Unit: Represents a military unit, containing a list of its equipped ComponentDesigns.

**Data Loading:**

* All static game data (technologies, base industry stats, events) will be loaded from **external JSON files** (e.g., data/technologies.json). This keeps game design data separate from the engine code, allowing for easier balancing and modification.

## **4\. UI Framework (The View)**

**Decision:** The prototype will use a **Text-Based / Command-Line Interface (CLI)**.

* This approach minimizes UI development time, allowing 100% of the focus to be on implementing and testing the core game mechanics.  
* Libraries like Python's built-in input() and print() will be sufficient, potentially enhanced with a library like rich for better formatting if needed.

## **5\. Persistence (Saving & Loading)**

**Decision:** Game state will be saved to and loaded from **JSON files**.

* While this requires writing custom serialization/deserialization logic for our classes, the benefit of having human-readable save files for debugging and manual editing is invaluable for a prototype.

## **6\. Implementation Details**

This section covers the "how-to" of the codebase, defining project structure and core processes.

### **6.1. The Game Loop**

The heart of the Game class will be a run() method that contains the main loop.  
**Turn Sequence:**

1. **Start of Turn Phase:** Increment turn counter and process start-of-turn events.  
2. **Player Action Phase:** Display game state (View) and wait for player input (Controller) until the player ends their turn.  
3. **AI Action Phase:** Iterate through each AI Nation and execute their decision-making logic.  
4. **End of Turn Phase (Resolution):** This is where the simulation happens in a specific order:  
   * *Step 1: Production.* Calculate resource generation, IC output.  
   * *Step 2: Research.* Add RP to projects, check for completions.  
   * *Step 3: Economy.* Calculate GDP growth, tax revenue, update treasuries.  
   * *Step 4: Global Meters.* Update Crisis Awareness and Social Dissonance.  
   * Loop back to the Start of Turn Phase.

### **6.2. Project Structure**

A clean folder structure is essential for keeping the project organized.  
**Directory Layout:**  
defense\_econ\_game/  
│  
├── run\_game.py           \# Main entry point to start the game  
├── requirements.txt      \# List of external libraries  
│  
├── data/                 \# Game design data (JSON files)  
│   ├── technologies.json  
│   ├── industries.json  
│   └── events.json  
│  
├── saves/                \# For saved game files  
│   └── savegame1.json  
│  
└── src/                  \# The main source code  
    ├── \_\_init\_\_.py  
    │  
    ├── models/           \# Core data classes (the "M" in MVC)  
    │   ├── game\_state.py  
    │   ├── nation.py  
    │   └── ...  
    │  
    ├── view/             \# UI-related code (the "V" in MVC)  
    │   ├── cli\_view.py  
    │  
    └── controller/       \# Input handling and logic mediation (the "C" in MVC)  
        ├── game\_controller.py  
        └── ai\_controller.py

### **6.3. AI Decision Making**

The prototype AI will be functional but simple.  
**Decision: Simple Rule-Based AI**

* The ai\_controller will use a straightforward set of "if-then" rules to make decisions, such as prioritizing research if a slot is open or building a new industry if its treasury is high. This is predictable, easy to implement, and sufficient for testing the core game systems.

### **6.4. Logging**

A logging system is crucial for debugging.  
**Decision: Use Python's built-in logging module.**

* It will be configured to print high-level INFO messages (e.g., "Turn 5: Player researched Fusion Power.") to the console, and detailed DEBUG messages (e.g., calculation breakdowns) to a log file for deeper analysis.
