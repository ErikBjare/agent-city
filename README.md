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
pip install pygame>=2.5.0
```

### Running the Game
```bash
PYTHONPATH=. python src/main.py
```

## Project Structure
```text
src/
├── __init__.py           # Package initialization
├── main.py              # Main game entry point
├── engine/              # Core game engine
│   ├── __init__.py
│   ├── game.py         # Main game loop and setup
│   └── time_system.py  # Day/night cycle and scheduling
├── entities/            # Game entities
│   ├── __init__.py
│   ├── agent.py        # Agent class with needs and behavior
│   └── building.py     # Building types and interactions
├── world/              # World components
│   ├── __init__.py
│   └── city.py        # City management and layout
└── ai/                 # AI and decision making
    ├── __init__.py
    ├── brain.py       # Agent decision making
    └── needs.py       # Need system
```

## Next Steps

### Debug and Fix
- [x] Fix window display issues
- [ ] Add error handling and logging
- [ ] Implement proper cleanup on exit

### Basic Improvements
- [ ] Add collision detection between agents
- [ ] Implement proper pathfinding
- [ ] Add more visual feedback for agent states

### Enhanced Features
- [ ] Add more building types
- [ ] Implement agent relationships
- [ ] Add day/night cycle effects

### UI and Visualization
- [ ] Add proper UI elements
- [ ] Implement agent inspection window
- [ ] Add city statistics display
- [ ] Building management interface
- [ ] City planning tools
- [ ] Statistics and graphs
- [ ] Better graphics and animations
- [ ] Path visualization
- [ ] Mood indicators
- [ ] Building occupancy visualization

### Advanced AI Integration
- [ ] Integration with LLMs for complex agent behavior
- [ ] Memory and learning from past experiences
- [ ] Social relationships between agents

### Extended City Features
- [ ] More building types (offices, schools, shops)
- [ ] Public transportation system
- [ ] Weather system affecting agent behavior
- [ ] Dynamic city growth

### Agent Customization
- [ ] Personality traits affecting decisions
- [ ] Jobs and daily routines
- [ ] Relationships and social networks
- [ ] Personal preferences for activities

### Simulation Features
- [ ] Economy system
- [ ] Resource management
- [ ] Events and celebrations
- [ ] Customizable schedules

### Technical Improvements
- [ ] Pathfinding optimization
- [ ] Multi-threading for better performance
- [ ] Save/load system

## Contributing

This is an early prototype. Feel free to open issues or submit pull requests.

## License

MIT License
