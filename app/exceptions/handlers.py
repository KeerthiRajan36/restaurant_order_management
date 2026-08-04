from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    AlreadyExistsException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    ValidationException,
    BusinessException
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AlreadyExistsException)
    async def already_exists_handler(
        request: Request,
        exc: AlreadyExistsException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": exc.detail
            }
        )

    @app.exception_handler(NotFoundException)
    async def not_found_handler(
        request: Request,
        exc: NotFoundException
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": exc.detail
            }
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(
        request: Request,
        exc: UnauthorizedException
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": exc.detail
            }
        )

    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(
        request: Request,
        exc: ForbiddenException
    ):
        return JSONResponse(
            status_code=403,
            content={
                "success": False,
                "message": exc.detail
            }
        )

    @app.exception_handler(ValidationException)
    async def validation_handler(
        request: Request,
        exc: ValidationException
    ):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": exc.detail
            }
        )

    @app.exception_handler(BusinessException)
    async def business_handler(
        request: Request,
        exc: BusinessException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": exc.detail
            }
        )