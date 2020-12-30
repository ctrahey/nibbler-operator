import kopf
import os
import kubernetes
import yaml
from kubernetes.client.rest import ApiException

@kopf.on.create('trahey.us', 'v1', 'nibblers')
def create_fn(spec, name, namespace, logger, **kwargs):
    print(f"A handler is called. name: {name}")
    worker_image = spec.get('image')
    if not worker_image:
        raise kopf.PermanentError(f"workerImage must be set. Got {worker_image!r}.")
    worker_env = spec.get('env')
    # API Clients
    core_api = kubernetes.client.CoreV1Api()
    apps_api = kubernetes.client.AppsV1Api()

    # Ensure DB secret is in place
    our_secret = core_api.read_namespaced_secret('mysql-db-user', 'nibbler-operator')
    new_secret_name = f"nibbler-db-user"
    new_secret = kubernetes.client.V1Secret()
    new_secret.metadata = kubernetes.client.V1ObjectMeta()
    new_secret.metadata.name = new_secret_name
    new_secret.data = our_secret.data
    try:
        core_api.create_namespaced_secret(namespace, new_secret)
    except ApiException as e:
        #secret likely exists already.
        pass

    # Vendor
    path = os.path.join(os.path.dirname(__file__), 'templates/vendor.yaml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(name=f"{name}")
    data = yaml.safe_load(text)
    kopf.adopt(data)
    apps_api.create_namespaced_deployment(
        namespace=namespace,
        body=data,
    )
    # Vendor Service
    path = os.path.join(os.path.dirname(__file__), 'templates/vendor-service.yaml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(name=f"{name}")
    data = yaml.safe_load(text)
    kopf.adopt(data)
    try:
        core_api.create_namespaced_service(
            namespace=namespace,
            body=data,
        )
    except ApiException as e:
        # service likely exists already.
        pass

    # Worker
    path = os.path.join(os.path.dirname(__file__), 'templates/nibbler.yaml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(name=f"{name}", worker_image=worker_image)
    data = yaml.safe_load(text)
    env = data["spec"]["template"]["spec"]["containers"][0]["env"]
    data["spec"]["template"]["spec"]["containers"][0]["env"] = env + worker_env
    kopf.adopt(data)
    apps_api.create_namespaced_deployment(
        namespace=namespace,
        body=data,
    )


    logger.info(f"Deployment child is created")

@kopf.on.update('trahey.us', 'v1', 'nibblers')
def update_fn(spec, status, namespace, logger, **kwargs):
    logger.warn(f"An update handler is being called. body: {spec}")

@kopf.on.delete('trahey.us', 'v1', 'nibblers')
def update_fn(spec, status, namespace, logger, **kwargs):
    logger.warn(f"A DELETE handler is being called. body: {spec}")

