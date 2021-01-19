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


# vivino top rated wines

Scrape the data of the top rated wines for the highest ranked vivino users via selenium for python and Mozilla Firefox webdriver

- "https://www.vivino.com/users/{user_id}/top"

# Wines recommendations

The notebook [vivino_wines_recommendations.ipynb](https://github.com/sansar-choinyambuu/vivino-users/blob/main/vivino_wines_recommendations.ipynb) presents a collaborative filtering-based recommendation system for wines and users.
The model fills a user-item matrix, providing recommendations in both directions: wines to users and users to wines.
The model is built with the support of [pyspark.ml](https://spark.apache.org/docs/latest/api/python/pyspark.ml.html) and the [Alternating Least Squares (ALS)](https://dl.acm.org/doi/10.1109/MC.2009.263) algorithm. 

## Wines ratings graph

A basic analysis of a graph of users and their rated wines is performed with [GraphFrames](https://graphframes.github.io/graphframes/docs/_site/index.html)