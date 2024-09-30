# Code Generation and Documentation Search using Large Language Model

This repository contains the project for code generation and documentation using a Large Language Model.

---

## Goals:
1. Evaluate the effectiveness of manual augmentation through the quality of generated code and answers
2. Automate the augmentation with Retrieval-Augmented Generation (RAG)
3. Compare the quality of results of the RAG system against manual augmentation
4. Test the computational costs of RAG
5. Provide suggestions on implementing an efficient RAG system

## Directory Contents:

`requirements.txt`
* Dependencies 
* Does not include installed models
* Look at `sources.md` for links to the models

`sources.md`
* A list of papers and website links containing relevant work

`manual-augmentation/`
* `conversations/`
  *  All manual interactions with llama3
* `code/`
  * Generated code from the conversations in .py format
  * A notebook testing Sage Data Client (SDC) features and the produced data

`rag/`
  * One notebook with a basic example of RAG 
  * Three notebooks with more advanced RAG techniques and testing using LangChain
  * A python file of generated code with associated images

## Daily Blogs:

**Monday July 1, 2024**
* Joined Waggle slack channel

**Tuesday July 2, 2024**
* Looked into LM Studio and Ollama
* Browsed the Sage documentaiton [website](https://sagecontinuum.org/docs/about/overview) to gather documentation snippets
* Read up on multiple resources: 
  * [LLMs](https://www.ibm.com/topics/large-language-models)
  * [vector bases](https://www.cloudflare.com/learning/ai/what-is-vector-database/)
  * [data augmentation](https://stancsz.medium.com/prompt-engineering-data-augumentation-d475b8ee4450)
  * [RAGs by AWS](https://aws.amazon.com/what-is/retrieval-augmented-generation/)
  * [RAGs by NVIDIA](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/)
  * [RAGs by IBM](https://research.ibm.com/blog/retrieval-augmented-generation-RAG)

**Wednesday July 3, 2024**
* Sage meeting
* Talked to Sean to clarify a few questions I had about the project:
  * What does it mean to manually augment prompts? 
  * What kind of code are we trying to generate? 
  * What LLM models and hosting platforms should I look at? 

**Friday July 5, 2024**
* Looked at Sean's examples of manually augmenting prompts
* Began experimenting with Ollama

**Monday July 8, 2024**
* I realized llama3 is not trained on Sage's data
* Tried out llama3 70b version, but it was far too slow on my Macbook
  
**Tuesday July 9, 2024**
* Llama's lack of information on Sage gave me a baseline to start manually augmenting prompts
  * I know the extents of what I need to manually train it on
* I also figured out how to save models by running `/save <model name>` while running llama3
> Never save  the model as "llama3" because you won't be able to run the base llama3 model when you start with `ollama run llama3`. It'll keep the saved context

**Wednesday July 10, 2024** 
* Looked at Sage's documentation and brainstormed the minimum amount of information I need to provide to the model

**Thursday July 11, 2024**
* Sage meeting

**Friday July 12, 2024**
* Types of snippets:
  * code examples
  * written documentation
* Entry-points for code generation: 
  * https://sagecontinuum.org/docs/tutorials/access-waggle-sensors
  * https://sagecontinuum.org/docs/tutorials/edge-apps/intro-to-edge-apps
  * https://sagecontinuum.org/docs/tutorials/accessing-data
* Given a few sentences of context, the model explained what Sage and Waggle are
* However, the generated information was a copy and paste of the provided context and often misinterpreted acronyms

**Monday July 15, 2024**
* Started providing llama3 snippets of code context from Sage repos and website 
* It was able to explain precisely the purpose of each line of code and even mentioned IoT, edge computing, and plugin terminology

**Tuesday July 16, 2024**
* The model finally produced perfect code with just a few lines of context! 
* In more complex tasks like generating two talking plugins, it missed a few imports or details

**Wednesday July 17, 2024**
* Asked it questions about Sage and Waggle with only code context
* It responded better than providing text context of what Sage and Waggle are
* Asked for the model's reasoning

**Thursday July 18, 2024**
* Sage meeting

**Friday July 19, 2024**
* Prepared my presentation

**Monday July 22, 2024**
* Seminar presentation

**Tuesday July 23, 2024**
* Provided the entirety of `writing-a-plugin.md` from `waggle-sensor/pywaggle` repo
* Did not use the context properly to generate its own plugin 
* Model used a lot of external libraries not present in the code snippets 

**Wednesday July 24, 2024**
* Pushed the model to explain its generation of irrelevant code given code context
* Explained its errors properly but proceeded to provide incorrect code

**Thursday July 25, 2024**
* Sage meeting

**Friday July 26, 2024**
* Team outing!!

**Monday July 29, 2024**
* Based on the comments from the presentation, I decided to give the model confusing instructions with Sage context

**Tuesday July 30, 2024**
* Further tested the model's ability to reason with irrelevant instructions

**Wednesday July 31, 2024**
* Analyzed the naiveness of the model with fictional scenarios given Sage context

**Thursday August 1, 2024**
* Sage meeting

**Friday August 2, 2024**
* Familiarized myself with the Sage Data Client library and functionality

**Monday August 5, 2024**
* Worked on a script to clean DFs provided by calling `sage_data_client.query()`

**Tuesday August 6, 2024**
* Compared the differences in generated code when the model is given a raw DF instead of a clean DF (both scenarios are given a snippet of SDC code to get pressure data from a node)
* Both codes overlooked small, unexplained, details like grouping sensor queries into one query (gave HTTP ERROR 400)
* But the clean DF gave more reasonable results

**Wednesday August 7, 2024**
* Model produced perfect code with further instructions to not group sensor queries!

**Friday August 9, 2024**
* Looked into RAG and VBs in detail

**Monday August 12, 2024**
* Listed out the steps to make a basic RAG system in `rag-basic.ipynb`
* Got Ollama to work on Jupyter Notebook without RAG

**Tuesday August 13, 2024**
* Made a basic RAG system:
  * custom embed function with llama3.1 embed model
  * custom similarity function with cosine similarity 

**Wednesday August 14, 2024**
* Tested the accuracy of the basic RAG by seeing which data strings were chosen to be the most similar to the question 

**Thursday August 15, 2024**
* Tested mxbai-embed-large model
* It worked so much better than llama3.1 embedding
* Tested the extents of my similarity function
* Sage meeting

**Friday August 16, 2024**
* Searched how to do data ingestion with unstructured Sage repositories

**Monday August 19, 2024**
* Got data ingestion pipeline to work and split the retrieved information

**Tuesday August 20, 2024**
* Searched various VB benchmarks
* Chroma's functionality was well supported by Langchian, so I chose that one
* Produced the first query with Chroma, mxbai-embed-large, and Langchain for the question "What is Sage?"
* Properly retrieved relevant information 

**Wednesday August 21, 2024**
* Automated the process more by introducing chains and retrievers
* Instead of asking the model to retrieve relevant information, storing that information, and using again the same stored question to make the prompt, the prompt is auto-generated with one invoke function by searching the VB for relevant information and directly passing it to the prompt
* The original question is passed through to the prompt as well. 

**Thursday August 22, 2024**
* Tested different sizes of retrieved snippets
* Sage meeting

**Friday August 23, 2024**
* Figured out how to also include .py and .ipynb files in data ingestion
  * This requires specific data loaders
* Expanded the sources of Sage data to the sage website, pywaggle, and SDC repos

**Monday August 26, 2024**
* Made a script to recursively load the three different file types with specific data loaders
* Searched how to efficiently split each file type according to important delimeters 
  * This improved the relevance of snippets (splits) by maintaing context by not splitting them incorrectly

**Tuesday August 27, 2024**
* Another important foundation of a RAG system is prompting (how context and question are presented with retrieved contexts)
* I experimented with different prompt templates
  
**Wednesday August 28, 2024**
* I was able to construct a more accurate prompt template
  * I call it the Sage prompt
* Thus, the RAG pipeline for Sage was finalized (though it can always be improved)
* I tested a wider variety of text questions 

**Thursday August 29, 2024**
* Tested more coding questions that I used in manual augmentation and compared the results
* The results were similar 
* Sage meeting

**Friday August 30, 2024**
* Looked into how to improve the efficiency of the RAG system
* It will be important to test the accuracy and speed of the current one 
* Looked into LLM accuracy and speed metrics
* LLM accuracy is a highly discussed topic
* There are no set standards for LLM accuracy

**Tuesday September 3, 2024**
* Expanded the Sage sources to "./sage-website/docs/", "./sage-website/news/", "./sage-data-client/", "./pywaggle/"
* Made a list of testing variables for speed and accuracy
  * number of embeddings
  * chunk sizes and overlap
  * different vector databases
  * different embedding models
  * number of retrieved snippets, k
  * question types

**Wednesday September 4, 2024**
* Made the script to plot embedding model speeds 
* Tested Jina embedding model and FAIS VB
* Testing the number of embeddings took longer than expected
* With all the Sage data, mxbai-embed-large took ~8 minutes with one VB
* With four different embeding sizes (number of splits), it would take ~one hour to test the speed of one embedding model at four different numbers of splits
* It would take all day to run all the tests I had planned

**Thursday September 5, 2024**
* Brought up the time concern in the Sage meeting
* Was reassured it is normal for LLMs, especially on personal computers, to take so long

**Friday September 6, 2024**
* I considered transferring the notebooks to my computer with a dedicated GTX 1080 GPU
* However, I focused first on testing with a smaller subset of Sage data to focus on building the testing framework

**Monday September 9, 2024**
* With a solid testing framework, I tested again on the full Sage data
* I left my computer to run as I did other tasks 
* The results showed an increasing linear relationship between number of snippets and embedding time
* There was no real difference between the Chroma and FAISS VBs
* Jina greatly outperformed mxbai due to its external computing

**Tuesday September 10, 2024**
* Tested the accuracy of the different VBs
* I did this by comparing the retrieved snippets at different k values
* There was no difference in retrieval
* mxbai/jina with Chroma or FAISS are equally as accurate
* At least with Sage data, there is no difference in accuracy with any combination of Chroma, FAISS, mxbai, or jina
> Note: I encountered a dimensionality error in the early stages of testing. Within the same RAG system, you can't mix embedding models with one VB because  each VB stores the previous model's params. 
>
> To overcome this, the VB must be deleted before another model is used.

**Wednesday September 11, 2024**
* Made a script to test the speed of generation at different k values and questions

**Thursday September 12, 2024**
* Tested the code with a small subset of Sage data
* Started cleaning up the previous notebooks

**Friday September 13, 2024**
* Expanded the test with more Sage data

**Monday September 16, 2024**
* Plotted the final results of all the tests with all the Sage sources: "./sage-website/docs/", "./sage-website/news/", "./sage-data-client/", "./pywaggle/"
* There is a clear increasing linear relationhsip with k and generation time
* Some questions are also consistent in their placement in generation time relative to other questions
* Reorganized all my work

**Tuesday September 17, 2024**
* Polished the work with manual augmentation and the RAG system

**Wednesday September 18, 2024**
* Collected all of my sources in making the RAG system

**Thursday September 19, 2024**
* Presented final test plots in Sage meeting
* Started working on final blog post and pushing all the deliverables to GitHub
