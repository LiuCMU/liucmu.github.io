---
title: "Agents in a Nutshell"
date: 2026-07-26
draft: true
authors: ["Zhen Liu"]
tags: ["software engineering"]
summary: "This blog sets up an overall thinking framework for building agents: tools, context and memory, quality, production"
---

Large language models (LLMs) are more powerful when equpped with the capability to interact with the outside world, and agent is the way to let a LLM to interact with the outside world. In essence, a LLM predicts next word or token based on existing words in a sentence. This is a classical statistical problem. With recent innovation in language model architectures, both the model size and training data can scale to a much larger scale. Current popular LLMs are blieved to have been trained on all available information on the internet, and contain billions of parameters, hence the term "large" language model. Increasing in the model size and training data leads to very good advantages in model behavior. By **summarizing all information patterns** as model parameters, LLMs now essentiallly is a compressed storage of all information on the internet. With a little bit fine-tuning, they can now answer many questions reasonally well. Apparently, LLMs are like super brain are limited to information up to certain date, and without hands for interacting with the outside world. Consequently, people begin to explore ways to let the LLM get up-to-date information and act in real world. 

Agents turn LLMs from passive token predictions to an entity that can automatically do tasks. An agent roughly contains three core components:
- LLM: this is the **brain** of the system. For agentic systms, the reasoning ability is the key to to navigate complex and multi-step problems. A good reasoning model already has the chain-of-thoughts (CoT) and ReAct (reasoning and actions) built-in, thus simplify the orchestration layer burden. [Add links for the CoT and ReAct paper]
- Tools: this **hands** of the system. Tools brings the ability to gather additional information and interact with the outside world. 
- Orchestration: this is like the **central nervous system** or layer that connect the LLM and tools, it handles context information for a specific session, memory for project or personal level personalization and improvement, agent logic, etc. This is also where a developer's carefully crafted logic comes into life.

Agents can be assembled to form more complex systems. A common taxonomy of agentic systems divide include the following levels:
- level 0: the core reasoning system, i.e. the LLMs operates in isolation.
- level 1: the connected problem solver. This is the minimal agent that contains the three core components mentioned above. These typically can be implemented in a few lines of code with common agent develop kit (such as Google ADK, OpenAI SDK, Anthropic SDK, LangChain, LallaIndex, etc.[find links to each example in their official websites]). You probably saw them in quick start examples from many of these SDKs. The agent comes with a simbple context iformtion and some built-in tools, orchestration is largely handled by the built-in SDK.
- level 2: a strategic problem solver. At this level, customized context information and tools are provided in. Most context engineering, customized tool building and logics are built-in. At this evel, the agent is like a domain expert that would outperform a general model like GPT without customized tools or context. 
- level 3: A collaborative multi-agent system. In this level, multiple agents collaborate to achieve a goal. Agents are able to communicate with each other to assign each other tasks and receive the results.  One common arrangement is one agent act as a the orchestrator, and a few other agent are like different domain experts solving different problems. The larger and complex goal s decomposed to smaller goals by the orchestrator, each agent solving tasks for their roles and report the results to the orchestrator, the orchestrator integrate the results into one complete answer, and spawn new sub agents as needed.
- level 4. self-evoling system. The agent uses a multi-agent system to solve a long-running task, got some initial results, understand the gap between the ideal solution and its current capability limits, then it able to create new context, skill, tool or even agents to fill and gap and achieve its target.

[search literature or onling blogs to identify if there are comparisons between agent performances four these levels]


## Agent tools and MCPs
Tools empower LLMs to do more tasks. Trained LLMs become an expert in general domains, but it lacks information on current status and the ability to take actions. Tools serve the purpose. Apparently, a tool either enables the LLM to get more information of allow it to take actions in the real world. Some informational tool examples include web search tool that enables LLM to get up-to-date information, or a tool that can query internal database. Action tools example inlude a code execution sandbox for data analyis. The boundaries between informational and action tools are fuzzy, because  for example, some tools take actions in order to get information. In essence, it's all about gather information and transform information. The gathered information forms a context that is tailored to a specific task and aligns with a general patterns that the LLM knows, then the LLM outputs the next tokens based on the surrounding context information, which turns out to be the solution.

Tools take many formats. Actually, main stream agent deloveper kit mentioned above all come with a suite of powerful built-in tools, like web search. Customized tools can be comand line tools for certain softwares, for example aws cli for exploring Cloud Status; Python functions for achieving a specific task; or any other APIs that can be consumed. 

A common way for integrating models and tools is called model context protocal (MCP). MCP aims to serve as the universal interface between AI applications and the vast world of external tools and data. MCP contains the following components:
- Host: The application respoinsible for creating and maintaing the MCP clients.
- Client: A software component embedded in the Host that maintains the connection with the Server.
- Server: the server that exposes the MCP tools, it tells the client what tools this MCP can achieve, how to use them. It receives the request from the client, execute the request, then return the results back to the client.
In practice, the host and client are not distinguished clearly, we can think of the host as the agent and the client as the modules of the agent. These concepts are often mentioned in convention because MCP is inspired by the Language Server Protocol in the software development, which contains these major components [This paragraph needs verification]. The most important part is to know how to add MCP as an available tool for your agent.

![MCP integrates the model and tools](mcp2.png) In this example, the agent application contains the core agent architecture and a local MCP server, communication via stdio. There are two external servers connected via HTTP. Both the MCP host and client are embedded in the agent application. The MCP clients can simply be different modules that connect with different MCP servers. 



All communications between MCP clients and servers are built with standardized technical foundation for consistency and interpretability. MCP uses JSON-RPC 2.0 as its base message format, so MCP speaks JSON. All message types are made up from basic components like request, results, erros and notifications. There are typically two types of standard for communication between the client and the server:
- stdio (Standard input/output): Used for fast and direct communication in local environments of the agent where the MCP server runs as a subprocess of the Host application.
- Streamable HTTP: These are capabilties provided by remote servers. 
MCP is more or less like a thin wrapper with good documents on existing tools or APIs. For many local use cases, a well documented tools and MCP behave similarily. But the existing of remote MCP server make it easier for sharing the capability across multple agents, fostering a reusable ecosystem.

Clear documentation is the key for buidling good tools, including MCPs. We need clear definition of the input meaning and types, output meaning and types, doc string on what does this tool do, informative names, etc. Everything is pretty much the same as we have in the [PEP8 guidlinces](https://peps.python.org/pep-0008/) for writing clear code. 

Skills are just markdown files telling the agent how to use a setup tools to achieve a specific task. If we think of tools as the cooking wares, then the skills are the receipe. 

MCP empower agents to do more, but also brings more risks as the agent utilize external tools. Among many risks, a tpical security risk of providing tools is called the "confused deputy" problem. It is a classic security vulnerabilty where a program with privileges (the "deputy") is tricked by another entity with fewer previleges into missuing its authrority, performing actions on behalf of the attacker. Imagine a tool or MCP server that has access to confidential information that is only available to certain special user groups. A common user may have access to the agent but not the MCP server. If the user tricks the agent to call the MCP tool to do thing on behalf of the user that can not be done by the user, this could cause serious information leakage. Thus, security needs to be carefully considered when adding tools to agents. 

## Context engineering and memory
LLMs are stateless in isolation. They don't remember anything beyond what is fed into it as the input. A stateful and personal chat experience in commercial chatbots comes from context engineering. Let's define a turn as a user input and the corresponding LLM response. A session as a complete chat history, containing many turns between the LLM and user. On agentic applications, it appears that the LLM knows the chat history in a turn, that is because all the questions and anwers are fed to the LLM before each turn starts. The mechanism enabling LLMs to remember chat history in a session is called short-term memory.  To enable session memroy so that the LLM knows every context in a chat session, the most common ways are sliding window or async summary. For sliding window, the orchestration layer keeps only the most recent k turns. This is simple and cheap, but loses relevant information in a long chat. Recursive summary uses an LLM to summarize the chat history as the conversation goes, so the each question and answer in the chat history is stored as a brief format as context for the LLM to answer current question. The summary process typically runs in the background. This method is able to keep more relevant information, but also require more compute; when we start a new session, it appears the LLM has some general persona tailored to the user or project, this is because there is a factsheet preloaded before the start of each session. The mechanism for managing LLM persona and tailor to a user or project is called long-term memory. Long-term memory are typically general factual or procedure information extracted from shor-term memory. They are saved to benefit future conversations.

Both short-memory and long-term memory are just text files, like ReadME, the tricky part is how to curate, retrieve, use and update these information, which collectively is called prompt engineering and context engineering. Let's take an example to demonstrate the ideas. Imagine in an agentic application, in a turn, the user ask a question, what the LLM says is probably something like the following. The LLM sees much more than just the user questions, but many other relevant information that are useful to answer the question:

```
Context to guide reasoning defines the agent 's fundamental reasoning patterns and available actions, dictating its behavivor:
    system prompt: High-level directives defining the agent's persona, capabilities and constraints.
    Tool definition: Schemas for APIs or functions or MCPs that the agent can to achieve tasks.
    Few-shot examples: curated examples that guide the models' reasoning process. 


Evidential and Factual Data:
    Long term memory: persisted knowledge about the user or topic gather across sessions
    External knowledge: information retrieved from the database or documetns
    Tool Outputs: resuted returned by tools (including subagents)
    Artifact: non-text data, such as files, images associated with the user or session

Immediate conversational information:
    Chat History
    Scratchpad: temporary , in-progress information or calculations the agent uses for its immdediate reasoninig process
    User's prompt: the immdeidate query or question.
```

prompt engineering typically means either of the following: Optimizing a specific system prompt so the LLM pretend itself as some domain expert for something and response always follow certain pattern in answering questions. It's common to see a prompt like "You are an expert in molecular expert". This short phrase "molecular expert" helps the LLM navigate to the molecular region in the latent space so it's ready to pull relevant data patterns in answering this type of question [Are there research paper or blog on the effective of this sentence? or best ways of prompting?]. Another common meaning is to structure your own question in a way that is easy for the LLM to answer or do certain task for us. For example, a detailed prompt on how to make a perfect plot for you. I find the [openai prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering) is a good reference for prompt engineering. 

Context engineering is more about how to curate, retrieve and feed the context information to the LLM. It's a larger scope than the prompt engineering. It is a dynamic context management process, aiming to provide just everthing needed to answer a specific question. The dynamic context include memory, skill files, domain knoelwdge, etc. This information is typically too large to be fed to LLM directly, so only relevant chunks are retrieved to answer specific questions. In the above example, probably only relevant tool definition, examples, memory, external knowledge and artifact are included in the context. A common retrieve method is called retrieval augmented generation (RAG). It works like the follows, all relevant context information is stored in a database, chunked into small pieces and vectorized, then for each question, which is also vectorized, a similarity core calcualted based on the vectors is used to retrieve the relevant context information. Of course, similarity score is not always sufficnet, very often other factors, like recency, exact match, etc are all used together to determin the relevance and importance of a relevant context information in answering the current question. The goal is that the LLM has precisely the context needed to anwser the question. 

A recent trend in context engineering is skills. Skills are procecures or instructions on how to use a set of tools to achieve a specific task. Skills are typically stored in markdown files, and can be shared across agents. A skill file contains a concise description of what the skill can do, when to invoke it and a detailed instructions. The concise description allows the skill to be dynamically found by an agent session without occupying unnecessary context window. A skill is only fullly loaded when it is deemed to be useful to the current task. Some skills are bultin, but most skills can are curated by domain experts or the agent users. This enables a user to transform a more general storng agent for specific tasks or use cases.  

Providing more context to the LLM to get better performance is often called "in-context learning". The LLM learns how to perform tasks from demonstrations in the prompt. It's import to provide just the needed context. INsufficient context hinders model performance because certain key information is missing in the reasoning process. Too much context also degrade the model perofrmance because the model's ability to pay attention to critical information diminishes as context grows [Is there researon showing how LLM performs as the context size change?]. This is sometimes called "context rot".

Beyond context engineering (i.e. in-context learning), it's also popular to post-train an LLM on domain knowledge. Post-training uses curated training examples to change model behavior to suit it for specific domain knowledge, the LLM parameters are slightly changed during this process. post-training is also more expensive than context engineering. I think post training is more suited for non-public information and shows up repeatedly in a customized domain, while context engineering is more suited foradd-hoc information to solve a specific task. [Need to list a table comparing the differences/relationship between incontext learning and post-training. If there are papers comparing the differences, worth pull the results too.] 

## Evals


Is the question answerable? Does the question contain all information needed to answer the question?



### Agent security
Traditional, deterministic guardrails is necessary for agent security. For example, a hardcoded logic that an explicit user confirmation is needed to call a specific tool. Relying on LLM's judgement could be a supplement, but it can be manipulated by techniques like prompt injection.


## Practical design tips


## Use agents effectively
Agents are good at tasks with clear goals and well-defined workflows. This is determined by the nature of LLMs, and is helpful in using agents more efficiently.



