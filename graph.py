from graphframes import *

users = sqlContext.createDataFrame(df.drop(["image", "background_image", "address", "statistics"], axis = 1))
relationships = sqlContext.createDataFrame(df[["id", "following"]].explode("following").rename(columns={"id": "src", "following":"dst"}).append(
  df[["id", "followers"]].explode("followers").rename(columns={"id": "dst", "followers":"src"})))

g = GraphFrame(users, relationships)
