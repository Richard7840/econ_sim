# **Prototype Defense Economics Game: Specification Document**

## **1\. Game Overview**

### **1.1. High-Concept**

A turn-based economic and strategic simulation set in a post-apocalyptic, magic-infused future. The player leads a fledgling city-state, managing its economy and military to survive and thrive against rival human factions and a hostile, awakened planetary intelligence known as the "Crisis."

### **1.2. Core Theme**

The game explores humanity's struggle for survival and meaning in a world of its own making. It combines the classic "Guns vs. Butter" dilemma with a "Man vs. Nature" conflict, forcing players to balance industrial growth, military necessity, and the ecological/magical consequences of their actions.

### **1.3. Setting & Factions**

* **The World:** A century after a global war of resource scarcity and climate collapse ended in nuclear fire, an ancient, eldritch power within the Earth has awakened. This entity, the source of a new and volatile magic, seeks to reclaim the planet. Humanity exists in scattered enclaves, possessing modern technological knowledge but lacking the industrial base to wield it properly.  
* **The Crisis:** The primary antagonist is the planet's awakened consciousness and its magical ecosystem. It acts as a scaling, game-wide threat, periodically releasing monstrous beasts and causing ecological disasters.  
* **Factions:** Players and AI nations represent different human ideologies on how to confront the Crisis, shaping their unique tech trees, victory conditions, and diplomatic stances.

### **1.4. Player Goal & Victory Conditions**

* **Primary Goal:** Ensure the survival and sovereignty of your people. This requires out-scaling the growing Crisis threat by building a robust economy, advancing technologically, and fielding a capable military, as well as collaborating with AI nations to cover each other’s weaknesses.  
* **Victory Conditions:** Tied to faction ideology, all victory conditions revolve around resolving the Crisis.  
  * *Example (Radical Naturalist Faction):* Learn to coexist with the Crisis as a part of nature by eliminating anti-Crisis factions and abandoning anti-environmental industry. Can cooperate with the Crisis.  
  * *Example (Militarist Faction):* Construct a superweapon to destroy the Crisis's central nexus. Take advantage of both previous human industry, as well as new magical technologies to retake the Earth and return to the status quo with Humans on top.  
  * *Example (Escape Faction):* Build a colony ship to escape Earth and create a self-sustaining colony on another planet.  
* **Losing Condition:** Military defeat of your capital city-state by a rival faction or the Crisis. Economic stagnation is a slow death, leaving you vulnerable to being out-scaled and conquered.

### **1.5. The Crisis & Awareness Meter**

The player's relationship with the primary antagonist is managed through a core mechanic: the **Crisis Awareness Meter**. This is not a resource, but a measure of how threatening the planet perceives your civilization to be.

* **Baseline Growth:** The Crisis's overall power grows steadily over time, representing the planet's slow healing and reclamation. This creates a soft pressure on all factions to keep pace.  
* **Raising Awareness:** The player's meter increases through:  
  * **Industrial Pollution:** Aggressive, unregulated industry that damages the ecosystem.  
  * **Aetheric Disruption:** Designing and using highly unstable magical equipment.  
  * **Social Dissonance:** Employing powerful, unnatural magic to influence your own society (see 4.4).  
* **Consequences:** A higher Awareness meter leads to more frequent, more powerful, and more intelligent attacks from Crisis beasts on your territory and expeditions.  
* **Managing Awareness:** The player can lower their Awareness by investing in ecological restoration projects, choosing low-impact industries, and researching technologies that harmonize with nature. This creates a central strategic choice: advance recklessly for short-term power, or grow carefully to avoid unwanted attention.

## **2\. Core Gameplay Loop**

The game proceeds in turns. Each turn represents one year.

1. **Start of Turn:**  
   * Receive economic/political summary (GDP growth, tax revenue, budget report).  
   * Trigger random or scripted **Events & Expeditions**.  
2. **Action Phase:**  
   * Player makes key decisions for the year:  
     * **Budget Allocation:** Distribute government funds.  
     * **Policy Levers:** Adjust taxes, regulations, and subsidies to influence the private sector.  
     * **Government Production:** Queue state-run construction.  
     * **Research & Development:** Assign RP to Technology Trees, Design Projects, and Retrofit Projects.  
     * **Civic Glyphs:** Slot or change the active Civic Runes for your government.  
     * **Intelligence:** Assign your intelligence agency to a mission.  
3. **End of Turn:**  
   * Simulate the year's economic activity based on player choices.  
   * Calculate results: economic growth, production output, research progress, changes to global meters.  
   * Present end-of-turn report.

## **3\. Economic Engine**

### **3.1. Key Resources**

* **Treasury (£):** Government funds.  
* **Industrial Capacity (IC):** Manufacturing capability.  
* **Research Points (RP):** For technology and design.  
* **Public Opinion (%):** Population's satisfaction.

### **3.2. Government & Private Sectors**

* **Government Sector (Direct Control):** The player has direct control over the state's budget and actions.  
  * **Income:** Taxation, State-Owned Enterprise (SOE) revenue.  
  * **Expenditures:** Social Spending, Infrastructure, R\&D, Military Procurement, SOE Investment.  
* **Private Sector (Indirect Influence):** The private economy is an autonomous engine that the player guides, but does not directly command.  
  * **GDP & Growth:** The private sector's total value. It grows based on its own profitability and reinvestment.  
  * **Autonomous Investment:** Private capital automatically flows towards the most profitable industries. The player's goal is to make strategically important industries more attractive.  
  * **Levers of Influence:**  
    * **Subsidies/Tax Breaks:** Reduce costs for a target industry, increasing its profitability and attracting private investment.  
    * **Government Contracts:** Issuing large orders for specific goods creates demand, boosting that industry's profitability.  
    * **Infrastructure:** Better infrastructure lowers costs for specific industries, making them more competitive.

### **3.3. Industry & Specialization**

Industries are the backbone of the economy. Specializing provides significant competitive advantages.

* **Industry Level:** Each industry has a level that increases with accumulated production.  
* **Benefits of Leveling:** Unlocks efficiency gains, powerful national bonuses, and research boosts for related fields. A key way to gain stat increases without relying on flat tech bonuses.  
* **Example Industry Tiers:**  
  * **Tier 1:** Food Production, Ore Mining, Lumber Mills, **Ley Line Tapping**.  
  * **Tier 2:** Metal Refineries, Polymer Plants, Basic Electronics Fab, **Aetheric Distilleries**.  
  * **Tier 3:** Advanced Machinery, Vehicle Assembly, Aerospace Plant, **Golem Foundries**.  
  * **Tier 4:** AI Development, Nanotechnology, Bio-Engineering, **Arcane Synthesis**.

### **3.4. Global Meters**

* **Crisis Awareness:** How hostile the Crisis is towards you.  
* **Social Dissonance:** A measure of societal instability caused by magical manipulation. High dissonance can trigger negative internal events (cults, paranoia, magical plagues) and increases Crisis Awareness.

## **4\. Research, Design, & Doctrines**

### **4.1. The R\&D Pipeline**

Technology, design, and production are distinct but sequential steps.

1. **Technology Research:** The player invests RP into three main tech trees (Industry, Society, Magic). Unlocking a technology does **not** grant a new unit or a flat bonus. Instead, it unlocks new **mechanics** or new **Design Projects**.  
2. **Design Projects:** To create a new component from scratch. The player invests RP into designing a specific **component** (e.g., the "Helios-I Power Core"). This is the most expensive and time-consuming option but offers the highest performance potential.  
3. **Retrofit Projects:** To upgrade existing equipment. The player invests a smaller amount of RP to adapt an existing, obsolete component to use newer technologies. This is cheaper and faster than a new design but results in lower performance than a purpose-built component.  
4. **Equipment Production:** Once a design (new or retrofitted) is complete, it can be manufactured by industries and equipped onto military units.

### **4.2. Tech Trees**

* **Industry Tree:** Focuses on economic efficiency, unlocking new tiers of industry, advanced resource extraction, and mass production techniques.  
* **Society Tree:** Unlocks new policies, diplomatic options (e.g., increasing alliance count), and methods for boosting public opinion and research output.  
* **Magic Tree:** Focuses on understanding and manipulating the world's new magical properties. Unlocks new "Runes" and "Weaving Patterns" for the Aetheric Weaving system.

### **4.3. Magical Doctrine: Aetheric Weaving**

This is the core mechanic for magic in equipment, a system of high-risk, high-reward enchantment.

* **Runes & Glyphs:** The Magic tech tree unlocks powerful runes that can be woven into equipment during the design phase.  
* **Aetheric Stress:** Instead of pure randomness, unstable runes add to a unit's **Aetheric Stress** capacity. In combat, using abilities tied to these runes fills up a Stress bar.  
* **Overload Effects:** If the Stress bar exceeds the unit's capacity, it "overloads," triggering negative effects. The further over the limit, the more severe the consequences.  
  * *Minor Overload:* Temporary weapon debuff, minor self-damage.  
  * *Major Overload:* Unit is stunned for a turn, weapon disabled, major self-damage.  
  * *Critical Overload:* Permanent component destruction, temporary mind-control by the Crisis, self-destruct.  
* **Weaving Patterns:** Advanced magic research unlocks "Weaving Patterns"—ways to combine specific runes that increase a unit's Stress capacity, allowing for more aggressive use of powerful magic before overloading.

### **4.4. Social Doctrine: Civic Glyphs**

This is the core mechanic linking the Magic and Society systems, inspired by policy card systems. It allows the player to magically influence their society, balancing powerful buffs with societal instability.

* **Civic Capacity:** Your government has a **Civic Capacity** limit (measured in "pips"). This represents how much magical influence your society can bear without fracturing. This limit can be increased through the Society tech tree and by completing major national milestones.  
* **Civic Runes:** The Magic and Society tech trees unlock Civic Runes, each with a specific **pip cost** and a **conditional buff**. Stronger, more universally applicable runes have a higher cost.  
  * *Example 1 (Low Cost):* **Rune of Frugal Ingenuity (2 pips):** "+15% RP towards technologies you are behind the global average in."  
  * *Example 2 (High Cost):* **Rune of the Forgeheart (5 pips):** "For every 2 levels in your Metal Refineries industry, all armored units gain \+1% armor."  
  * *Example 3 (Faction-Specific):* **Rune of Natural Harmony (3 pips):** "(Naturalist Faction Only) Ecological restoration projects are 50% cheaper and reduce Crisis Awareness twice as fast."  
* **Staying Under Capacity:** If the total pip cost of your slotted runes is at or below your Civic Capacity, the system is stable. You gain all the benefits with minimal downside, though a low chance for minor negative events may persist.  
* **Exceeding Capacity \- The Dissonance Cost:** For every pip you are over your Civic Capacity, you generate a scaling amount of **Social Dissonance** each turn.  
* **Dissonance Amplification (Potential Mechanic):** A late-game technology could be researched that increases the effectiveness of all slotted Civic Runes for every point of Social Dissonance being generated, creating a high-risk, high-reward "desperation" strategy.

### **4.5. Espionage & Intelligence**

A lightweight system for information warfare, funded from the Treasury. After researching the "Intelligence Agency" tech, the player can assign it to one mission per turn.

* **Counter-Intelligence:** Reduces the effectiveness of rival intelligence operations and provides a chance to identify which nation is targeting you.  
* **Monitor Rival:** Gather intelligence on a target nation, potentially revealing their production numbers, Crisis Awareness level, true equipment stats, or active research. Provides a research bonus for techs they have that you don't.  
* **Analyze Crisis:** Focus intelligence efforts inward, attempting to predict the timing and nature of the next major Crisis attack and providing a small, temporary reduction to your own Crisis Awareness meter.

## **5\. Events & Expeditions**

Events will frequently generate opportunities for small-scale military action outside of major wars. These are optional missions that allow players to test unit designs and gain valuable rewards.

* **Triggers:** An ancient ruin uncovered by an earthquake, a Crisis beast nesting near a vital resource, a convoy of independent scavengers with rare tech. Triggers can be tied to the Crisis Awareness meter.  
* **Deployment:** The player assigns a small, pre-defined force (e.g., one infantry platoon, one armored vehicle) to the expedition.  
* **Rewards:** Success can yield unique component designs, bonus RP, rare resources, boosts to an industry's level, or intelligence on rival factions. Failure can result in the loss of the units and potentially angering a neutral party.

## **6\. Military & Combat**

### **6.1. Modular Unit Construction**

Military units are assembled from components, allowing for immense customization.

1. **Select Chassis:** The player chooses a base unit template (e.g., "Tracked Light Armor Chassis," "Powered Infantry Suit," "Aerospace Fighter Frame"). The chassis determines base stats like speed, armor slots, and available hardpoints.  
2. **Assign Equipment:** The player fills the chassis's slots with designed components from their available list (produced locally or imported).  
   * *Example Light Tank:*  
     * **Chassis:** Tracked Light Armor  
     * **Main Weapon:** 45mm Autocannon (High rate of fire, low damage)  
     * **Engine:** Helios-I Power Core (High speed, adds 20 to Stress Capacity)  
     * **Armor:** Composite Plating (Standard protection)  
     * **Special:** "Rune of Invisibility" woven into the power core.  
3. **Finalize Unit:** The final unit's stats, cost, and role are determined by the sum of its parts. This allows a single chassis type to be adapted for wildly different roles (e.g., a scout, a tank destroyer, an anti-infantry platform).

### **6.2. Geopolitics, Trade, & Procurement**

* **Tactical Combat:** The types and quantity of units produced by the economic engine, with their specific modular loadouts, will become the forces used in a separate, turn-based tactics game.  
* **Geopolitics:** Economic strength (GDP) and military power will be primary components of diplomatic power.  
* **International Arms Market:** Nations can engage with each other through a dedicated procurement interface, creating a dynamic global market.  
  * **Buying Equipment:** Purchase finished components or entire unit loadouts directly from other nations. This is expensive but provides immediate access to technology you don't have.  
  * **Leasing Designs:** A diplomatic agreement where a nation with high R\&D can lease the production rights for a component to a nation with high industrial capacity. The lessee pays a fee and can then produce the component in their own factories, saving on import costs. This requires a good diplomatic relationship
  