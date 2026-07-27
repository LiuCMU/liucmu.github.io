---
title: "Agents"
date: 2026-07-26
draft: true
authors: ["Zhen Liu"]
tags: ["software engineering"]
summary: "This blog sets up an overall thinking framework for building agents: tools, context and memory, quality, production"
---

Large language models (LLMs) are more powerful when equpped with the capability to interact with the outside world, and agent is the way to let a LLM to interact with the outside world. In essence, a LLM predicts next word or token based on existing words in a sentence, which is common for even ancient language models dated decades ago. With recent innovation in language model architectures, both the model size and training data can scale to a much larger scale. Current popular LLMs are blieved to have been trained on all available information on the internet, and contain billions of parameters, hence the term "large" language model. Increasing in the model size and training data leads to very good advantages. By **summarizing all information patterns** as model parameters, LLMs now essentiallly is a compressed storage of all information on the internet. With a little bit fine-tuning, they can now answer many questions reasonally well. Apparently, LLMs are like super brain are limited to information up to certain date, and without hands for interacting with the outside world. Consequently, people begin to explore ways to let the LLM get up-to-date information and act in real world. 

Agents turn LLMs from passive token predictions to an entity that can automatically do tasks. An agent roughly contains three core components:
- LLM: this is the **brain** of the system.
- Tools: this **hands** of the system. Tools brings the ability to gather additional information and interact with the outside world. 
- Orchestration: this is like the central nervous system or layer that connect the LLM and tools, it handles context information for a specific session, memory for project or personal level personalization and improvement, agent logic, etc. This is where a developer's carefully crafted logic comes into life.

Agents can be assembled to form more complex systems. A common taxonomy of agentic systems divide include the following levels:
- level 0: the core reasoning system, i.e. the LLMs operates in isolation.
- level 1: the connected problem solver. This is the minimal agent that contains the three core components mentioned above. These typically can be implemented in a few lines of code with common agent develop kit (such as Google ADK, OpenAI SDK, Anthropic SDK, LangChain, LallaIndex, etc.). You probably saw them in quick start 
- level 2: a strategic problem solver.
- level 3: A collaborative multi-agent system.
- level 4. self-evoling system.



Agents are good at tasks with clear goals and well-defined workflows. This is determined by the nature of LLMs, and is helpful in using agents more efficiently.
