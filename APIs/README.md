# LLMs API Testing - Colombian Idioms

Multi-model LLM evaluation framework for classifying and defining Colombian idioms using Azure OpenAI and Straico APIs.

## Project Structure

- **DataSet/**: Colombian idioms dataset with examples
- **Azure/**: Azure OpenAI (GPT-5.1) API calls and results
- **Straico/**: Multiple LLM providers (22+ models) API calls and results
- **Results/**: Aggregated results and metrics processing

## Prompts

Three evaluation tasks:
1. **Prompt 1**: Binary classification (is/isn't Colombian idiom)
2. **Prompt 2**: Definition generation (max 60 words)
3. **Prompt 3**: Context usage examples

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure API keys in notebooks:
   - Azure: Update `subscription_key` in `Azure/API/*.ipynb`
   - Straico: Update `API_KEY` in `Straico/APIs/*.ipynb`

3. Update model lists:
   - `Results/models.txt`: Model names for processing
   - `Straico/models.txt`: Straico model identifiers

## Usage

### Run API Calls
Execute notebooks in `Azure/API/` or `Straico/APIs/` for each prompt.

### Generate Results
```bash
jupyter notebook Results/GenerateResults.ipynb
```

### Process Metrics
```bash
jupyter notebook Results/ProcessResults.ipynb
```

## Output

- Individual model responses: `{Provider}/Results/Prompt {N}/{model}/`
- Combined responses: `Results/Prompt {N}/all_models.json`
- Processed metrics: `Results/Clean/prompt_{N}_metrics_data.json`

## Models Evaluated

Azure: gpt-5.1
Straico: 22+ models (GPT-4, Claude, Gemini, Llama, Mistral, etc.)
