# Technology Review Report

## Python Package Choices

### Section 1: Background
Our project needs to be able to idenfity offensive or innapropriate license plates. This has many technological components and the two we decided to focus on for this review is mentioned below: 
1. Decoding leetspeak and character substitutions
2. Measuring similarity between a plate string and a list of prohibited terms

We need to be able to recognize “slur” as “s1ur” for example. 
Therefore, we evaluated Python libraries that support leetspeak decoding and fuzzy string matching. 

### Section 2: Python Package Choices
1. Package for leetspeak decoding
- **Name:** leetspeak-encoder-decoder (https://github.com/Monotoba/leetspeak-encoder-decoder)
- **Author:** Monotoba
- **Brief summary of library’s purpose:**
    a leetspeak to multiple languages translator that allows for encoding and decoding leetspeak. The package also has a dictionary for multiple character replacements in different languages and can identify the correct character and language based on language identifiers

2. Package for fuzzy matching? (calculates difference or similarity between two strings)
- **Name:** RapidFuzz (https://pypi.org/project/RapidFuzz/#description) 
- **Author:** Max Bachmann
- **Brief summary of library’s purpose:**
Calculates similarity or “distance” between two or more strings and assigns a score/ratio based on this distance. Builds off of string similarities calculations from FuzzyWuzzy library

3. Package for fuzzy matching? (calculates difference or similarity between two strings)
- **Name:** TheFuzz (https://pypi.org/project/thefuzz/) 
- **Author:** Adam Cohen
- **Brief summary of library’s purpose:**
Uses Levenshtein distance to calculate similarity or “distance” between strings and assigns a score/ratio based on this distance. 

### Section 3: Package Comparison
1. leetspeak-encoder-decoder
- **Pros**
    - Has simple API: decode_leet(text, lang)
    - provides a built-in character replacement dictionary
    - Reduces need to manually create leetspeak mapping

- **Cons**
    - Not pip-installable
    - Requires manual cloning and path modification
    - Gives normalized/lossy outputs
    - Low adoption signal which could mean long-term maintenance risk

2. RapidFuzz
- **Pros**
    - Very fast and actively maintained
    - Lots of useful APIs: 
    - Easy pip installation
    - Great for finding the closest “bad-word candidate” after normalizing

- **Cons**
    - Requires preprocessing (normalization + token handling)
    - Needs threshold tuning

3. TheFuzz
- **Pros**
    - Simple API
    - Widely documented
    - Easy pip installation
- **Cons**
    - Generally slower than RapidFuzz
    - Very similar in functionality to RapidFuzz with no clear advantage
    - Also requirees preprocessing and threshold tuning


### Section 4: Your Choice and Why
**Chosen Package:** RapidFuzz

**Reason:** 
We chose RapidFuzz as the primary fuzzy matching library due to its computational efficiency, active maintenance, and clean API. While the leetspeak decoder simplifies some normalization, it introduces integration complexity and lossy outputs that are risky for license plate validation. TheFuzz was not selected because RapidFuzz offers superior performance with similar functionality.

### Section 5: Drawbacks/Remaining Concerns
For RapidFuzz:
- Requires manual threshold tuning

- Needs additional preprocessing logic

- Does not provide built-in explanations

- Risk of false positives without careful tokenization
