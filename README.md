# Question-answering app using local LLM and Neo4j-power knowledge graphs from LlamaIndex

**Step-by-step guide on Medium**: [Local LLM Generated Knowledge Graphs Powered by Local Neo4j](https://ai.gopubby.com/local-llm-generated-knowledge-graphs-powered-by-local-neo4j-4111c5234993?sk=9091faa56d4ce983d8120dffcafcfe48)
___
## Context
Knowledge graphs are expected to improve adaptation of LLMs to niche domains, as they capture semantics or relationships underlying entities from text documents unlike the approach used by the RAG method. To help with robustness and scalability, the knowledge graphs are stored in a Neo4j database.

In this project, we develop a QA system using `LlamaIndex`'s module `PropertyGraphIndex` powered by a locally hosted LLM loaded using `llama-cpp-python` and backed by the graph-native Neo4j database. 
<br><br>
![Knowledge Graph](/assets/kgraph.png)
___
## How to Install Neo4j Database on Mac
- Launch Terminal and Install OpenJDK 17 using `brew`:
```
% brew install --cask temurin@17
```
- Extract the contents of the downloaded neo4j community edition tarball:
```
% tar -xf neo4j-community-5.21.0-unix.tar.gz
```
- Place the extracted files in a permanent home on your machine. I chose /opt/.

- The top level directory is referred to as `NEO4J_HOME`. Add an environment variable. E.g. added the following to my ~/.zshrc file:
```
export NEO4J_HOME=/opt/neo4j-community-5.21.0
```
- To accept the eval license, run: 
```
% $NEO4J_HOME/bin/neo4j-admin server license --accept-evaluation
```
- Run Neo4j as a console application, invoke the following command and you should see the startup log entries: 
```
% $NEO4J_HOME/bin/neo4j console
```
___
## How to Setup Python virtual environment
- Create and activate the environment:
```
$ python3.11 -m venv kg_qa
$ source kg_qa/bin/activate
```
- Install libraries:
```
$ pip install -r requirements.txt
```
- Download Mistral-7B-Instruct-v0.3.Q2_K.gguf from [MaziyarPanahi HF repo](https://huggingface.co/MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF) to directory `models`.

- To start the Neo4j app, run script `main_n4j.py`:
```
$ python main_n4j.py
```
- Optionally, to start SimpleGraphStore app, run script `main_sgs.py`:
```
$ python main_sgs.py
```
___
## Quickstart
- To start the Neo4j app, launch Terminal from the project directory and run the following command:
```
$ source kg_qa/bin/activate
$ python main_n4j.py
```
- Here is a sample run:
```
$ python main_n4j.py
KG generation completed in: 0:02:21.182923
Query: How do you enable HTTP/2 optimization on SteelHeads? Provide the specific commands.

Response: 1. Enter the below commands on the CLI of both client-side (CFE / C-SH) and server-side (S-SH / SFE) SteelHeads:
   - SteelHead # protocol ssl backend client-tls-1.2
   - SteelHead # protocol ssl backend alpn-forward enable

This ensures that end-to-end TLS v1.2 and ALPN are enabled on both SteelHeads, which is required for HTTP/2 optimization.
Time: 75.57
================================================================================
Query: When enabling HTTP/2 optimization on SteelHead, on which SteelHead do you enable them?

Response:  Both client-side (CFE / C-SH) and server-side (S-SH / SFE) SteelHeads need to have end-to-end TLS v1.2 and ALPN enabled for HTTP/2 optimization.
Time: 67.13
================================================================================
```
___
## Key Libraries
- **LlamaIndex**: Framework for developing applications powered by LLM
- **llama-cpp-python**: Library to load GGUF-formatted LLM from a local directory
- **neo4j**: Python driver for Neo4j support
- **llama-index-graph-stores-neo4j**: Library to support Neo4j integration

___
## Files and Content
- `models`: Directory hosting the downloaded LLM in GGUF format
- `pdf`: Directory hosting the sample niche domain documents
- `main_n4j.py`: Main Python script to launch the Neo4j app
- `main_sgs.py`: Main Python script to launch the Simple Graph Store app
- `requirements.txt`: List of Python dependencies (and version)
___

## References
- https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/
