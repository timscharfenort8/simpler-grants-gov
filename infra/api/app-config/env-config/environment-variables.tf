locals {
  # Map from environment variable name to environment variable value
  # This is a map rather than a list so that variables can be easily
  # overridden per environment using terraform's `merge` function
  default_extra_environment_variables = {
    FLASK_APP = "src.app:create_app()"
    # Example environment variables
    # WORKER_THREADS_COUNT    = 4
    # LOG_LEVEL               = "info"
    # DB_CONNECTION_POOL_SIZE = 5
  }

  # Configuration for secrets
  # List of configurations for defining environment variables that pull from SSM parameter
  # store. Configurations are of the format
  # {
  #   ENV_VAR_NAME = {
  #     manage_method     = "generated" # or "manual" for a secret that was created and stored in SSM manually
  #     secret_store_name = "/ssm/param/name"
  #   }
  # }
  secrets = {
    API_AUTH_TOKEN = {
      manage_method     = "manual"
      secret_store_name = "/api/${var.environment}/api-auth-token"
    }
  }
}
