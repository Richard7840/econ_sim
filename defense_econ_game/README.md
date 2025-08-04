# Defense Economics Game Prototype

This is a turn-based economic and strategic simulation game prototype, built as a command-line interface (CLI) application in Python. It follows a Model-View-Controller (MVC) architecture to separate game logic, user interface, and input handling.

## Project Structure

```bash
defense_econ_game/
├── run_game.py           # Main entry point to start the game
├── requirements.txt      # List of external libraries (currently empty)
│  
├── data/                 # Game design data (JSON files)
│   ├── technologies.json  # Defines available technologies and their effects
│   ├── industries.json    # Defines industry types, their base profitability, and level bonuses
│   └── events.json        # Defines game events and their triggers/effects
│  
├── saves/                # For saved game files (not yet implemented)
│  
└── src/                  # The main source code
    ├── __init__.py
    │  
    ├── models/           # Core data classes (the "M" in MVC)
    │   ├── game_state.py  # Manages the overall game state (turn, nations, etc.)
    │   ├── nation.py      # Represents a player or AI faction, manages resources, industries, and research
    │   ├── industry.py    # Defines industry attributes (IC, profitability, levels, bonuses)
    │   ├── technology.py  # Defines technology attributes (cost, progress, unlocks)
    │   ├── event.py       # Defines event attributes (trigger, effects)
    │   ├── component_design.py # Placeholder for unit components (not yet implemented)
    │   ├── rune.py        # Placeholder for magical runes (not yet implemented)
    │   └── unit.py        # Placeholder for military units (not yet implemented)
    │  
    ├── view/             # UI-related code (the "V" in MVC)
    │   ├── cli_view.py    # Handles displaying game state to the command line
    │  
    └── controller/       # Input handling and logic mediation (the "C" in MVC)
        ├── game_controller.py # Handles player input and translates to game actions
        └── ai_controller.py   # Placeholder for AI decision-making (not yet implemented)
```

## How to Run the Game

1. Navigate to the `defense_econ_game` directory in your terminal.
2. Run the main game script:

    ```bash
    python run_game.py
    ```

## Current Game Flow & Mechanics

* **Turn-Based:** The game progresses in turns. Each turn, the player makes decisions, and then the game simulates economic activity, research progress, and checks for events.
* **Resources:**
  * **Treasury:** Government funds, gained from industry profits.
  * **Industrial Capacity (IC):** Represents manufacturing capability. Divided into Government IC and Private IC.
  * **Research Points (RP):** Used for technology research.
  * **Public Opinion:** Placeholder, not yet actively used.
* **Industries:**
  * Players start with Tier 1 industries.
  * Industries have `government_ic` and `private_ic` components.
  * `profitability` is calculated based on `base_profitability`, `tax_rate`, and `subsidy_per_ic`.
  * **Investment:** Players can invest treasury to increase an industry's `government_ic`.
  * **Leveling:** Industries level up automatically when their total IC reaches certain thresholds (geometric progression). Leveling increases `profitability`.
  * **Private Reinvestment:** A portion of private industry profits is automatically reinvested into industries based on their profitability.
* **Research:**
  * Players can choose a technology to research.
  * Research progresses each turn based on `Research Points` and `effective_research_points` (which can be boosted by certain industry levels).
  * Researching technologies can unlock new industries.
* **Policy Levers:**
  * **Tax Breaks:** Players can reduce the tax rate on an industry, increasing its effective profitability for private IC.
  * **Subsidies:** Players can provide direct treasury payments to an industry, increasing its effective profitability for private IC.
* **Crisis Awareness:** Increases based on total industrial capacity. Triggers events when thresholds are met.
* **CLI Interface:** All interactions are currently text-based via the command line. Actions can be selected using single-letter commands (e.g., `E` for End turn, `R` for Research).

## Future Development (Based on Design Documents)

* Fleshing out Crisis mechanics and Social Dissonance.
* Implementing Design Projects and Retrofit Projects for R&D.
* Developing the Events & Expeditions system.
* Implementing AI for rival nations.
* Adding persistence (save/load game functionality).
* Developing Modular Unit Construction and Combat systems.
* Implementing Magical Doctrine (Aetheric Weaving) and Social Doctrine (Civic Glyphs).
* Building out Espionage & Intelligence systems.
* Implementing Geopolitics, Trade, & Procurement.
