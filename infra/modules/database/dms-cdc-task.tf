# docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dms_replication_task
resource "aws_dms_replication_task" "task-cdc" {
  replication_instance_arn = aws_dms_replication_instance.instance.replication_instance_arn
  source_endpoint_arn      = aws_dms_endpoint.source_endpoint.endpoint_arn
  target_endpoint_arn      = aws_dms_endpoint.target_endpoint.endpoint_arn
  migration_type           = "full-load-and-cdc"
  replication_task_id      = "${var.environment_name}-task-cdc"
  replication_task_settings = jsonencode(
    {
      "Logging" : {
        "EnableLogging" : true,
        "EnableLogContext" : true,
      },
      "ValidationSettings" : {
        "EnableValidation" : true,
      },
    }
  )
  table_mappings = jsonencode(
    {
      "rules" : [
        {
          "rule-type" : "selection",
          "rule-id" : "1",
          "rule-name" : "Include TOPPORTUNITY table",
          "object-locator" : {
            "schema-name" : "EGRANTSADMIN",
            "table-name" : "TOPPORTUNITY"
          },
          "rule-action" : "explicit"
        },
        {
          "rule-type" : "transformation",
          "rule-id" : "2",
          "rule-name" : "Rename schema",
          "rule-action" : "rename",
          "rule-target" : "schema",
          "object-locator" : {
            "schema-name" : "EGRANTSADMIN"
          },
          "value" : "api"
        },
        {
          "rule-type" : "transformation",
          "rule-id" : "3",
          "rule-name" : "Rename table TOPPORTUNITY to transfer_topportunity_temp",
          "rule-action" : "rename",
          "rule-target" : "table",
          "object-locator" : {
            "schema-name" : "EGRANTSADMIN",
            "table-name" : "TOPPORTUNITY"
          },
          "value" : "transfer_topportunity_temp"
        },
        {
          "rule-type" : "transformation",
          "rule-id" : "4",
          "rule-name" : "Lowercase column names",
          "rule-action" : "convert-lowercase",
          "rule-target" : "column",
          "object-locator" : {
            "schema-name" : "%",
            "table-name" : "%",
            "column-name" : "%",
          }
        },
        {
          "rule-type" : "transformation",
          "rule-id" : "5",
          "rule-name" : "Exclude column TOPPORTUNITY.LISTED",
          "rule-action" : "remove-column",
          "rule-target" : "column",
          "object-locator" : {
            "schema-name" : "EGRANTSADMIN",
            "table-name" : "TOPPORTUNITY",
            "column-name" : "LISTED"
          }
        },
        {
          "rule-type" : "transformation",
          "rule-id" : "6",
          "rule-name" : "Exclude column TOPPORTUNITY.INITIAL_OPPORTUNITY_ID",
          "rule-action" : "remove-column",
          "rule-target" : "column",
          "object-locator" : {
            "schema-name" : "EGRANTSADMIN",
            "table-name" : "TOPPORTUNITY",
            "column-name" : "INITIAL_OPPORTUNITY_ID"
          }
        },
        {
          "rule-type" : "transformation",
          "rule-id" : "7",
          "rule-name" : "Exclude column TOPPORTUNITY.FLAG_2006",
          "rule-action" : "remove-column",
          "rule-target" : "column",
          "object-locator" : {
            "schema-name" : "EGRANTSADMIN",
            "table-name" : "TOPPORTUNITY",
            "column-name" : "FLAG_2006"
          }
        },
        {
          "rule-type" : "transformation",
          "rule-id" : "8",
          "rule-name" : "add time",
          "rule-target" : "column",
          "object-locator" : {
            "schema-name" : "EGRANTSADMIN",
            "table-name" : "TOPPORTUNITY"
          },
          "rule-action" : "add-column",
          "value" : "created_at",
          "expression" : "datetime ()",
          "data-type" : {
            "type" : "datetime",
            "precision" : 6
          }
        },
        {
          "rule-type" : "transformation",
          "rule-id" : "9",
          "rule-name" : "add time",
          "rule-target" : "column",
          "object-locator" : {
            "schema-name" : "EGRANTSADMIN",
            "table-name" : "TOPPORTUNITY"
          },
          "rule-action" : "add-column",
          "value" : "updated_at",
          "expression" : "datetime ()",
          "data-type" : {
            "type" : "datetime",
            "precision" : 6
          }
        }
      ]
    }
  )
}
