# Authentication and Authorization in Plain Language

This post explains auth (authentication) and authz (authorization) in plain language. With the power of AI, many scientist can build projects in an unprecedented way (myself included). This will for sure accelerate the pace of scientific discovery. However, many engineering conventions are not well known to scientists. Without knowing this concept, we can hardly provide effective prompts to Agents and judge the quality of their responses. This post is a brief introduction to concepts, and how they are used in practice in plain language. The goal is to help scientists understand the concepts and use them in practice.

Auth in the simplist form can just be the username and password. This is the foundation of auth and is still widely used nowadays. This simple format becomes insufficient when our needs change in the real world. Nowadays, everyone has hundreds of accounts, each of which requires a authentication method. Creating a password for each account is satisfies the basic need of auth, but it is really hard to mamange all the accounts and passwords. 

Of the hundreds of accounts, some are used more frequently than others. For example, our Google account or Apple account is used almost daily. One natural idea to remove unnecessary passwords is to use a few common accounts like Google or Apple to login to other accounts. However, providing our Google or Apple account and passwords to other accounts is not a good idea. We need a way to safely use our Google or Apple account to login to other accounts without providing our credentials. This is where OAuth and OIDC come into play.

Before OAuth takes place, certifacates are used to verify the identity of the server. 

The way auth works for softwares, very much mimics auth in real life. 


## Useful References
1. [jtw.io](https://www.jwt.io/) is a great website to play with JWT encoding and decoding. 
2. The [YouTube Video by Nate Barbettini](https://youtu.be/996OiexHze0) introduces the concepts and examples of OAuth and OIDC in very easy to understand way.