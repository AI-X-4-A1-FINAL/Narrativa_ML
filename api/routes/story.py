# api/routes/story.py

from fastapi import APIRouter, HTTPException
from schemas.story_class import (
    StoryGenerationStartRequest,
    StoryGenerationChatRequest,
    StoryEndRequest,
    StoryResponse
)
from service.story_service import StoryService
from models.story_generator import StoryGenerator
from models.s3_manager import S3Manager

router = APIRouter()

# S3Manager 초기화
s3_manager = S3Manager()

# StoryGenerator에 S3Manager 주입
story_generator = StoryGenerator(s3_manager=s3_manager)
story_service = StoryService(story_generator=story_generator)


@router.post("/start", response_model=StoryResponse)
async def generate_story_endpoint(request: StoryGenerationStartRequest):
    """
    스토리를 생성하는 엔드포인트
    """
    try:
        response = await story_service.generate_initial_story(genre=request.genre)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating story: {str(e)}")


@router.post("/continue", response_model=StoryResponse)
async def continue_story_endpoint(request: StoryGenerationChatRequest):
    """
    스토리를 이어가는 엔드포인트
    """
    try:
        print(f"[Continue Endpoint] Received request: {request}")
        response = await story_service.continue_story(request)
        print(f"[Continue Endpoint] Generated response: {response}")
        return response
    except ValueError as e:
        print(f"[Continue Endpoint] Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        print(f"[Continue Endpoint] Server error: {str(e)}")
        print(f"Error type: {type(e)}")
        raise HTTPException(status_code=500, detail=f"Error continuing story: {str(e)}")

@router.post("/end", response_model=StoryResponse)
async def generate_ending_endpoint(request: StoryEndRequest):
    """
    스토리의 마지막 엔딩을 생성하는 엔드포인트
    """
    try:
        print(f"[End Endpoint] Received request: {request}")
        response = await story_service.generate_ending_story(request.story_id)
        print(f"[End Endpoint] Generated ending: {response}")
        return response
    except ValueError as e:
        print(f"[End Endpoint] Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        print(f"[End Endpoint] Server error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating ending: {str(e)}")

