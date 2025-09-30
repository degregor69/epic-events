from app.views.main import main_view
import sentry_sdk

sentry_sdk.init(
dsn="https://e0abf3f84d858b16cf29c69aba20c953@o4510107730182144.ingest.de.sentry.io/4510107733131344",
# Add data like request headers and IP for users,
# see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
send_default_pii=True,
)

if __name__ == "__main__":
    division_by_zero = 1 / 0
    main_view()
