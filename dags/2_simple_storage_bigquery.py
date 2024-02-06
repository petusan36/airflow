from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator

default_args={
    'owner':'Pedro Turriago Sanchez',
    'start_date': days_ago(7)
}

dag_args ={
    'dag_id':'2_simple_storage_bigquery',
    'schedule_interval':'@daily',
    'catchup':False,
    'default_args': default_args
}

with DAG(**dag_args) as dag:

    cargar_datos = GCSToBigQueryOperator(
        task_id='cargar_datos',
        bucket='testingbucketairflow',
        source_objects=['*'], # -> signifca todos los elementos que encuentres
        source_format='CSV',
        skip_leading_rows=1,
        field_delimiter=',',
        destination_project_dataset_table='datapath-sql.testingairflow.cardio_base',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_APPEND'
    )

    query=(
        '''
        SELECT `age`, `gender`, `height` 
        FROM `datapath-sql.testingairflow.cardio_base`
        ORDER BY `age` ASC
        '''
    )

    tabla_detalle = BigQueryExecuteQueryOperator(
        task_id='tabla_detalle',
        sql=query,
        destination_dataset_table='datapath-sql.testingairflow.tabla_detalle_cardio_base',
        write_disposition='WRITE_TRUNCATE',
        create_disposition='CREATE_IF_NEEDED',
        use_legacy_sql=False,
        location='us-east1',
        gcp_conn_id='google_cloud_default'
    )

    #DEPENDENCIAS
    cargar_datos >> tabla_detalle