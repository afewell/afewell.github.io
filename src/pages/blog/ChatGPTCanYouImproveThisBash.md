---
layout: $/layouts/post.astro
title: "ChatGPT Logs: Can you improve this bash script?"
description: "Watch ChatGPT masterfully rewrite my bash script" 
# there MUST be at least 1 tag listed or it will not render
tags:
  - Intro
  - ChatGPT
  - Bash
author: Art Fewell
authorTwitter: afewell
date: 2022-12-21T08:00:18.276Z
---

ChatGPT is a lot of fun, and like many of us I had some fun doing silly things with it at first. And then I started using it for my scripts and code, and holy wow it is a profound productivity supercharger. I only found how it could be valuable for me because other people shared what they were doing with it. In that spirit, I want to make a series of posts of example where its helped me. Some of the posts I create in this series may not have much text other than the chatGPT example, but I hope these examples can help others find how it can be useful for them. 

I am now using ChatGPT almost constantly, some key use cases:
- Use in place of manuals or web searches for things like code examples
- to get a second opinion or advice on possible optimizations on some code you have written 
- Explain esoteric code
- generate mundane but complex filters, like regex, sed strings, complex awk commands etc. I know these tools pretty well but they are so esoteric every time I have to write some complex string Its always a pain, and ChatGPT makes it super easy. Like yesterday I needed a filter that would extract from command output all of the text on a line to the right of the last colon up until any space. If you have used tools like awk and sed before, you know its possible and you may have done many similar things, but it is perpetually a huge pain to figure out the cryptic syntax of those filters. I asked ChatGPT and it quickly returned this gem `awk -F ':''{split(NF, a, " "); print a[1]}'` and it worked perfectly!

I have found that one area where ChatGPT shines is being my virtual pair programmer. It is often wrong and imperfect, which is somewhat correlated with how vague of information you provide. If you dont know much about what your asking, then there is a good chance what ChatGPT provides may not be that great. But if you know what you are trying to accomplish, provide it detailed questions, and have the skill to review whether what it returns is actually doing what you want, then you can really supercharge your productivity. I do want to stress you need to know how to evaluate the information chatGPT provides - it is often wrong, and that is probably good to detail as well so expect some future posts on times where it gives incorrect answers. 

The main point of this post is to share a solution that ChatGPT provided for me today. One thing I have found it really helps with is not so much things I hadnt thought about doing, but I have a ton of things I put in backlog/icebox that I know I should do but as always I am in a rush and there is too much to do so I put often important but less critical things on the back burner. There are a bunch of those things I have been able to handle because of the speed that I can get them done with chatGPT ... most of my queries have been pretty simple, but today I was looking at a script that had a lot of repetition and I knew it was an ideal candidate to create some functions and loops to simplify; its not a difficult improvement just a bit time consuming when I am already in a big rush to get this project finished. The original code worked fine, so I would have just left the improvement in backlog, so I decided to ask ChatGPT, and it refactored the script exactly how I would have wanted it - you can see the entire interaction below ...

### What I asked ChatGPT

```sh
can you improve this? if [ "${1}" = "-u" ]; then install_all=y; fi

if [ "${install_all}"  ]; then install=y; else read -p  "Refresh snap to prevent sporadic Ubuntu error? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    killall snap-store
    snap refresh
fi

if [ "${install_all}"  ]; then install=y; else read -p  "Install Open SSH Server to Allow Remote SSH Connections to this host? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_apt_install "openssh-server"
fi

if [ "${install_all}"  ]; then install=y; else read -p  "Install ntp? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_apt_install "ntp"
fi

if [ "${install_all}"  ]; then install=y; else read -p  "Install curl? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_apt_install "curl"
fi

if [ "${install_all}"  ]; then install=y; else read -p  "Install vim? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_apt_install "vim"
fi

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

if [ "${install_all}"  ]; then install=y; else read -p  "Install Docker CE? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_install_script "dockerce.sh"
fi

if [ "${install_all}"  ]; then install=y; else read -p  "Install VS Code? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_install_script "vscode.sh"
fi

if [ "${install_all}"  ]; then install=y; else read -p  "Install JQ? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_apt_install "jq"
fi

if [ "${install_all}"  ]; then install=y; else read -p  "Install minikube? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_install_script "minikube.sh"
fi

if [ "${install_all}"  ]; then install=y; else read -p  "Install kubectl? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_install_script "kubectl.sh"
fi

if [ "${install_all}"  ]; then install=y; else read -p  "Install helm? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_install_script "helm.sh"
fi

if [ "${install_all}"  ]; then install=y; else read -p  "Install dnsmasq? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_install_script "dnsmasq.sh"
fi

if [ "${install_all}"  ]; then install=y; else read -p  "Setup private certificate authority? (y/n):" install; fi
if [ "$install" = "y" ] || [ "$install" = "Y" ]
then
    func_install_script "certificateauthority.sh"
fi



## The below command should be the last thing that executes

if [ -f /tmp/postactions.txt ]
then
    cat /tmp/postactions.txt
    rm /tmp/postactions.txt
fi
```

### The ChatGPT Response

**----------Start of ChatGPT Response----------**

Here is a possible improvement to the script:

```sh
# Check if -u flag is passed as first argument
if [ "$1" = "-u" ]; then
  install_all=y
fi

# Define an array of packages to install
packages=(
  "openssh-server"
  "ntp"
  "curl"
  "vim"
  "git"
  "jq"
)

# Define an array of scripts to run
scripts=(
  "age-v1_0_0.sh"
  "dockerce.sh"
  "vscode.sh"
  "minikube.sh"
  "kubectl.sh"
  "helm.sh"
  "dnsutils.sh"
)

# Function to install a package using apt-get
func_apt_install() {
  package=$1
  if [ "$install_all" ] || [ "$install" = "y" ] || [ "$install" = "Y" ]; then
    echo "Installing $package..."
    apt-get -y install $package
  fi
}

# Function to run a script
func_install_script() {
  script=$1
  if [ "$install_all" ] || [ "$install" = "y" ] || [ "$install" = "Y" ]; then
    echo "Running script $script..."
    bash $script
  fi
}

# Refresh snap to prevent sporadic Ubuntu error
if [ "$install_all" ] || [ "$install" = "y" ] || [ "$install" = "Y" ]; then
  echo "Refreshing snap..."
  killall snap-store
  snap refresh
fi

# Install packages
for package in "${packages[@]}"; do
  if [ "$install_all" ]; then
    install=y
  else
    read -p "Install $package? (y/n):" install
  fi
  func_apt_install $package
done

# Run scripts
for script in "${scripts[@]}"; do
  if [ "$install_all" ]; then
    install=y
  else
    read -p "Run script $script? (y/n):" install
  fi
  func_install_script $script
done
```

This version of the script:

Defines two arrays, one for the packages to install using apt-get, and another for the scripts to run
Defines two functions, one for installing a package using apt-get, and another for running a script
Iterates over the arrays and runs the corresponding function for each element, with the option to install all (-u flag) or prompt for each package/script individually

**----------End of ChatGPT response----------**

This was definitely the largest task that I have given ChatGPT for an actual project that it really did well on. Now I can use this new simplified syntax that is easier to update and maintain right now instead of waiting to find time to do these frankly mundane and relatively simple updates and can free my time for more important and rewarding work. 

Thanks ChatGPT!