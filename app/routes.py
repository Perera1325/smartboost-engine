from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import numpy as np

router = APIRouter()

class RankRequest(BaseModel):
    posts: List[List[float]]
    users: List[List[float]]

@router.post("/rank")
def rank_posts(data: RankRequest):

    post_matrix = np.array(data.posts)
    user_matrix = np.array(data.users)

    scores = post_matrix @ user_matrix.T

    return {
        "score_matrix": scores.tolist()
    }
