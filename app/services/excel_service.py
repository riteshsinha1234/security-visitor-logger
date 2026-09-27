from pathlib import Path
from threading import Lock

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIRECTORY = PROJECT_ROOT / "data"

EXCEL_FILE = DATA_DIRECTORY / "visitor_logs.xlsx"

excel_lock = Lock()


HEADERS = [
    "Timestamp (UTC)",
    "IP Address",
    "IP Type",
    "Country",
    "Country Code",
    "State",
    "State Code",
    "City",
    "Postal Code",
    "Latitude",
    "Longitude",
    "Timezone",
    "ISP",
    "Organization",
    "Network",
    "Proxy",
    "Hosting",
    "Mobile Network",
    "Method",
    "Path",
    "User Agent",
    "Referrer",
    "Language",
]


def create_excel_file() -> None:
    DATA_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    if EXCEL_FILE.exists():
        return

    workbook = Workbook()

    worksheet = workbook.active
    worksheet.title = "Visitor Logs"

    worksheet.append(HEADERS)

    for cell in worksheet[1]:
        cell.font = Font(bold=True)

    worksheet.freeze_panes = "A2"

    workbook.save(EXCEL_FILE)
    workbook.close()


def save_visitor_to_excel(
    visitor_ip: str,
    ip_type: str,
    geolocation: dict,
    request,
    timestamp: str,
) -> None:
    with excel_lock:
        create_excel_file()

        workbook = load_workbook(EXCEL_FILE)

        worksheet = workbook["Visitor Logs"]

        security = geolocation.get("security", {})

        if geolocation.get("available"):
            country = geolocation.get("country", "unknown")
            country_code = geolocation.get(
                "country_code",
                "unknown",
            )
            state = geolocation.get("state", "unknown")
            state_code = geolocation.get(
                "state_code",
                "unknown",
            )
            city = geolocation.get("city", "unknown")
            postal_code = geolocation.get(
                "postal_code",
                "unknown",
            )
            latitude = geolocation.get(
                "latitude",
                "unknown",
            )
            longitude = geolocation.get(
                "longitude",
                "unknown",
            )
            timezone = geolocation.get(
                "timezone",
                "unknown",
            )
            isp = geolocation.get("isp", "unknown")
            organization = geolocation.get(
                "organization",
                "unknown",
            )
            network = geolocation.get(
                "network",
                "unknown",
            )

            proxy = security.get("proxy", False)
            hosting = security.get("hosting", False)
            mobile_network = security.get(
                "mobile_network",
                False,
            )

        else:
            country = "unavailable"
            country_code = "unavailable"
            state = "unavailable"
            state_code = "unavailable"
            city = "unavailable"
            postal_code = "unavailable"
            latitude = "unavailable"
            longitude = "unavailable"
            timezone = "unavailable"
            isp = "unavailable"
            organization = "unavailable"
            network = "unavailable"
            proxy = False
            hosting = False
            mobile_network = False

        worksheet.append(
            [
                timestamp,
                visitor_ip,
                ip_type,
                country,
                country_code,
                state,
                state_code,
                city,
                postal_code,
                latitude,
                longitude,
                timezone,
                isp,
                organization,
                network,
                proxy,
                hosting,
                mobile_network,
                request.method,
                request.url.path,
                request.headers.get(
                    "user-agent",
                    "unknown",
                ),
                request.headers.get(
                    "referer",
                    "unknown",
                ),
                request.headers.get(
                    "accept-language",
                    "unknown",
                ),
            ]
        )

        workbook.save(EXCEL_FILE)
        workbook.close()