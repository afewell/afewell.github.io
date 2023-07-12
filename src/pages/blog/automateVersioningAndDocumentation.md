---
layout: $/layouts/post.astro
title: "Automate Versioning and Documentation for gitops with Semantic Release and Github Projects"
description: "Learn how to use github projects and semantic release to simplify and automate versioning and documentation for your" 
# there MUST be at least 1 tag listed or it will not render
tags:
  - GitOps
  - "Platform Engineering"
  - Kubernetes
  - "Github Projects"
  - Agile
  - Semantic release
author: Art Fewell
authorTwitter: afewell
date: 2023-07-24T08:00:18.276Z
---

A well-documented project is like a well-oiled machine. It's vital for smooth collaboration and efficiency. But documentation can be time-consuming, especially when we're also racing against the clock to push out features and updates. Thankfully, I've stumbled upon a solution to this challenge that I am thrilled to share with you. It's a nifty little combination of semantic release and GitHub projects.

Before I go further I should mention I also created a demo video that shows the solution discussed here, [you can find it here](https://youtu.be/JT-THsrR04M).

First off, let's look at the project I'll be using as an example today. It's a chatbot project that I've developed as an accelerator, which is a kind of template that people can download, iterate on and then build. I also set this up so that the accelerator itself is versioned and when developers use this accelerator to create their own implementations, it sets up automated versioning for their new projects. 

Now, here's where the magic happens. When you make your commits, leave useful commit messages. Semantic version will automatically generates a tidy changelog for you.

![Changelog](https://raw.githubusercontent.com/afewell/afewell.github.io/blob/main/public/images/changelog.png)

Observe that each commit is nicely organized along with the notes in the changelog, making it much easier to find exactly what changes were made, why and when. Further, issue tickets are nicely linked here as well, and when you leverage github projects you can easily combine planning with additional notes to provide a solid set of informal documentation for the fellow users of your project.

It doesn't just stop there— it also packages a release that encapsulates your code at that particular point in time. This mechanism also generates a tag that you can use to navigate to different points in your project's history, just like you would with branches.

While these capabilities alone do a great job, combining semantic release with github projects can bring it to the next level.  Github projects offers multiple different views from the same dataset including kanban boards and a roadmap view, but my favorite has become their simple default task list view. 

![Github Projects Task List](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/projects_task_list.png
)

Here, you can plan out the next things you want to work on for your project very quickly and easily while ensuring that your rational and intent for planned changes is captured in your automated documentation. You can easily convert these tasks to issues, which can automatically be included in your changelog to provide additional documentation for each change made to your repo. I try to always create a project task for planned changes, even a simple note can become invaluable in any case where understanding the reason for a change becomes important, and if you make this a habit its quick, easy, and it can really simplify your commit messaging knowing that you can reference the project task you created during planning. 

Semantic release requires that you enter a keyword with your commit message to trigger a release, I can use "fix:" for patch release, "feat:" for a minor release, and "BREAKING CHANGE:" for a major release. This syntax is part of a popular standard for commit messaging known as [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/).

This makes it really easy when I want to trigger a release, while at the same time the process makes it simple to batch multiple commits into a common release. If you dont want to trigger a release, dont include the keyword in your commit message. When you do decide to trigger a release, semantic version will automatically include every commit since your last release. This works regardless of whether you are commiting to main or doing feature development on a branch. 

Let me walk you through the process. First I use github projects to create a task list for updates I am planning and convert the note into an issue and get a unique issue number. Then I open up VS Code, add my changes, and make a commit. 

Here is an example commit message: `fix: Updating references to my-chatbot-1 to resolve #3`. Because I included the "fix:" preamble, the message will trigger semantic version to create a release, update the version number, and update the changelog. Also because the commit message includes "resolve #3", this will automatically close the associated issue ticket, ensure the issue ticket is referenced in the changelog, and because the issue gets closed it shows as completed on my github projects task list!



So how do you set this up? It's pretty simple, you just need two files, both of which you can copy from my repo. First, you need to add a GitHub workflow for semantic release. After experimenting with a few different versioning options in the github actions marketplace, I decided on using [this action which you can learn more about by clicking here](https://github.com/marketplace/actions/action-for-semantic-release). If you would like to setup a project like mine, you can [copy the action from my repo by clicking here](https://github.com/afewell/chatbot-1-accelerator/blob/main/.github/workflows/semantic_release.yml) as I have configured it with the plugins required to provide the features discussed in this post. Also note that you will need to configure your github repo settings to enable workflows and to enable write permissions for actions, as semantic release will need to push updates to your repo to write the changelog. You can find this setting by clicking in the settings tab for your repo, select Actions > General, and then in the workflow permissions section, select the option for `read and write permissions`.

You will also need a configuration file named releaserc.json in the root of your repo. This configuration allows you to link to Git commits and code revisions, trigger releases with each conventional commit message, and automatically update the changelog and create a release package. Semantic version also has a lot of other features you could use if desired, including integration with many popular programming languages. I recommend looking at the [marketplace page for the semantic version action](https://github.com/marketplace/actions/action-for-semantic-release) which has information on additional configuration options. But if you just want to use the features I have shown in this post, you can simply [copy the releaserc.json from my repo](https://github.com/afewell/chatbot-1-accelerator/blob/main/.releaserc.json), just be sure to change the releaseUrl value to the URL for your repo. 

I hope this tutorial helps you strike the right balance between documentation and speed in your GitOps projects. I believe this approach, while simple, can make a big difference, keeping our projects well-documented and our development process speedy. Let's keep creating, innovating. Happy coding!