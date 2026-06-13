# AI Resume Screening System

## Project Overview

The AI Resume Screening System is an intelligent recruitment assistance platform designed to automate the candidate evaluation process.

The system analyzes candidate resumes and compares them against a Job Description (JD) to identify the most suitable applicants. It uses Retrieval Augmented Generation (RAG), LangChain, ChromaDB, and Gemini AI to perform resume analysis, candidate ranking, skill matching, and recruiter question answering.

---

# Problem Statement

Recruiters often receive hundreds of resumes for a single position.

Manual screening can be:

* Time consuming
* Error prone
* Inconsistent

This project automates the screening process and helps recruiters identify the best candidates quickly.

---

# Objectives

* Automate resume analysis
* Compare resumes with job requirements
* Rank candidates based on skill relevance
* Identify matching and missing skills
* Reduce manual recruitment effort
* Support recruiter question answering

---

# Technologies Used

## Frontend

* Streamlit

## Backend

* Python

## AI & LLM

* Gemini AI

## Frameworks

* LangChain

## Database

* ChromaDB

## Architecture

* Retrieval Augmented Generation (RAG)

---

# Project Structure

AI_WORKSHOP_RAG

├── app.py

├── rag.py

├── resume_parser.py

├── .env

├── resumes/

├── chroma_db/

└── README.md

---

# File Description

## app.py

Main application file.

Responsibilities:

* User Interface
* Resume Loading
* Job Description Input
* Candidate Ranking
* Recruiter Question Answering

Run this file to start the application.

---

## resume_parser.py

Responsible for:

* Reading DOCX resumes
* Extracting resume content
* Returning cleaned text

---

## rag.py

Responsible for:

* Creating embeddings
* Creating ChromaDB vector store
* Semantic retrieval
* Context generation

---

## resumes/

Stores candidate resumes.

---

## chroma_db/

Stores vector embeddings generated from resume data.

---

## .env

Stores Gemini API Key.

Example:

GOOGLE_API_KEY=YOUR_API_KEY

---

# System Architecture

Resume Files
↓
Resume Parser
↓
Text Extraction
↓
Embeddings
↓
ChromaDB
↓
Retriever
↓
Gemini AI
↓
Candidate Analysis
↓
Final Ranking

---

# Workflow

## Step 1

Load candidate resumes.

## Step 2

Extract text from resumes.

## Step 3

Generate vector embeddings.

## Step 4

Store embeddings in ChromaDB.

## Step 5

Enter Job Description.

## Step 6

Retrieve relevant candidate information.

## Step 7

Send retrieved information to Gemini AI.

## Step 8

Generate candidate rankings and recommendations.

---

# Features

## Candidate Ranking

Ranks candidates based on suitability.

## Skill Matching

Identifies matching skills.

## Skill Gap Analysis

Identifies missing skills.

## Match Percentage

Calculates candidate-job alignment.

## Recruiter Q&A

Allows recruiters to ask questions about candidates.

---

# Sample Questions

* Who is the best candidate?
* Which candidate has Python experience?
* Who has Machine Learning skills?
* Which candidate has the highest match score?
* What skills are missing in Candidate A?

---

# How to Run

## Create Virtual Environment

python -m venv venv

## Activate Environment

.\venv\Scripts\Activate.ps1

## Install Dependencies

pip install -r requirements.txt

## Add API Key

Create .env file

GOOGLE_API_KEY=YOUR_API_KEY

## Run Application

python -m streamlit run app.py

---

# Expected Output

* Candidate Ranking
* Match Percentage
* Matching Skills
* Missing Skills
* Top Candidates
* Recruiter Q&A

---

# Future Enhancements

* PDF Resume Support
* ATS Compatibility Score
* Interview Question Generation
* Candidate Dashboard

---

# Conclusion

The AI Resume Screening System automates candidate evaluation using Gemini AI, LangChain, ChromaDB, and RAG, enabling faster and more accurate recruitment decisions.
