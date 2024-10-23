# JIRA Comments Analysis with NLTK

This project explores trends in defect-related comments from JIRA using Natural Language Toolkit (NLTK).

## Business Goal
The primary goal was to investigate if any patterns or trends could be identified from JIRA comments, aiming to uncover common reasons for defects raised.

## Project Overview

- **Methodology**:
  - Used multithreading to fetch relevant issues and their comments from JIRA into a DataFrame.
  - Applied extensive data cleaning to prepare comments for analysis.
  - Leveraged NLTK for natural language processing, using:
    - `nltk.pos_tag()` for part-of-speech tagging.
    - Lemmatization for word normalization.
    - Stop word removal to focus on meaningful terms.
  - Extracted the top 10 most common words and used them to classify comments based on their content.

## Key Steps

1. **Data Collection**:
   - Fetched comments for all relevant issues using multithreaded API calls.
   - Gathered comments into a structured format for analysis.

2. **Data Cleaning**:
   - Performed extensive data wrangling on raw comments, removing unnecessary symbols, stopwords, and irrelevant terms.

3. **Natural Language Processing**:
   - Used NLTK's `pos_tag()` for part-of-speech tagging.
   - Applied a lemmatizer to standardize words.
   - Identified and removed stop words to focus on key content.

4. **Analysis**:
   - Extracted the 10 most common words from the cleaned comment dataset.
   - Compared each comment against this top-10 list to classify comments by their likely cause for the defect.

## Results

- The analysis provided **40% accuracy**, identifying patterns in defect-related comments.
- Though not highly accurate, the process did uncover repetitive areas that helped highlight some recurring issues in JIRA, supporting further investigation by senior team members.

## Tools & Libraries

- **Python**: Multithreading, Data Cleaning, Data Wrangling
- **NLTK**: Part-of-speech tagging, Lemmatization, Stop word filtering
- **Pandas**: DataFrame handling and data manipulation

## Future Improvements

- Enhance accuracy by exploring other NLP techniques or deep learning models.
- Investigate more advanced text classification methods to refine defect cause identification.
- Incorporate feedback loops with developers to improve classification relevance.
