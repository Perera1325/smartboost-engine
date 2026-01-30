from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import numpy as np

router = APIRouter()

class RankRequest(BaseModel):
    posts: List[List[float]]
    users: List[List[float]]
    total_budget: float = 100.0

# Simple weight vector (acts like ML model)
WEIGHTS = np.array([0.6, 0.4, 0.7, 0.3])

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

@router.post("/rank")
def rank_posts(data: RankRequest):

    post_scores = []

    for idx, post in enumerate(data.posts):

        combined_score = 0

        for user in data.users:

            if len(post) != 2 or len(user) != 2:
                return {"error": "Each post and user must have exactly 2 features"}

            features = np.array(post + user)
            score = sigmoid(np.dot(features, WEIGHTS))
            combined_score += score

        post_scores.append({
            "post_id": idx,
            "score": float(combined_score)
        })

    # Sort posts by score
    ranked = sorted(post_scores, key=lambda x: x["score"], reverse=True)

    total_score = sum(p["score"] for p in ranked)

    # Allocate boost budget proportionally
    for p in ranked:
        p["allocated_budget"] = round((p["score"] / total_score) * data.total_budget, 2)

    return {
        "ranked_posts": ranked
    }
