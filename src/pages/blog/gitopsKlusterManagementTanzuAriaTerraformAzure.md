---
layout: $/layouts/post.astro
title: "Gitops-based Kubernetes Cluster lifecycle management with Tanzu, Aria Automation, Terraform and Azure"
description: "This post walks through setting up infrastructure as code deployments of Tanzu Mission Control managed Kubernetes clusters using Aria Automation and Terraform. It provides a step-by-step guide on connecting a Git repo to Aria, enabling the Terraform service, creating Terraform files to deploy an Azure Kubernetes Service cluster with Tanzu Mission Control, importing the Terraform into an Aria blueprint, and deploying the cluster. The author shares their hands-on experience and lessons learned from using Aria Automation to implement a GitOps-based workflow for provisioning lifecycle managed clusters. Key highlights include Aria's support for Terraform, secrets management, and its robust platform capabilities that enable creating custom automations." 
# there MUST be at least 1 tag listed or it will not render
tags:
  - VMware
  - Tanzu
  - Tanzu Mission Control
  - Tanzu Application Platform
  - Tanzu for Kubernetes Operations
  - Kubernetes
  - Aria Automation
  - Aria Assembler
  - Aria Pipelines
  - Aria Service Broker
  - Terraform
  - Azure
  - Azure Kubernetes Service
  - ABX Actions
  - Aria Blueprints
  - Infrastructure-as-code
  - Gitops
author: Art Fewell
authorTwitter: ACMTechZone
date: 2023-10-04T08:00:18.276Z
---

I've been working on some projects lately using gitops across the Tanzu Portfolio. Most of what I have been working on has been using gitops to customize my cluster and manage applications after I have deployed the cluster. But I have been mostly creating my clusters with clickops. Tanzu Mission Control (TMC) provides really easy ways to provision and lifecyle manage kubernetes clusters on vSphere, AWS and Azure all from the gui. Nearly all large organizations manage a lot of their infrastructure config through their SaaS provider gui and there is nothing wrong with that, but for this project I want to do end-to-end automation and gitops rather than using a graphical interface. I can use gitops and still take advantage of all the rich features from TMC either by using its API's directly or by using the [Tanzu Mission Control Terraform Provider](https://registry.terraform.io/providers/vmware/tanzu-mission-control/latest).

While both are great options, the terraform provider already has a lot of the capabilities I desire built in like being declarative, having a pretty straight forward yaml configuration, having a lifecycle management model ... but, in order to take advantage of lifecycle and state management capabilities, you need infrastructure in place to provide those services. Fortunately, Aria Automation has built-in support for terraform! I have used Aria Auto for years and am a big fan of the solution overall, some may wonder why Aria to manage terraform and for me personally, I love the flexibility of the Aria solution to support so very many different automation capabilities in a common easy to use platform. 

Beyond its native blueprinting service, Aria automation supports a huge range of configuration management options including terraform, puppet, ansible, its own native blueprinting capabilities for a broad range of out-of-the-box vsphere, aws, azure and gcp services. Further, VMware purchased popular configuration management company Salt and now has the entire saltstack portfolio fully integrated including the powerful new open source configuration language from the salt creators known as "Idem". And beyond traditional config management solutions, Aria includes a powerful eventing and faas based framework for custom resource management. Aria provides simple low code interfaces that empower Platform Engineers(PE's) to easily create event-driven faas-based services built on advanced cloud native patterns. 

With this framework PE's can create custom resources by entering in a few form fields and providing functions for the create, read, update and delete operations for that object, the Aria platform does all the rest of the heavy lifting. It provides a cloud-consumer like interface with the service catalog which also provides the advanced identity and policy capabilities that large organizations require. It organizes deployments by user and projects allowing users and project owners to easily identify the state and execute lifecycle management actions against custom objects. You can also easily provide functions that can be used as day-2 actions on deployed objects ... you can add custom actions both to custom resource types and to any other of the many different types of objects you can create and manage including any resources you create with the terraform service for example. 

The faas-based "ABX actions" solution inherently abstracts the functions provided for custom resources and custom actions and can automatically execute the functions on AWS Lambda, as Azure Functions, or on your own kubernetes cluster. You can define metadata to leverage metadata-based routing if you want to automate where or how functions are executed. These custom faas-based services can be triggered manually, or by creating a subscription to an event using the kafka (or rabbitMQ when on-prem) based eventing framework that provides event triggers for all the lifecycle management events for all the various objects supported in the framework along with the ability to create custom events and other platform capabilites to tie in git, registry or gerrit-based webhooks. The service leverages kafka to provide reliable message delivery to event subscribers and makes it easy to trigger custom actions based on lifecycle events to bring infrastructure automation capabilities to the next level. 

If that werent enough, you can also leverage Aria Pipelines to provide robust CICD pipeline capabilities. Pipelines can include elements with custom vm and container builds that can automate pretty much anything that can be automated. And while I love the flexibility of pipelines, it does highlight the immense value in Aria Assembler's configuration management and custom resource toolsets as those help PE's tackle the hardest part of infracode ... which is full lifecycle management. Its not all that hard to create some deployment scripts and deploy things, but to reliably maintain the state and handle all configuration changes and lifecycle management tasks needed for all deployed objects is profoundly more complex, so having the platform handle those parts is ideal for me as a consumer of the service.  

The most valuable part of Aria Automation overall in my opinion however is not its support for so many popular frameworks and powerful extensibility, its the elegant core platform features that allow you to compose all of these different modular components together so that you can create virtually any type of cloud service and deliver a cloud-provider like consumer experience for your own custom environment.

The main point of my post today is to share how I setup an Aria blueprint that uses the Tanzu Mission Control terraform provider to create a service that can allow myself or other users to deploy TMC lifecycle-managed kubernetes clusters based on an infrastructure-as-code and gitops methodology. While one does not require a graphical interface to use infracode or gitops, I really prefer to have the benefits of both approaches, and that capability is one of the things I love most about Aria Automation. Aria provides graphical interfaces that lets users who prefer the GUI use the gui but then trigger the same underlying gitops-based automations to deliver a service.

## Environment Setup

Here are the high level steps I went through to setup this service:

1. Connect your git repo to Aria Automation
2. Enable Terraform-based deployments in your project
3. Create your terraform files and save them in the connected git repo
4. Create an aria assembler blueprint and import your terraform file
5. Deploy! (Optionally, you can also expose the ability to deploy through Aria Service Broker)


### 1. Connect your git repo to Aria Automation

1. Login to VMware Cloud and Navigate to Aria Automation Assembler
2. On the `Infrastructure` tab, select `Integrations`
3. Select the `+ ADD INTEGRATION` button
4. Select the type as `GitHub` (GitLab is also supported)
5. In the `Name` field enter the name for your username or github org name if your repo will be saved under an organization. 
6. In the `Server URL` field enter the value `https://api.github.com` for github, or the appropriate API value for gitlab. 
7. Enter an API Token for the github/gitlab account with appropriate permission.

Below please find a screenshot of my github integration configuration for your reference:
![Enable Aria GitHub Integration](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/enable_aria_github_integration.png)

### 2. Enable Terraform-based deployments in your project

Enabling Terraform in your project is very simple:

1. Login to VMware Cloud and Navigate to Aria Automation Assembler
2. On the `Infrastructure` tab, select `Projects`
3. Select your project and navigate to the `Provisioning` tab
4. Scroll to bottom of the page and in the section titled `Cloud Zone Mapping for Template Terraform Resources`, Enable the toggle to `Allow terraform cloud zone mapping` as shown in the image below:

![Enable Terraform for Aria Project](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/enable_terraform_for_aria_project.png)

5. Select the `Integrations` tab and click `Add Repository`. Note you will need to connect Aria to your git provider as shown in section 1 before you will be able to add the repository here.

On the Add Repository pane, set the following values:
- Type: `Terraform configurations`
- Repository: The `username/reponame` value for your git repo. For example, the full url for my repository is [https://github.com/afewell/opsdev.git](https://github.com/afewell/opsdev.git) where `afewell` is my username and `opsdev` is the name of my repository. Accordingly the value I put in the Repository field as shown in the image below is `afewell/opsdev`
- Branch: The name of the git branch you would like to use
- Folder: The subdirectory where your terraform files will be located within your repo. In my case I created a folder at the root of my repository named `terraform`. All of the terraform files you want Aria to access must be located within this directory. You can place multiple terraform files within this directory, or organize them into sub-folders that you can define in the blueprint. Note that Aria only allows one level of subdirectories nested within the top-level terraform directory to organize your terraform files, you cannot have complex multi-level nesting schemas. 

Here is an example image from my environment:

![Add Terraform Repository to Project](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/add_terraform_repo_to_project.png)


### 3. Create your terraform files and save them in the connected git repo

Now for the fun part, lets review the terraform needed to manage an Azure Kubernetes Cluster with the Tanzu Mission Control terraform provider. In this demo, I used the Azure module and deployed an AKS cluster, but the process is almost exactly the same for deploying AWS EKS or vSphere clusters through TMC and in the future I hope to share some follow-ons to this post with examples for vSphere and EKS clusters. 

If you have previous terraform experience, the [TMC Terraform Provider](https://registry.terraform.io/providers/vmware/tanzu-mission-control/latest) and the Aria Assembler Terraform service should both feel very natural to you. The TMC provider configuration felt similar to most other terraform providers I have used, and using the Aria Terraform Service is just like doing it from my own desktop, I use the same terraform file with no special formatting. One thing to take into consideration is that the Aria Terraform Service executes the terraform plan and apply commands against a directory you specify with terraform files in it, you do not have the ability to execute other terraform commands and should organize your terraform files accordingly. 

Before I proceed I want to highlight a couple of great guides written by my teammates [Corey Dinkens](https://apps-cloudmgmt.techzone.vmware.com/users/corey-dinkens) and [Scott Rogers](https://apps-cloudmgmt.techzone.vmware.com/users/scott-rogers) about the TMC Terraform Provider. Their guides combined with the great provider documentation made it really easy for me to setup:
- [Terraform, GitOps, Helm: Automation and package management with VMware Tanzu Mission Control](https://tanzu.vmware.com/content/blog/tanzu-mission-control-automation-and-package-management)
- [Automate Kubernetes Platform Operations with Tanzu](https://apps-cloudmgmt.techzone.vmware.com/blog/automate-kubernetes-platform-operations-tanzu)


#### Exploring the terraform files

You can find the terraform files I used in my environment here: [https://github.com/afewell/opsdev/tree/main/terraform/tmc-akscluster]

If you examine the above link you can see I created a main.tf and a vars.tf file. I prepared these files to expose the more commonly configured attributes of the akscluster module in the TMC Terraform Provider. 

First, lets review the top part of the main.tf file:
```
terraform {
  required_providers {
    tanzu-mission-control = {
      source  = "vmware/tanzu-mission-control"
      version = "1.2.3"
    }
  }
}

// Basic details needed to configure Tanzu Mission Control provider
provider "tanzu-mission-control" {
  endpoint            = var.tmc_endpoint
  vmw_cloud_api_token = var.vmw_cloud_api_token
}
```
Here you can see the standard terraform syntax to define which terraform provider you are using and how to authenticate to the provider. Aria Assembler supports any terraform provider published in the terraform registry, or there is a method available to upload a zip file with your custom provider. In this case the TMC provider is located in the official terraform registry so its easy to specify, and I just copied the version number from the provider documentation. Remember this is the version number of the terraform provider plugin, not the version of terraform itself. 

One additional highlight here is that the variable value used here for the provider token is being injected by the Aria Assembler secrets service ... I will go into more detail on that when I review the vars.tf file below. 

First, lets review the remainder of the main.tf file which specifies the configuration values for the akscluster module:
```
resource "tanzu-mission-control_akscluster" "aks_cluster" {
  credential_name = var.azure_credential_name
  subscription_id = var.azure_subscription_id
  resource_group  = var.azure_resource_group
  name            = var.cluster_name
  meta {
    description = var.cluster_description
    labels      = var.cluster_labels
  }
  spec {
    cluster_group   = var.cluster_group_name
    config {
      location           = var.cluster_location
      kubernetes_version = var.kubernetes_version
      network_config {
        dns_prefix = var.cluster_dns_prefix
      }
    }
    nodepool {
      name = var.nodepool_1_name
      spec {
        count   = var.nodepool_1_count
        mode    = "SYSTEM"
        vm_size = var.nodepool_1_vm_size
        os_disk_size_gb = var.nodepool_1_node_disk_size_gb
        auto_scaling_config {
          enable    = var.nodepool_1_enable_auto_scaling
          max_count = var.nodepool_1_max_node_count
          min_count = var.nodepool_1_min_node_count
        }
      }
    }
  }
}
```
If you have created an AKS cluster, especially if you have done so through TMC before all these values should look pretty familiar to you as these are the same options you can select through the GUI just in terraform format. 

One important point to note here is that before this will work, you have to configure Tanzu Mission Control with a credential for Azure, I almost forgot to mention that because I already had it setup long before this exercise. You must have the azure credential configured within TMC, and you can view the credential in TMC to identify the azure credential name and subscription ID. The same would be true for vSphere or AWS. 

Most of the additional fields shown for the akscluster module are pretty straightforward so I want go into more detail but please reach out if you have any questions. 

Now we have reviewed the main.tf file, lets examine the vars.tf file and how the Aria Terraform Service handles terraform variables. 

Aria wraps the terraform code within an Aria Blueprint which provides a lot of additional functionality outside of terraform. For example, Aria provides a really nice form service allowing the service creator to make a simple form or wizard to make it easy for users to create a deployment using the terraform template. The GUI for the forms provides both a code and a form view for the user to enter the data in the way they are most comfortable. The service also provides a visual forms designer so you can customize forms just how you like. Aria also provides an elegant REST API that allows you to instantiate the service and provide values per your defined schema with API calls. Aria also provides input and output bindings allowing the blueprint to be called by other services, resources, actions or pipelines enabling you to combine the various capabilities of the Aria portfolio into combined workflows and recipes!

The blueprint itself is another item that must be managed in addition to the terraform files. It is a thin layer of markup and a small configuration to manage for the powerful benefits it provides but is something you have to consider when you are setting up the solution. 

The blueprint plays a central role in how you manage your terraform variable bindings as any time you or some automation calls this blueprint this will bind the blueprint inputs to the variables you define in terraform. Or in other words, you will need to define your variables in terraform, and also define them in the aria blueprint. When a user instantiates the blueprint from a service catalog or rest call for example, they are communicating with the blueprint service, which will then pass and bind values to the terraform variables. 

Defining variables in Aria is simple and very similar to terraform, and to make it even easier, you can define your vars in terraform and use the import function in Aria Assembler and it will automatically create the variable definitions for the blueprint. Keep in mind the import operation is a one-time operation, and after the initial import service owners will need to ensure they keep the variables in sync between the aria blueprint and the terraform file. 

Here is my vars.tf file:
```
variable "terraform_tmc_version" {
  type        = string
  description = "Terraform TMC Provider Version"
  default = "1.2.3"
}

variable "tmc_endpoint" {
  type        = string
  description = "TMC endpoint URL"
  default = "tanzutmm.tmc.cloud.vmware.com"
}

variable "vmw_cloud_api_token" {
  type        = string
  description = "VMware Cloud API Token"
  sensitive   = true
}

variable "azure_credential_name" {
  type        = string
  description = "TMC Credential Name for Azure Account"
  default     = "afewell-azure"
}

variable "azure_subscription_id" {
  type        = string
  description = "Azure Subscription ID"
  sensitive   = true
}

variable "azure_resource_group" {
  type        = string
  description = "Azure Resource Group"
  default     = "genaissance"
}

variable "cluster_name" {
  type        = string
  description = "Enter a name for the cluster that will be created"
  default     = "my-new-aks-cluster"
}

variable "cluster_group_name" {
  type        = string
  description = "Enter the name for the cluster group the created cluster will be associated to."
  default     = "genaissance"
}

variable "cluster_description" {
  type        = string
  description = "Enter a description for this cluster"
  default     = "Enter a description for this cluster"
}

variable "cluster_labels" {
  type        = map(string)
  description = "Enter any labels for this cluster"
  default     = {
    key1 = "value1"
    key2 = "value2"
  }  
}

variable "cluster_location" {
  type        = string
  description = "The Azure Region where the cluster will be deployed"
  default     = "westus2"
}

variable "cluster_dns_prefix" {
  type        = string
  description = "DNS Prefix for cluster"
  default     = "westus2"
}

variable "kubernetes_version" {
  type        = string
  description = "Kubernetes Version for this cluster"
  default     = "1.26.6"
}

variable "nodepool_1_name" {
  type        = string
  description = "TMC Credential Name for Azure Account"
  default     = "systemnp"
}

variable "nodepool_1_count" {
  type        = number
  description = "Number of nodes, ignored if autoscaling"
  default     = 3
}

variable "nodepool_1_vm_size" {
  type        = string
  description = "VM size for nodepool 1 nodes"
  default     = "Standard_A2m_v2"
}

variable "nodepool_1_node_disk_size_gb" {
  type        = number
  description = "OS Disk Size in GB to be used to specify the disk size for every machine in the nodepool. If you specify 0, it will apply the default osDisk size according to the vmSize specified"
  default     = 150
}

variable "nodepool_1_enable_auto_scaling" {
  type        = bool
  description = "Enable auto-scaling for this cluster (true or false)?"
  default     = true
}

variable "nodepool_1_max_node_count" {
  type        = number
  description = "Maximum number of nodes for this cluster"
  default     = 5
}

variable "nodepool_1_min_node_count" {
  type        = number
  description = "Minimum number of nodes for this cluster"
  default     = 1
}
```

As you can see these are standard terraform variable declarations. One thing Ive learned after my initial use of these is that going forward I dont think its a good idea to define the default values within terraform unless you have some specific need to. The reason why is you will also need to create default values in the Aria blueprint which would override any default values specified in terraform directly and be a potential source of confusion, in addition to needing to manually keep the default values in sync after the initial import, I think it would be easier to keep the default values exclusively in the Aria blueprint and I will probably change my setup to reflect that at some point. 

Next lets look at how to import the terraform files into an Aria blueprint. 

### Create an Aria Assembler blueprint and import your terraform file


Now lets look at how to import the terraform files:

1. Log into Aria Automation Assembler
2. On the design tab select the option for `New From Terraform`

![new_blueprint_from_terraform](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/new_blueprint_from_terraform.png)

3. Enter the desired name and description for the terraform object and select the same project you enabled for terraform in step 1, as shown in the following image and then click next.

![new_blueprint_from_terraform_wizard_p1](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/new_blueprint_from_terraform_wizard_p1.png)

4. Select the repository where your terraform files are located, the commit ID for the git commit with the correct version of your terraform files, and the source directory where your terraform files are located. 

Note that the fields on this screen have dynamic selectors that only display relevant values. The value for the repository will automatically appear in the pulldown based on the integration and project add repository steps we covered in sections 1 and 2 of this document. The commit ID will automatically populate the most recent commit ID relevant for the terraform files found. The Source Directory field will dynamically display subdirectories nested directly (only 1 level deep) within the terraform directory defined in the Project/Repository settings as shown in section 2 of this document. 

Here is a screenshot of my setup for your reference:

![new_blueprint_from_terraform_wizard_p2](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/new_blueprint_from_terraform_wizard_p2.png)

The final 3rd page of the wizard to import our terraform files is shown in the screenshot below:

![new_blueprint_from_terraform_wizard_p3](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/new_blueprint_from_terraform_wizard_p3.png)

Observe that the above screenshot shows a preview of the import operation where we can see details of the terraform file we previously saved on github now visible in Aria, you can specify the terraform version to use and verify key details from your terraform file such as provider details and most importantly that the variables imported from your vars.tf file look correct. 

One key detail to note is the "Sensitive" column, which in this case is referring to how the Aria blueprint input will treat the variable, checking this box does not change anything in your vars.tf file. I did have a couple vars in my vars.tf file marked as sensitive in my terraform variable declarations, and it did not automatically select the sensitive checkbox when importing. I am not sure if its supposed to as I am not an expert on Aria but in any case its important to understand what happens when you check the sensitive column to ensure it aligns with your secrets management strategy. 

If the Sensitive column is checked/true for a given variable, then when the input variable is declared in the blueprint, it will have the attribute `encrypted`. I think the main purpose of the encrypted attribute is to ensure the user input form properly handles the input form in cases where a user would manually type in the secret into the form. 

In my configuration I am not defining any blueprint-level inputs for my secrets because I am injecting the secrets directly from the Aria secrets service as I will explain further when we get to the input bindings section of the blueprint. 

Regardless of how secrets are injected by Aria, they will still need to be accessible to terraform which means you should still declare your secret variables in terraform and be sure to mark them as Sensitive within terraform. 

After you complete the import, a new blueprint will be created. Here is the first part of the blueprint that was automatically created when I imported my terraform file:
```
inputs:
  terraform_tmc_version:
    type: string
    default: 1.2.3
    description: Terraform TMC Provider Version
  tmc_endpoint:
    type: string
    default: tanzutmm.tmc.cloud.vmware.com
    description: TMC endpoint URL
  azure_credential_name:
    type: string
    default: afewell-azure
    description: TMC Credential Name for Azure Account
  azure_resource_group:
    type: string
    default: genaissance
    description: Azure Resource Group
  cluster_name:
    type: string
    default: my-new-aks-cluster
    description: Enter a name for the cluster that will be created
  cluster_group_name:
    type: string
    default: genaissance
    description: Enter the name for the cluster group the created cluster will be associated to.
  cluster_description:
    type: string
    default: Enter a description for this cluster
    description: Enter a description for this cluster
  cluster_labels:
    type: object
    default:
      key1: value1
      key2: value2
    description: Enter any labels for this cluster
  cluster_location:
    type: string
    default: westus2
    description: The Azure Region where the cluster will be deployed
  kubernetes_version:
    type: string
    default: 1.26.6
    description: Kubernetes Version for this cluster
  nodepool_1_name:
    type: string
    default: systemnp
    description: TMC Credential Name for Azure Account
  nodepool_1_count:
    type: number
    default: '3'
    description: Number of nodes, ignored if autoscaling
  nodepool_1_vm_size:
    type: string
    default: Standard_A2m_v2
    description: VM size for nodepool 1 nodes
  nodepool_1_node_disk_size_gb:
    type: number
    default: '150'
    description: OS Disk Size in GB to be used to specify the disk size for every machine in the nodepool. If you specify 0, it will apply the default osDisk size according to the vmSize specified
  nodepool_1_enable_auto_scaling:
    type: boolean
    default: true
    description: Enable auto-scaling for this cluster (true or false)?
  nodepool_1_max_node_count:
    type: number
    default: '5'
    description: Maximum number of nodes for this cluster
  nodepool_1_min_node_count:
    type: number
    default: '1'
    description: Minimum number of nodes for this cluster
```

As you can see the format to create inputs in an Aria blueprint is similar to Terraform and pretty simple, and there are a ton of additional options beyond what I will explore here to provide advanced form controls to improve the user experience. 

All the variables you see here were automatically imported when I imported the terraform file. 

The above blueprint section defines the input variables but not the bindings. Lets now examine the final section of the blueprint code which defines the terraform version, the input bindings, the git integration, commit id, and directory of the terraform files that will be used for the blueprint:

```
resources:
  terraform:
    type: Cloud.Terraform.Configuration
    properties:
      variables:
        terraform_tmc_version: ${input.terraform_tmc_version}
        tmc_endpoint: ${input.tmc_endpoint}
        vmw_cloud_api_token: ${secret.afewell_vmw_cloud_api_token}
        azure_credential_name: ${input.azure_credential_name}
        azure_subscription_id: ${secret.afewell_azure_subscription_id}
        azure_resource_group: ${input.azure_resource_group}
        cluster_name: ${input.cluster_name}
        cluster_group_name: ${input.cluster_group_name}
        cluster_description: ${input.cluster_description}
        cluster_labels: ${input.cluster_labels}
        cluster_location: ${input.cluster_location}
        kubernetes_version: ${input.kubernetes_version}
        nodepool_1_name: ${input.nodepool_1_name}
        nodepool_1_count: ${input.nodepool_1_count}
        nodepool_1_vm_size: ${input.nodepool_1_vm_size}
        nodepool_1_node_disk_size_gb: ${input.nodepool_1_node_disk_size_gb}
        nodepool_1_enable_auto_scaling: ${input.nodepool_1_enable_auto_scaling}
        nodepool_1_max_node_count: ${input.nodepool_1_max_node_count}
        nodepool_1_min_node_count: ${input.nodepool_1_min_node_count}
      providers: []
      terraformVersion: 1.5.5
      configurationSource:
        repositoryId: a7de56c9-6d79-490d-a643-ea40fdbe787c
        commitId: f92f7112e729b887168c500bdfbdebda3d4f3faa
        sourceDirectory: tmc-akscluster
```

This section of the blueprint was also automatically created when I imported the terraform file. 

You can see the type is a terraform configuration, the variables defined here bound to the terraform variables defined in your vars.tf file and they are mapped to input values defined in the `inputs` section of the blueprint. 

One key thing to note is that you will not see the `vmw_cloud_api_token` or `azure_subscription_id` fields defined as inputs in the blueprint, and if you examine those fields you will see they are mapped to the values ${secret.afewell_azure_subscription_id} and ${secret.afewell_vmw_cloud_api_token}. The variable binding here shows how we can inject values from Aria Automations secret service to take care of our secrets handling. I can create secrets easily through the Aria Assembler gui or via API call and easily use them within various Aria solutions which is essential in my case as I want to be able to deploy these without needing to setup additional components and this built-in secrets service allows me to easily and securely bootstrap my initial deployments. The terraform vars bound to these secrets are defined in my vars.tf with the sensitive attribute so that after the secret is injected terraform will handle the values as secret in its visible operations and logs. 

### 5. Deploy!

Ok we have now completed all the required setup and can deploy a new AKS cluster leveraging Tanzu Mission Control to handle all the lifecycle management and provide a fleet-level management plane. 

First I want to note that now that the blueprint is created, we can manually create deployments from Aria Assembler, we can trigger deployments automatically from lifecycle events or webhooks, we could include the blueprint execution in pipelines and workflows or expose it to project users with a Aria Service Broker catalog. In this case I am going to deploy it directly from Assembler but I wanted to highlight all the available options. 

1. Login to VMware Cloud and navigate to Aria Automation Assembler
2. On the design tab, click to open your blueprint. 
3. Click `DEPLOY`
4. Observe the option to either create a new deployment or update an existing deployment. Select `Create a new deployment`
5. On the first page of the Deploy wizard, create a name for the deployment and if desired specify a blueprint template version and/or description as shown as the image below and click next.

![deploy_wizard_p1](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/deploy_wizard_p1.png)

6. On the second page of the Deploy wizard, you can see all the input fields that need to be filled in to create the deployment. As you can see I put in sensible default values for my project to simplify the user experience when creating deployments. Once a user has validated all the inputs as shown in the following image, click `Deploy`

Now all we need to do is wait while we observe our deployment executing. 

When I setup this environment, it was the first time I had used the TMC Terraform Provider. I anticipated that I would need to do some troubleshooting with my terraform files before I had them fully working and it would be more familiar to troubleshoot locally first, but I decided it would be a fun test and learning experience to bootstrap the terraform config development using the Aria Terraform service. 

I use the [Github Action for Semantic Release](https://github.com/marketplace/actions/action-for-semantic-release) to maintain gitops based versioning and automated release management to track and document commits to my repo, so if your are interested you can [check out the changelog](https://github.com/afewell/opsdev/blob/main/CHANGELOG.md) to see the full details of each of the little kinks I had to work out to get the script nailed down. 

I was concerned that using the service to deploy the terraform may be more difficult to troubleshoot but the opposite turned out to be true, its super easy to create a deployment and you can click on it to see the near realtime console and log output. 

![assembler_tmc_akscluster_deployment_history](https://raw.githubusercontent.com/afewell/afewell.github.io/main/public/images/assembler_tmc_akscluster_deployment_history.png)

I often build similar types of services from scratch, and it was refreshing in this case using the Aria Terraform Service. It was really nice to not need to bootstrap a container host or write a dockerfile to setup the runtime environment or ssh anywhere or type long docker or kubectl commands to troubleshoot, just a couple clicks to find the key information I needed, and at least in this case terraform was providing nice error messages so I was able to iterate through all the issues quickly and within an hour or two had it working exactly as desired ... and that time is considering I have never used the Aria terraform service before, I've never used the TMC Terraform provider, and I'm also not all that experienced with Terraform. 

I feel like all the ease of use features in Aria just feel like a really premium, luxurious experience not just in setting up the terraform files, but then handling the state file management and maintaining deployment objects that I can easily keep track of and providing all the hooks I need maintain my cluster deployments in TMC using infrastructure-as-code and gitops methods. 

## Summary and Next Steps

In this post I reviewed my demo setup including setting up the Aria Assembler terraform service, bootstrapping the terraform file development, integrating github with Aria to use git version control to manage my terraform files, and finally we reviewed how to create Tanzu Mission Control Lifecycle Managed Azure Kubernetes Cluster deployments with the final blueprint and observed a successful deployment. 

While this has been a great experience so far, it is just the tip of the iceberg of what I want to build out and I plan to follow this up with additional posts as I build out all the steps to get to my final goal of a fully automated build of my complete demo environment, which I want to make pretty fancy so hopefully will be a lot of fun. 

Next up is I need to complete the gitopsificiation of this service, so far I am part way there but there are several more elements I need to complete to achieve complete gitops coverage. First, note that the Aria Blueprint statically references a specific commit ID for the version of terraform file to use, so we will need to setup an automation to update the Aria blueprint with a new commit id that is triggered when a new commit is merged to the main branch of our terraform files to update the deployment template, consider automated testing, and will need to make some decisions about how to handle application of potential updates to existing deployments. 

After that, you may have noticed that while my terraform files are saved in git, the aria blueprint for the service is managed by the service and I am not yet managing the blueprint in git. Aria fully supports managing blueprints with git and has some really elegant graphical interfaces that fully integrate with git and gitops methods so I am really looking forward to setting it up and will share a post with the details when I do. 

Thus far we have accounted for managing our terraform files and our aria blueprints with git, both of which are templates. the final step for full gitopsification will be to gitopsify the deployment values themselves. When we created the blueprint we created variable declarations and inputs such that when we create a deployment, we have to provide specific values that are sort of the centerpiece of the configuration management for these clusters. In general once we setup a cluster we should not need to change the template itself much unless we add a new capability. In general it is more common to change some configuration value for a deployment for some reason, maybe adding or removing nodes or any number of other things that you may want to manage with infracode. 

Accordingly when this service is final, I would like the process to be that when a file that includes all the needed input variables is approved and merged into a specific directory in a git repo, a webhook triggers a deployment or update whenever a deployment values file is created or updated. Further, I mentioned I like having the best of both worlds between graphical interfaces and gitops. I would like to create a custom resource to manage these deployment values files to make sure lifecycle events such as updating a configuration value for an existing deployment or deleting a values file are handled correctly. This way a user could execute a pull request or make an API call to upload a deployment values file, or use the deployment wizard in assembler to fill in the values, or use Aria Service Broker to expose the service with a nice form to allow the service to be consumed by gui but stil be fully gitops based. 

Once I get to this sort of final version of my k8s cluster deployment service, I will work on getting the clusters all setup with some open source application/service deployments, Tanzu Application Platform and some of our own custom application demos and do it all with end-to-end gitops. For me, this is a lot of fun, and I will share posts with my experience along the way and hope it is interesting and valuable for you. 

Thanks for reading!

