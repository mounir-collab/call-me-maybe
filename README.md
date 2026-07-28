*This project has been created as part of the 42 curriculum by manzar.*

# Call Me Maybe

## Description

**Call Me Maybe** is a function-calling system powered by a Small Language Model (LLM) and a constrained decoding engine.

The objective of the project is to translate natural language requests into structured JSON function calls while guaranteeing that the generated output always respects a predefined JSON schema.

Unlike prompt-only approaches, this project performs **token-level constrained decoding**, restricting the language model to produce only valid tokens at every generation step. This guarantees syntactically valid JSON while enforcing parameter types defined in the provided function definitions.

The project demonstrates how modern LLMs can safely interact with external tools through deterministic decoding instead of relying solely on prompt engineering.

---

# Features

- Function selection using constrained decoding
- Schema-aware JSON generation
- Guaranteed valid JSON output
- Type-constrained parameter generation
    - Integer
    - Float / Number
    - Boolean
    - String
- Token-by-token decoding
- Interactive terminal visualization using Rich
- Automatic generation of result JSON file

---

# Project Architecture

```
Natural Language Prompt
            │
            ▼
     System Prompt
            │
            ▼
     Small Language Model
            │
            ▼
  Constrained Decoder
            │
 ┌──────────┴──────────┐
 │                     │
 ▼                     ▼
Function Name      Parameters
 Decoder            Decoder
 │                     │
 └──────────┬──────────┘
            ▼
      Valid JSON Output
```

---

# Algorithm Explanation

The decoding process follows a deterministic constrained decoding strategy.

## 1. System Prompt Construction

The application first builds a system prompt describing every available function:

- function name
- description
- parameter names
- parameter types
- return type

This prompt gives semantic knowledge to the language model.

---

## 2. Function Name Decoding

Instead of allowing every token from the vocabulary, only tokens belonging to existing function names are considered.

For every decoding step:

1. Compute logits.
2. Collect valid candidate tokens.
3. Select the highest-probability valid token.
4. Continue until a complete function name is produced.

This guarantees that the generated function is always one of the available functions.

---

## 3. Parameter Decoding

Each parameter is decoded according to its declared type.

### Numbers

Only tokens representing digits, decimal points and minus signs are allowed.

After generation, floating-point values are normalized before insertion into the JSON output.

Example:

```
16
```

becomes

```
16.0
```

when required.

---

### Strings

Only valid string tokens are accepted.

Generation stops only when the closing quotation mark is reached.

Escaped characters inside strings are preserved.

---


## 4. JSON Construction

The decoder itself generates the JSON structure.

The language model never decides where braces, commas or quotation marks should appear.

Therefore the produced JSON is always syntactically valid.

---

# Design Decisions

Several implementation decisions were made to improve reliability.

## Token-level constraints

Instead of trusting the language model to produce valid JSON, invalid tokens are removed during decoding.

---

## Separation of responsibilities

The project is divided into independent modules:

- parser
- system prompt builder
- constrained decoder
- parameter decoders
- vocabulary utilities
- UI

This keeps the implementation modular and easy to extend.

---

# Performance Analysis

## Accuracy

The constrained decoder significantly improves output reliability compared to prompt-only generation.

The generated JSON is always parsable.

Function names always belong to the provided function definitions.

Parameter types respect the declared schema.

---

## Speed

Most computation time comes from:

- LLM inference
- repeated logits computation

The constrained decoder itself introduces only a small overhead.

---

## Reliability

The implementation prevents:

- malformed JSON
- invalid parameter types
- unknown function names
- schema violations

The remaining errors mainly come from semantic misunderstanding by the language model.

---

# Challenges Faced

Several technical challenges were encountered during development.

## Large numbers

Long numeric values occasionally caused unstable generation.

This was solved by improving numeric decoding and token normalization.

---

## Escaped characters

Strings containing escaped quotation marks required careful handling to avoid premature termination.

---

## Regular expressions

Extracting regex patterns proved difficult because language models often interpret rather than copy them exactly.

The system prompt was refined to emphasize literal extraction.

---

## JSON comments

The model sometimes generated comments such as

```json
// comment
```

Additional prompt constraints and decoding rules were introduced to prevent these outputs.

---


# Testing Strategy

The implementation was validated using the provided function-calling dataset.

Testing included:

- arithmetic functions
- string manipulation
- regex substitution
- SQL queries
- boolean parameters
- integer parameters
- floating-point parameters

Additional manual tests were created for:

- escaped quotes
- empty strings
- negative numbers
- decimal values
- long numbers
- repeated parameters

Every generated output was verified by parsing it with Python's `json.loads()`.

---

# Instructions

## Requirements

- Python 3.10+
- uv
- Hugging Face account (optional, for higher download limits)

---

## Installation

Clone the repository:

```bash
git clone <repository_url>
cd call-me-maybe
```

Install dependencies:

```bash
uv sync
```

---

## Running

```bash
python -m src
```

or

```bash
uv run python -m src
```

---

## Command Line Options

```text
--functions_definition
--input
--output
--model
```

Example:

```bash
uv run python -m src \
    --functions_definition data/input/functions_definition.json \
    --input data/input/function_calling_tests.json \
    --output data/output/function_calling_results.json
```

---

# Example Usage

Input:

```
Reverse the string "hello"
```

Output:

```json
{
  "prompt": "Reverse the string \"hello\"",
  "name": "fn_reverse_string",
  "parameters": {
    "s": "hello"
  }
}
```

---

Input:

```
What is the sum of 12 and 35?
```

Output:

```json
{
  "prompt": "What is the sum of 12 and 35?",
  "name": "fn_add_numbers",
  "parameters": {
    "a": 12.0,
    "b": 35.0
  }
}
```

---

# Resources

## Constrained Decoding

- OpenAI Function Calling documentation
- Hugging Face Transformers documentation
- JSON Schema specification
- Qwen documentation
- Rich documentation

Useful references:

- https://huggingface.co/docs/transformers
- https://json-schema.org/
- https://rich.readthedocs.io/
- https://platform.openai.com/docs/guides/function-calling

---

## AI Usage

Artificial Intelligence was used as an engineering assistant during the development of this project.

It was used to:

- discuss constrained decoding algorithms
- review implementation ideas
- explain tokenizer behavior
- improve Python code quality
- assist with debugging
- review the project documentation

All architectural decisions, constrained decoding logic, implementation, testing, debugging, and final validation were completed and verified by me.

---

# Future Improvements

- Trie-based constrained decoding
- Grammar-based decoding
- Beam search support
- Streaming generation
- Support for nested JSON schemas
- Parallel decoding
- Faster vocabulary filtering
- Better semantic extraction for regular expressions

---