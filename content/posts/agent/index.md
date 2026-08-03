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


## Context engineering and memory


## Practical design tips

### Agent security
Traditional, deterministic guardrails is necessary for agent security. For example, a hardcoded logic that an explicit user confirmation is needed to call a specific tool. Relying on LLM's judgement could be a supplement, but it can be manipulated by techniques like prompt injection.

## Evals


Is the question answerable? Does the question contain all information needed to answer the question?


## Use agents effectively
Agents are good at tasks with clear goals and well-defined workflows. This is determined by the nature of LLMs, and is helpful in using agents more efficiently.
