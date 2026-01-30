WEB_APPS = {

    "fastapi": [
        "http_requests_total",
        "http_request_duration_seconds_bucket",
        "http_request_duration_seconds_sum",
        "http_request_duration_seconds_count",
        "http_requests_in_progress",
        "process_cpu_seconds_total",
        "process_resident_memory_bytes",
        "python_gc_objects_collected_total",
        "python_gc_objects_uncollectable_total"
    ],

    "django": [
        "django_http_requests_total",
        "django_http_responses_total",
        "process_cpu_seconds_total",
        "process_resident_memory_bytes"
    ],

    "springboot": [
        "http_server_requests_seconds_count",
        "http_server_requests_seconds_sum",
        "jvm_memory_used_bytes",
        "jvm_gc_pause_seconds_sum",
        "jvm_threads_live",
        "process_cpu_usage"
    ],

    "node": [
        "http_requests_total",
        "http_request_duration_seconds",
        "nodejs_eventloop_lag_seconds",
        "nodejs_heap_size_used_bytes",
        "process_resident_memory_bytes"
    ],

    "go": [
        "http_requests_total",
        "http_request_duration_seconds",
        "go_goroutines",
        "go_memstats_heap_alloc_bytes",
        "go_gc_duration_seconds"
    ]
}
FRONTEND_APPS = {
    "browser": [
        "frontend_page_load_seconds",
        "frontend_first_contentful_paint_seconds",
        "frontend_largest_contentful_paint_seconds",
        "frontend_js_error_total",
        "frontend_api_latency_seconds"
    ],

    "mobile": [
        "app_launch_time_seconds",
        "api_response_latency_seconds",
        "app_crash_total",
        "network_failure_total"
    ]
}
WORKERS = {

    "celery": [
        "celery_tasks_total",
        "celery_task_runtime_seconds",
        "celery_tasks_failed_total",
        "celery_queue_length"
    ],

    "sidekiq": [
        "sidekiq_jobs_processed_total",
        "sidekiq_jobs_failed_total",
        "sidekiq_queue_latency_seconds"
    ],

    "cron": [
        "cron_job_success_total",
        "cron_job_failure_total",
        "cron_job_duration_seconds"
    ]
}
MESSAGING = {

    "kafka": [
        "kafka_server_brokertopicmetrics_messagesin_total",
        "kafka_consumer_lag",
        "kafka_network_requestmetrics_requests_total",
        "kafka_controller_active_controller_count"
    ],

    "rabbitmq": [
        "rabbitmq_queue_messages_ready",
        "rabbitmq_queue_messages_unacked",
        "rabbitmq_connections",
        "rabbitmq_channel_messages_published_total"
    ],

    "sqs": [
        "ApproximateNumberOfMessagesVisible",
        "ApproximateAgeOfOldestMessage"
    ]
}
DATABASES = {

    "postgres": [
        "pg_stat_activity_count",
        "pg_stat_database_xact_commit",
        "pg_stat_database_xact_rollback",
        "pg_stat_database_blks_read",
        "pg_stat_database_blks_hit",
        "pg_replication_lag"
    ],

    "mysql": [
        "mysql_global_status_threads_connected",
        "mysql_global_status_slow_queries",
        "mysql_global_status_questions"
    ],

    "mongodb": [
        "mongodb_connections",
        "mongodb_op_counters_total",
        "mongodb_memory_resident_bytes"
    ],

    "elastic": [
        "elasticsearch_cluster_health_status",
        "elasticsearch_indices_docs_count",
        "elasticsearch_jvm_memory_used_bytes"
    ]
}
CACHE = {

    "redis": [
        "redis_connected_clients",
        "redis_used_memory_bytes",
        "redis_commands_processed_total",
        "redis_keyspace_hits_total",
        "redis_keyspace_misses_total"
    ],

    "memcached": [
        "memcached_current_connections",
        "memcached_items_evicted_total",
        "memcached_bytes"
    ]
}
KUBERNETES = [
    "container_cpu_usage_seconds_total",
    "container_memory_usage_bytes",
    "container_fs_usage_bytes",
    "kube_pod_status_phase",
    "kube_pod_container_status_restarts_total",
    "kube_node_status_condition",
    "kube_deployment_status_replicas"
]
CLOUD = {

    "aws": [
        "EC2_CPUUtilization",
        "EC2_NetworkIn",
        "ALB_RequestCount",
        "RDS_CPUUtilization",
        "Lambda_Duration",
        "Lambda_Errors"
    ],

    "gcp": [
        "compute.googleapis.com/instance/cpu/utilization",
        "cloudfunctions.googleapis.com/function/execution_count",
        "cloudsql.googleapis.com/database/cpu/utilization"
    ],

    "azure": [
        "Percentage CPU",
        "Network In Total",
        "Function Execution Count"
    ]
}
AI_SYSTEMS = {

    "llm_api": [
        "llm_requests_total",
        "llm_tokens_input_total",
        "llm_tokens_output_total",
        "llm_latency_seconds",
        "llm_errors_total"
    ],

    "model_inference": [
        "inference_requests_total",
        "inference_latency_seconds",
        "gpu_utilization",
        "gpu_memory_used_bytes"
    ],

    "training": [
        "training_step_duration_seconds",
        "training_loss",
        "gpu_temperature_celsius"
    ]
}
BLACKBOX = [
    "probe_success",
    "probe_duration_seconds",
    "probe_http_status_code",
    "dns_lookup_duration_seconds",
    "tcp_connect_duration_seconds"
]
SECURITY = [
    "http_4xx_total",
    "http_5xx_total",
    "auth_failures_total",
    "rate_limit_exceeded_total",
    "ddos_suspected_requests"
]
BASE_METRICS = [
    "up",
    "process_cpu_seconds_total",
    "process_resident_memory_bytes",
    "process_open_fds",
    "process_start_time_seconds"
]
GOLDEN_SIGNALS = {
    "latency": [
        "http_request_duration_seconds_bucket",
        "http_request_duration_seconds_sum"
    ],
    "traffic": [
        "http_requests_total"
    ],
    "errors": [
        "http_5xx_total",
        "http_4xx_total"
    ],
    "saturation": [
        "process_cpu_seconds_total",
        "process_resident_memory_bytes"
    ]
}
API_GATEWAYS = {

    "nginx": [
        "nginx_http_requests_total",
        "nginx_http_request_duration_seconds",
        "nginx_connections_active",
        "nginx_connections_waiting",
        "nginx_ingress_controller_requests"
    ],

    "envoy": [
        "envoy_http_downstream_rq_total",
        "envoy_http_downstream_rq_xx",
        "envoy_cluster_upstream_rq_time",
        "envoy_server_memory_allocated"
    ],

    "istio": [
        "istio_requests_total",
        "istio_request_duration_milliseconds",
        "istio_tcp_sent_bytes_total",
        "istio_tcp_received_bytes_total"
    ]
}
SERVERLESS = {

    "aws_lambda": [
        "Lambda_Invocations",
        "Lambda_Duration",
        "Lambda_Errors",
        "Lambda_Throttles",
        "Lambda_ConcurrentExecutions"
    ],

    "gcp_cloud_functions": [
        "cloudfunctions.googleapis.com/function/execution_count",
        "cloudfunctions.googleapis.com/function/execution_times",
        "cloudfunctions.googleapis.com/function/user_memory_bytes"
    ],

    "azure_functions": [
        "Function Execution Count",
        "Function Execution Units",
        "Function Errors"
    ]
}
STORAGE = {

    "object_storage": [
        "s3_bucket_size_bytes",
        "s3_requests_total",
        "gcs_storage_object_count",
        "azure_blob_capacity"
    ],

    "block_storage": [
        "disk_read_bytes_total",
        "disk_write_bytes_total",
        "disk_io_time_seconds_total"
    ]
}
NETWORK = [
    "node_network_receive_bytes_total",
    "node_network_transmit_bytes_total",
    "node_network_receive_errs_total",
    "node_network_transmit_errs_total",
    "tcp_retransmits_total"
]
CI_CD = {

    "github_actions": [
        "ci_pipeline_runs_total",
        "ci_pipeline_duration_seconds",
        "ci_pipeline_failures_total"
    ],

    "jenkins": [
        "jenkins_job_duration_seconds",
        "jenkins_job_failures_total",
        "jenkins_queue_size"
    ]
}
DATA_PIPELINES = {

    "spark": [
        "spark_executor_cpu_time_seconds",
        "spark_executor_memory_used_bytes",
        "spark_job_duration_seconds"
    ],

    "flink": [
        "flink_taskmanager_job_task_busy_time_ms",
        "flink_jobmanager_numRunningJobs",
        "flink_taskmanager_Status_JVM_CPU_Load"
    ],

    "airflow": [
        "airflow_dag_run_duration_seconds",
        "airflow_task_failures_total",
        "airflow_scheduler_heartbeat"
    ]
}
AI_SYSTEMS.update({

    "vector_db": [
        "vector_queries_total",
        "vector_query_latency_seconds",
        "vector_index_size",
        "vector_insert_failures_total"
    ],

    "feature_store": [
        "feature_fetch_latency_seconds",
        "feature_fetch_errors_total",
        "feature_store_size_bytes"
    ]
})
SLO_METRICS = [
    "availability_percentage",
    "error_budget_remaining",
    "latency_p95_seconds",
    "latency_p99_seconds"
]
COST_METRICS = [
    "cloud_cost_daily_usd",
    "data_transfer_cost_usd",
    "storage_cost_usd",
    "compute_cost_usd"
]
