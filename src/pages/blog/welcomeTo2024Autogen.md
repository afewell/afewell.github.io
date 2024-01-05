---
layout: $/layouts/post.astro
title: "Welcome to 2024: Time to Start Kicking A$$ with AI - Bootstrap your multi-agent workflows the easy way with AutoGen Studio on Tanzu Kubernetes Grid"
description: "Asking the chatbot questions was so 2023, time to step up to multi-agent workflows with Microsoft's awesome new multi-agent framework Autogen and it's simple, easy-to-use no code web app, Autogen Studio. We will run it on Tanzu Kubernetes Grid on vSphere using vscode dev containers to grok it with cloud server performance with a local desktop UX, strap in and come along for the ride!" 
# there MUST be at least 1 tag listed or it will not render
tags:
  - ChatGPT
  - Tanzu
  - "Artificial Intelligence"
  - Kubernetes
  - GPT4
  - AutoGen
  - "Machine Learning"
  - LLM
  - "Tanzu Application Platform"
author: Art Fewell
authorTwitter: afewell
date: 2024-01-03T11:00:18.276Z
---
*Description: Asking the chatbot questions was so 2023, time to step up to multi-agent workflows with Microsoft's awesome new multi-agent framework Autogen and it's simple, easy-to-use no code web app, Autogen Studio. We will run it on Tanzu Kubernetes Grid on vSphere using vscode dev containers to grok it with cloud server performance with a local desktop UX, strap in and come along for the ride!*

None of us will ever forget the impact AI had in 2023 ... getting access to ChatGPT I felt like Clark Kent busting out his cape, I felt like I could take on anything. And with enough time, I could have endless conversations with the chatbot and learn more than I ever thought possible. 

After we spent some time talking to the out-of-the-box chatgpt model, we learned the model didnt know everything, and we could potentially add differentiated value by finding ways to get the bots to know about things they were not trained on. So we figured out how to feed our own data to the bots all without needing a PhD or massively expensive and complex model training by using retrieval augmented generation (RAG). At first to use RAG you had to get your hands dirty, there are tons of different knobs one can turn when trying to get a chatbot to answer different types of questions about different types of data, what is the optimal chunking strategy, how do you setup a vectordb, how do you automate the retrieval and insertion of contextual data in a prompt etc etc ... but by the fall of 2023 when OpenAI introduced the assistants API and the ability to create "GPT's", now I can just log in and click a button to upload whatever documents I want the chatbot to know about and thats it. 

And I dont mean to give all the credit to OpenAI here as well before the assistants API was out scores of libraries to sdk's to simple free open source and commercial applications could let you chat with your pdf or other documents in simple and easy ways.

All of that is profoundly empowering and productivity enhancing ... if we werent all watching it unfold before our eyes it would be hard to believe that what we have seen so far is just the tip of the iceberg.

For those who jumped in the deep end in 2023, we didnt just stop with asking questions to chatbots, the next powerful realm of mindblowing potential was starting to be seen in agents (aka copilots) where you would not simply ask for a simple single response from the chatbot, but may ask for something complex that required multiple steps. With this approach you could prompt the bot with a single question and the agent could take a number of steps to try to figure out how to answer your query on your behalf. We also learned that LLM's have a powerful ability to use tools and could go far beyond just answering your questions, they could actually do things for you. 

The first highly visible project of this kind that I saw was [autogpt](https://github.com/Significant-Gravitas/AutoGPT), an awesome open source project that continues to grow today but at first, it was VERY rough around the edges. You could ask it to figure out a complex question or task and then just sit back and watch it reason with itself in a loop trying to figure out the solution, and it would try and try and try and try usually getting completely confused in the process. Nonetheless there was no doubt they were on to something big and that with further development and refinement, this approach would be nothing short of revolutionary. 

One of the biggest challenges we ran into with these approaches is, the size of the context window you can provide to an LLM is quite small. Small is relative but even [Claude's](https://claude.ai/) monstrous window size is trivial when you are trying to do complex things. But, what if instead of one bot with one limited sized prompt, you had several bots, all of which had their own seperate context windows, and these bots could work together ... well it turns out, it works quite magically well, and while mind-blowing new inference applications are coming to market every day, we are just scratching the surface of what is possible with this insanely powerful paradigm. It is a strange phenomenon as you may have dozens of agents with only one llm that you are essentially asking to switch personalities, but it works profoundly well. 

There are lots of really great frameworks and libraries for building multi-agent systems, libraries like [langchain](https://www.langchain.com/) and [llama-index](https://www.llamaindex.ai/) have extremely powerful constructs and I heartily recommend them. My focus on [AutoGen](https://microsoft.github.io/autogen/) in this post is not due to any preference or superiority, but I do think each of these frameworks has its strengths. As a point of clarity, some would say langchain and llamaindex are not multi-agent frameworks and I disagree on that but they do have a broader focus and accordingly may require some more coding than something purpose-built for multi-agent workflows like [Autogen](https://microsoft.github.io/autogen/). There are a couple of similar new multi-agent frameworks including [chatdev](https://github.com/OpenBMB/ChatDev), [agentverse](https://github.com/OpenBMB/AgentVerse), [metagpt](https://github.com/geekan/MetaGPT) and [crewAI](https://github.com/joaomdmoura/crewai) are all very interesting projects and I hope to explore and compare all of them. The reason why I am starting with AutoGen here is, all of these frameworks are new and under active development and my suspicion is that because Microsoft is massive and has a lot of resources, I anticipate this may be a bit smoother at least at this early stage of development. That may be an incorrect assumption and I plan to evaluate all of these frameworks to offer a more fair comparison soon. 

If your goal is to create a multi-agent workflow and you dont need to do more granular and low level customization, AutoGen's purpose-built focus results in a really simple and elegant model that really simplifies creating multi-agent workflows. 

And this simplicity is most pronounced in AutoGen Studio, a gui-based click, drag and drop no code playground for bootstrapping your multi-agent workflows. The AutoGen framework itself would typically consist of code you would write to create some application ... but the Studio provides a way where you can easily play around with the prompts, instructions and common settings for agents so you can easily tweek and adjust those configurations until you get them just right and can then implement your agent in your code to make workflows and applications. 

But, AutoGen Studio is really much more than just something for coders to boostrap agents with, it is an extremely powerful productivity application in and of itself. The interface is a lot like ChatGPT, and not the basic old version either, its like the new ChatGPT with the assistants API/GPT's and even more. And, its free, and it can work with just about any LLM out there so you could plug it into a quantized mixtral model on your desktop and have something a lot like ChatGPT with Assistants/GPT's and even more with its integrated workflow engine, all for free. 

I want to stress how profoundly easy it is to get started. All you need to do is have python and of course you should use a venv, and then its just 2 commands:
```
pip install autogenstudio
autogenstudio ui --port 8081
```
Now I normally die inside a little when I see instructions that say just run this pip command its so easy as, in my experience, I frequently run into python dependency hell and then 300 hours of pain and suffering later ... but, fingers crossed, this just worked for me! And if by chance it doesnt just work for you well you are in luck because that is exactly why I am going to show you how to run it in a container starting with a vanilla ubuntu container to help ensure that you can get it up and running without getting stuck in python dependency hell. 

I often will create containers to run projects such as autogen using docker desktop. But I try out a LOT of different projects and my desktop is getting super bloated with bunches of containers. At the same time, I have a lot of access to Tanzu Kubernetes clusters, so I figured why not run my dev container remotely on the k8s cluster ... well, there are reasons as it can get pretty complicated to setup, but there is an easy button ... I will show you how to connect vscode dev containers with kubernetes and it will take care of all the connectivity needs for you so when you run autogen on your k8s cluster you can just browse to localhost on your desktop and it just works ... now lets dive in!

### Setup Overview
*Please note that while AutoGen does offer support for multiple different LLM's, in this example I will use OpenAI and you will need an OpenAI API Key to follow along with the provided examples. I do plan to explore using different LLM's in future posts.*

Before we jump into the details, here is a high-level list of the steps we will be walking through:

1. Install required vscode plugins
2. Establish kubectl access to your cluster
3. Run a plain ubuntu container pod on your k8s cluster
4. Attach VS Code to the pod on your k8s cluster
5. Install and launch Autogen Studio
6. Explore AutoGen Studio

#### Install required vscode plugins

First, you will need to have visual studio code. I am not going to provide detailed explanations about using vscode so if you dont have any experience, I would recommend going through their documentation or a blog that goes over how to do basic installation and setup before proceeding. You will need 2 extensions installed in your vscode environment: Dev Containers, and Kubernetes, both by Microsoft. I have included screenshots below to help ensure you find the correct extensions.

![Dev_Containers_Extension_Screenshot](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/Dev_Containers_Extension_Screenshot.png)



![Kubernetes_Extension_Screenshot](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/Kubernetes_Extension_Screenshot.png)

#### Establish kubectl access to your cluster

Next, open a terminal in your vscode environment, and ensure you can execute kubectl commands on your desired kubernetes cluster as vscode will leverage your kubeconfig file to establish connectivity to the kubernetes cluster. 

![Kubectl_Connectivity_Screenshot](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/Kubectl_Connectivity_Screenshot.png)

#### Run a plain ubuntu container pod on your k8s cluster

*Note: If you are running Tanzu Kubernetes Grid on vSphere, you will need to disable or modify the default pod security policy to run this container. The same commands used in this post should work on any standard kubernetes cluster*

Next, run a plain ubuntu container on your kubernetes cluster:
```
$ kubectl run dev-pod --image=ubuntu -- /bin/sleep infinity
pod/dev-pod created
$ kubectl get pods
NAME      READY   STATUS    RESTARTS   AGE
dev-pod   1/1     Running   0          22h
```
*Note: Since this is just a temporary bootstrapping instance I used the imperative kubectl run command here, but if you prefer to create a deployment or workload feel free to use your preferred method.*

#### Attach VS Code to the pod on your k8s cluster

Next, open the kubernetes extension on the left sidebar of vs code, expand the cluster where you deployed the ubuntu pod, expand each node until you find the pod, then right click the pod and select "Attach Visual Studio Code" as shown in the screenshot below:

*Note: Its clearly annoying to have to go through each node to find the pod, but I havent found another way that works. One would think you could find it via workloads>pods menu, or namespaces, but neither works for me.*

![Attach_VS_Code_Screenshot](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/Attach_VS_Code_Screenshot.png)

Once you select this option it should load a new vscode window attached directly to the ubuntu pod on your kubernetes cluster.

#### Install and launch Autogen Studio

Enter the following commands to install and launch AutoGen Studio:

```
# Note that you will need to enter your OpenAI API Key or AutoGen Studio will not load correctly
export OPENAI_API_KEY=enter-your-openai-api-key-here
apt update
apt install git
apt install python3 pip
pip install autogenstudio
autogenstudio ui --port 8081
```
![Launch_AutoGen_Studio_Screenshot](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/Launch_AutoGen_Studio_Screenshot.png)

### Explore AutoGen Studio

Now if you open a web browser to [http://127.0.0.1:8081](http://127.0.0.1:8081) you should see the AutoGen Studio Web UI! Even though it is running on your remote kubernetes cluster, you can access it just the same as if you were running locally thanks to the magic of the vscode dev pod and kubernetes extensions!

This post is already getting too long to go over the AutoGen Studio in detail, but I will cover a quick overview here and will write another post soon to explore the interface in more detail. 

Please reference the screenshot below, the numbers shown in the image correspond to the explanations:
*Note: The steps below reflect the default installation experience at the time of writing. This project is under active development so the default experience may change.*

![AutoGen_Studio_UI_Playground_Tab_Screenshot](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/AutoGen_Studio_UI_Playground_Tab_Screenshot.png)
1. When you launch the web UI, it lands on the Playground tab by default. 
2. In the main body of the page, you can see a chat client where you can enter queries
3. Observe that by default the Visualization Agent Workflow is selected. This means that when you enter a query in the (2) chat window, it will use this workflow to process your request. Different workflows can use different models, skills and settings for handling your query.
4. The "Sessions" section of the nav bar allows you to create multiple different chat sessions. This is very similar to how you can use multiple tabs with ChatGPT to organize different conversation topics and threads. 


Now that we have observed the layout of the playground tab, lets try having a conversation with our agent. Since the workflow is set to the "Visualization Agent Workflow", that implies the agent should use the mixed-mode capability of GPT4 to create images. 

Just for fun I will try to ask the question "please create some abstract art that expresses the wonder and joy of multi-agent workflows and kubernetes!". If you are following along note that it may take some time for this query to complete, and when it does, you will notice that this did not work! Also note your error message may not be exactly the same as mine, thats ok, we will fix the issue in the next step:
![AutoGen_Studio_Failed_Query](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/AutoGen_Studio_Failed_Query.png)

The reason this failed is just because there is a setup step we need to do when we first load up the studio, but, before we fix it, there are some important details to review in the above screenshot. Observe in the Agent's response there is a block that says "Agent Messages (9 Messages)" ... which is extremely cool and highlights that this is not your typical chatbot, it is an agent, which means that when you ask the agent something, it may run through a number of thoughts and actions while trying to fulfill your request. The standard view of the chat window will display your input and the final agent response, but the output will also include the expandable "Agent Messages" block which you can expand to see each thought and action taken by the agent to formulate the final response. 

Another important detail here is, you may have noticed that the agent took a while to respond during which time, the AutoGen Studio UI had an indicator it was working, but you could not see what it was doing, the UI only displays the agent messages after the request is complete ... but, if you open your vscode window while a query is being processed, you can see the agent messages displayed in realtime while the response is being formulated!

![VS_Code_Output_Log_Screenshot](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/VS_Code_Output_Log_Screenshot.png)

Now, lets fix the problem so we can get some abstract kubernetes art to enjoy!

In the AutoGen Studio UI, navigate to the Build tab and on the left navbar, select the Skills tab. Observe that there is a skill called generate_images. Feel free to examine it, but for now the main observation is that this skill exists, I will explore more detail about skills in the future:

![Skills_Screenshot](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/Skills_Screenshot.png)

Now on the nav bar, select the `Workflows` tab and open the `Visualization Agent Workflow`. Observe that in the right column, the "Reciever" is the "visualization_assistant". Scroll to the bottom of this column to the "Skills" section and observe that by default (at the time of writing) this workflow does not give our visualization assistant any skills! No wonder it couldnt create the image! Go ahead and click the `add+` button and add the `generate_image` skill, and then select OK to update the workflow.  

![Visualization_Agent_Workflow_Screenshot](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/Visualization_Agent_Workflow_Screenshot.png)

![Add_Skill_Screenshot](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/Add_Skill_Screenshot.png)

Now that we have added the generate_images skill, lets return to the Playground tab and see if the agent can complete our image request!

On the Playground tab of the UI, I will ensure that the Visualization Agent Workflow is selected. To have a clean session, I will select the option to delete the previous failed query, and click the `New+` button to create a new session. Now I will ask the question again to see if our update image can generate the image. If you are following along, I recommend opening your web UI side by side next to your vscode window so you can observe the terminal output of the agent processing the request.

The screenshot below shows the result of our query! If you followed along, since this query requests abstract art, each response to this same query will yield very different and unique responses!

![Query_Result_Screenshot](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/Query_Result_Screenshot.png)

The final piece of the UI I did not cover is the Gallery tab. To understand this you can see that on the playground tab, just beneath your session, you can see the option to either delete or publish the session, and if you publish it, the session can be saved on the Gallery tab, where it can be persisted. Note that in our case since we are working on a kubernetes pod and we did not provision a persistent volume, there is no way for it to persist data, but if you would like to be able to persist data you could install this locally on your desktop or provision the kubernetes pod to use a persistent volume. 

While we have only barely touched on the capabilities of the Studio UI or the even broader capabilities of the AutoGen framework, we have learned enough to get started playing and experimenting with how to create multi-agent workflows! 

This is the first of many posts I hope to publish on the Autogen framework, and in the meantime I hope you take time to explore AutoGen Studio and start putting AI to work for you! Thanks for reading!
