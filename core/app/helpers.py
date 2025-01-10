from kubernetes import client, config


def create_worker_for_user(username):
    config.load_incluster_config()
    apps_v1 = client.AppsV1Api()

    worker_name = f'celery-worker-{username}'

    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=worker_name),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(
                match_labels={"app": worker_name}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(
                    labels={"app": worker_name}
                ),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name=worker_name,
                            image="piyushbugmetrics/dynamic-worker-dj:latest",
                            command=["celery", "-A", "core", "worker",
                                     "-l", "info", "-Q",
                                     f"user_queue_{username}"])]))))

    apps_v1.create_namespaced_deployment(
        namespace="default",
        body=deployment)


def create_worker_job(username):
    config.load_incluster_config()
    batch_v1 = client.BatchV1Api()

    worker_name = f'celery-worker-{username}'

    job = client.V1Job(
        metadata=client.V1ObjectMeta(name=worker_name),
        spec=client.V1JobSpec(
            ttl_seconds_after_finished=10,
            backoff_limit=3,
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(
                    labels={"app": worker_name}
                ),
                spec=client.V1PodSpec(
                    restart_policy="Never",
                    containers=[
                        client.V1Container(
                            name=worker_name,
                            image="piyushbugmetrics/dynamic-worker-dj:latest",
                            command=["celery", "-A", "core", "worker",
                                     "-l", "info", "-Q",
                                     f"user_queue_{username}"])]))))

    batch_v1.create_namespaced_job(
        namespace="default",
        body=job
    )
