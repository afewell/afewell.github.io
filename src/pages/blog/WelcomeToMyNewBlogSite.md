---
layout: $/layouts/post.astro
title: Welcome to my new blog site
description: Introducing the new Art of Tanzu blog site, scope, plans & vision. 
# there MUST be at least 1 tag listed or it will not render
tags:
  - Intro
author: Art Fewell
authorTwitter: afewell
date: 2022-11-19T08:00:18.276Z
---

Hi, My name is Art Fewell, pleased to meet you. I am starting this blog mostly to share info I learn about tech stuff. I do have a life beyond work, but I am fortunate to work doing what I love. And so my primary hobby just happens to coincide with what I do for work. 

At my job I spend a lot of time working on and learning about cloud native technologies, digital transformation, and VMware Tanzu solutions. Most of what I do for work is for official projects, and I am starting this blog because in addition to the official projects I work on, I have a number of personal projects I would like to take on that I think will be fun and useful for the community. 

Another key reason for this blog is, while I am working on various demos and projects, I have a ton of things I learn that may not be the focus of my work project. I know all of these learning experiences I have are super valuable for me and I hope they can be helpful to others like me who are out there trying to keep up with and lead in our shared journey into the next generation of application and infrastructure technologies. 

## A shared learn-by-doing experience

I am launching this site with an initial project, a journey into Tanzu Application Platform. Until recently, I worked as a generalist across the entire Tanzu family of products. While I did get to learn a lot about the entire Tanzu Portfolio, I did not get to have the depth of focus I wanted to on all the products. 

I want to be able to go beyond the lab into quasi-production scenarios to maximize my own understanding and hopefully be able to bring practical guidance to the community of Tanzu Operators and Platform Engineers. Accordingly I recently adjusted my role on my team to focus primarily on Tanzu Application Platform (TAP). 

While I have heard a lot and read a lot about TAP, and even done some spoon-fed lab exercises, I had no meaningful hands-on experience with it. There are lots of moving parts in TAP and tons to learn. As I write this, I am still very much a beginner, but my role allows me to spend a lot of time and have direct access to the engineering teams that build, deliver and support the product across a wide array of enterprise environments, and so I hope I can help bring the benefits of my own accelerated learning environment to the community through this blog. 

## A Platform Engineering perspective

I have been focused primarily on cloud native tech for over 6 years now, but the 15+ years prior I was primarily focused on networking with some systems and database administration. 

I have spent the past several years focused on building developer platforms and elevating the developer experience. I think a lot of media over the past years has made it sound like this is a topic for developers, but I would argue that it is really an operations function, and it needs the expertise of people with both development and operational backgrounds. 

The rise of devops popularized the idea of the developer working on ops - but even if a developer team skipped past their IT org and went straight to a cloud provider, somebody still needs to setup and configure the account and VM templates and IAM roles and on and on. And the vast majority of developers do not want to setup their infrastructure, toolchains, processes etc, they want their organization to provide good tools and processes so they can focus on their own code and project goals. 

The truth is, there have always been some people in the developer organization that focused on toolchains and processes and the operational side of development. Likewise, there were always some people on the IT ops teams focused primarily on supporting developer needs. The key benefits and advancements achieved in devops models, in my opinion, were not about making developers do ops, but rather to provide a substantially improved operational model by which operational and developer functions could work together in a streamlined continuum.

An ideal platform engineering team is made up of people from both ops and dev backgrounds. It is an ideal role for those who from the developer side enjoy working on tech stacks, build pipelines and improved processes that automate and streamline all of the needed requirements to get code from check-in to production. Likewise, the platform engineering team needs people with solid experience in ops with a desire to automate operational delivery and innovative process improvements to continually improve and accelerate service delivery and consumption.

Whether you come from a dev or ops background, an ideal platform engineering team needs people from both backgrounds - not to remain as seperate teams from seperate backgrounds, but to form a new type of team with hybrid skills and a new culture driven from the common goal and earnest desire to implement innovative methods and drive continuous improvement in agility and efficiency and organizational impact.  

## Now to the fun part

I want to build and host this site using TAP. And more, I want to set up a brand new full stack Tanzu environment to host the production site, and use this blog to chronicle the process of setting up the Tanzu for Kubernetes Operations (TKO) and TAP environments that I want the blog to run on. 

This creates a chicken and egg scenario as its hard for me to use this blog to chronicle the experience of setting up my environment when I need the blog to be live before the target hosting environment. So at launch, I am hosting with github pages. Over the next several posts, I will document the setup of the TKO and TAP environments and cover topics like how to use gitops for your cluster setup with flux, how to setup simple semantic versioning for your infracode and scripts, and how to implement CI/CD for a variety of different frameworks and applications I hope to play with in the future. 

Over the coming days and weeks I will be adding new posts that chronicle my own journey into Tanzu Application Platform along with various lessons learned that I hope can help others learn and advance in our shared journey to embrace and deliver the latest technologies.

Thanks for reading, I look forward to engaging with all of you as I embark on this journey!

