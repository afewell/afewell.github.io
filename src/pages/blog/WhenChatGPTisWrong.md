---
layout: $/layouts/post.astro
title: "When ChatGPT is wrong"
description: "ChatGPT is an amazing tool, but it is often wrong. And perhaps its biggest weakeness is that it does not seem to express uncertainty - when it answers, even if it is wrong, it does so with an authoritative certainty that could cause big problems if not understood and used with strict discipline." 
# there MUST be at least 1 tag listed or it will not render
tags:
  - ChatGPT
  - GitOps
  - "Platform Engineering"
  - Kubernetes
  - Devops
  - "Artificial Intelligence"
  - "Machine Learning"
author: Art Fewell
authorTwitter: afewell
date: 2022-12-28T08:00:18.276Z
---

ChatGPT has very quickly become my single favorite tool to provide assistance while working on my automation projects. While it is an incredibly powerful tool, it is often wrong, and perhaps its biggest weakness is that, I have not seen it express uncertainty. I have at times seen it respond clearly that it does not know the answer to some question. But much more often, I have seen it provide completely incorrect and invalid responses as though certain it was right. When it provides an incorrect command instruction, you can interact with chatGPT to inform it that its response was incorrect, and it will acknowlege that it was wrong, apologize and then provide another revised response that may also be invalid and it will again respond as though it were certain it was right. 

In my research thus far I think that this is the biggest problem and area for improvement - I would find it far more valuable if it were able to express uncertainty or probability in its responses, if it could say things like "Based on available information, I am not certain what is correct, I feel x percent likely that the following syntax should work, but it should be tested and verified to confirm ..." or something to that effect. 

None of these challenges take away from my opinion that ChatGPT is still the most powerful tool in my arsenal. But it does really show how incredibly risky it can be. There are so many short-sighted people out there I have no doubt many may try to automate and replace human expertise in effort to save money, and there is just no way that should be considered as a real use case for the current level of technology. 

It is also critical that ChatGPT not be thought of as a tool that can make a less skilled worker replace a more skilled worker. If chatGPT responded with degrees of uncertainty and probability, perhaps it could be used by less skilled workers such that, if it provided a response with a low probability, the lower skilled worker could use that to know when to seek assistance. But, ChatGPT doesnt do that, it happily expresses absolute certainty when it is wrong, which is an incredibly risky thing, it would be pretty easy for even an expert to overlook an invalid response from chatgpt and accidentally introduce an undesirable behavior into an automation/code project. 

One last key consideration here before I get into specific examples is, ChatGPT may often provide perfectly good and valid responses that could be used incorrectly by inexperienced workers which could lead to huge problems. For example, it could provide some example code or command syntax that may not implement an important security feature. This may not be the result of a flaw in ChatGPT, but perhaps the byproduct of the fact it can give very detailed, nuanced and customized responses. 

People fully understand when they are looking up an example in documentation that, its just a reference and they need to do some research and testing to understand how to transform the example into something usable for their production environment standards. And ChatGPT may in many cases be able to understand some of those nuances, if you know how to ask it the right questions. But, you can ask it questions like "how can I do some thing" and it can provide a response that works - but its only responding to what you ask, as in this example it was not asked to include what security considerations and best practices may be relevant, or many other things that may be important for your organization or environment. 

This point is not a critique of ChatGPT per se but a reminder that this is a tool that must be used by an expert and with appropriate caution and strict discipline before being used in any important or production projects. I should also note I am not an expert on the potential legal considerations of using responses from ChatGPT and would strongly urge anyone to seek legal validation from an expert before considering the use of ChatGPT on any professional project.

> "The most critical finding from my research into ChatGPT is that a user must both have a level of expertise such that they can fully validate ChatGPT responses, And, experts MUST maintain the discipline to fully validate every aspect of ChatGPT responses before using any of its findings or recommendations in any important or production project"

## Example of ChatGPT being unable to answer a question

Before I get into some examples of ChatGPT providing incorrect responses, I'd like to first share a simple example of ChatGPT clearly stating it does not know an answer to a question. The other day I was deciding on a gift for someone when I found a box of chocolates that didn't have a very good description. I did a quick web search and didnt see any good immediate responses so thought why not ask ChatGPT? Here is the result of that interaction:

### My Question: 
"can you provide some details about merci's "lovelies" chocolates?" 

#### ChatGPT Response: 
I'm sorry, but I don't have any information about a brand called "Merci's Lovelies" or "Lovelies" chocolates. Could you provide some more context or specify which brand you are referring to?

#### Discussion:

I did try to ask this question in a few different ways, and each time I got a similar response, which I think is a good thing. Of course we would like ChatGPT to know everything, but I think it is crucial that it acknowledges when it doesnt. 

As I was preparing this blog though, I asked this question again, and tried to add some additional detail with further questions ... I dont want to get into the full response as it gets away from my main points here, but this is the first time I have noticed a response from ChatGPT that expressed uncertainty - its response to my further prompting included the statement "The brand offers a wide range of chocolate products, including a selection of chocolate assortments sold in distinctive blue packaging. It's possible that the "Lovelies" chocolates you are referring to are a part of this product line."

That was the first time I have seen it express uncertainty so I am glad to know that it can, but as the following examples will highlight, I think ChatGPT needs to get MUCH better at knowing when its wrong or expressing uncertainty or probability. 

## Examples of ChatGPT providing incorrect/invalid responses:
### Wildcard entries in hosts files

 While I have been wanting to write this post for a while, I was working on a project today where I got a glowing example of an invalid response - I am working an a project to build an demo/educational lab for VMware Tanzu Application Platform that will use the Contour ingress controller which uses the Envoy proxy that is widely used by various service meshes and other Kubernetes networking solutions. The Envoy proxy provides layer 7/URL routing, as is common with many network proxies and gateways. 

This common scenario means that traffic for many different URL's should be forwarded to envoy's IP address, and envoy is able to look at the full URL to determine which kubernetes pod the traffic should be forwarded to. As a result, a DNS server does not contain 1:1 entries like `host1.example.com <host1 ip address>` but would instead have wildcard entries like `*.example.com <envoy proxy ip address>` or `*.subdomain.example.com <envoy proxy ip address>`.

This is not a problem for DNS servers, but in small lab environments that may not have a DNS server, this is a challenge, as host files on linux and windows do not support wildcard entries. So a common solution for linux is to install a lightweight dns server like `dnsmasq`, and I had already done this and have it working fine. 

But I am always looking to optimize, and while I knew that hosts files don't support wildcard entries, I also know that it is common to find creative solutions in Linux, so I had the thought, perhaps chatGPT may now of some trick or workaround to meet my need so I could remove the need to install a dns server. Here is the interaction - remember, hosts files DO NOT support wildcard entries:

#### My Question:
can you use wildcard entries in hosts files?

#### ChatGPT Response:

Yes, it is possible to use wildcard entries in the hosts file. A wildcard entry is a special type of entry in the hosts file that allows you to specify a group of IP addresses or hostnames that should be resolved to the same address.

For example, you can use a wildcard entry to specify that all subdomains of a particular domain should be resolved to a specific IP address. To do this, you would use the following syntax in your hosts file:

```sh
<IP address>    *.example.com
```

This would cause all subdomains of example.com (such as www.example.com, mail.example.com, etc.) to be resolved to the specified IP address.

It's important to note that wildcard entries in the hosts file will only apply to subdomains of the specified domain, and not to the root domain itself. For example, the above wildcard entry would not apply to example.com itself, only to subdomains of example.com.

You can also use wildcard entries in the hosts file to specify that a group of hostnames should be resolved to a specific IP address. To do this, you would use the following syntax:

```sh
<IP address>    host1 host2 host3
```

This would cause host1, host2, and host3 to be resolved to the specified IP address.

#### Discussion

It is amazing to me how the above response can seem so authoritative while being so completely wrong. And while the majority of interactions I have had have been accurate, I have had several different responses that were very similar. 

Another really interesting thing is that you can respond back to ChatGPT and tell it that it was wrong, and it will fully acknowlege that it was wrong. But I do wonder how it ingests and updates its own learning as, even after ChatGPT acknowleges that its wrong and provides a corrected response, I can log into a new session with ChatGPT, ask the original question, and still get back the same exact invalid response as though it were again completely unaware it was wrong. 

Perhaps with a bit of time it will update, and together we can investigate ... If you read this post, try to ask ChatGPT `can you use wildcard entries in hosts files` and see if it updates its standard response - and please let me know if you find anything different!

So lets see what ChatGPT said when I told it the response was incorrect. 

#### My Question 
you are wrong, in both windows and linux, it is not supported, nor does it work, to make an entry like *.example.com in a hosts file

#### ChatGPT Response

Thank you for pointing out my mistake. You are correct that it is not possible to use wildcards in the host file in Windows or Linux to match multiple hostnames at once. The host file is a simple text file that maps individual hostnames to IP addresses, and it does not support wildcard entries.

In Windows, the host file is located at C:\Windows\System32\drivers\etc\hosts, and it consists of lines containing an IP address followed by one or more hostnames, separated by white space. For example:

```sh
127.0.0.1   localhost
192.168.1.1 example.com
```

In Linux, the host file is located at /etc/hosts, and it follows the same format as the Windows host file.

It is possible to block or redirect certain hostnames by adding entries to the host file, but you must specify the hostname or domain name explicitly, rather than using wildcards. For example, to block access to "example.com", you would add an entry like the following to the host file:

```sh
127.0.0.1   example.com
```

This would cause the operating system to resolve the hostname "example.com" to the IP address "127.0.0.1", which is the loopback address and is used to refer to the localhost. This would effectively block access to the website, as any attempt to connect to "example.com" would be redirected to the local machine.

I apologize for the error in my previous response. I hope this information is helpful.

### Questions about YQ

The first time I really noticed ChatGPT produce highly confident responses that are wrong were when I asked some questions about the utility `yq` which is used to parse and manipulate yaml files. It's not the most popular or well known app, and it has gone through some significant syntax changes through different versions, so I could see how it would be a bit tricky for it to get the syntax perfect. 

But it does still seem quite strange to see its responses as you normally don't find anything like this type of response from humans. While we humans are often glowingly wrong about many things, its exceedingly rare to find writing that is professionally written and authoritative like documentation about something as straightforward as a basic command that is just completely wrong. It takes some getting used to. 

I have asked ChatGPT many questions about `yq` and I think all of the responses were wrong. Many times I pointed out something wrong in a command it provided and it would provide back a revised response that was also wrong. If you want to find some good example scenarios of ChatGPT being wrong about some command syntax, `yq` is a inquiry to start with. 

Another interesting point is that, I never specified which version of YQ I used in any of my questions, and ChatGPT never asked me. It does appear that the problems with the `yq` commands it provided were not simply because they were the wrong version number, as I don't think the provided commands would have worked in any version of yq. But it does highlight some interesting things about its logic and areas for improvement ... why did it not ask me what version number or other clarifying questions? Was it aware of the version differences in the answers it provided, or did its learning model possibly concatenate different information about yq from the internet without considering version differences? I dont know the answer, but it is interesting to consider how it reasons. 

#### What I asked ChatGPT
given the following yaml, how can I use yq to set the value for the key ca_cert_data as the string "potato":
 shared:
  ingress_domain: "tanzu.demo"
  image_registry: 
    project_path: "http://192.168.49.2:30002/tap"
    username: "admin"
    password: ""
  ca_cert_data:

#### ChatGPT Response

To set the value for the key ca_cert_data as the string "potato" using yq, you can use the following command:
```sh
yq write -i -- 'ca_cert_data' 'potato' file.yaml
```
This will update the file.yaml file in place, replacing the value of ca_cert_data with "potato".

Alternatively, you can use the yq command to write the updated value to a new file:
```sh
yq write -- 'ca_cert_data' 'potato' file.yaml > updated_file.yaml
```
This will create a new file called updated_file.yaml with the updated value for ca_cert_data.

Note that yq requires the jq command-line JSON processor to be installed. You can install jq using your package manager, or download the binary from the jq website (https://stedolan.github.io/jq/).

If you want to update the value of ca_cert_data in a specific location within the YAML file, you can specify the path to the key using dot notation. For example, to update the value of ca_cert_data within the shared object, you can use the following command:
```sh
yq write -i -- 'shared.ca_cert_data' 'potato' file.yaml
```
This will update the value of ca_cert_data within the shared object in the file.yaml file.

#### Discussion

I created a new container with a fresh install of the latest stable `yq` version, and, the above commands do not work. I am not going to get into what syntax does work, as this blog is already pretty long and my main point here is that the commands provided by ChatGPT for `yq` simply do not work. 

Also the response states that the utility `jq` is a required dependency for `yq`, and I am pretty certain it is not, and that requirement is not listed in the `yq` documentation. In the many questions I have asked ChatGPT about `yq`, this is the first time it stated that `yq` was dependant on `jq`, although I do remember that in one response, it mentioned I could accomplish the same task with `jq` and provided an example of manipulating the yaml file with `jq`, I do not know if `jq` can manipulate yaml or if the example provided would have worked, but I do find it very strange how sporadically ChatGPT responses have mentioned `jq`, when I could see nothing in my questions that would have prompted a different response from my other `yq`questions.

Another very strange thing about the questions I asked about `yq` is, I have tried to ask very similar questions, and I seem to get very different responses even with a very very similar question. For example, I originally asked almost the same exact question about the same ca_cert_data key in the same yaml file and I accidentally closed the tab so I entered essentially the same question again expecting to get the same response for the blog, but the response is different. I did not save all the detail from each question I asked, but I did keep the command it gave me from the first time I asked the question and it had given me the command `yq write -i --DOCUMENT_LOADER 'text' -d'*' shared.ca_cert_data "potato" potato.test`, which is also invalid. I remember not recognizing the "DOCUMENT_LOADER" flag and looking at the instructions in case that were a placeholder value, but the instructions it provided indicated I should use the "DOCUMENT_LOADER" flag verbatim - and the strange thing about that is I cannot find any reference to "DOCUMENT_LOADER" or "Document Loader" when searching either the `yq` documentation or github repo, which really makes me curious how it arrived at that recommendation. 

### Errors in code
The last example I will share is, I recently wrote [another blog about a script I asked ChatGPT to refactor](https://artfewell.com/blog/ChatGPTCanYouImproveThisBash/). Overall it did a great job improving the script, but it was not perfect, in fact the script it provided would not have worked at all due to a key error I was kind of surprised it missed. 

Please [see the original blog post](https://artfewell.com/blog/ChatGPTCanYouImproveThisBash/) to see the full text of the question and response, here I will focus in just on the part that had a problem. 

The original script I provided to ChatGPT included the following lines:
```sh
if [ "${install_all}"  ]; then install=y; else read -p  "Refresh snap to prevent sporadic Ubuntu error? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    killall snap-store
    snap refresh
fi
```

The above code checks to see if the "install_all" variable is present, and if so it executes the code block. If the "install_all" variable is not present, It executes the `read` command which prompts the user to enter "y" if they want to execute the commands in the block. It works just fine in this format. 

In the revised script that was provided by ChatGPT, it included the following revised code:
```sh
# Refresh snap to prevent sporadic Ubuntu error
if [ "$install_all" ] || [ "$install" = "y" ] || [ "$install" = "Y" ]; then
  echo "Refreshing snap..."
  killall snap-store
  snap refresh
fi
```
Now the huge problem with the revised version is, it never asks the user to press y to install, so there is never any opportunity for the "install" variable to get set to anything, so this code block would simply never execute unless the install_all variable were set, and that can only be set by passing in a flag when calling the script. So if a user did an unattended install it would work, but in any other case, the code in the above block would just never get executed. It was surprising to me that ChatGPT did not recognize this, especially given that every other line it provided in the revised script worked fine. 


#### Efficiency vs Readability?

Another problem I found with the revised script is, it seemed to make a pretty trivial optimization that made the code less readable - let me share the code before I discuss further ... 

The original script file installed several programs, almost all of which used 2 functions, one was for a standard apt-get install syntax, and the other would execute an installation script. Here is a sample:
```sh
if [ "${install_all}"  ]; then install=y; else read -p  "Install git? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_apt_install "git"
fi

if [ "${install_all}"  ]; then install=y; else read -p  "Install age? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_install_script "age-v1_0_0.sh"
fi
```

As you can see in this code sample, for each install, it prompted the user to enter "y" if the user wanted to install that item. The script was verbose, but easy to reason about as each block was sorrounded by identical logic that is pretty straightforward. 

As there were numerous similar code blocks that all repeated the same logic, it made a lot of sense to create some loops to loop through all the redundant items, and ChatGPT placed these redundant code blocks very nicely into loops, overall it did a good job and the logic provided worked fine, but the way it updated the logic made it more difficult to read and reason about. 

Here is an example from the ChatGPT provided script that shows what I mean:
```sh
func_apt_install() {
  package=$1
  if [ "$install_all" ] || [ "$install" = "y" ] || [ "$install" = "Y" ]; then
    echo "Installing $package..."
    apt-get -y install $package
  fi
}

for package in "${packages[@]}"; do
  if [ "$install_all" ]; then
    install=y
  else
    read -p "Install $package? (y/n):" install
  fi
  func_apt_install $package
done
```

This code works fine, the for statement loops through each package in a list it provided and calls func_apt_install for each. The problem that I have with this solution is, the conditional logic is divided between the function and the function call, and I think that makes it harder to understand or reason about should the code need to be extended or modified. This is very different than being wrong, but it is sort of a related topic that I wanted to mention here. 


### Summary

Even though it is wrong sometimes, ChatGPT is still my favorite new tool, and still supercharges my productivity. It can be really awesome, if you think about it in the right way, as a tool in the toolbag of an expert, and only to be used with disciplined process controls as it can be easy for even an expert to overlook flaws in ChatGPT's responses. 

Please share your experiences and examples, I look forward to exploring this more together with the community!