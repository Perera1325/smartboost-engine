from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import numpy as np
import json
from datetime import datetime

router = APIRouter()

class RankRequest(BaseModel):
    posts: List[List[float]]
    users: List[List[float]]
    total_budget: float = 100.0

WEIGHTS = np.array([0.6, 0.4, 0.7, 0.3])

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

METRICS_FILE = "../analytics/metrics.json"

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

    ranked = sorted(post_scores, key=lambda x: x["score"], reverse=True)

    total_score = sum(p["score"] for p in ranked)

    for p in ranked:
        p["allocated_budget"] = round((p["score"] / total_score) * data.total_budget, 2)

    # Save metrics
    record = {
        "timestamp": datetime.now().isoformat(),
        "ranked_posts": ranked
    }

    with open(METRICS_FILE, "r+") as f:
        data_json = json.load(f)
        data_json.append(record)
        f.seek(0)
        json.dump(data_json, f, indent=2)

    return {"ranked_posts": ranked}


@router.get("/metrics")
def get_metrics():
    with open(METRICS_FILE) as f:
        return json.load(f)
