from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "authur",
    "start_date": datetime(2025, 1, 1),
}

with DAG(
    dag_id="mandera_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:

    customers_generator = BashOperator(
        task_id="generate_customers",
        bash_command="python3 '/Users/mac1/Mandera Analytics operates/mandera_pipeline/generator/data_generator.py'"
    )

    products_generator = BashOperator(
        task_id="generate_products",
        bash_command="python3 '/Users/mac1/Mandera Analytics operates/mandera_pipeline/generator/faker_products.py'"
    )

    orders_generator = BashOperator(
        task_id="generate_orders",
        bash_command="python3 '/Users/mac1/Mandera Analytics operates/mandera_pipeline/generator/faker_orders.py'"
    )

    transform_customers = BashOperator(
        task_id="transform_customers",
        bash_command="python3 '/Users/mac1/Mandera Analytics operates/mandera_pipeline/transformation/transform_customers.py'"
    )

    transform_products = BashOperator(
        task_id="transform_products",
        bash_command="python3 '/Users/mac1/Mandera Analytics operates/mandera_pipeline/transformation/transform_products.py'"
    )

    transform_orders = BashOperator(
        task_id="transform_orders",
        bash_command="python3 '/Users/mac1/Mandera Analytics operates/mandera_pipeline/transformation/transform_orders.py'"
    )

    load_customers = BashOperator(
        task_id="load_customers",
        bash_command="python3 '/Users/mac1/Mandera Analytics operates/mandera_pipeline/loading/load_customers.py'"
    )

    load_products = BashOperator(
        task_id="load_products",
        bash_command="python3 '/Users/mac1/Mandera Analytics operates/mandera_pipeline/loading/load_products.py'"
    )

    load_orders = BashOperator(
        task_id="load_orders",
        bash_command="python3 '/Users/mac1/Mandera Analytics operates/mandera_pipeline/loading/load_orders.py'"
    )

    validate_quality = BashOperator(
        task_id="validate_quality",
        bash_command="python3 '/Users/mac1/Mandera Analytics operates/mandera_pipeline/validation/validate_data_quality.py'"
    )

    customers_generator >> transform_customers >> load_customers

    products_generator >> transform_products >> load_products

    orders_generator >> transform_orders >> load_orders

    [
        load_customers,
        load_products,
        load_orders
    ] >> validate_quality