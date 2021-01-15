# vivino-users

Scrape the data on vivino users via following API's
- HTTP POST https://www.vivino.com/users/x/country_rankings - top ranked users for a country
```
  {
      "page": 1,
      "country_code": "ca"
  }
```
- HTTP GET http://app.vivino.com/api/users/mikhail-mikhail20 - user information
- HTTP GET http://app.vivino.com/api/users/mikhail-mikhail20/followers?start_from=0&limit=10 - followers of user 
- HTTP GET http://app.vivino.com/api/users/mikhail-mikhail20/followers?start_from=0&limit=10 - following of user

# Graph analysis

The notebook [vivino-users-graph-analysis.ipynb](https://github.com/sansar-choinyambuu/vivino-users/blob/main/vivino-users-graph-analysis.ipynb) is used to analyze the vivino users in graph context. 
Vivino users are graph vertices and the follower relationships build the edges between the vertices. Apache Spark's [GraphFrames](https://graphframes.github.io/graphframes/docs/_site/index.html) library is used to analyze the graph. For visualizations [networkx](https://networkx.org/) and [pyvis](https://pyvis.readthedocs.io/en/latest/index.html) packages are used.

## Community detection
A community detection algorithm LPA Label Propagation Algorithm was ran on the graph of vivino users. For details please open the [above notebook](https://github.com/sansar-choinyambuu/vivino-users/blob/main/vivino-users-graph-analysis.ipynb). One of the resulting communities were plotted interactively in the following html using the [pyvis](https://pyvis.readthedocs.io/en/latest/index.html) library

[Interactive plot of a vivino user community](https://github.com/sansar-choinyambuu/vivino-users/blob/main/nx.html)


