🧠 RAG-Based Text2SQL Agent

A production-ready Retrieval-Augmented Generation (RAG) Text-to-SQL system that converts natural language questions into executable SQL queries using a hierarchical multi-agent architecture, semantic caching, query validation, and dynamic schema understanding.

🚀 Overview

This project implements a modular LLM-powered SQL generation pipeline capable of:

Translating natural language to SQL

Validating and executing queries

Explaining results in natural language

Supporting dynamic .db file uploads

Auto-generating ER diagrams

Measuring execution accuracy via benchmark suite

The system is designed to behave like a lightweight database reasoning agent rather than a simple prompt wrapper.

🏗 System Architecture

The agent follows a hierarchical RAG workflow pattern:
      User Question
           ->
      Intent Detection Agent
           ->
      Semantic Cache (Embedding Similarity Search)
           ->
     Schema-Aware SQL Generator (LLM)
           ->
     SQL Validator Agent (Safety + Syntax)
           ->
     Execution Engine (SQLAlchemy / SQLite)
           ->
     Result Analyzer Agent (Natural Language Explanation)
           ->
     Dashboard Output (Streamlit UI)
     
🧠 RAG Design Philosophy

   -Unlike traditional Text2SQL systems, this project implements:

   -Retrieval layer (semantic caching)

   -Schema grounding

   -Multi-agent validation

   -Execution-based evaluation

This makes it closer to a structured reasoning agent than a prompt-based tool.

📊 Benchmarking Framework

The system includes a 30-query benchmark suite measuring:

   -Execution Accuracy (~65–75%)

   -Average Latency (~2–3 seconds)

   -Cache hit performance

   -Complex join reasoning capability

Evaluation is execution-based, not string-matching based.

📈 Key Features:

✅ Multi-Agent Hierarchy

   Intent → Retrieval → Generation → Validation → Execution → Explanation

✅ Semantic Caching

   Embedding-based query reuse for performance optimization.

✅ Dynamic Schema Support

   Automatically adapts to uploaded .db files.

✅ Auto ER Diagram Generation

   Uses foreign key detection + graph visualization.

✅ Query Safety Layer

   Prevents destructive SQL execution.

✅ Streamlit Deployment

   Interactive dashboard with live SQL generation.

🛠 Tech Stack

   -Python

   -Streamlit

   -SQLite

   -SQLAlchemy

   -Groq LLM

   -Pandas

   -Scikit-learn (cosine similarity)

   -NetworkX (ER diagrams)

   -Matplotlib
   

