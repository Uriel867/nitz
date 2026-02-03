from typing import Annotated
from fastapi import APIRouter, Response, Depends

from di.dependencies import provide_riot_games_service, provide_rate_limiter
from rate_limiter.rate_limiter import LeakyBucketRateLimiter
from riot_games.service import RiotGamesService
from riot_games.models import RiotGamesRegion

router = APIRouter()

RiotGamesServiceDependency = Annotated[RiotGamesService, Depends(provide_riot_games_service)]
RateLimiter = Annotated[LeakyBucketRateLimiter, Depends(provide_rate_limiter)]


async def _apply_rate_limit_headers(
    response: Response,
    service: RiotGamesService,
    rate_limiter: LeakyBucketRateLimiter
) -> bool:
    """Apply rate limit headers and return whether request is allowed."""
    allowed, queued, wait_time, remaining_tokens = await rate_limiter.is_allowed(key=service.api_key)
    headers = {
        "X-RateLimit-Limit": str(rate_limiter.capacity),
        "X-RateLimit-Remaining": str(int(remaining_tokens)),
    }

    if queued:
        headers["X-RateLimit-Queued"] = "1"
        headers["Retry-After"] = str(max(1, int(wait_time)))

    response.headers.update(headers)
    return allowed


@router.get("/account/by-id/{region}/{game_name}/{tag_line}")
async def get_account_by_riot_id(
    response: Response,
    tag_line: str,
    game_name: str,
    service: RiotGamesServiceDependency,
    rate_limiter: RateLimiter,
    region: RiotGamesRegion = RiotGamesRegion.EUROPE
):
    if not await _apply_rate_limit_headers(response, service, rate_limiter):
        return response
    return service.get_account_by_riot_id(tag_line=tag_line, game_name=game_name, region=region)


@router.get("/account/by-puuid/{region}/{puuid}")
async def get_account_by_puuid(
    response: Response,
    puuid: str,
    service: RiotGamesServiceDependency,
    rate_limiter: RateLimiter,
    region: RiotGamesRegion = RiotGamesRegion.EUROPE
):
    if not await _apply_rate_limit_headers(response, service, rate_limiter):
        return response
    return service.get_account_by_puuid(puuid=puuid, region=region)


@router.get("/match/by-match-id/{match_id}")
async def get_match_by_match_id(
    response: Response,
    match_id: str,
    service: RiotGamesServiceDependency,
    rate_limiter: RateLimiter,
    region: RiotGamesRegion = RiotGamesRegion.EUROPE
):
    if not await _apply_rate_limit_headers(response, service, rate_limiter):
        return response
    return service.get_match_by_match_id(match_id=match_id, region=region)


@router.get("/match/by-puuid/{puuid}")
async def get_matches_by_puuid(
    response: Response,
    puuid: str,
    service: RiotGamesServiceDependency,
    rate_limiter: RateLimiter,
    region: RiotGamesRegion = RiotGamesRegion.EUROPE
):
    if not await _apply_rate_limit_headers(response, service, rate_limiter):
        return response
    return service.get_matches_by_puuid(puuid=puuid, region=region)


@router.get("/match/timeline/by-match-id/{match_id}")
async def get_match_timeline_by_match_id(
    response: Response,
    match_id: str,
    service: RiotGamesServiceDependency,
    rate_limiter: RateLimiter,
    region: RiotGamesRegion = RiotGamesRegion.EUROPE
):
    if not await _apply_rate_limit_headers(response, service, rate_limiter):
        return response
    return service.get_match_timeline_by_match_id(match_id=match_id, region=region)
