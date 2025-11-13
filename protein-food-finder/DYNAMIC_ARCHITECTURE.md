# Dynamic Architecture Documentation

## Overview

The Protein Food Finder now features a **dynamic, store-based architecture** that automatically adjusts the number of agents based on stores found near your location. This replaces the previous static workflow with a more flexible and resilient system.

## Key Improvements

### 1. **Dynamic Agent Creation**
- **Before:** Fixed set of 4 agents regardless of store availability
- **After:** Creates one specialist agent per discovered store (3-5 agents typically)
- **Benefit:** More targeted search, better product coverage per store

### 2. **Resilient Execution**
- **Before:** If one agent failed, the entire workflow could fail
- **After:** If a store agent fails (e.g., Costco unavailable), continues with other stores
- **Configuration:** `agent_behavior.continue_on_failure: true` in `settings.yaml`

### 3. **Configurable Products Per Store**
- **Before:** Hardcoded search strategy
- **After:** Configurable min/max/default products per store in `settings.yaml`
- **Default:** 5 products per store, adjustable from 3-5 range

### 4. **Parallel Execution Ready**
- **Current:** Sequential execution for proper context flow
- **Future:** Can enable parallel store searches via `agent_behavior.parallel_execution: true`

---

## Architecture Flow

### Phase 1: Store Discovery (Static)
```
┌─────────────────────┐
│  Store Locator      │  1 agent
│  Agent              │
└──────────┬──────────┘
           │
           ▼
    [Find Stores Task]
           │
           ▼
    Parse store names
    (e.g., "Trader Joe's", "Whole Foods", "Costco")
```

### Phase 2: Dynamic Agent Creation
```
For each discovered store:
  ┌──────────────────────────────────────┐
  │  1. Load store_specialist_template   │
  │  2. Replace variables:               │
  │     - {store_name}                   │
  │     - {store_website}                │
  │     - {location}                     │
  │     - {dietary_preferences}          │
  │     - {products_count}               │
  │  3. Create Agent + Task              │
  └──────────────────────────────────────┘
           │
           ▼
    Store-Specific Agent Created
```

**Example:** If 4 stores found → 4 specialist agents created

### Phase 3: Store-Specific Searches (Dynamic)
```
┌──────────────────────┐
│ Trader Joe's Agent   │──→ [Search Task] ──→ 5 products
└──────────────────────┘

┌──────────────────────┐
│ Whole Foods Agent    │──→ [Search Task] ──→ 5 products
└──────────────────────┘

┌──────────────────────┐
│ Costco Agent         │──→ [Search Task] ──→ 5 products
└──────────────────────┘

┌──────────────────────┐
│ Molly Stone's Agent  │──→ [Search Task] ──→ 5 products
└──────────────────────┘
```

**Key Feature:** If Costco search fails, system continues with other 3 stores

### Phase 4: Validation & Recommendations (Static)
```
All Store Results
       │
       ▼
┌──────────────────────┐
│ Nutrition Validator  │──→ Validate all products
│ Agent                │    (20g+ protein, dietary rules)
└──────────┬───────────┘
           │
           ▼
    Validated Products
           │
           ▼
┌──────────────────────┐
│ Recommendation       │──→ Top picks, shopping strategy
│ Specialist Agent     │    Best value, convenience
└──────────────────────┘
           │
           ▼
    Final Report (MD file)
```

---

## Configuration Files

### 1. `config/settings.yaml` (NEW)

Central configuration for dynamic behavior:

```yaml
# Products per store
products_per_store:
  min: 3
  max: 5
  default: 5

# Agent behavior
agent_behavior:
  continue_on_failure: true      # Keep going if store fails
  parallel_execution: true       # Future: search stores in parallel
  max_parallel_agents: 5         # Limit concurrent agents
  timeout_per_agent: 300         # 5 min timeout per store

# Store mappings
stores:
  "Trader Joe's":
    website: "traderjoes.com"
    search_aliases: ["trader joes", "tj's"]
  # ... more stores

# Dietary validation
dietary_validation:
  min_protein_grams: 20
  exclude_keywords: ["beef", "pork", "turkey", "tuna"]
  include_keywords: ["chicken", "fish", "salmon", "shrimp", "eggs", "plant-based"]
  max_sugar_grams: 10
```

### 2. `config/agents.yaml` (Updated)

Added **template agent** for dynamic creation:

```yaml
store_specialist_template:
  role: "{store_name} Protein Products Specialist"
  goal: >
    Find {products_count} high-protein products...
  backstory: >
    Expert researcher specializing in {store_name}...
  llm: gpt-4o-mini
```

**Variables replaced at runtime:**
- `{store_name}` → "Trader Joe's", "Whole Foods", etc.
- `{store_website}` → "traderjoes.com", "wholefoodsmarket.com"
- `{location}` → User's location
- `{dietary_preferences}` → User's dietary rules
- `{products_count}` → From settings (default: 5)

### 3. `config/tasks.yaml` (Updated)

Added **template task** for dynamic creation:

```yaml
store_search_template:
  description: >
    Research {products_count} high-protein products at {store_name}...

    SEARCH STRATEGY:
    1. "{store_name} high protein products 20g"
    2. "site:{store_website} protein 20g"
    ...

  expected_output: >
    List of {products_count} products from {store_name}
  agent: "{store_name}_specialist"
  context:
    - find_stores_task
```

---

## Code Implementation

### Key Methods in `crew.py`

#### 1. `parse_stores_from_output(find_stores_output: str) -> List[str]`
Parses store names from the find_stores task output.

```python
# Input: "1. Trader Joe's - 2.3 miles\n2. Whole Foods - 3.1 miles"
# Output: ["Trader Joe's", "Whole Foods"]
```

#### 2. `create_store_specialist_agent(store_name, location, dietary_preferences) -> Agent`
Dynamically creates a store-specific agent from template.

**Error Handling:**
- If creation fails and `continue_on_failure=true`: Returns `None`, continues
- If creation fails and `continue_on_failure=false`: Raises exception

#### 3. `create_store_search_task(store_name, agent, ...) -> Task`
Dynamically creates a store-specific task from template.

**Context:** Each task depends on `find_stores_task` for location/store info

#### 4. `build_dynamic_crew(location, dietary_preferences) -> Crew`
Main orchestrator that:
1. Runs find_stores task first
2. Parses discovered stores
3. Creates N agents + N tasks (one per store)
4. Adds validation + recommendation agents
5. Returns complete crew ready to execute

**Execution Flow:**
```python
# Step 1: Find stores
initial_crew = Crew(agents=[store_locator], tasks=[find_stores])
result = initial_crew.kickoff()

# Step 2: Parse stores
stores = parse_stores_from_output(result)

# Step 3: Create dynamic agents/tasks
for store in stores:
    agent = create_store_specialist_agent(store, ...)
    task = create_store_search_task(store, agent, ...)

# Step 4: Build complete crew
all_agents = [locator] + dynamic_agents + [validator, recommender]
all_tasks = [find_stores] + dynamic_tasks + [validate, recommend]
return Crew(agents=all_agents, tasks=all_tasks)
```

---

## Running the System

### Dynamic Mode (Default)
```bash
crewai run
```

Set `USE_DYNAMIC_WORKFLOW=true` in `.env` (default)

**What happens:**
1. Finds stores near Belmont, CA
2. Creates 3-5 specialist agents (depending on stores found)
3. Each agent searches its assigned store
4. Validates all products together
5. Generates final recommendations

### Legacy Mode (Fallback)
```bash
# Set in .env:
USE_DYNAMIC_WORKFLOW=false

crewai run
```

Uses static workflow with fixed 4 agents (store_locator, nutrition_researcher, validator, recommender)

---

## Example Execution Log

```
🚀 Starting Protein Food Finder Crew (DYNAMIC mode)
================================================================================
📍 Location: Belmont, CA 94002
🥗 Dietary Preferences: High protein, no beef/pork/turkey/tuna...

🏗️  Building dynamic crew for location: Belmont, CA 94002

📍 Step 1: Finding stores...
[Store locator executes...]

🔍 Step 2: Parsing stores from output...
📍 Parsed 4 stores: ["Trader Joe's", "Whole Foods", "Costco", "Molly Stone's"]

🤖 Step 3: Creating 4 store specialist agents...
✅ Created agent for Trader Joe's
✅ Created agent for Whole Foods
✅ Created agent for Costco
✅ Created agent for Molly Stone's
✅ Created task for Trader Joe's
✅ Created task for Whole Foods
✅ Created task for Costco
✅ Created task for Molly Stone's

📋 Step 4: Building complete workflow with 4 store tasks...

✅ Dynamic crew built:
   - 6 agents (4 store specialists)
   - 6 tasks (4 store searches)

[Execution continues...]
```

---

## Handling Failures

### Scenario 1: Store Agent Creation Fails
```
❌ Failed to create agent for Costco: [Error details]
⏭️  Continuing without Costco
```

**Result:** System continues with 3 other stores

### Scenario 2: Store Task Execution Fails
```
❌ Costco search failed: Timeout
```

**Result:**
- Costco products excluded from validation
- Other 3 stores proceed normally
- Final recommendations based on 3 stores

### Scenario 3: No Stores Found
```
⚠️  No stores found. Falling back to legacy workflow.
```

**Result:** Uses static `nutrition_researcher` agent to search broadly

---

## Performance Characteristics

### Dynamic Workflow
- **Agents:** 3-7 (1 locator + 3-5 store specialists + 1 validator + 1 recommender)
- **Tasks:** 5-9 (1 find_stores + 3-5 store searches + 1 validate + 1 recommend)
- **Execution Time:** ~5-8 minutes (sequential)
- **Product Coverage:** 15-25 products (5 per store)

### Legacy Workflow
- **Agents:** 4 (fixed)
- **Tasks:** 4 (fixed)
- **Execution Time:** ~4-6 minutes
- **Product Coverage:** 15-25 products (mixed stores)

---

## Configuration Examples

### Example 1: Get More Products Per Store
```yaml
# settings.yaml
products_per_store:
  default: 7  # Change from 5 to 7
```

**Result:** 28 products total (7 per store × 4 stores)

### Example 2: Strict Execution (Fail Fast)
```yaml
# settings.yaml
agent_behavior:
  continue_on_failure: false  # Stop if any store fails
```

### Example 3: Add New Store
```yaml
# settings.yaml
stores:
  "Safeway":
    website: "safeway.com"
    search_aliases: ["safeway", "safeway stores"]
```

**Result:** If store locator finds Safeway, agent automatically created

---

## Testing Different Scenarios

### Test with 2 stores:
Edit `find_stores` task to return only 2 stores
```
Expected: 2 specialist agents created
```

### Test with 5 stores:
Ensure store locator returns maximum 5 stores
```
Expected: 5 specialist agents created
```

### Test with failure:
Manually inject error in one store search
```
Expected: Other stores continue, final report excludes failed store
```

---

## Limitations & Future Enhancements

### Current Limitations
1. **Sequential Execution:** Store searches run one after another
2. **No Retry Logic:** Failed stores not automatically retried
3. **Fixed Store List:** Only searches predefined stores from settings

### Planned Enhancements
1. **Parallel Execution:** Enable `parallel_execution: true` for faster searches
2. **Smart Retry:** Retry failed stores with exponential backoff
3. **Dynamic Store Discovery:** Use Google Places API to find any nearby grocery store
4. **Store Prioritization:** Rank stores by distance/reputation before searching

---

## Troubleshooting

### Issue: "No stores found"
**Cause:** Store locator output doesn't match patterns in `settings.yaml`

**Fix:**
1. Check `find_stores` task output format
2. Ensure store names exactly match keys in `settings.stores`
3. Update `parse_stores_from_output()` regex if needed

### Issue: "Failed to create agent for [Store]"
**Cause:** Template variable missing or settings misconfigured

**Fix:**
1. Verify `agents.yaml` has `store_specialist_template`
2. Check `settings.yaml` has store info for that store
3. Review error message for specific missing variable

### Issue: Too many/few products returned
**Cause:** `products_per_store` setting not respected by agents

**Fix:**
1. Check `settings.yaml` → `products_per_store.default`
2. Ensure store search template uses `{products_count}`
3. Remind agents in prompt to find exactly N products

---

## Migration Guide

### From Legacy to Dynamic

**No code changes required!**

Just set in `.env`:
```
USE_DYNAMIC_WORKFLOW=true
```

**Optional:** Customize `config/settings.yaml` for your preferences

### Rollback to Legacy

Set in `.env`:
```
USE_DYNAMIC_WORKFLOW=false
```

All legacy agents/tasks still present in configs.

---

## Summary

The dynamic architecture provides:

✅ **Flexibility:** Adapts to any number of stores found (3-5)
✅ **Resilience:** Continues when individual stores fail
✅ **Configurability:** Easy tuning via `settings.yaml`
✅ **Scalability:** Add new stores without code changes
✅ **Maintainability:** Template-based agent/task creation

**Best For:** Production use where store availability varies and robustness is critical.

**Use Legacy When:** Quick testing, simple scenarios, or when you need full control over search strategy.

---

**Last Updated:** 2025-01-13
**Version:** 2.0 (Dynamic Architecture)
