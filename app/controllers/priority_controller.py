from fastapi import APIRouter, Query, HTTPException
from app.services.priority_service import PriorityService

router = APIRouter()


@router.get("/priority/issues")
def get_priority_issues(
    limit: int = Query(5, ge=1, le=20),
    min_days: int = Query(1, ge=0),
    min_amount: float = Query(0, ge=0)
):
    results = PriorityService.get_priority_issues(
        limit=limit,
        min_days=min_days,
        min_amount=min_amount
    )

    if not results:
        return {
            "message": "No priority issues found for the given filters",
            "top_issues": []
        }

    return {
        "top_issues": [r.to_dict() for r in results]
    }
