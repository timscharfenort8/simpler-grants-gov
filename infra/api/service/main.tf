# docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc
data "aws_vpc" "network" {
  filter {
    name   = "tag:Name"
    values = [module.project_config.network_configs[var.environment_name].vpc_name]
  }
}

# docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/subnet
data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.network.id]
  }
  filter {
    name   = "tag:subnet_type"
    values = ["private"]
  }
}

# docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/subnet
data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.network.id]
  }
  filter {
    name   = "tag:subnet_type"
    values = ["public"]
  }
}

locals {
  # The prefix key/value pair is used for Terraform Workspaces, which is useful for projects with multiple infrastructure developers.
  # By default, Terraform creates a workspace named “default.” If a non-default workspace is not created this prefix will equal “default”,
  # if you choose not to use workspaces set this value to "dev"
  prefix = terraform.workspace == "default" ? "" : "${terraform.workspace}-"

  # Add environment specific tags
  tags = merge(module.project_config.default_tags, {
    environment = var.environment_name
    description = "Application resources created in ${var.environment_name} environment"
  })

  service_name = "${local.prefix}${module.app_config.app_name}-${var.environment_name}"

  is_temporary = startswith(terraform.workspace, "t-")

  environment_config                             = module.app_config.environment_configs[var.environment_name]
  service_config                                 = local.environment_config.service_config
  database_config                                = local.environment_config.database_config
  incident_management_service_integration_config = local.environment_config.incident_management_service_integration
  domain                                         = local.environment_config.domain
}

terraform {
  required_version = "< 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.68.0"
    }
  }

  backend "s3" {
    encrypt = "true"
  }
}

provider "aws" {
  region = local.service_config.region
  default_tags {
    tags = local.tags
  }
}

module "project_config" {
  source = "../../project-config"
}

module "app_config" {
  source = "../app-config"
}

data "aws_rds_cluster" "db_cluster" {
  count              = module.app_config.has_database ? 1 : 0
  cluster_identifier = local.database_config.cluster_name
}

data "aws_acm_certificate" "cert" {
  count  = local.domain != null ? 1 : 0
  domain = local.domain
}

data "aws_iam_policy" "app_db_access_policy" {
  count = module.app_config.has_database ? 1 : 0
  name  = local.database_config.app_access_policy_name
}

data "aws_iam_policy" "migrator_db_access_policy" {
  count = module.app_config.has_database ? 1 : 0
  name  = local.database_config.migrator_access_policy_name
}

# Retrieve url for external incident management tool (e.g. Pagerduty, Splunk-On-Call)

data "aws_ssm_parameter" "incident_management_service_integration_url" {
  count = module.app_config.has_incident_management_service ? 1 : 0
  name  = local.incident_management_service_integration_config.integration_url_param_name
}

module "service" {
  source                 = "../../modules/service"
  service_name           = local.service_name
  is_temporary           = local.is_temporary
  image_repository_name  = module.app_config.image_repository_name
  image_tag              = local.image_tag
  vpc_id                 = data.aws_vpc.network.id
  public_subnet_ids      = data.aws_subnets.public.ids
  private_subnet_ids     = data.aws_subnets.private.ids
  desired_instance_count = local.service_config.instance_desired_instance_count
  max_capacity           = local.service_config.instance_scaling_max_capacity
  min_capacity           = local.service_config.instance_scaling_min_capacity
  enable_autoscaling     = true
  cpu                    = local.service_config.instance_cpu
  memory                 = local.service_config.instance_memory
  environment_name       = var.environment_name

  cert_arn = local.domain != null ? data.aws_acm_certificate.cert[0].arn : null

  app_access_policy_arn      = data.aws_iam_policy.app_db_access_policy[0].arn
  migrator_access_policy_arn = data.aws_iam_policy.migrator_db_access_policy[0].arn

  scheduled_jobs = local.environment_config.scheduled_jobs
  s3_buckets     = local.environment_config.s3_buckets

  db_vars = module.app_config.has_database ? {
    security_group_ids = data.aws_rds_cluster.db_cluster[0].vpc_security_group_ids
    connection_info = {
      host        = data.aws_rds_cluster.db_cluster[0].endpoint
      port        = data.aws_rds_cluster.db_cluster[0].port
      user        = local.database_config.app_username
      db_name     = data.aws_rds_cluster.db_cluster[0].database_name
      schema_name = local.database_config.schema_name
    }
  } : null

  enable_drafts_bucket = true

  extra_environment_variables = merge(local.service_config.extra_environment_variables)

  secrets = concat(
    [for secret_name in keys(local.service_config.secrets) : {
      name      = secret_name
      valueFrom = module.secrets[secret_name].secret_arn
    }],
    local.environment_config.search_config != null ? [{
      name      = "SEARCH_USERNAME"
      valueFrom = data.aws_ssm_parameter.search_username_arn[0].arn
    }] : [],
    local.environment_config.search_config != null ? [{
      name      = "SEARCH_PASSWORD"
      valueFrom = data.aws_ssm_parameter.search_password_arn[0].arn
    }] : [],
    local.environment_config.search_config != null ? [{
      name      = "SEARCH_ENDPOINT"
      valueFrom = data.aws_ssm_parameter.search_endpoint_arn[0].arn
    }] : []
  )
}

module "monitoring" {
  source = "../../modules/monitoring"
  #Email subscription list:
  email_alerts_subscription_list = ["grantsalerts@navapbc.com"]

  # Module takes service and ALB names to link all alerts with corresponding targets
  service_name                                = local.service_name
  load_balancer_arn_suffix                    = module.service.load_balancer_arn_suffix
  incident_management_service_integration_url = module.app_config.has_incident_management_service ? data.aws_ssm_parameter.incident_management_service_integration_url[0].value : null
}
