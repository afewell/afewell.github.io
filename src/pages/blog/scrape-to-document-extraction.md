---
layout: $/layouts/post.astro
title: "Automated Data Ingestion and AI-Assisted Extraction with GPT-4 and example extraction from VMware Tanzu documentation - Part 1"
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

For a project I am working on now, I want to create a list of Tanzu CLI commands in a specific format. Tanzu CLI has hundreds of commands each with different options. I need to look at the detailed documentation for command groups to get the level of detail I want to extract, which involves processing hundreds of pages of data. 

To automate this process, I am using the python scrapy web scraping library configured to crawl a website, or a subsection of a website. For this example, I wanted to identify all pages within the Tanzu Application Platform (TAP) 1.4 documentation that document the tanzu CLI plugins that are specific to TAP. Docs.vmware.com is a really massive website, it not only has the complete documentation for every single VMware product, it has documentation for every version of every current VMware product. 

I dont have any data on how big it is, but, its massive. Just crawling this entire site would be a very inefficient way to identify the specific documents I need, so I originally tried a simple filter to restrict the crawling behavior, which ended up being overly restrictive and not identifying all the documents I needed. I ended up implementing a multi-tiered filtering logic that strikes the right balance between finding all the relevant URLs I want while still being fast and efficient. I will explain in more detail in the scraping section below. 

Once the data is gathered and cleaned with scrapy, another function inserts the ingested text into a prompt and uses the openai python library to query GPT-4 with a prompt that successfully instructs GPT-4 to look through the provided text and extract the information I want based on a reference pattern, and formats its return in the exact format I specify in the prompt. I wrote a separate [blog post about this prompt you can find here.](https://artfewell.com/blog/fewshot-command-extraction/)

## Scraping the pages that you want

Here is my scrapy code:
```
import scrapy
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse
from scrapy.selector import Selector

class UrlScraperSpider(CrawlSpider):
    name = 'url_scraper'
    allowed_domains = [os.environ.get('ALLOWED_DOMAINS')]
    start_urls = [os.environ.get('START_URLS')]

    rules = (
        Rule(LinkExtractor(allow=os.environ.get('ALLOW_RULE')), callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(UrlScraperSpider, self).__init__(*args, **kwargs)
        self.urls = set()

    def parse_item(self, response):
        links = LinkExtractor(allow=os.environ.get('PARSING_RULE')).extract_links(response)
        for link in links:
            url = urlparse(link.url)._replace(fragment='').geturl()
            self.urls.add(url)
        return {}

    def closed(self, reason):
        with open('urls.txt', 'w') as f:
            f.write('\n'.join(sorted(self.urls)))


class HtmlScraperSpider(scrapy.Spider):
    name = 'html_scraper'
    allowed_domains = [os.environ.get('ALLOWED_DOMAINS')]

    def __init__(self, *args, **kwargs):
        super(HtmlScraperSpider, self).__init__(*args, **kwargs)
        os.makedirs('/scrapy/html', exist_ok=True)
        self.start_urls = self.get_start_urls()

    def get_start_urls(self):
        with open('urls.txt', 'r') as f:
            urls = f.read().split('\n')
        return urls

    def parse(self, response):
        filename = os.path.join('/', 'scrapy', 'html', response.url.split('/')[-1])

        content = response.css('div.rhs-center.article-wrapper').get()

        if content:
            content = Selector(text=content).xpath('//text()').getall()
            content = ''.join(content).strip()

            with open(filename, 'w') as f:
                f.write(content)

        return {}
```

The way I have it configured now is to use one process to gather the URL's that I want to scrape from the site, which is handled by the UrlScraperSpider class in the above code. I then run a separate function to download and clean each of the URL's identified by UrlScraperSpider. This second function is called HtmlScraperSpider in the above code.

### About UrlScraperSpider

If you look at the scraper code, you can see I gather 4 environmental variables for this function: ALLOWED_DOMAINS, START_URLS, ALLOW_RULE and PARSING_RULE. To explain how this works, it will help to provide the values I used for this example:
```
export ALLOWED_DOMAINS=docs.vmware.com
export START_URLS='https://docs.vmware.com/en/VMware-Tanzu-Application-Platform/index.html'
export ALLOW_RULE="en/VMware-Tanzu-Application-Platform/1.4/*"
export PARSING_RULE='en/VMware-Tanzu-Application-Platform/1.4/tap/cli-*'
```
Here I will explain how each of these values work. Please keep in mind these need to be from least restrictive to most restrictive, in order from top to bottom.

The ALLOWED_DOMAINS value is the highest level filter, in this case it ensures the crawler only looks at urls within docs.vmware.com.

The START_URLS provides the seed page that the crawler starts with. The crawler then works recursively to map all links it can find on this page, and then recursively maps until it maps every link on every page it can find from this seed page. In this specific case, if not for the ALLOW_RULE, it would map the entire docs.vmware.com site and would map even more if it did not have the ALLOWED_DOMAINS filter. It is important to make sure you include a start url that is linked through recursive mapping to the target URL's you want to collect. 

The ALLOW_RULE restricts the behavior of the crawler, and so the crawler will only crawl pages that match the pattern specified in the ALLOW_RULE. 

I originally used the ALLOW_RULE to try to find all the pages I wanted, and it did have results, which highlights a tricky aspect of this project ... do you know how many pages match your pattern? This may be known at times, but often times it is not, so you need a mechanism to ensure your results are accurate. In my case, I ran an instance of UrlScraperSpider with less restrictive filters to gather a much larger list of URLs, and then used `cat urls.txt | grep <pattern> | wc -l` to see if I was actually finding all the URLs, and I discovered a problem with the filtering logic. 

Using only the ALLOW_RULE can run into an issue if a page you want is a child of a page you dont want. Remember the crawler starts at the starting rule, and it has to crawl through pages starting with the start URL, and then navigates through linked pages so long as each page it finds matches the ALLOW_RULE pattern. But if a page that doesnt match your pattern sits between the start URL and pages with the pattern you want, the crawler will not find all the pages you want. In that sense, eliminating the ALLOW_RULE entirely should still eventually get your desired results, but in a large site like docs.vmware.com, this would mean making the crawler crawl through tons of irrelevant pages to find your data. 

The PARSING_RULE does not restrict the behaviour of the crawler. In the code above, the `__init__` function within the UrlScraperSpider class initiates the crawler using the ALLOWED_DOMAINS, START_URLS, and ALLOW_RULE to define the behaviour of the crawler. After this function crawls the website, it then calls the parse_item function, which applies the PARSING_RULE, which filters all the URLs that were crawled to only the URL's that match the pattern defined in the PARSING_RULE. 

With the combination of these filters, I restricted the crawler to only crawl and gather the URL's for the Tanzu Application Platform 1.4 documentation. Since I gathered the URLs for the entire TAP 1.4 documentation, I can be sure I can find all of the URLs in the documentation that match the pattern I want in the PARSING_RULE. The code then parses the URLs to only those I want, and creates a urls.txt file with the results. I could have had it output json and may eventually, but as it is it places one complete URL on each line in a text file which is all the structure I need to loop through each listed URL. 

### The HtmlScraperSpider

Once the UrlScraperSpider generates the urls.txt file, I call the HtmlScraperSpider to process the urls.txt file, and download each of the URLs, parse the section of the page I want to keep, and then clean the metacharacters while preserving new lines and spacing as that context is important to properly extract the data I want. 

The most important part of this class to highlight is in its parse function, specifically the line `content = response.css('div.rhs-center.article-wrapper').get()`. This line instructs the parser to only keep content that is within the tag div.rhs-center.article-wrapper, which is a tag that is specific to the docs.vmware.com website and highlights a challenge with scraping data from websites ... there is tons of irrelevant metadata on most sites. 

In some cases you may want all the data from the webpage, but in most cases you probably want data from the main body of visible text on the page, which in many cases is much smaller than all the irrelevant metadata. You could just send the whole pages worth of data and metadata to the AI model and I do suspect that it is often smart enough to figure it out, but, that is problematic on many levels. 

In this case, I am fortunate that I am only gathering data from docs.vmware.com, and this site has a very consistent structure. I can use dev tools to find that for documentation page, the tag `div.rhs-center.article-wrapper` is a consistent wrapper just for the main visible text. Accordingly, as long as I am only gathering data from docs.vmware.com, this should work pretty consistently, but, if I want to target a different website, I would on a site-by-site basis need to adjust this value, and that is only if a given site is consistently organized and tagged, if not, this could be a much bigger challenge. 

In a future post, I will explore python's unstructured library, which provides a universal method for ingesting and organizing not just HTML, but bunches of different types of documents, and then applying intelligent tagging to the various sections of the input document, such that you could conceivably create a universal ingester. This could potentially allow you to target the main body of text with one consistent logic on a wide variety of websites for example. I havent played with it enough yet to know if it will work ideally for this use case, but it looks very promising and I will definitely write some future posts about this.

#### Additional challenges with token prediction and chunking

There is sort of a 2-fold big whammy problem here, you may not care about cost as it pertains to finding the answer you want, but you almost certainly dont want to pay more by including a bunch of irrelevant data from ingested pages. And worse, what if all the irrelevant data makes the responses from the AI less accurate, which I imagine it would to at least some extent. And so you end up paying a lot more for worse results. 

Another big challenge this complicates is data chunking. How large is the content you want to send to the AI? If its larger than you can send in one query, you have to add logic to break your data into chunks, which is very tricky. If you arbitrarily break your data into chunks, you will most likely break it in the middle of some important logic, and so when the AI has to look separately at each chunk of data, it may not be able to find the relevant data you need. 

The reality is you may not be able to avoid the need to chunk data at all, its a standard part of most data processing pipelines and I have blogged about some chunking methods before. While the provided code should work well in this case, I am making some shortcuts here that I will need to address soon ... that is, I really need to add a token predictor to predict token usage to determine if it needs to be chunked. And if data does need to be chunked, what is the best way to chunk it and how do you create or configure a chunker that will behave how you want it to. 

In this specific case however, I took a shortcut to bypass the chunking issue at the expense of cost and possibly missing important data ... so I will not consider this code complete until I add those capabilities, which I will add and share in a blog post soon. 

The shortcut I took is, in this case, the documentation for the Tanzu CLI commands is already broken up into relatively small sections, and accordingly I think I can get away with skipping the chunking for now. That being said, I have already found that some of these pages + the AI response is more than the 4096 tokens than can be handled by gpt-3.5-turbo, but I _think_ the pages + responses will be small enough to fit into the larger 8096 token limit I can access through the GPT-4 API. Note that GPT-4 has an API that can handle 32k tokens which will be amazing for certain use cases, but all GPT-4 access is in beta and I only have been given access to the 8k model so far. Even still, all GPT-4 access is orders of magnitude more expensive than gpt-3.5, and GPT-4 32k is even more expensive per token than gpt-4 8k. These larger contexts will unlock powerful use cases, but in most cases where chunking can work, it will be well worth it.

So since I am not doing any chunking of my data in this code, the most obvious inneficiency is that I am paying substantially more to use GPT-4, and in this case I have already verified that, in the cases where the pages are short enough to use gpt-3.5, it produces comparable code. So in the near future I will add a token predictor and depending on the prediction to determine whether to send to gpt-3.5, to send to gpt-4, or if larger, I will need to find a chunking method that works optimally with my data and target goal. I may end up adding a vectorizing step and query a vectordb for data rather than trying to preserve the exact original context as I am in this code. I am sure I will end up testing a few approaches and will write additional blogs with the results I find. In general I find that vectorizing and integrating a vector db search can ease some of the challenges 

## Summary and part 2

This post is already pretty long, and since the scraping job and the calls to openAI are separate functions. It makes sense to break this blog into 2 parts. The first part here described how we are doing the scraping and cleaning. Part 2 will cover the rest of the process to automatically insert each piece of source data into a prompt that is used to query openAI as many times as needed for the dataset, and organize the response into a common json schema. 

I have already completed the code for part 2, so I should be able to have the blog published within a day or 2, so please stay tuned for part 2! Thanks for reading!