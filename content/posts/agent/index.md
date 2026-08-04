---
title: "Agents"
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
LLMs are stateless in isolation. They don't remember anything beyond what is fed into it as the input. Let's define a turn as a user input and the corresponding LLM response. A session as a complete chat history, containing many turns between the LLM and user. On agentic applications, it appears that the LLM knows the chat history in a turn, that is because all the questions and anwers are fed to the LLM before each turn starts. The mechanism enabling LLMs to remember chat history in a session is called short-term memory; when we start a new session, it appears the LLM has some general persona tailored to the user or project, this is because there is a factsheet preloaded before the start of each session. The mechanism for managing LLM persona and tailor to a user or project is called long-term memory. 

Both short-memory and long-term memory are just text files, like ReadME, the tricky part is how to curate, retrieve, use and update these information, which collectively is called prompt engineering and context engineering. Let's cake an example to demonstrate the ideas. Imagine in an agentic application, in a turn, the user ask a question, what the LLM says is probably something like the following:

```
system prompt:

Context information:
    Chat History or Summary
    Relevant tool documentation
    Relevant examples
    Relevant Skill information
    Broad Memory

User question:
```

prompt engineering typically means either of the following: Optimizing a specific system prompt so the LLM pretend itself as some domain expert for something and response always follow certain pattern in answering questions. It's common to see a prompt like "You are an expert in molecular expert". This shoft phrase "molecular expert" helps the LLM navigate to the molecular region in the latent space so it's ready to pull relevant data patterns in answering this type of question [Are there research paper or blog on the effective of this sentence?]. Another common meaning is to structure your own question in a way that is easy for the LLM to answer or do the task for us. For example, a detailed prompt on how to make a perfect plot for you. 

Context engineering is more about how to curate, retrieve and feed the context information to the LLM. It's a larger scope than the prompt engineering.

## Practical design tips

### Agent security
Traditional, deterministic guardrails is necessary for agent security. For example, a hardcoded logic that an explicit user confirmation is needed to call a specific tool. Relying on LLM's judgement could be a supplement, but it can be manipulated by techniques like prompt injection.

## Evals


Is the question answerable? Does the question contain all information needed to answer the question?


## Use agents effectively
Agents are good at tasks with clear goals and well-defined workflows. This is determined by the nature of LLMs, and is helpful in using agents more efficiently.
