from fastapi import Request
from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware
from datadog import statsd

def send_event(title: str, message: str, alert_type: str):
    try:
        statsd.event(title, message, alert_type)
    except:
        pass

class DatadogEventMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            send_event(f"{request.method} {request.url} {response.status_code}", "", "info")
            return response
        except Exception as e:
            send_event(
                f"{request.method} {request.url} {status.HTTP_500_INTERNAL_SERVER_ERROR}",
                str(e),
                "error"
            )
