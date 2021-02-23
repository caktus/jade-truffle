# Setup AWS for K8s
This document is meant for a first time setup after jade-truffle has been used to 
create a new project.  It is meant entirely for use on a brand new AWS sub-account
that has been configured to use the CaktusAccessRole-Admins assume role.

## Requirements
* AWS CLI
* Boto
* Ansible
* Kubernetes
* Invoke

## Setup
Demonstration assumptions for this document are these:

1. Project Name is: ``apple_pie``
2. AWS_REGION is: ``us-east-1``
3. Caktus Main Account profile is ``caktus``
4. ``CaktusAccessRole-Admins`` is used to assume into the project account

### Add the AssumeRole ARN to your ``~/.aws/config`` and ``~/.aws/credentials``

```sh
    $> vi ~/.aws/config
    ...
    [profile apple_pie]
    region = us-east-1

    $> vi ~/.aws/credentials
    ...
    [apple_pie]
    role_arn = arn:aws:iam::<APPLE_PIE_ASSUME_ROLE_ID>:role/CaktusAccountAccessRole-Admins
    source_profile = caktus
```

If the ``role_arn`` is not known, it should be: either pinned in the project slack channel, or in lastpass under the project name. If it is not found in either place, check with Tech Support or the person who created the sub-account.

### Install the roles for the project

First verify that the role versions are up to date in this file: [/deploy/requirements.yml](https://github.com/caktus/jade-truffle/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/deploy/requirements.yml):

* [ansible-role-django-k8s](https://github.com/caktus/ansible-role-django-k8s/tags)
* [ansible-role-aws-web-stacks](https://github.com/caktus/ansible-role-aws-web-stacks/tags)
* [ansible-role-k8s-web-cluster](https://github.com/caktus/ansible-role-k8s-web-cluster/tags)

If not, bump version numbers as necessary in the ``requirements.yml`` file then run:

```sh
    (~/deploy) $> ansible-galaxy install -r requirements.yml
```

### Create an ansible vault secret.

With the assume role URL which will look something like this: ``https://signin.aws.amazon.com/switchrole?roleName=CaktusAccountAccessRole-Admins&account=<APPLE_PIE_ASSUME_ROLE_ID>&displayName=ApplePieProject`` log into AWS.

NOTE: Make sure the aws account is showing the correct ``us-east-1`` region, before following the next steps.

1. Switch to ``Secrets Manager``
1. Select ``Store a new secret``
1. Choose ``Other type of secret``
1. Select ``Plaintext``
1. Remove any populated characters and insert a random string. ``$> pwgen 32`` is a good way to get these.
1. Select ``Next``.
1. In ``Secret Name`` use the value found in [/deploy/echo-vault-pass.sh](https://github.com/caktus/jade-truffle/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/deploy/echo-vault-pass.sh) for ``SECRET_ID``. Any value will work but they must match.
1. Select ``Next``
1. Make sure ``Disable automatic rotation`` is selected
1. Select ``Next``
1. Select ``Store``

Run ``./echo-vault-pass.sh``, and secret should be sent to stdout without errors.

### Use AWS Web Stacks to configure the installation.

Next AWS web stacks, an ansible role that is included in ``jade-truffle`` will be used to configure stack of resources the project needs to run the system.

The key files for this process are:
* [deploy/group_vars/all.yml](https://github.com/caktus/jade-truffle/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/deploy/group_vars/all.yml)

* [deploy/play-deploy-cf-stack.yml](https://github.com/caktus/jade-truffle/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/deploy/play-deploy-cf-stack.yml)

In the ``group_vars/all.yml`` 



