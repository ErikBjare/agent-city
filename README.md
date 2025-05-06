# Agent City

A 2D simulation of a city populated by AI-driven agents using Pygame. Agents have needs, make decisions, and interact with various buildings in a day/night cycle.

## Features

- AI-driven agents with individual needs (energy, hunger, social)
- Dynamic decision making based on needs and time of day
- Day/night cycle with scheduled events
- Different building types (houses, restaurants, parks)
- Agent visualization with personality colors and need indicators
- Debug mode for monitoring agent states
- City statistics
- Interactive time control

## Controls

- **Space**: Toggle simulation speed (1x/3x)
- **D**: Toggle debug information
- **S**: Toggle city statistics
- **Click**: Send nearest agent to clicked location

## Agent Behavior

Agents make decisions based on:
- Their current needs (energy, hunger, social)
- Time of day
- Available buildings
- Schedule events

### Need System
- Energy: Depletes over time, restored by sleeping in houses
- Hunger: Depletes faster, restored at restaurants
- Social: Depletes slowly, improved at parks and restaurants

### Daily Schedule
- 6:00 - Wake up time
- 12:00 - Lunch time (some agents visit restaurants)
- 22:00 - Bedtime (agents return home)

## Building Types

- **Houses**: Restore energy (sleep)
- **Restaurants**: Satisfy hunger
- **Parks**: Improve social needs

## Development

### Requirements
```bash
pip install -r requirements.txt
```

### Running the Game
```bash
python src/main.py
```

## Project Structure
```text
src/
├── __init__.py
├── main.py                 # Main game entry point
├── engine/                 # Core game engine
│   ├── __init__.py
│   ├── game.py            # Main game loop and setup
│   ├── renderer.py        # Rendering utilities
│   └── time_system.py     # Day/night cycle and scheduling
├── entities/              # Game entities
│   ├── __init__.py
│   ├── agent.py          # Agent class with needs and behavior
│   └── building.py       # Building types and interactions
├── world/                 # World components
│   ├── __init__.py
│   ├── city.py           # City management and layout
│   └── location.py       # Location utilities
└── ai/                    # AI and decision making
    ├── __init__.py
    ├── brain.py          # Agent decision making
    ├── needs.py          # Need system
    └── schedule.py       # Schedule management
```

## Future Enhancements

1. **Advanced AI Integration**
   - Integration with LLMs for more complex agent behavior
   - Memory and learning from past experiences
   - Social relationships between agents

2. **Extended City Features**
   - More building types (offices, schools, shops)
   - Public transportation system
   - Weather system affecting agent behavior
   - Dynamic city growth

3. **Enhanced Visualization**
   - Better graphics and animations
   - Path visualization
   - Mood indicators
   - Building occupancy visualization

4. **Agent Customization**
   - Personality traits affecting decisions
   - Jobs and daily routines
   - Relationships and social networks
   - Personal preferences for activities

5. **Simulation Features**
   - Economy system
   - Resource management
   - Events and celebrations
   - Customizable schedules

6. **UI Improvements**
   - Agent inspection window
   - Building management interface
   - City planning tools
   - Statistics and graphs

7. **Technical Improvements**
   - Pathfinding optimization
   - Multi-threading for better performance
   - Save/load system
   - Mod support
