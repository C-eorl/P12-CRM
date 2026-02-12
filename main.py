import dotenv
dotenv.load_dotenv()

from src.infrastructures.sentry.sentry import init_sentry

from src.presentation.cli.cli_main import app


def main():

    init_sentry()
    app()

if __name__ == '__main__':
    main()

