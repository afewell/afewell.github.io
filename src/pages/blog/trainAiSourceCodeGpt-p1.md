---
layout: $/layouts/post.astro
title: "Can I train an AI effectively with just source code? Accelerating bot training with ChatGPT - Part 1"
description: "A lot of the data needed to train a bot has needed significant human input, but, can ChatGPT dynamically provide this data and dramatically simplify and accelerate bot training? Lets find out!" 
# there MUST be at least 1 tag listed or it will not render
tags:
  - ChatGPT
  - "Developer Experience"
  - Devx
  - "Artificial Intelligence"
  - "Machine Learning"
  - "Plugin Oriented Programming"
  - "Fine-Tuning"
  - Idem
  - "Idem project"
  - Python
author: Art Fewell
authorTwitter: afewell
date: 2023-2-14T08:00:18.276Z
---

I created a video on this same topic with some additional details, [please check it out here](https://www.youtube.com/watch?v=QLm5irtOXmg)!

Like many of us, Ive been really swept up by the whole ChatGPT craze. It's inspiring me to dive deeper into machine learning. Just since ChatGPT launched I have already taken a few courses in machine learning and AI and its been a fun and humbling experience. Machine learning is an extremely deep subject that is filled with really complex math. Fortunately I had some background from grad school doing similar math so I am not completely lost, but I think perhaps a more important realization for me was how ChatGPT itself dramatically changes the process of technology transfer for the dissimination of machine learning as it grows. 

Every time there is a complex new technology, at first you have to have very specialized knowledge to understand the language of the scientists who have made key discoveries and advancements, and it usually takes years for companies to build increasingly common language and abstractions to the point where there are simplified software interfaces with full sets of documentation and training in more common language that is easier to understand. This process of technology transfer has to happen before any new complex technology can grow towards becoming mainstream, there simply aren't enough people out there who can read doctoral level research and distill it into practical day-to-day applications. The real big impact of this is, any time there is a new technology, you can only grow it as fast as the market can absorb it. 

This to me is one of the most fascinating and powerful impacts of ChatGPT. It understands the deep scientitific and mathematical language of the latest machine learning research and can explain concepts better than most tutors, it can break concepts down to simple levels and then granularly add detail as you learn more. It can use its knowledge of advanced machine learning constructs to help you easily figure out a variety of different potential practical applications and then support you step by step as you seek to apply the technologies. Its imperfect, but it would have taken me years more study to even arrive at whatever limited insights I gained just over this past weekend. And while this is a cool exercise, perhaps the biggest impact of it is the realization that, having a trained bot can dramatically, profoundly accelerate tech transfer. You could start training a bot with your source code as you are starting a new development project, you could teach it the paradigms, practices and requirements for your project and it could onboard and pair program with your devs to make start faster and produce better and more consistent code and even with automated code completion kind of like co-pilot, but specific to your projects requirements. As you prepare support teams it could both train them and be a consistently available tutor and ... it can also help troubleshoot errors, a lot. It can work with you to write PRD's that are highly nuanced, help prepare marketing plans, and by launch be ready to help train your salesforce and customer base. You could train a model that could effectively convert product knowledge to training courses on the fly.  

While it is always interesting that new technology disruptions accelerate future disruptions because each disruptive tech brings capabilities that help accelerate the development of the next disruptive tech. But typically a technical innovation will have a technical discovery that makes developing the next technically possible. Its not often that a new tech arrives that can fundamentally change market adoption of new technologies by offering the potential to nearly eliminate the time needed for humans to be able to understand and apply the new technology. The internet itself was similar in this regard, but the potential for ChatGPT to address this issue, it will have a much larger impact in this regard even when compared to the introduction of the internet itself.

Now, one of the most difficult parts of training machine learning models is that you need data that's already verified to start training. Content that can teach the machine learning model correct answers, or responses that would align with what a human may associate with a request. But getting human provided data on thousands of records, which may be highly specialized, is a substantial investment. For example, consider getting data from source code itself - it seems logical that working source code could provide examples of code snippets that work, but what about answering questions from humans in plain speaking terms about code? What about questions beyond basic code completion where you may want to do planning or exploration and reason together, as you can do with ChatGPT about ideas, but in the context of the style and paradigms of your code project?

So let's say you have a source of static data, like for example, source code or documentation. Could ChatGPT itself provide the simulated human element to add the rich context needed to create a dataset that could result in a bot that could be highly effective in a specialized area? Something like source code and documentation would not be anywhere near enough data to train a model from scratch, but since we can build upon existing models like chatGPT, I feel very optimistic that a relatively simple, inexpensive, and fully automatable process could have this result. I have been wanting to experiment with making some fine-tuning datasets to train an OpenAI model, to see how well it may be able to answer questions with datasets that are made entirely from existing data + ChatGPT to provide the "human" element, so I was excited to spend this past weekend getting started on figuring this out. 

Over this past weekend, I decided to dive into the deep end and get started on a fun project to try to train an ai bot. I was planning on starting off trying to make a Tanzu bot and I still want to, but I recently got assigned to a project that I think would be an interesting and fun use case to try out. If you follow VMware good chance you have seen the recent product announcements for Aria Graph and Aria hub, which are really cool technologies that can model entire cloud infrastructures. It's a beautiful UI they're able to layer on top of it, which signifies the efficacy of the data modeling they're doing underneath.

One of the key underlying technologies that Aria Graph and Hub are built on is [the Idem project](https://www.idemproject.io/), which is a data flow-oriented programming language. The project has pretty good documentation, but I am also interested in using it for new and advanced use cases and plugin development - getting to this level of knowledge can take significant time and effort, and if this bot training yeilds effective results, it could dramatically accelerate my own path to gaining competence with this new language.

On top of that, Idem itself is based in another interesting new open source project called [Plugin Oriented Programming (POP)](https://pop-book.readthedocs.io/en/latest/). In the case of POP, we have source code, but since its a paradigm, the source code is really for tools that support programming in this paradigm. I think this is a very fascinating angle to approach the hypothesis of bot efficacy from source code and documents, as a paradigm represents a different and higher order sort of reasoning to be effective, and I really want to become proficient with pop quickly, so I think this makes pop a really interesting subject for bot training. 

I'm starting my project with the source code for POP and using it to generate training data. I will also use the documentation for Pop and source code from other related projects built on the POP paradigm to create more data. After cleaning and tokenizing the data, I'll use some python code and some freely available models to create embeddings, which will help the bot to calculate relationships and probabilities between words.

In the world of machine learning, natural language processing (NLP) is a critical area of study. It involves training models to understand human language and generate responses that sound like they were written by a person. One key challenge in NLP is figuring out how to represent words and sentences as numerical values that can be processed by a machine. This is known as tokenization and embedding.

I'm currently working on two approaches to NLP: creating embeddings from the entire base of source code, and using snippets. Snippets are a more common way to start, as they are smaller and easier to work with than full source code. They provide a lot of insights, and you can still be very effective at using them without understanding every deep aspect of the mathematics behind NLP.

To start, I'm worked with ChatGPT to create some Python code that searches a directory/repo of source code files and extracts snippets, which are just the functions, classes and main parts of code.  Next, I will add rich contextual data, such as labels, annotations, and questions - this data is critical for yielding an effective model, but is normally where we would need a lot of specialized human effort to derive. 

Here is the script I used to extract the snippets, which also places a delimeter between each snippet:
```python
# this code extracts code snippets from a directory of python files, and places a delimiter between each snippet
import ast
import os
import os.path

def extract_code_snippets(file):
    with open(file, 'r') as f:
        code = f.read()
    tree = ast.parse(code)
    code_snippets = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            code_snippet = ast.unparse(node)
            code_snippets.append(code_snippet)
    return code_snippets

def process_directory(directory):
    code_snippets = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith('.py'):
                code_snippets += extract_code_snippets(path)
    return code_snippets

def main():
    code_snippets = process_directory('.')
    with open('code_snippets_delimited.txt', 'w') as f:
        for snippet in code_snippets:
            f.write(snippet + '\n\n' + '-' * 80 + '\n\n')

if __name__ == '__main__':
    main()
```

 I am not sure if I should have used a structured data format like json or something for these which would also be easy to do and probably better. I am just doing tests manually right now but over time as I refine these steps more, and will want to keep these snippets in a structured database, so in the future I will update this code accordingly. 

 But for now I just put in a delimiter. this code uses a full line of dashes to seperate each snippet, which was a poor choice on my part, I had some issues processing it so instead I used another script to replace the delimiter with a different format. Thinking about it more now, I dont know why I didnt just wrap it in json. 

 Here is the code I used to update the delimiter:
 ```python
def replace_delimiter(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    with open(file, 'w') as f:
        for line in lines:
            if line.strip() == '-' * 80:
                f.write('"""\n-----delimiter-----\n"""\n')
            else:
                f.write(line)

if __name__ == '__main__':
    replace_delimiter('old_del.txt')
    with open('old_del.txt', 'r') as f_in:
        with open('new_delimited.txt', 'w') as f_out:
            f_out.write(f_in.read())
```

And after processing I ended up with over 650 snippets or just over 4000 lines with no blank lines. Here is a small sample of what the result looks like:

```python
"""
def discover_packages():
    modules = []
    skip_mods = ['tests']
    for package in (NAME,):
        for (root, _, files) in os.walk(os.path.join(SETUP_DIRNAME, package)):
            pdir = os.path.relpath(root, SETUP_DIRNAME)
            modname = pdir.replace(os.sep, '.')
            if modname not in skip_mods:
                modules.append(modname)
    return modules
"""
-----delimiter-----
"""
def initialize_options(self):
    pass
"""
-----delimiter-----
"""
def finalize_options(self):
    pass
"""
-----delimiter-----
"""
def run(self):
    for subdir in ('pop', 'tests'):
        for (root, dirs, files) in os.walk(os.path.join(os.path.dirname(__file__), subdir)):
            for dir_ in dirs:
                if dir_ == '__pycache__':
                    shutil.rmtree(os.path.join(root, dir_))
"""
```



In addition to the delimiter line, I also wrapped each snippet in triple quotes, which I added because my initial tests without them were having some strange results. When you send queries to ChatGPT when using an automation, you need predictable responses. One important part of that is providing a clear stop value, so that chatgpt knows when your question ends and has a que about how to respond. While a newline at the end of a prompt is the default stop value and usually works well, I was having issues with it, which I could see because the davinci API was sometimes returning 2 responses to a query, and the second one would be just made up, so something was wrong in my data processing that ended up causing davinci to think I wanted another response but since I didnt provide input for the 2nd response, it would just guess at something random. I couldnt quickly figure out what exactly was wrong in my scripts that produced the api calls that was causing this, but wrapping the fragments in triple quotes was an easy fix and ensures the davinci API. 

I forgot to mention earlier, as we get into querying the API, that the name of the API we will query is called davinci, which is another API from OpenAI (the company who makes chatGPT) that is what ChatGPT is based on and provides very similar behavior. The current ChatGPT model does not  have an API available, but is supposed to soon. In any case, davinci responses are very very close. 

Once I had the snippets ready, I could start using the davinci api to add rich contextual data to them. By providing annotations and data labels, it can associate the code with additional context that makes it more useful for things like generating code or writing documentation.

But, just sending the snippets alone to ChatGPT won't provide the result we want, we need to first create a prompt that asks ChatGPT what we want it to do with the snippet, which in our case is to create annotations. Prompting ChatGPT is a fascinating area ... as massive neural nets are so complex, nobody can predict how the system will respond. Nobody can predict exactly what the best way to word a question is to get the most ideal responses, but it is very clear that small differences in how you ask questions can yield major differences in the response you get. 

Fortunately, this is one thing that ChatGPT is supposed to be pretty good at. And I spent hours and hours discussing and planning different ideas and approaches to this project. Should I go for a model where I have multiple backend specialized models each trained on different things, like perhaps one for idem and another for pop, or maybe one for idem code completion, one for idem conversational bot, etc. But while I do plan to play with lots of variations, my discussions with chatGPT left me feeling like training a single model to handle all of my desired outcomes may be optimal. So that is where I will start, and I will test a lot of different tweeks and variations as I continue down the road on this project.

Its also important to note, that the annotations and labels you use to describe the code can be optimized for different purposes, such as code completion, conversation or documentation writing. I want this model to do all of these, so I asked ChatGPT to provide a prompt that would be good at getting this type of result from davinci, and here is the prompt:
```Please provide a complete annotation for the following python code snippet that includes information about what the code does, any relevant details, and how it can be used in questions, documentation, and code creation:\n" + code + "\n"
```

These prompts are exactly like what you might type into the ChatGPT app. Where it says "+ code" near the end is where a single fragment would be injected into the prompt before being sent to the API. 

But first I needed to model how I wanted to record the results. The next step after the snippets are annotated will be to run the annotated snippets through a tokenizer, so I wanted to output the results in a format optimized for the tokenizer, which I thought would be json but ChatGPT thought that while json would work well, it may be better to provide a less structured format to the tokenizer, it actually recommended a plaintext format like:
```
code snippet
unlabeled annotation describing code snippet

code snippet
unlabeled annotation describing code snippet

code snippet
unlabeled annotation describing code snippet
```

But, I wasnt comfortable with this format, and ChatGPT indicated it really didnt matter much. I think this plaintext format is too fragile with lots of automated text processing, I think it could lead to issues. So after more discussing with ChatGPT, I decided to use a format that uses html/xml like tags, but does not need to comply with any standard and can be used as simple, clear delimiters. I used slightly unusual tags so it would be unlikely that they might be used in the body of a snippet, and did a search to confirm. I came up with a proposed format, ran it by ChatGPT, and it said it would work great so here is the template:
```xml
<a-block><a-snippet>
"""
def initialize_options(self):
    pass
"""
</a-snippet><a-annotation>This code snippet declares a function called initialize_options() which takes in an argument, self. This function does not have any code inside its body, indicated by the ‘pass’ statement. This function can be used to set initial values for an object, such as variables or settings. It can be used when creating questions, documentation, or code.
</a-annotation></a-block>
```

Next we need to prepare for how we will record the metadata returned from each API call. To do that I needed to know what response metadata was returned. I could have gone through docs but instead I ran an initial test API call to get back a response that I would use to model a template to format the responses from the API requests. 

Here is a sample return value:
```json
{'id': 'cmpl-6jUEARs3HmTgNDtOSMrs7LhZXdOS1', 'object': 'text_completion', 'created': 1676298974, 'model': 'text-davinci-003', 'choices': [{'text': '\nThis code snippet is a function definition for a class that handles an error when it is called. The function takes in two parameters, *args and **kwargs, and checks if a verror is present in the edict. If so, it raises a PopError exception with the error message and verror specified in the self() object. Else, it raises a PopError exception with the error message and exception specified in the self() object and traceback if present. This code can be used to produce an error message in a class when certain conditions are not met.', 'index': 0, 'logprobs': None, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 168, 'completion_tokens': 116, 'total_tokens': 284}}
```

Not sure why, but I decided to incorporate the return metadata into the same file where I have the snippets. This really does not make sense to do it this way, as I will just have to extract it from the annotated snippets file before tokenizing it anyway, and there is no reason to just not record them seperately. So in the future, I will change this step to put the raw json returns either in a file and then into a database or just directly into a database.That beind said, I did learn some interesting things from doing it this way ...

I decided I only want to keep some of the data in the response, and so while making the code to format it correctly isnt that hard, its monotonous and time consuming to do by hand. So instead I just mocked it up in yaml and asked ChatGPT both to convert it to json and to update my script logic to filter the return values to map to my output template. 
Here is the template after I added the structure for the return metadata:
```
<a-block><a-snippet>
"""
def initialize_options(self):
    pass
"""
</a-snippet><a-annotation>This code snippet declares a function called initialize_options() which takes in an argument, self. This function does not have any code inside its body, indicated by the ‘pass’ statement. This function can be used to set initial values for an object, such as variables or settings. It can be used when creating questions, documentation, or code.
</a-annotation><a-meta>
{
  "api_response_metadata": {
    "id": "<id_from_response>",
    "object": "<object_from_response>",
    "created": "<created_from_response>",
    "model": "<model_from_response>",
    "logprobs": "<logprobs_from_response>",
    "finish_reason": "<finish_reason_from_response>",
    "usage": {
      "prompt_tokens": "<prompt_tokens_from_response>",
      "completion_tokens": "<completion_tokens_from_response>",
      "total_tokens": "<total_tokens_from_response>"
    }
  }
}
</a-meta></a-block>
```

With a little help from ChatGPT I wrote some python to automate batching each snippet into a prompt, sending to the davinci API, and then recording the results. Here is the updated script:
```python
import requests
import json
import sys

def annotate_code(code):
    prompt = "Please provide a complete annotation for the following python code snippet that includes information about what the code does, any relevant details, and how it can be used in questions, documentation, and code creation:\n" + code + "\n"
    print(prompt)
    # Make a request to the OpenAI API
    response = requests.post("https://api.openai.com/v1/completions",
                             headers={"Content-Type": "application/json",
                                      "Authorization": "Bearer <API-KEY>"},
                             data=json.dumps({
                                 "model": "text-davinci-003",
                                 "prompt": prompt,
                                 "max_tokens": 1024,
                                 "temperature": 0.7,
                                 "top_p": 1
                             }))

    # Check if the request was successful
    if response.status_code == 200:
        print("API request successful")
        print(response.json())
        return response.json()
    else:
        print("API request failed")
        print(response.json())
        return None

def save_annotated_code(code, response, filename):
    api_response_metadata = {
        "id": response["id"],
        "object": response["object"],
        "created": response["created"],
        "model": response["model"],
        "logprobs": response["choices"][0]["logprobs"],
        "finish_reason": response["choices"][0]["finish_reason"],
        "usage": response["usage"]
    }

    # Remove any blank lines from the code
    code = '\n'.join([line for line in code.split('\n') if line.strip()])

    # Write the annotated code to a file
    with open(filename, "a") as f:
        f.write(f"\n<a-block><a-snippet>\n{code}\n</a-snippet><a-annotation>{response['choices'][0]['text']}\n</a-annotation><a-meta>\n")
        f.write(json.dumps(api_response_metadata, indent=2))
        f.write("\n</a-meta></a-block>\n")

    # Read the contents of the file, remove any blank lines, and write the contents back to the file
    with open(filename, "r") as f:
        lines = f.readlines()
    with open(filename, "w") as f:
        for line in lines:
            if line.strip():
                f.write(line)

    print(f"Annotated code saved to {filename}")

def parse_code_snippets(filename):
    with open(filename, "r") as f:
        code_snippets = f.read().split("-----delimiter-----")

    for i, code in enumerate(code_snippets):
        response = annotate_code(code)
        if response:
            save_annotated_code(code, response, filename.replace(".txt", "_annotated.txt"))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 annotate_snippets.py <filename>")
        sys.exit(1)

    parse_code_snippets(sys.argv[1])
```

A couple of key tuning parameters you can see in the code include temperature, tokens and top_p ... I spend more time in the [video I made on this topic](https://www.youtube.com/watch?v=QLm5irtOXmg) going into these details if you would like to learn more.

Before I batch all of my snippets through the API, its important to do enough testing to be sure you are happy with your final result, as running all the data through the API will cost money, not that much, but it can add up quickly and its important before running anything beyond some basic tests that you calculate costs - I will show how to calculate the costs in a follow-on post soon. But I ran through enough tests to ensure I was happy with the output and here is an example of return data from my samples:

```xml
<a-block><a-snippet>
"""
def __init__(self, msg, exception=None, traceback=None, verror=None):
    self.edict = {'msg': msg, 'exception': exception, 'verror': verror}
    self.traceback = traceback
"""
</a-snippet><a-annotation>
"""
This code snippet is a constructor for a class, which initializes the instance fields for the class. Specifically, it creates a dictionary called 'edict' with the keys 'msg', 'exception', and 'verror' and assigns the values of those keys to the arguments of the constructor. It also initializes the 'traceback' field of the class with the value of the argument 'traceback'. This code can be used in questions, documentation, and code creation by providing a way to initialize the fields of a class with the appropriate values. 
"""
</a-annotation><a-meta>
{
  "id": "cmpl-6jUDeIcLHtZRIhBg2YSLBWhs4iGsF",
  "object": "text_completion",
  "created": 1676298942,
  "model": "text-davinci-003",
  "logprobs": null,
  "finish_reason": "stop",
  "usage": {
    "prompt_tokens": 103,
    "completion_tokens": 118,
    "total_tokens": 221
  }
}
</a-meta></a-block>
<a-block><a-snippet>
"""
def __call__(self):
    """
        Return the error cases
        """
    return self.edict
"""
</a-snippet><a-annotation>
This code snippet defines a function named "__call__" that takes in a self argument. The function returns the "edict" property of the self argument. This function can be used to return the error cases of a given object or class, which can be helpful in debugging and testing code. It can be used in questions to ask how to return the error cases of an object or class, in documentation to explain how to return error cases, and in code creation to define a function that returns error cases.
</a-annotation><a-meta>
{
  "id": "cmpl-6jUDpvzrTmGBV028eE3o7o4ZQV9tr",
  "object": "text_completion",
  "created": 1676298953,
  "model": "text-davinci-003",
  "logprobs": null,
  "finish_reason": "stop",
  "usage": {
    "prompt_tokens": 72,
    "completion_tokens": 104,
    "total_tokens": 176
  }
}
</a-meta></a-block>
<a-block><a-snippet>
"""
def __getattr__(self, attr):
    """
        Return a lambda that returns the edict
        """
    return self.__calling_load_error__
"""
</a-snippet><a-annotation>
This code snippet defines a method called __getattr__() which is part of the class definition. The method takes two parameters, self and attr, and returns a lambda that returns the edict. This can be used to access a specific attribute of an object, allowing for more efficient and flexible code creation. Additionally, this can be used in questions to access a specific attribute of an object and in documentation to explain the functionality of the __getattr__() method.
</a-annotation><a-meta>
{
  "id": "cmpl-6jUE0G6IuTH00psGbCOLTnmSIvA7J",
  "object": "text_completion",
  "created": 1676298964,
  "model": "text-davinci-003",
  "logprobs": null,
  "finish_reason": "stop",
  "usage": {
    "prompt_tokens": 85,
    "completion_tokens": 96,
    "total_tokens": 181
  }
}
</a-meta></a-block>
```


The next step is to split up our ~700 snippets into smaller files for batch processing. The way the code works is, it accepts an input file which includes a list of snippets, parses that file and makes api requests for each record in the source file. Once I automate this into a pipeline later I will adjust this method some, but for now since I am doing it manually I just used some python to split my file with all of snippets into multiple files with 50 snippets each. Here is the code I used for that:
```python
def split_file(filename, max_splits):
    with open(filename, "r") as f:
        content = f.read()

    parts = content.split("\n-----delimiter-----\n")
    for i in range(0, len(parts), max_splits):
        with open(f"{filename}_{i}.txt", "w") as f:
            f.write("\n-----delimiter-----\n".join(parts[i:i + max_splits]))

if __name__ == "__main__":
    filename = "input_file.txt"
    max_splits = 50
    split_file(filename, max_splits)
```

And that is where I ran out of weekend and paused to write this blog. Next I will going to be running a single batch through so I can calculate my average and predicted costs for running all the records, and then run all the records through. There are a lot of potential optimizations we could test at this stage, for example we could test different prompts, models, temperature, top_p values to evaluate how different inputs correlated to different response values for further tuning. I will reserve any further tuning of these parameters for now, and will continue to process all the data and move forward with some data cleaning, tokenization and generating embeddings next weekend, and hopefully get started processing our next input source. I will keep moving forward with it next weekend and report more findings.

I'm excited to continue working on this project and sharing my progress. Stay tuned for updates!