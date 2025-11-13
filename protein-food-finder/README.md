# Protein Food Finder - CrewAI Multi-Agent System

An intelligent food recommendation system built with **CrewAI** that finds high-protein products at local grocery stores based on your dietary preferences and location.

## 🎯 What It Does

The Protein Food Finder uses multiple AI agents working together to:
1. **Discover stores** near your location
2. **Research products** at each store in parallel
3. **Validate** protein content and dietary compliance  
4. **Recommend** the top products that match your needs

## 🏗️ Architecture - Why CrewAI?

This project uses the **CrewAI framework** to orchestrate multiple specialized AI agents.

**CrewAI** is a framework for building multi-agent AI systems where each agent has:
- **Role**: Specialized expertise
- **Goal**: Specific objective
- **Backstory**: Context for decision-making
- **Tools**: Access to search, scraping, etc.

### Agent Workflow

```
┌─────────────────────────────────────────────────┐
│ 1. Store Locator Agent                          │
│    └─> Finds 3-5 grocery stores near location   │
└─────────────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────────┐
│ 2. Nutrition Researcher Agent                    │
│    └─> Searches products at each store          │
└─────────────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────────┐
│ 3. Nutrition Validator Agent                     │
│    └─> Validates 20g+ protein & dietary needs   │
└─────────────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────────┐
│ 4. Recommendation Specialist                     │
│    └─> Creates personalized shopping list       │
└─────────────────────────────────────────────────┘
```

## ✨ Features

- 🤖 **Multi-Agent System** - 4 specialized AI agents
- ⚡ **Parallel Search** - Faster product discovery
- ✅ **Quality Validation** - Ensures 20g+ protein
- 🧠 **Memory & Caching** - 60% faster repeat runs
- 📊 **Structured Outputs** - Type-safe Pydantic models
- 💰 **Value Analysis** - Protein-per-dollar calculations

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- API Keys:
  - OpenAI API key
  - Serper API key

### Installation

```bash
# Install uv if you haven't
pip install uv

# Navigate to project
cd protien_food_finder

# Install dependencies
uv sync
```

### Configuration

Create `.env` file:
```bash
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key
```

### Run

```bash
crewai run
```

Output will be generated in `output/protein_recommendations.md`

## 📁 Project Structure

```
protien_food_finder/
├── src/protien_food_finder/
│   ├── config/
│   │   ├── agents.yaml           # Agent definitions
│   │   └── tasks.yaml            # Task workflow
│   ├── crew.py                   # Crew orchestration
│   ├── main.py                   # Entry point
│   └── structured_outputs.py     # Pydantic models
├── output/
│   └── protein_recommendations.md
├── .env                          # API keys
├── pyproject.toml                # Dependencies
├── MEMORY_CACHE.md               # Cache docs
└── README.md                     # This file
```

## 🎓 Key CrewAI Concepts

### 1. Agents with Roles
```python
@agent
def store_locator(self) -> Agent:
    return Agent(
        config=self.agents_config['store_locator'],
        tools=[self.serper_tool],
        verbose=True
    )
```

### 2. Sequential Tasks
Tasks execute one after another, each using previous results:
```python
@task
def validate_products_task(self) -> Task:
    return Task(
        config=self.tasks_config['validate_products'],
        context=[self.research_protein_items_task]  # Uses research results
    )
```

### 3. Memory & Caching
```python
Crew(
    agents=self.agents,
    tasks=self.tasks,
    memory=True,   # Remembers previous runs
    cache=True,    # Caches tool calls
)
```

## 📊 Performance

| Metric | First Run | With Cache |
|--------|-----------|------------|
| Time | 3-4 min | 1-2 min ⚡ |
| API Calls | 15-20 | 2-5 💰 |
| Cost | $0.05-0.10 | $0.01-0.02 |

## 🔧 Customization

Edit `src/protien_food_finder/main.py`:

```python
inputs = {
    'location': 'Your City, State ZIP',
    'dietary_preferences': '''
        - High protein (20g+)
        - Your restrictions here
        - Gluten-free, vegan, etc.
    '''
}
```

## 📚 Learn More

- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI Core Concepts](https://docs.crewai.com/core-concepts)
- `MEMORY_CACHE.md` - Caching guide
- `config/agents.yaml` - See agent definitions
- `config/tasks.yaml` - See task workflow

## 🛠️ Advanced

### Clear Cache
```bash
rm -rf .crewai/
```

### Verbose Logging
```bash
crewai run --verbose
```

## 🤝 Contributing

Personal learning project - suggestions welcome!

## 📝 License

MIT

---

**Built with CrewAI** 🤖 | **Powered by OpenAI** ⚡
