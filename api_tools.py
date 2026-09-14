from os_control import (
    open_application,
    search_browser,
    type_text
)

from email_automation import email_automation


TOOLS = {
    "open_application": open_application,
    "search_browser": search_browser,
    "type_text": type_text,
    "send_email": email_automation,
}