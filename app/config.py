import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()


class Settings:
    """
    Application configuration settings loaded from environment variables.
    """
    # RabbitMQ Settings
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")

    # General Application Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "DbSLoIREJtu6z3CVnpTd_DdFeMMRoteCU0UjJcNreZI")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Product Service")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "1.0.0")

    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:Sylvian@db:5433/product_service_db")
    TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "postgresql+psycopg2://postgres:Sylvian@db:5433/test_product_service_db")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "Sylvian")
    DATABASE_DB: str = os.getenv("DATABASE_DB", "product_service_db")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "5433"))

    # Test Mode
    TESTING: bool = os.getenv("TESTING", "0") == "1"

    @property
    def effective_database_url(self) -> str:
        """
        Returns the appropriate database URL depending on the environment.
        If TESTING is True, use the test database URL.
        """
        return self.TEST_DATABASE_URL if self.TESTING else self.DATABASE_URL


settings = Settings()
