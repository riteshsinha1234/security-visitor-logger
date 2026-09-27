import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from app.security.visitor import (
    get_visitor_ip,
    get_visitor_ip_type,
    print_security_report,
    should_log_visitor,
)
from app.services.excel_service import save_visitor_to_excel
from app.services.geolocation import get_ip_geolocation


load_dotenv()


REDIRECT_URL = os.getenv(
    "REDIRECT_URL",
    "https://www.youtube.com",
)


app = FastAPI(
    title="Security Visitor Logger",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "success": True,
        "message": "Security Visitor Logger is running",
    }


@app.get("/security-check")
async def security_check(request: Request):
    visitor_ip = get_visitor_ip(request)
    ip_type = get_visitor_ip_type(visitor_ip)

    geolocation = await get_ip_geolocation(visitor_ip)

    timestamp = datetime.now(timezone.utc).isoformat()

    if should_log_visitor(visitor_ip):
        print_security_report(
            visitor_ip=visitor_ip,
            ip_type=ip_type,
            geolocation=geolocation,
            request=request,
            timestamp=timestamp,
        )

        save_visitor_to_excel(
            visitor_ip=visitor_ip,
            ip_type=ip_type,
            geolocation=geolocation,
            request=request,
            timestamp=timestamp,
        )

        print("Visitor saved to Excel successfully.")

    else:
        print(
            f"Duplicate request ignored in terminal: {visitor_ip}"
        )

    return {
        "success": True,
        "message": "Security check completed",
    }


@app.get("/go")
async def go(request: Request):
    visitor_ip = get_visitor_ip(request)
    ip_type = get_visitor_ip_type(visitor_ip)

    geolocation = await get_ip_geolocation(visitor_ip)

    timestamp = datetime.now(timezone.utc).isoformat()

    if should_log_visitor(visitor_ip):
        print_security_report(
            visitor_ip=visitor_ip,
            ip_type=ip_type,
            geolocation=geolocation,
            request=request,
            timestamp=timestamp,
        )

        save_visitor_to_excel(
            visitor_ip=visitor_ip,
            ip_type=ip_type,
            geolocation=geolocation,
            request=request,
            timestamp=timestamp,
        )

        print("Visitor saved to Excel successfully.")

    else:
        print(
            f"Duplicate request ignored in terminal: {visitor_ip}"
        )

    return RedirectResponse(
        url=REDIRECT_URL,
        status_code=302,
    )