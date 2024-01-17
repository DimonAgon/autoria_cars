
import requests

from static_text import *
from re_patterns import autoria_authentic_search_url_re_pattern

import logging


def validate_autoria_search_url_is_authentic(search_url: str) -> bool:

    search_url_authenticity = autoria_authentic_search_url_re_pattern.match(search_url)

    if search_url_authenticity:
        logging.info(autoria_search_url_authenticity_validation_success_logging_info_message.format(search_url))

    else:
        logging.error(autoria_search_url_authenticity_validation_failure_logging_error_message.format(search_url))

    return search_url_authenticity


def validate_autoria_search_url_points_on_real_source(search_url: str) -> bool:

    response = requests.get(search_url)
    response_success_status = response.ok

    if response_success_status:
        logging.info(autoria_search_url_points_on_real_source_validation_success_logging_info_message.format(search_url))

    else:
        logging.error(autoria_search_url_points_on_real_source_validation_failure_logging_error_message.format(search_url))

    return response_success_status