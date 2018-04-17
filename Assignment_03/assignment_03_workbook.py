import json
import pandas as pd
# data = json.loads("reviews.json")
# data = json.loads("Assignment_03/reviews.json")
data = pd.read_json("Assignment_03/reviews.json")
data.shape
data.axes[1].tolist()
data.head(4)
data.select("date")