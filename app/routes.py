from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import numpy as np

router = APIRouter()

class RankRequest(BaseModel):
    posts: List[List[float]]
    users: List[List[float]]

# Simple weight vector (acts like trained model)
WEIGHTS = np.array([0.6, 0.4, 0.7, 0.3])

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

@router.post("/rank")
def rank_posts(data: RankRequest):

    scores = []

    for post in data.posts:
        for user in data.users:

            if len(post) != 2 or len(user) != 2:
                return {"error": "Each post and user must have exactly 2 features"}

            features = np.array(post + user)

            score = sigmoid(np.dot(features, WEIGHTS))
            scores.append(float(score))

    return {"engagement_scores": scores}
