
![made-with-python](https://img.shields.io/badge/Made%20with-Python3-brightgreen)
<h1>
<p align="center">
  <img src="static/images/heart.png" alt="Logo" width="300">
  <br>UAWelcome
</h1>
<h2>
  <p align="center">
Graphs connecting people to help the refugee crisis  <br />
    </p>
</h2>
</p>


UAWelcome is a graph-based crowdsourcing platform connecting refugees with those who can help, optimizing limited and scattered resources. Designed to be simple to use and maintain for rapidly changing workflows.

## Features
- Management of refugee and volunteer data in TigerGraph
- Importing CSV data collected from user-facing online forms
- Providing task-specific views of data (i.e. Ticket donators for email campaign). Designed so that adding a new view only takes a single GSQL query and <20 lines of code. The idea is to help volunteers navigate through data in the most efficient way, as well as protect data from accidental changes
- Matching people in need to those who can help. This is done with a GSQL query that checks the hard constraints of the match, i.e. shared language, and maximizes the matching of other factors for better individual experience and the optimization of resources.

## Tech

Built on top of a number of open source projects to work properly:

- [Flask] -  a micro web framework written in Python
- [pyTigerGraph] - a Python package for connecting to TigerGraph databases
- [Twitter Bootstrap] - UI boilerplate for modern web apps
- [jQuery] - a fast, small, and feature-rich JavaScript library

## Installation

UAWelcome requires [Python](https://python.org/) v3.9.10 to run.
Install the dependencies from requirements file and start the server.

## Docker
You can try out UAWelcome in a Docker container.
Download the image from https://github.com/erekhinskaya/UAWelcome-graph/releases/download/v0.0.1/uawelcome.tar.zip, unzip, load it and run as shown below.
You can change app-config.properties to use your Tigergraph instance.

```sh
docker load -i uawelcome.tar
docker run -d -p 5000:5000 --name=uawelcome 

```
## TigerGraph
If you want to use your instance of Tigergraph, please see the ./tigergraph folder with exported schema and GSQL queries used in this project. 
You can import them to your instance for full control: https://docs.tigergraph.com/gui/current/graphstudio/export-and-import-solution

## The Schema
Vertices represent people, the services they might need and the services they can offer. There are a variety of services with different attributes that can be exchanged. Also, volunteering activities such as Writing are represented separately as they are semantically different from helping refugees directly.

## Quick Start Guide

We recommend that you create your own instance of TigerGraph. The graph used by default is shared between users, so you might see different results depending on other user's actions.

1. Upload the form submission information ./data/demo_data.csv under Upload & Parse CSV app.
2. See a simple view for Ticket Donators - these are people selected by appTicketDonators query. You can export the data as a csv, upload it to MailChimp and do an email campaign. This is all you need to know at this point as a volunteer, nothing extra.
3. There are a number of views for the Verification of Refugees, Angels (those who hosts and helps Refugees directly), and Volunteers (those who coordinate the operations - the primary users of the platform). When a user works on verification, the idea is to contact the person, double-check the data and mark it as verified, so that the record is picked up by downstream tasks.
4. Matching apps allow us to connect  needs with available resources. You can see a single need on top, as well as options at the bottom.  If you run this scenario on top of the empty store, you can see that the first match shown requires the hosting for 4 people, while the next one goes down to 3. The overall idea of matching is to provide for the needs of refugees as best we can while avoiding the wasted resources. 
5. Entity Resolution. There is an early version of resolving person entities based on matching names, emails and phone numbers.

## Development

Want to contribute or use it for your team? Great!

### Create a new View
View is basically a table generated from the attributes of a person and services they can provide. This is mostly used for verification and collecting further details. You would need to create a single GSQL query to fetch the data, and a few lines of code to communicate how columns should behave - uneditable/editable text, drop down, etc.

### Create a new Match
The needs and available resources are sorted from larger/harder to smaller/easier. Then for each need, we find K resources (looping top-down on the sorted resource) that satisfy some hard-limit criteria and were not yet assigned more than M times. We can further enhance these benefit scores and do a full-blown [Assignment Problem]( https://en.wikipedia.org/wiki/Assignment_problem), but the current priority is to have a sub-optimal solution that is easy to maintain as we keep gathering insights. From architecture perspective, GSQL is flexible to represent the whole algorithm in one query, making it easy to maintain.

For a new match app, you need to create two per-installed queries: 
1. matchResourceType for generating candidate pairs. The ResourceType should be the exact Vertex type from the graph schema.
2. printResourceType for displaying the tables.

On the code side, all you need to do is extend Matcher<ResourceType>(AbstractMatcherApp).

## Vision

- to expand to all forms and tasks currently at hand
- improve UI to minimize clicks
- include guidelines for outliers and edge cases - general and specific (i.e. if you see that an applicant filled out the wrong form - fill out a correct form with relevant data, and remove the current record)
- error handling  

### Must-have Features:
1. Scaling for larger teams:
    - authentications & access group (can be modelled in the graph together with processes)
    - concurrent updates
2. Smarter parsing - mapping from original forms/csv headers to parsing functions to vertex attributes
3. User profile page to be able to enable/disable types of activities, maintain schedule 
4. Handling temporality - "X provides accommodation for Y from Date1 to Date2"

### In The Longer Run:
1. NLP - parse textual fields to extract more information about needs, recognize mistakes (contradicting data, filling a wrong form).
2. Machine Translation, to overcome language barrier for volunteers helping multi-language cases.
3. The overall ambition is to become an open-source crowdsourcing platform that can be used for various social causes.  



## Team
The project was started for the TigerGraph hackathon by:
  
[Tatiana Erekhinskaya] - Tech Lead, please contact via LinkedIn
  
[Kateryna Panova] - Project Lead
  
[Princess Dickens] - Content Lead

## Credits
The interactive html table implementation was inspired by these guides:
  
https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates
  
https://tutorial101.blogspot.com/2021/04/live-editable-table-using-python-flask.html

## License

MIT


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
   [Flask]: <https://github.com/pallets/flask>
   [pyTigerGraph]: https://github.com/pyTigerGraph/pyTigerGraph
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [Tatiana Erekhinskaya]: <https://www.linkedin.com/in/tatiana-erekhinskaya/>
   [Kateryna Panova]: <https://www.linkedin.com/in/kateryna-panova/>
   [Princess Dickens]: <https://www.linkedin.com/in/princess-dickens/>
