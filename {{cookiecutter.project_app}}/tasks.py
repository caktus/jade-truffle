import shutil
from pathlib import Path

import invoke
import kubesae
import yaml
from colorama import init


PROJECT_BASE = Path(__file__).resolve().parent

init(autoreset=True)


@invoke.task
def staging(c):
    c.config.env = "staging"
    c.config.namespace = "{{ cookiecutter.project_app }}-staging"


@invoke.task
def production(c):
    c.config.env = "production"
    c.config.namespace = "{{ cookiecutter.project_app }}-production"


@invoke.task
def build_deployable(c):
    """Builds a deployable image using the Dockerfile deploy target"""
    kubesae.image["tag"](c)
    c.run(f"docker build -t {c.config.app}:{c.config.tag} --target deploy .")


@invoke.task(pre=[build_deployable])
def build_deploy(c, push=True, deploy=True):
    """Pushes the built images"""
    if push:
        kubesae.image["push"](c)
    if deploy:
        kubesae.deploy["deploy"](c)


@invoke.task
def ansible_playbook(c, name, extra="", verbosity=1):
    with c.cd("deploy/"):
        c.run(f"ansible-playbook {name} {extra} -{'v'*verbosity}")


@invoke.task
def pod_stats(c):
    """Report total pods vs pod capacity."""
    nodes = yaml.safe_load(c.run("kubectl get nodes -o yaml", hide="out").stdout)
    pod_capacity = sum(
        [int(item["status"]["capacity"]["pods"]) for item in nodes["items"]]
    )
    pod_total = c.run(
        "kubectl get pods --all-namespaces | grep Running | wc -l", hide="out"
    ).stdout.strip()
    print(f"Running pods: {pod_total}")
    print(f"Maximum pods: {pod_capacity}")
    print(f"Total nodes: {len(nodes['items'])}")


project = invoke.Collection("project")
project.add_task(build_deploy)
project.add_task(pod_stats)
project.add_task(ansible_playbook, name="playbook")

ns = invoke.Collection()
ns.add_collection(kubesae.image)
ns.add_collection(kubesae.aws)
ns.add_collection(kubesae.deploy)
ns.add_collection(kubesae.pod)
ns.add_collection(kubesae.utils)
ns.add_collection(project)
ns.add_task(staging)
ns.add_task(production)

ns.configure(
    {
        "app": "{{ cookiecutter.project_app }}_app",
        "aws": {"region": "<<FILL_IN>>", "profile_name": "{{ cookiecutter.project_app }}"},
        "cluster": "{{ cookiecutter.project_app }}-stack-cluster",
        "container_name": "app",
        "repository": "<<Container Repository Here>>",
        "run": {
            "echo": True,
            "pty": True,
            "env": {
                "COMPOSE_FILE": "docker-compose.yml:docker-compose-deploy.yml",
            },
        },
    }
)
