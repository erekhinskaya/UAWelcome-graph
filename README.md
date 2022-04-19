
![made-with-python](https://img.shields.io/badge/Made%20with-Python3-brightgreen)

<p>
<img src="static/images/heart.png" width="360"/>
</p>
# UAWelcome

## Graphs connecting people to help the refugee crisis

UAWelcome is a graph-based crowdsourcing platform connecting refugees with those who can help, optimizing limited and scattered resources. Designed to be simple to use and maintain for rapidly changing workflows.

## Features
- Management of refugee and volunteer data in TigerGraph
- Importing CSV data collected from user-facing online forms
- Providing task-specific views of data (i.e. Ticket donators for email campaign). Designed so that adding a new view only takes a single GSQL query and <20 lines of code. The idea is to help volunteers navigate through data in most efficient way, as well as protect data from accidental changes
- Matching people in need to those who can help. Done with a GSQL query that checks hard constraints of the match - i.e. shared language and maximizes for better individual experience while optimizing the usage of resource pool.

## Tech

Built on top of a number of open source projects to work properly:

- [Flask] -  a micro web framework written in Python
- [pyTigerGraph] - a Python package for connecting to TigerGraph databases
- [Twitter Bootstrap] - UI boilerplate for modern web apps
- [jQuery] - a fast, small, and feature-rich JavaScript library

## Installation

UAWelcome requires [Python](https://python.org/) v3.9.10 to run.
Install the dependencies from requirements file and start the server.

```sh
cd dillinger
npm i
node app
```

## Docker
You can try out UAWelcome in a Docker container.
Download the image from TODO, load it and run as shown below. You can change tigergraph.yaml to use your Tigergraph instance - see [/Tigergraph] section below 

```sh
docker load -i windowsservercore.tar
docker run -d -p 5000:5000 --name=uawelcome TODO tigerfile
```

## Quick Start Guide

We recommend you to create your own instance of TigerGraph. The graph used by default is shared between users, so you might see different results depending on other user actions.

1. Upload the csv from ./data folder in Upload & Parse CSV app.
2. See a simple view for Ticket Donators - these are people selected by appTicketDonators query. You can export the data as a csv, upload it to MailChimp and do an email campaing.
3. There is a number of views for Verification of Refugees, Angels (those who hosts and directly helps Refugees), and Volunteers (those who coordinate the operations - the primary users of the platform). When user works on verification, the idea is to contact the person, double-check the data and mark as verified to be picked up by downstream tasks. For more details, please see the app-specific GSQL query.
4. Matching apps allow to connect the need and available resource. You can see a single need on top, as well as options at the bottom.  TODO - you can see that 
 For more details, please see the app-specific GSQL query.

## Development

Want to contribute or use it for your team? Great!

### Create a new View

### Create a new Matching

## TigerGraph
The ./tigergraph folder contains the schema and GSQL queries used in this project. 
You can import it to your instance for full control: https://docs.tigergraph.com/gui/current/graphstudio/export-and-import-solution

## Team
The project was started for TigerGraph hackaton by:
[Tatiana Erekhinskaya] - Tech Lead, please contact via LinkedIn
[Kateryna Panova] - Project Lead
[Princess Dickens] - Content Lead

## Credits
The interactive html table implementation were inspired by these guides:
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
MD.txt
Displaying MD.txt.