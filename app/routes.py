from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import List
import numpy as np
import json
from datetime import datetime

from security import verify_key, log_request, check_rate

router = APIRouter()

class RankRequest(BaseModel):
    posts: List[List[float]]
    users: List[List[float]]
    total_budget: float = 100.0

# Acts like trained ML weights (logistic regression style)
WEIGHTS = np.array([0.6, 0.4, 0.7, 0.3])

METRICS_FILE = "../analytics/metrics.json"

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


@router.post("/rank")
async def rank_posts(
    data: RankRequest,
    request: Request,
    auth=Depends(verify_key)
):
    # Security
    await log_request(request)
    check_rate(request.client.host)

    post_scores = []

    for idx, post in enumerate(data.posts):

        combined_score = 0.0

        for user in data.users:

            # Validation: exactly 2 features each
            if len(post) != 2 or len(user) != 2:
                return {"error": "Each post and user must have exactly 2 features"}

            features = np.array(post + user)  # 4 features total
            score = sigmoid(np.dot(features, WEIGHTS))
            combined_score += score

        post_scores.append({
            "post_id": idx,
            "score": float(combined_score)
        })

    # Rank posts
    ranked = sorted(post_scores, key=lambda x: x["score"], reverse=True)

    total_score = sum(p["score"] for p in ranked)

    # Allocate boost budget
    for p in ranked:
        p["allocated_budget"] = round((p["score"] / total_score) * data.total_budget, 2)

    # Save analytics
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
async def get_metrics(
    request: Request,
    auth=Depends(verify_key)
):
    # Security
    await log_request(request)
    check_rate(request.client.host)

    with open(METRICS_FILE) as f:
        return json.load(f)
