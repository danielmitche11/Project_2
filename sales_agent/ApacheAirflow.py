from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStorageObjectUpdatedSensor
from airflow.operators.email_operator import EmailOperator
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
import logging

load_dotenv()

def process_and_upload_to_pinecone(**kwargs):
    # Load text from GCS
    loader = TextLoader("gs://your_gcs_bucket/your_file_in_gcs.txt")
    pages = loader.load_and_split()

    # Split text into chunks
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=10)
    documents = text_splitter.split_documents(pages)

    # Initialize HuggingFace embeddings model
    embeddings_model = HuggingFaceEmbeddings(
        model_name="thenlper/gte-large",
        encode_kwargs={"normalize_embeddings": True},
    )

    # Upload embeddings to Pinecone
    index = "starter"
    namespace = 'documents' # new namespace in pinecone
    Pinecone.from_documents(documents, embeddings_model, index_name=index, namespace=namespace)

    # Log a message indicating successful upload
    logging.info("Document successfully uploaded to Pinecone.")

    # Send an email notification
    send_notification_email(**kwargs)

def send_notification_email(**kwargs):
    # Your email notification logic here
    subject = "Document Upload Notification"
    body = "The document has been successfully uploaded to Pinecone."

    # Example EmailOperator usage
    email_task = EmailOperator(
        task_id='send_email_notification',
        to='your@email.com',
        subject=subject,
        html_content=body,
    )
    email_task.execute(context=kwargs)

default_args = {
    'owner': 'your_owner',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'your_dag_id',
    default_args=default_args,
    description='Your DAG description',
    schedule_interval='@weekly',  # Adjust as per your requirement
)

with dag:
    # Sensor task to wait for the file to be uploaded to GCS
    gcs_sensor = GoogleCloudStorageObjectUpdatedSensor(
        task_id='gcs_sensor',
        bucket='your_gcs_bucket',
        object='your_file_in_gcs.txt',
        google_cloud_storage_conn_id='google_cloud_default',
        timeout=600,  # Adjust as per your requirement
    )

    # PythonOperator to process and upload to Pinecone
    process_and_upload_task = PythonOperator(
        task_id='process_and_upload_to_pinecone',
        python_callable=process_and_upload_to_pinecone,
        provide_context=True,
    )

    # Set up task dependencies
    gcs_sensor >> process_and_upload_task
