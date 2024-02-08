# DMS replication instance and endpoint connections

# docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/subnets
data "aws_subnets" "all" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }
}

# docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dms_replication_subnet_group
resource "aws_dms_replication_subnet_group" "subnet" {
  replication_subnet_group_description = "${var.environment_name} replication subnet group"
  replication_subnet_group_id          = "${var.environment_name}-replication-subnet-group"
  subnet_ids                           = data.aws_subnets.all.ids
}

# docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dms_replication_instance
resource "aws_dms_replication_instance" "instance" {
  # checkov:skip=CKV_AWS_212:Not sure how this triggered, EBS volumes are a seperate resource.
  allocated_storage          = 50
  apply_immediately          = true
  auto_minor_version_upgrade = true
  # needs to refer to the actual zone not whole region like it was before: https://github.com/hashicorp/terraform-provider-aws/issues/29198#issuecomment-1422457911
  availability_zone            = "us-east-1a"
  engine_version               = "3.5.2"
  multi_az                     = false
  preferred_maintenance_window = "sun:10:30-sun:14:30"
  publicly_accessible          = false
  replication_instance_class   = "dms.t3.small"
  replication_instance_id      = "${var.environment_name}-db-replication-instance"
  replication_subnet_group_id  = aws_dms_replication_subnet_group.subnet.id

  vpc_security_group_ids = [
    data.aws_security_group.dms.id
  ]
}

# docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dms_endpoint
resource "aws_dms_endpoint" "target_endpoint" {
  endpoint_id                     = "${var.environment_name}-simpler-grants-target"
  certificate_arn                 = "arn:aws:dms:us-east-1:315341936575:cert:GWOIQRTIVQVRBL5ERMCKTUPHMM33MMDGIP57J4I"
  database_name                   = "app"
  endpoint_type                   = "target"
  engine_name                     = "aurora-postgresql"
  kms_key_arn                     = aws_kms_key.dms_endpoints.arn
  secrets_manager_access_role_arn = aws_iam_role.dms_access.arn
  ssl_mode                        = "verify-ca"
  secrets_manager_arn             = data.aws_secretsmanager_secret.target_db.id
}

# docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dms_endpoint
resource "aws_dms_endpoint" "source_endpoint" {
  # checkov:skip=CKV2_AWS_49: This endpoint doesn't need SSL
  endpoint_id                     = "${var.environment_name}-grants-gov-source"
  database_name                   = "tstgrnts"
  endpoint_type                   = "source"
  engine_name                     = "oracle"
  kms_key_arn                     = aws_kms_key.dms_endpoints.arn
  ssl_mode                        = "none"
  secrets_manager_access_role_arn = aws_iam_role.dms_access.arn
  secrets_manager_arn             = data.aws_secretsmanager_secret.source_db.id
  extra_connection_attributes     = "exposeViews=true"
}

resource "aws_kms_key" "dms_endpoints" {
  description         = "KMS key for endpoints associated with DMS"
  enable_key_rotation = true
}

# These credentails were provided to us by MicroHealth.
# docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/secretsmanager_secret
data "aws_secretsmanager_secret" "source_db" {
  name = "${var.environment_name}/grants_gov_source_db"
}

# Unfortunatly, the secret auto-generated by AWS RDS does not include the host and the port.
# So here we have created a new secret with the host and the port.
# docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/secretsmanager_secret
data "aws_secretsmanager_secret" "target_db" {
  name = "${var.environment_name}/simpler_grants_target_db"
}
