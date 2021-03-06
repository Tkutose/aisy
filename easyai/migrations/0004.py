# Generated by Django 3.2.3 on 2022-02-12 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('easyai', '0001_initial'),
    ]

    sql = """
CREATE VIEW done_categorical AS
SELECT models.id as model_id, categorical_transformation.column_name, categorical_transformation.before_value as before_str, categorical_transformation.after_value as after_str
FROM models
LEFT OUTER JOIN machine_learning
ON models.machine_learning_id = machine_learning.id
LEFT OUTER JOIN feature_values
ON machine_learning.feature_value_id = feature_values.id
LEFT OUTER JOIN categorical_transformation
ON feature_values.id = categorical_transformation.feature_value_id;
"""

    reverse_sql = """
    DROP VIEW done_categorical;
    """

    operations = [
        migrations.RunSQL(sql, reverse_sql),
    ]
