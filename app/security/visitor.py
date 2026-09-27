import time

from fastapi import Request

from app.services.geolocation import get_ip_type


REQUEST_COOLDOWN_SECONDS = 10

recent_visitors: dict[str, float] = {}


def get_visitor_ip(request: Request) -> str:
    # Proxy headers should only be trusted when the deployed
    # application is behind a reverse proxy that you control.
    cf_ip = request.headers.get("cf-connecting-ip")

    if cf_ip:
        return cf_ip.strip()

    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    if request.client:
        return request.client.host

    return "unknown"


def should_log_visitor(ip: str) -> bool:
    current_time = time.monotonic()

    last_request_time = recent_visitors.get(ip)

    if last_request_time is not None:
        elapsed = current_time - last_request_time

        if elapsed < REQUEST_COOLDOWN_SECONDS:
            return False

    recent_visitors[ip] = current_time

    return True


def print_security_report(
    visitor_ip: str,
    ip_type: str,
    geolocation: dict,
    request: Request,
    timestamp: str,
) -> None:
    print()
    print("SECURITY VISITOR DETECTED")
    print("=" * 50)

    print(f"Time (UTC)      : {timestamp}")
    print(f"IP Address      : {visitor_ip}")
    print(f"IP Type         : {ip_type}")

    if geolocation.get("available"):
        print(
            f"Country         : "
            f"{geolocation.get('country', 'unknown')}"
        )

        print(
            f"Country Code    : "
            f"{geolocation.get('country_code', 'unknown')}"
        )

        print(
            f"State           : "
            f"{geolocation.get('state', 'unknown')}"
        )

        print(
            f"State Code      : "
            f"{geolocation.get('state_code', 'unknown')}"
        )

        print(
            f"City            : "
            f"{geolocation.get('city', 'unknown')}"
        )

        print(
            f"Postal Code     : "
            f"{geolocation.get('postal_code', 'unknown')}"
        )

        print(
            f"Latitude        : "
            f"{geolocation.get('latitude', 'unknown')}"
        )

        print(
            f"Longitude       : "
            f"{geolocation.get('longitude', 'unknown')}"
        )

        print(
            f"Timezone        : "
            f"{geolocation.get('timezone', 'unknown')}"
        )

        print(
            f"ISP             : "
            f"{geolocation.get('isp', 'unknown')}"
        )

        print(
            f"Organization    : "
            f"{geolocation.get('organization', 'unknown')}"
        )

        print(
            f"Network         : "
            f"{geolocation.get('network', 'unknown')}"
        )

        security = geolocation.get("security", {})

        print(
            f"Proxy           : "
            f"{security.get('proxy', False)}"
        )

        print(
            f"Hosting         : "
            f"{security.get('hosting', False)}"
        )

        print(
            f"Mobile Network  : "
            f"{security.get('mobile_network', False)}"
        )

        print(
            "Location Note   : "
            "IP-based location is approximate, not a street address"
        )

    else:
        print("Location        : unavailable")

        print(
            f"Reason          : "
            f"{geolocation.get('reason', 'unknown')}"
        )

    print(f"Method          : {request.method}")
    print(f"Path            : {request.url.path}")

    print(
        f"User Agent      : "
        f"{request.headers.get('user-agent', 'unknown')}"
    )

    print(
        f"Referrer        : "
        f"{request.headers.get('referer', 'unknown')}"
    )

    print(
        f"Language        : "
        f"{request.headers.get('accept-language', 'unknown')}"
    )

    print("=" * 50)
    print()


def get_visitor_ip_type(ip: str) -> str:
    return get_ip_type(ip)