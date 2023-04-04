---
layout: $/layouts/post.astro
title: "Automated Data Ingestion and AI-Assisted Extraction with GPT-4 and example extraction from VMware Tanzu documentation - Part 2"
description: "In this 2 part series, I go over code that can scrape a website or subsection of a website, clean the data, and automate calling GPT-4 with context from the ingested documents with a prompt that successfully extracts desired content in a specified format." 
# there MUST be at least 1 tag listed or it will not render
tags:
  - ChatGPT
  - Tanzu
  - "Platform Engineering"
  - Kubernetes
  - Devops
  - AIops
  - "Artificial Intelligence"
  - "Machine Learning"
  - "Tanzu CLI"
  - "Tanzu Application Platform"
author: Art Fewell
authorTwitter: afewell
date: 2023-04-03T08:00:18.276Z
---

Picking up from where we left off from [part 1 of this series](./scrape-to-document-extraction.md), we finished covering the scraping and cleaning functions, and now we will get into calling the Open AI API's using the openai python library, which makes it really simple. 

The HtmlScraperSpider class that we covered in part 1 downloaded each of the URL's that we discovered with the UrlScraperSpider class. For this example I had set the scraper to download the files into the /scrapy/html directory in my local filesystem. Next, I want to present each page that I downloaded to the AI model along with instructions about how what we want it to do with the data that we provide. This query we sent to the openai api is referred to as a prompt. Until gpt-3.5-turbo, every example I am aware of used the openai completions endpoint to query the model, and with that endpoint, the field you would pass the query to was called the prompt field. But, with gpt3.5 and gpt4, there is a new format using the ChatCompletions endpoint, which allows you to use a new "messages" format, which is a more flexible and descriptive method to provide the query. I dont know if the chatcompletions endpoint was available before gpt-3.5-turbo, but as far as I can tell, you cannot query the old completions endpoint for gpt3.5 and gpt4, you have to use the chatcompletions endpoint as shown in the code I will share below. 

One of the reasons I draw attention to this point is, this point was not obvious to me. I am sure there are lots of examples on the web that share the chatcompletions endpoint, but when I was initially searching for how to query the newer models, I found a lot of outdated data using the old completions endpoint, and I didnt find the information on the openai website to be very helpful. But, the best place to find information about openai APIs is the [openai cookbook](https://github.com/openai/openai-cookbook), which has lots of great detail on how to query the newer models for a variety of use cases. 

For my use case, I want to provide each page I downloaded with my prompt, one page at a time, so that openai can look through each page to find each command and usage examples. This is very different from say, making a chatbot, which I found to be a much more streamlined process because of libraries like langchain and llamaindex. With the chatbot use case and llamaindex, its pretty easy to have it ingest a variety of data formats and have them ingested into a vector db, that provides relevant search results from your data to the gpt api, so the AI model has context from your data for which to answer a question. I think things like cleaning and chunking are a bit more forgiving in that context as your query will help find the relevant text to send to the model, and will send multiple chunks if your query has enough token space, which can help deal with a less refined chunking methodology. I do think that the chatbot use case is equally nuanced but more forgiving if your dataset is imperfect. 

But, in the chatbot model, I dont think there would be any way to do what I want, which is extract every single tanzu cli command from dozens of different pages. So accordingly I am using the approach to sequentially present all of my data to the model, one page at a time. As I mentioned in [part 1](./scrape-to-document-extraction.md), I am taking some shortcuts so I shouldnt need to chunk my data in this case, but if I were, I would still send each chunk sequentially, but I would be careful to try to use a chunking method that did not carelessly chunk the data as this could likely lead to obscuring the context and reducing the accuracy of the model. 

I found the simplest way to get this method working accurately was to create a function that called openai api with a single pages data, I have saved this code in a file called openai.py. Then I created a main.py file which uses a separate function that loops through each document in the directory of pages that was downloaded by the HtmlScraperSpider, and calls the function from the openaicall.py file with the text from each file, one by one until we have looped through each page. 

To best understand these files, it will be easiest if I explain the openaicall.py file first in the context of a single call, and after we will look at the main.py call to see how we loop through all of the source documents. 

## openaicall.py:
````
import os
import json
import openai
import logging

# Set up an error logger with a specific name and level
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)

# Create a file handler to log errors
error_file_handler = logging.FileHandler('openaicall_error_log.txt')
error_file_handler.setLevel(logging.ERROR)

# Set up an action logger with a specific name and level
action_logger = logging.getLogger('action_logger')
action_logger.setLevel(logging.INFO)

# Create a file handler to log actions
action_file_handler = logging.FileHandler('openaicall_action_log.txt')
action_file_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
error_file_handler.setFormatter(formatter)
action_file_handler.setFormatter(formatter)

# Add the file handlers to the loggers
error_logger.addHandler(error_file_handler)
action_logger.addHandler(action_file_handler)

# Define the filename for the JSON file
json_filename = 'openai_responses.json'

def save_response_to_json(response, filename):
    try:
        data = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
        data.append(response)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Error in save_response_to_json: {e}")

def call_openai_api(text, api_key):
    try:
        openai.api_key = api_key
        messages = [
            {
                "role": "system",
                "content": "You are an AI language model. Assist the user by answering their query with answers derived from the provided Context."
            },
            {
                "role": "user",
                "content": f"Example:\n---###---\nCommand: `tanzu apps clustersupplychain list`\nExample Usage:\n```sh\ntanzu apps clustersupplychain list\nNAME                 READY   AGE\nbasic-image-to-url   Ready   11d\nsource-to-url        Ready   11d\n```\nCommand:`tanzu apps clustersupplychain get SUPPLYCHAIN-NAME`\nExample Usage:\n```sh\ntanzu apps cluster-supply-chain get source-to-url\n---\n# source-to-url: Ready\n---\nSupply Chain Selectors\n   TYPE          KEY                                   OPERATOR   VALUE\n   expressions   apps.tanzu.vmware.com/workload-type   In         web\n   expressions   apps.tanzu.vmware.com/workload-type   In         server\n   expressions   apps.tanzu.vmware.com/workload-type   In         worker\n```\n---###---\nContent:\n---###---\n{text}\n---###---\n\nIdentify the pattern and format shown in the example. Examine the Content for commands and example usage patterns like those shown in the example. Your response should only include the Command and Example usage for each relevant item you found in the Content. Your response should be formatted exactly the same way as the example, and your response should not include any other details."
            }
        ]

        completions = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            n=1,
            temperature=0.5,
        )

        action_logger.info(f"OpenAI API call made for text: {text[:100]}...")  # Log the API call action (truncated text for brevity)

        response = completions.choices[0].to_dict()
        save_response_to_json(response, json_filename)
        return response
    except Exception as e:
        error_logger.error(f"Error in call_openai_api: {e}")
        return None
````

The first part of this file is just generic scaffolding to setup standard logging and other generic stuff. Where is starts to get interesting is the call_openai_api function. The first thing to point out about this is, the function accepts 2 inputs: text, and api_key. You may notice that the api key is neither defined nor imported in this file, and this is because we will execute this function by calling it from the main.py file I will share below, and the main.py file will send the api_key when it calls the call_openai_api function. But, when I was building this file, I executed it directly, and you too could use this as a reference for your own use, but note that you will need to define or better, import your openai api key from an os envar or secrets provider, and add a line that calls the function. 

An important detail about the api_key is, if you are calling the call_openai_api function from a separate file as I do, you cannot simply import environmental variables into the openaicall.py file like `openai_api_key = os.environ.get('OPENAI_API_KEY')' as you can when you execute openaicall.py directly. The reason why is that when you execute openaicall directly, you directly spawn the process it runs in from your environment, so your envars are accessible to it. But, when you call it from a separate file as I do with main.py, it is main.py that spawns the process that the call_openai_api function runs within, and so it cannot directly access your os envars, and you have to use a method to pass the value to the called function. So the net net is, use it like it is above if you intend to call it from a separate process, but if you want to execute the call directly you will need to add or import the key within the openaicall.py file. 

Moving on, if you look at the  call_openai_api function in the openaicall.py file, skip past the messages and you can see the line `completions = openai.ChatCompletion.create`. The `openai.ChatCompletion.create` part of that statement is what defines that we are calling the openai ChatCompletion endpoint. If you have tried to call the newer models from older code, this is the key part that changed, we used to call the openai.Completion.create endpoint, which will not work with the newer models. In addition to just calling the newer endpoint name, there are also some schema differences, the most notable being the messages field and format. With the old completions endpoint, there was no messages field, you put your query into the prompt field, and it was just one string. While you can put very complex as I did in the second message shown, the new messages format is significantly more expressive and really offers an updated approach towards prompt engineering that can be very interesting. There are a lot of great examples in the [openai cookbook](https://github.com/openai/openai-cookbook) of different creative ways to use the messages format for different use cases. 

If you look at the messages I included, you will see I included 2 messages, where the first provides an instruction to the model for how it should behave when approaching the question. The second message is my prompt, which includes a 2-shot example that defines both the pattern of the data I want it to find and the format I want it to return the found data in. The prompt is in a single string format so its hard to read, so I will put it in a readable format below. But first I wanted to mention if you are not familiar with the term 2-shot I used in the previous sentence, what this means is that I provide it with 2 examples I want it to emulate. You may have seen terms like zero-shot and few-shot in papers about AI models as they are common terms to describe methods used for testing AI models. If I were have tried to describe the items I want found and how I wanted the return without providing examples (and assuming the model wasnt previously trained on my specific example), that would have been considered a zero-shot prompt. 

Here is my prompt in a readable format:
````
Example:
---###---
Command: `tanzu apps clustersupplychain list`
Example Usage:
```sh
tanzu apps clustersupplychain list
NAME                 READY   AGE
basic-image-to-url   Ready   11d
source-to-url        Ready   11d
```
Command:tanzu apps clustersupplychain get SUPPLYCHAIN-NAME
Example Usage:
```sh
tanzu apps cluster-supply-chain get source-to-url
---
# source-to-url: Ready
---
Supply Chain Selectors
   TYPE          KEY                                   OPERATOR   VALUE
   expressions   apps.tanzu.vmware.com/workload-type   In         web
   expressions   apps.tanzu.vmware.com/workload-type   In         server
   expressions   apps.tanzu.vmware.com/workload-type   In         worker
```
---###---
Content:
---###---
{text}
---###---

Identify the pattern and format shown in the example. Examine the Content for commands and example usage patterns like those shown in the example. Your response should only include the Command and Example usage for each relevant item you found in the Content. Your response should be formatted exactly the same way as the example, and your response should not include any other details.

In summary, the example shows two command examples for the `tanzu apps clustersupplychain` command: `list` and `get`. The usage pattern for each command is shown along with the expected output. The task is to identify similar command and usage patterns in the content and provide them in the same format as shown in the example.
````

I will not go into great detail explaining the prompt as I wrote another blog about that [you can find here](./fewshot-command-extraction.md). But, I will add that I have since started using html/xml like tags as delimiters pretty much exclusively because they work awesomely. In the above prompt, I am using the string `---###---` as a delimiter, which works well for more basic scenarios. But, the more you work with these models, the more you may find very complex prompt needs that benefit greatly from a more expressive format. When I say html/xml-like tags, I do not mean you should use real html/xml tags, but rather, that you should make up your own. The most important thing about a delimiter is that it is unique and not found in the text its wrapping. That is extremely easy to do with an html/xml-like format. But, using simple delimiters of nonsense strings misses out on an extremely powerful possibility of delimiters, that you can include descriptive elements and instructions within the delimiter. For example, when I am using chatgpt and I want to ask it a question about some code, I will wrap it with an identifier which will allow chatgpt to easily be able to find and answer questions about that specific code snippet without having to include it in the prompt everytime at least for the chatgpt web clients ability to query your history with it. You could use a descriptive name in the tag, a version number, I often just use the day and time to provide a simple unique id value, for example like `<code 04031033> your code </code 04031033>. You could use standard attribute format like id="0431033" or something like that, but chatgpt doesnt care how you provide the info, but how you provide the info does matter in the sense of how you want chatgpt to be able to find the data, like if you wanted to query it about code with a specific version number it would probably make sense to wrap it like <mycode version="1.2.3"> or similar. You could put any number of attributes or words in delimiters like this, I think it makes for a more powerful and expressive method of prompt engineering. 

One thing to note about the prompt is, it is definitely interesting that by providing those 2 examples gpt is so effective at extracting a wide variety of commands. And you may wonder, how would I actually know if it found all the commands are found, which is an astute observation. In this case im sure it wouldnt be that difficult to find a list of all the tanzu cli commands, or write some logic that could extract static patterns like tanzu <command group name>, so this could be pretty easy to validate, but we could use this same ingestion method for things that are much harder to validate, and so the general approach is statistical sampling, and if accuracy is important to you, you would not just want to use pure random sampling to ensure each archetype is included in whatever depth of statistical sampling is needed for your desired accuracy level. In my case thus far I have done some very non-scientific random manual validation of several different samples I tested, and after playing with the prompt some I was at 100% in my informal tests. Perfect accuracy is not essential to my current use case so for now, I am happy taking a casual approach on this one, but as I implement more long-standing pipelines, I will implement more testing and tuning of model parameters and methods, for which it is useful to use a standard linear regression model to compare each configuration to provide a standardized and mature approach to evolve and maintain the performance of your setup. 

In the ChatCompletion call, the parameter `n=1` means I want the model to return one response. Temperature essentially controls the creativity of the model, much is written about temperature so I wont go into depth on it here other than to note, I started with 0.5 because that essentially indicates to use a medium level of creativity, which I thought was appropriate for this use case. I got good results without needing to adjust the temperature, which really isnt meaningful unless I test other values, and without that data its hard for me to comment on if or to what extent this parameter may be influencing my model performance. 

The rest of the code just saves the results to a json file. The save function creates the json file if it doesnt exist, and appends to it if it does exist, so if you loop this job a number of times, all the returns are in a nicely organized json file. 

## main.py:
````
import os
from openaicall import call_openai_api

openai_api_key = os.environ.get('OPENAI_API_KEY')

# Set the path to the directory containing the source text files
directory = '/scrapy/html'

# Loop through the files in the directory
for filename in os.listdir(directory):
    # Make sure the file is a text file
    if filename.endswith('.html'):
        # Open the file and read the contents
        with open(os.path.join(directory, filename), 'r') as f:
            text = f.read()
        print(text)
        # Call the call_openai_api function with the text and the API key as input
        response = call_openai_api(text, openai_api_key)
        
        # Do something with the response (e.g. print it)
        print(response)
````

The main.py file is nothing exotic. As explained above, we want to get the API key from the environmental variable in this file. The `directory` var is set to `/scrapy/html` for my test environment, and it could be changed to any local directory easily to meet different needs. Next a for loop loops through each file listed in the directory. In each loop, it reads the content of the source file into a variable named `text`. It then prints the text to the console and calls the call_open_api function and passes in the contents of the `text` variable and the openai_api_key. The final line prints the response to the console, which is sort of insignificant, it may be useful if someone manually executes this from a prompt, but the main output in this case is done by the openaicall.py file, which saves the response into the openairesponses.json file. 

## The Results:

I am only going to include a small sample of results here or it would be too long, but as you will see, I have a nicely organized json file where I can easily access each response:

```
[
    {
        "message": {
            "role": "assistant",
            "content": "Example:\n---###---\nCommand: `tanzu accelerator apply`\nExample Usage:\n```sh\ntanzu accelerator apply --filename <path-to-resource-manifest>\n```\n---###---"
        },
        "finish_reason": "stop",
        "index": 0
    },
    {
        "message": {
            "role": "assistant",
            "content": "Example:\n---###---\nCommand: `tanzu insight vulnerabilities get --cveid <cve-id> [--format <format>] [flags]`\nExample Usage:\n```sh\ntanzu insight vulnerabilities get --cveid CVE-123123-2021\n```\n---###---"
        },
        "finish_reason": "stop",
        "index": 0
    }
]

I should definitely add some additional metadata to this, like the name of the file it was extracted from and other stuff I will think about later. 

Here are the results in a more readable format:

````
Command:
tanzu accelerator apply

Example Usage:
```
tanzu accelerator apply --filename <path-to-resource-manifest>
```
Command:
tanzu insight vulnerabilities get --cveid <cve-id> [--format <format>] [flags]

Example Usage:
```
tanzu insight vulnerabilities get --cveid CVE-123123-2021
```
````
I did check the documentation I fed in for these results, and in these sample cases there was 1 command listed in each document and the example usage was exactly as could be derived from the source. I also ran other samples with multiple commands per page and more complex output, and all worked great, but this post is already pretty long so wanted to keep this part short. At some point I will probably put the full results on github somewhere, this is all public data. 

## Summary and Whats next

As I mentioned in the blog, I want to do some testing with the unstructured library to identify an ideal general purpose ingestion model, I need to add logging and error handling to each of the files and various other things, but, the biggest thing I am most excited about and want to do next is some light refactoring to implement this in a FaaS model using Tanzu/Knative functions and eventing, and create some application accelerators to easily roll out new executions of this for different target sites or data collections. I plan to have a number of different functions for different use cases like document extraction, chatbots, code generation, and other interesting things, so stay tuned for more blogs to come, I plan to document and share everything interesting I find. Thanks for reading!