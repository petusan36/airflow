from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator

from airflow.providers.google.cloud.transfers.s3_to_gcs import S3ToGCSOperator ## <---

default_args={
    'owner':'Pedro Turriago Sanchez',
    'start_date': days_ago(7)
}

dag_args ={
    'dag_id':'2.2_aws_storage_bigquery',
    'schedule_interval':'@daily',
    'catchup':False,
    'default_args': default_args
}

with DAG(**dag_args) as dag:

    transferir_aws=S3ToGCSOperator(
        task_id='transferir_aws',
        bucket='airflows3datapath',
        dest_gcs='gs://from-bucket-aws',
        prefix='cardio_',
        replace=False,
        aws_conn_id='aws_default',
        gcp_conn_id='google_cloud_default'
    )

    cargar_datos = GCSToBigQueryOperator(
        task_id='cargar_datos',
        bucket='from-bucket-aws',  # <---
        source_objects=['*'], # -> signifca todos los elementos que encuentres
        source_format='CSV',
        skip_leading_rows=1,
        field_delimiter=',',
        destination_project_dataset_table='datapath-sql.testingairflow.cardio_base_aws',  # <--
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_APPEND'
    )

    query=(
        '''
        SELECT `age`, `gender`, `height` 
        FROM `datapath-sql.testingairflow.cardio_base_aws`
        ORDER BY `age` ASC
        '''
    )

    tabla_detalle = BigQueryExecuteQueryOperator(
        task_id='tabla_detalle',
        sql=query,
        destination_dataset_table='datapath-sql.testingairflow.tabla_detalle_cardio_base_aws',  # <--
        write_disposition='WRITE_TRUNCATE',
        create_disposition='CREATE_IF_NEEDED',
        use_legacy_sql=False,
        location='us-east1',
        gcp_conn_id='google_cloud_default'
    )

    #DEPENDENCIAS
    transferir_aws >> cargar_datos >> tabla_detalle