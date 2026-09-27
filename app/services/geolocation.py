import ipaddress

import httpx


def get_ip_type(ip: str) -> str:
    try:
        parsed_ip = ipaddress.ip_address(ip)

        if parsed_ip.is_loopback:
            return "loopback"

        if parsed_ip.is_private:
            return "private"

        return "public"

    except ValueError:
        return "unknown"


async def get_ip_geolocation(ip: str) -> dict:
    if get_ip_type(ip) != "public":
        return {
            "available": False,
            "reason": "Geolocation is only available for public IP addresses",
        }

    fields = (
        "status,message,country,countryCode,region,regionName,"
        "city,zip,lat,lon,timezone,isp,org,as,query,"
        "proxy,hosting,mobile"
    )

    url = f"http://ip-api.com/json/{ip}"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                url,
                params={
                    "fields": fields,
                },
            )

            response.raise_for_status()
            data = response.json()

        if data.get("status") != "success":
            return {
                "available": False,
                "reason": data.get(
                    "message",
                    "Geolocation lookup failed",
                ),
            }

        return {
            "available": True,
            "ip": data.get("query"),
            "country": data.get("country"),
            "country_code": data.get("countryCode"),
            "state_code": data.get("region"),
            "state": data.get("regionName"),
            "city": data.get("city"),
            "postal_code": data.get("zip"),
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
            "timezone": data.get("timezone"),
            "isp": data.get("isp"),
            "organization": data.get("org"),
            "network": data.get("as"),
            "security": {
                "proxy": data.get("proxy", False),
                "hosting": data.get("hosting", False),
                "mobile_network": data.get("mobile", False),
            },
        }

    except httpx.HTTPStatusError as error:
        return {
            "available": False,
            "reason": (
                f"Geolocation HTTP error: "
                f"{error.response.status_code}"
            ),
        }

    except httpx.RequestError as error:
        return {
            "available": False,
            "reason": f"Geolocation connection error: {str(error)}",
        }

    except ValueError:
        return {
            "available": False,
            "reason": "Invalid response received from geolocation service",
        }