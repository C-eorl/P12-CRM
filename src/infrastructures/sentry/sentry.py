import os

import sentry_sdk


def init_sentry():
    SENTRY_DSN = os.getenv("SENTRY_DSN")
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        send_default_pii=True,
    )

