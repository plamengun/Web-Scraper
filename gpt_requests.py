import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.environ.get('OPENAI_ORG')
openai.api_key = os.environ.get('OPENAI_API_KEY')
completion = openai.ChatCompletion()

PROMPT = """
RULES
Keep the length of the proposal similar to the job post length.
Don’t use “I” in the first sentence.
Depending on the industry and the business, there are a few main outcomes most businesses desire. If it is not specified in the job post, incorporate one of the examples below so it makes sense:
For SaaS companies, it is reduced CPL, increased retention, increased subscriptions, and cheaper leads and signups
For Local businesses, it is reduce of CPL, Cost of appointment,
For ecom businesses and online shops/brands, it is an increase in the:
ROAS
ROI 
sales 
Revenue
More sales
Campaign management and optimization

Greeting and Introduction

Hi 👋, [Name] [insert a short summary of his posts in "you" format]. For the last 5 years, I’ve been doing precisely this. Helping [insert what their problem, challenge, or need is based on the job post]. 

With my experience managing ad spending up to 7 figures, I can bring expertise to [Inser resolution to their problem], and I'm ready to talk clearly and quickly through. 

Let’s discuss your business needs in detail on a call!
Customized Case Study Introduction
If you want to look at my past work and dig a bit deeper before deciding, here are some links that can help you choose

This is what I do https://sendspark.com/share/klnb2ya67spxe8dq
. 
[insert a link to a case study that matches their industry or business, followed by a brief explanation of the case study]
Body
Over the years, I've managed over $60 million in Facebook & Instagram ad spend, generating over $110 million in revenue across various industries. This has given me a comprehensive understanding of how to  [insert their desired result, it could be increasing their ROAS,ROI scaling their business.. or reducing their CAC,CPL,CPP]
Moreover, my continuous interaction with Facebook representatives has given me insider knowledge of the most effective current practices. My focus lies in performance-based marketing, aiming to provide optimal [insert desired outcome based on their job post] for businesses in the [insert their industry or type of business].
Offer
I'd be happy to offer you a free consultation call. I am available Tomorrow or the day after. Let me know which of these days suits you best for a free consultation call.

Looking forward to hearing from you,
Best,
Miro



#1 Job post:
We are looking for an experienced advertiser who can help scale our online store through effective ad campaigns. The ideal candidate should have a strong understanding of digital advertising platforms and techniques. They should be able to create compelling ads that drive traffic and conversions. The main responsibilities of this role include designing and launching ad campaigns, optimizing performance, and analyzing results to make data-driven decisions. Key skills required for this role include:


#1 Cover Letter example:
Hi 👋, It seems like you are looking for an experienced advertiser who can help scale your online store.  For the last 5 years, I’ve been doing precisely this I've been helping online stores scale through effective ad campaigns. With my experience managing ad spending up to 7 figures monthly, I can bring tons of expertise to your business.


Let’s discuss your business needs in detail on a call!

If you want to look at my past work and dig a bit deeper before deciding, here are some links that can help you choose.

This is what I do: https://sendspark.com/share/klnb2ya67spxe8dq

Here's how I helped a similar business achieve their goals: https://drive.google.com/file/d/1L8TKTXKjJ36EgpIXfHya-JgjGz8fd-Lw/view?usp=sharing ($120K daily ad spent)

Portfolio:
https://drive.google.com/file/d/1tvDnGSzbzDGLMMGF_OvFe2VD9xfRoiAF/view?usp=sharing (collection of case studies for different online brands)


Over the years, I've managed over $60 million in Facebook & Instagram ad spend, generating over $110 million in revenue across various industries. This has given me a comprehensive understanding of increasing your ROAS and scaling businesses like your online store.

My focus lies in performance-based marketing, aiming to provide optimal results for businesses in the e-commerce industry.

I'd be happy to offer you a free consultation call. I am available Tomorrow or the day after. Let me know which of these days suits you best for a free consultation call.

Looking forward to hearing from you,
Best,
Miro



#2 Job post:
We are an emerging startup looking for an experienced and result-driven Meta Ads Manager to help elevate our marketing campaigns to the next level. You should have extensive experience working with the Meta (formerly Facebook) Ads Manager and be comfortable creating, managing, and optimizing campaigns from scratch.


Responsibilities:

Set up and manage our Meta Ads campaigns.
Conduct A/B testing to validate various hypotheses.
Monitor and analyze campaign results to maximize efficiency.
Create detailed reports on the performance of our campaigns.
Work closely with our team to ensure our marketing objectives are achieved.


Requirements:

At least 3 years of experience managing Meta Ads campaigns.
Familiarity with A/B testing and data-driven marketing.
Strong analytical skills and experience interpreting campaign data.
Excellent communication skills and the ability to report clearly and accurately.
Experience working with startups or in a fast-paced environment is a plus.

Please include in your application examples of successful campaigns you have managed in the past, as well as specific data that demonstrate your skills and experiences.
Note that we will be providing the creatives and texts, and you will be responsible for setting up and optimizing the campaigns.

We look forward to hearing from you!


#2Cover Letter example:
Hi 👋, It seems like you're in need of an experienced and result-driven Meta Ads Manager to elevate your marketing campaigns. For the last 5 years, I’ve been doing precisely this. I've been helping startups to reach new heights by creating, managing, and optimizing campaigns on Facebook. With my experience managing ad spending up to 7 figures monthly, I can bring tons of expertise to your business.


Let’s discuss your business needs in detail on a call!

If you want to look at my past work and dig a bit deeper before deciding, here are some links that can help you choose.

This is what I do: https://sendspark.com/share/klnb2ya67spxe8dq

Here's how I helped a similar business achieve their goals:
https://drive.google.com/file/d/1L8TKTXKjJ36EgpIXfHya-JgjGz8fd-Lw/view?usp=sharing (Managed $1M monthly ad spent for online business)

Portfolio: https://drive.google.com/file/d/1tvDnGSzbzDGLMMGF_OvFe2VD9xfRoiAF/view?usp=sharing (collection of case studies for different companies)

Over the years, I've managed over $60 million in Facebook & Instagram ad spend, generating over $110 million in revenue across various industries. 

My focus lies in performance-based marketing, aiming to provide optimal results for businesses like yours.

I'd be happy to offer you a free consultation call. I am available Tomorrow or the day after. Let me know which of these days suits you best for a free consultation call.

Looking forward to hearing from you,
Best,
Miro


JOB POSTING

QGIS Plug-in Development\nWe are seeking an experienced software developer to create a custom plug-in for QGIS, version 3.28 or higher, that will revolutionize the process of determining optimal wind farm locations. The final product will be a powerful tool to automatically identify prospective zones for wind farm placement based on specified input criteria.\nKey Features:\n\u00a0\u00a0\u00a0\u00a0\u2022 Automated determination of perspective zones for wind farm locations.\n\u00a0\u00a0\u00a0\u00a0\u2022 Seamless integration as a QGIS plug-in.\n\u00a0\u00a0\u00a0\u00a0\u2022 Intuitive user interface for setting search criteria.\n\u00a0\u00a0\u00a0\u00a0\u2022 Visualization of identified areas as polygons.\nPlug-in Usage:\n\u00a0\u00a0\u00a0\u00a01. Installation\n\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a01. Install the plug-in from the provided package or QGIS repository.\n\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a02.\u00a0\u00a0Load the required layers into QGIS.\n\u00a0\u00a0\u00a0\u00a02. Configure search criteria.\n\u00a0\u00a0\u00a0\u00a03. Initiate the wind site area search.\n\u00a0\u00a0\u00a0\u00a04. Manual change of the polygons.\n\u00a0\u00a0\u00a0\u00a05. Update the statistics of polygons.\nPlug-in Results:\n\u00a0\u00a0\u00a0\u00a01. Polygons which meet search criteria depicted on the map.\n\u00a0\u00a0\u00a0\u00a02. Key statistics calculated for each polygon as its attribute, depicted on the map.\nThe plug-in will efficiently identify intersections of layers based on the specified criteria, displaying the results as polygons and statistics of each polygon. The input data for calculations can be accessed via the provided link.\nSupport and System Requirements: The selected developer will be required to provide support for the software for a period of 2 months after project completion. The software should be compatible with the following operating systems:\n\u00a0\u00a0\u00a0\u00a0\u2022 Windows 7 or higher\n\u00a0\u00a0\u00a0\u00a0\u2022 Linux Mint 21.2 or higher\nBefore commencing work, the developer must sign a Software Development Agreement.\nProposal Requirements: If you are experienced in developing QGIS plug-ins and are interested in this project, please include the word \"QGIS\" at the beginning of your proposal. Additionally, kindly provide the following information:\n\u00a0\u00a0\u00a0\u00a0\u2022 Estimated project timeline.\n\u00a0\u00a0\u00a0\u00a0\u2022 Development cost estimate.\nThis is an exciting opportunity to contribute to a cutting-edge project in the field of renewable energy. If you're ready to take on this challenge and make a significant impact, we look forward to receiving your proposal.\nPlease propose your delivery schedule in order to meet the Deadline of September 15th
"""


# def askgpt(question, chat_log=None):
#     if chat_log is None:
#         chat_log = [{
#             'role': 'system',
#             'content': """As a marketing professional with over five years of experience, 
#                             you are actively bidding on relevant job postings on Upwork. 
#                             To streamline this process, you're leveraging personalized templates that comprise an introduction and a body.
#                             These templates are adapted according to the specific job post to reflect a professional, confident, and friendly tone.
#                             At the end of the template there are examples of job posts and examples of proposals to help you write.
#                             You can find the job posting that you need to apply to under JOB POSTING title."""
#         }]
#     chat_log.append({'role': 'user', 'content': question})
#     response = completion.create(model='gpt-3.5-turbo', messages=chat_log)
#     answer = response.choices[0]['message']['content']
#     chat_log.append({'role': 'assistant', 'content': answer})
#     return answer

# print(askgpt(PROMPT))



def askgpt(questions, chat_log=None):
    if chat_log is None:
        chat_log = [{
            'role': 'system',
            'content': """As a marketing professional with over five years of experience, 
                            you are actively bidding on relevant job postings on Upwork. 
                            To streamline this process, you're leveraging personalized templates that comprise an introduction and a body.
                            These templates are adapted according to the specific job post to reflect a professional, confident, and friendly tone.
                            At the end of the template, there are examples of job posts and examples of proposals to help you write.
                            You can find the job posting that you need to apply to under JOB POSTING title."""
        }]
    
    if not questions:
        return chat_log
    
    question = questions[0]
    chat_log.append({'role': 'user', 'content': question})
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="\n".join([message['content'] for message in chat_log]),
        max_tokens=100
    )
    
    answer = response.choices[0]['text']
    chat_log.append({'role': 'assistant', 'content': answer})
    
    # Recursively call askgpt with the remaining questions
    return askgpt(questions[1:], chat_log)

# Example usage:
# questions = [PROMPT, "What are some tips for writing an effective proposal?", "How can I stand out to clients on Upwork?"]
# log = askgpt(questions)
# # print(log)
# # for entry in log:
# #     print(entry)
# for entry in log:
#     if entry['role'] == 'assistant':
#         print(entry['content'])