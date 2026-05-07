## Problem Statement: AI-Powered Restaurant Recommendation System (Zomato Use Case)

Build an AI-powered restaurant recommendation service inspired by Zomato. The system should suggest restaurants tailored to a user’s preferences by combining structured restaurant data with a Large Language Model (LLM) to produce personalized, human-readable recommendations.

## Objective

Design and implement an application that:

- Accepts user preferences such as **location**, **budget**, **cuisine**, and **minimum rating**
- Uses a real-world restaurant dataset as the source of truth
- Uses an LLM to **rank** candidates and generate **clear explanations** for each recommendation
- Presents results in a format that is easy for the user to compare and decide

## Inputs

Collect the following from the user:

- **Location** (e.g., Delhi, Bangalore)
- **Budget** (e.g., low / medium / high or an approximate cost range)
- **Cuisine** (e.g., Italian, Chinese)
- **Minimum rating**
- **Additional preferences** (optional), e.g., family-friendly, quick service, ambience, etc.

## Data Source

- Load and preprocess the Zomato dataset from Hugging Face: `https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation`
- Extract relevant fields such as:
  - Restaurant name
  - Location / city
  - Cuisine(s)
  - Average cost / price range
  - Rating
  - Any other useful metadata available in the dataset

## System Workflow

1. **Data ingestion**
   - Load, clean, and normalize the dataset
   - Prepare a structured representation of restaurants for filtering and prompting

2. **Preference collection**
   - Capture user inputs and validate them (e.g., rating in valid range, budget format)

3. **Candidate selection (integration layer)**
   - Filter the dataset based on user preferences to produce a shortlist of relevant restaurants
   - Convert the shortlist into a structured prompt input for the LLM

4. **Recommendation generation (LLM)**
   - Use the LLM to:
     - Rank restaurants (best match first)
     - Provide short, specific reasoning for each choice
     - Optionally summarize the overall recommendation set

5. **Output presentation**
   - Display the top recommendations in a user-friendly format including:
     - **Restaurant name**
     - **Cuisine**
     - **Rating**
     - **Estimated cost**
     - **AI-generated explanation**
