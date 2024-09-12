# Enhancing User Support through Code Generation and Documentation Search

This repository contains the project for code generation and documentation search for the Sage project. 

### Goals:
1. Evaluate the effectiveness of manual augmentation through the quality of generated code and answers
2. Automate the augmentation with Retrieval-Augmented Generation (RAG)
3. Compare the quality of results of the RAG system against manual augmentation
4. Test the computational costs of RAG
5. Provide suggestions on implementing an efficient RAG system

### Directory Contents:

**manual-augmentation/**
* `conversations/` directory contains:
  *  all manual augmentation interactions with llama3
* `code/` directory contains:
  * generated code from the conversations in .py format
  * a notebook testing Sage Data Client (SDC) features and the produced data
* `progress-reports/` directory contains:
  * three PowerPoint reports with the concluding results of manual augmentation
* `rag/` directory contains:
  * one notebook with a basic example of RAG 
  * three notebooks with more advanced RAG techniques and testing using LangChain
  * a python file of generated code with associated images