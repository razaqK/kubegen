import yaml
import json


def get_properties_state(properties):
    error = {}
    error_exist = False
    for key, value in properties.items():
        if not value:
            error_exist = True
            error[key] = key + ' is required. kindly supply a valid ' + key
            if key == 'port':
                error[key] = error[key] + '. It is not a good idea to run application on privilege ports'
    return error_exist, error


def set_volume_mounts(argument, config):
    if argument and len(argument) > 0:
        config['spec']['template']['spec']['containers'][0]['volumeMounts'] = argument


def set_volumes(argument, config):
    if argument and len(argument) > 0:
        config['spec']['template']['spec']['volumes'] = argument


def set_image_pull_secret(argument, config):
    if argument and argument.strip():
        config['spec']['template']['spec']['imagePullSecrets'] = [{'name': argument}]


def set_environment_variables(argument, config):
    if argument and len(argument) > 0:
        config['spec']['template']['spec']['containers'][0]['env'] = argument


def set_deployment_environment(argument, config):
    if argument and argument.strip():
        config['metadata']['labels']['environment'] = argument
        config['spec']['template']['metadata']['labels']['environment'] = argument


def set_service_environment(argument, config):
    if argument and argument.strip():
        config['metadata']['labels']['environment'] = argument
        config['spec']['selector']['environment'] = argument


def set_namespace(argument, config):
    if argument and argument.strip():
        config['metadata']['namespace'] = argument


def set_labels(argument, config):
    if bool(argument):
        config['metadata']['labels'] = argument
        if config['kind'] == 'Deployment':
            config['spec']['template']['metadata']['labels'] = argument


def set_annotations(argument, config):
    if argument and len(argument) > 0:
        config['metadata']['annotations'] = argument


def set_readiness_probe(argument, config):
    if bool(argument):
        config['spec']['template']['spec']['containers'][0]['readinessProbe'] = argument


def set_liveness_probe(argument, config):
    if bool(argument):
        config['spec']['template']['spec']['containers'][0]['livenessProbe'] = argument


def set_deployment_args(argument, config):
    if argument and len(argument) > 0:
        config['spec']['template']['spec']['containers'][0]['args'] = argument


def set_resources(argument, config):
    if bool(argument):
        config['spec']['template']['spec']['containers'][0]['resources'] = argument


def set_strategy(argument, config):
    if bool(argument):
        config['spec']['strategy'] = argument


def set_image_pull_policy(argument, config):
    if argument and argument.strip():
        config['spec']['template']['spec']['containers'][0]['imagePullPolicy'] = argument


def set_restart_policy(argument, config):
    if argument and argument.strip():
        config['spec']['template']['spec']['restartPolicy'] = argument


def set_affinity(argument, config):
    if bool(argument):
        config['spec']['template']['spec']['affinity'] = argument


def set_policy_attributes(key, argument, config):
    switcher = {
        'deploy_environment': set_deployment_environment,
        'service_environment': set_service_environment,
        'environment_variables': set_environment_variables,
        'image_pull_secret': set_image_pull_secret,
        'volumes': set_volumes,
        'volume_mounts': set_volume_mounts,
        'annotations': set_annotations,
        'readiness_probe': set_readiness_probe,
        'liveness_probe': set_liveness_probe,
        'deployment_args': set_deployment_args,
        'labels': set_labels,
        'namespace': set_namespace,
        'resources': set_resources,
        'strategy': set_strategy,
        'image_pull_policy': set_image_pull_policy,
    }
    func = switcher.get(key)
    func(argument, config)


class KubePolicyGen:

    def __init__(self, kind, data):
        self.input_json = json.loads(data)
        self.kind = kind

    @staticmethod
    def get_deployment_yaml_parameters(input_json):
        version = input_json.get('version', 'apps/v1')
        name = input_json.get('name')
        replicas = input_json.get('replicas', 1)  # set 1 as default value if replicas is not part of the config
        image = input_json.get('image')
        port = input_json.get('port')
        image_pull_secret = input_json.get('image_pull_secret')
        environment = input_json.get('environment')
        envs = input_json.get('environment_variables')
        volume_mounts = input_json.get('volume_mounts')
        volumes = input_json.get('volumes')
        args = input_json.get('deployment_args')
        readiness_probe = input_json.get('readiness_probe')
        liveness_probe = input_json.get('liveness_probe')
        namespace = input_json.get('namespace')
        labels = input_json.get('labels')
        resources = input_json.get('resources')
        strategy = input_json.get('strategy')
        image_pull_policy = input_json.get('image_pull_policy')
        return version, name, image, image_pull_secret, environment, \
               port, envs, volume_mounts, volumes, replicas, args, \
               readiness_probe, liveness_probe, namespace, labels, resources, strategy, image_pull_policy

    @staticmethod
    def get_multi_container_deployment_yaml_parameters(input_json):
        version = input_json.get('version', 'apps/v1')
        metadata = input_json.get('metadata')
        replicas = input_json.get('replicas', 1)  # set 1 as default value if replicas is not part of the config
        containers = input_json.get('containers')
        environment = input_json.get('environment')
        image_pull_secret = input_json.get('image_pull_secret')
        volumes = input_json.get('volumes')
        namespace = input_json.get('namespace')
        strategy = input_json.get('strategy')

        return version, metadata, replicas, containers, environment, image_pull_secret, \
               volumes, namespace, strategy

    @staticmethod
    def get_ingress_yaml_parameters(input_json):
        version = input_json.get('version', 'extensions/v1beta1')
        name = input_json.get('name')
        port = input_json.get('port')
        host = input_json.get('host')
        tls_secret_name = input_json.get('tls_secret_name')
        path = input_json.get('path', '/')
        annotations = input_json.get('annotations')

        return version, name, annotations, host, tls_secret_name, path, port

    @staticmethod
    def get_service_yaml_parameters(input_json):
        version = input_json.get('version', 'v1')
        name = input_json.get('name')
        port = input_json.get('port')
        environment = input_json.get('environment')
        service_type = input_json.get('service_type')
        protocol = input_json.get('protocol', 'TCP')

        return version, name, environment, service_type, port, protocol

    @staticmethod
    def get_secret_yaml_parameters(input_json):
        version = input_json.get('version', 'v1')
        metadata = input_json.get('metadata')
        secret_type = input_json.get('type')
        data = input_json.get('data')

        return version, metadata, secret_type, data

    @staticmethod
    def build_response(policy_attrs, config):
        for attr in policy_attrs:
            set_policy_attributes(attr.get('key'), attr.get('value'), config)

        response = yaml.dump(config, default_flow_style=False, sort_keys=False)
        return {'status': 'success', 'data': response}

    def populate_deployment_config(self, input_json):
        version, name, image, image_pull_secret, environment, \
        port, envs, volume_mounts, volumes, replicas, args, \
        readiness_probe, liveness_probe, namespace, \
        labels, resources, strategy, image_pull_policy = self.get_deployment_yaml_parameters(input_json)

        error_exist, error = get_properties_state({
            'port': port, 'name': name, 'image': image
        })
        if error_exist:
            return {'status': 'error', 'error': error}

        config_in = {
            'apiVersion': version,
            'kind': 'Deployment',
            'metadata': {
                'name': name,
                'labels': {
                    'app': name,
                },
            },
            'spec': {
                'replicas': replicas,
                'selector': {
                    'matchLabels': {'app': name}
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': name,
                        }
                    },
                    'spec': {
                        'containers': [
                            {
                                'name': name,
                                'image': image,
                                'ports': [
                                    {
                                        'containerPort': port
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }

        policy_attrs = [
            {'key': 'deploy_environment', 'value': environment},
            {'key': 'environment_variables', 'value': envs},
            {'key': 'image_pull_secret', 'value': image_pull_secret},
            {'key': 'volume_mounts', 'value': volume_mounts},
            {'key': 'volumes', 'value': volumes},
            {'key': 'deployment_args', 'value': args},
            {'key': 'readiness_probe', 'value': readiness_probe},
            {'key': 'liveness_probe', 'value': liveness_probe},
            {'key': 'namespace', 'value': namespace},
            {'key': 'labels', 'value': labels},
            {'key': 'resources', 'value': resources},
            {'key': 'strategy', 'value': strategy},
            {'key': 'image_pull_policy', 'value': image_pull_policy},
        ]

        return self.build_response(policy_attrs, config_in)

    def populate_ingress_config(self, input_json):
        version, name, annotations, host, tls_secret_name, path, port = self.get_ingress_yaml_parameters(input_json)

        error_exist, error = get_properties_state({
            'port': port, 'name': name, 'host': host, 'tls_secret_name': tls_secret_name
        })
        if error_exist:
            return {'status': 'error', 'error': error}

        config_in = {
            'apiVersion': version,
            'kind': 'Ingress',
            'metadata': {
                'name': name,
            },
            'spec': {
                'tls': [
                    {
                        'hosts': [host],
                        'secretName': tls_secret_name
                    }
                ],
                'rules': [
                    {
                        'host': host,
                        'http': {
                            'paths': [
                                {
                                    'path': path,
                                    'backend': {
                                        'serviceName': name,
                                        'servicePort': port
                                    }
                                }
                            ]
                        }
                    }
                ],
            }
        }

        policy_attrs = [
            {'key': 'annotations', 'value': annotations},
        ]

        return self.build_response(policy_attrs, config_in)

    def populate_service_config(self, input_json):
        version, name, environment, service_type, port, protocol = self.get_service_yaml_parameters(input_json)
        error_exist, error = get_properties_state({'port': port, 'name': name, 'service_type': service_type})
        if error_exist:
            return {'status': 'error', 'error': error}

        config_in = {
            'apiVersion': version,
            'kind': 'Service',
            'metadata': {
                'name': name,
                'labels': {
                    'app': name,
                },
            },
            'spec': {
                'type': service_type,
                'ports': [
                    {
                        'port': port,
                        'protocol': protocol,
                        'name': 'p' + name
                    }
                ],
                'selector': {
                    'app': name,
                },
            }
        }

        policy_attrs = [
            {'key': 'service_environment', 'value': environment},
        ]

        return self.build_response(policy_attrs, config_in)

    def populate_secret_config(self, input_json):
        version, metadata, secret_type, data = self.get_secret_yaml_parameters(input_json)
        error_exist, error = get_properties_state({'type': secret_type, 'data': data, 'metadata': metadata})
        if error_exist:
            return {'status': 'error', 'error': error}

        config_in = {
            'apiVersion': version,
            'kind': 'Secret',
            'metadata': metadata,
            'type': secret_type,
            'data': data
        }

        policy_attrs = []

        return self.build_response(policy_attrs, config_in)

    def populate_multi_container_deployment_config(self, input_json):
        version, metadata, replicas, containers, environment, image_pull_secret, \
        volumes, namespace, strategy = self.get_multi_container_deployment_yaml_parameters(input_json)

        error_exist, error = get_properties_state({
            'metadata': metadata, 'containers': containers
        })
        if error_exist:
            return {'status': 'error', 'error': error}

        config_in = {
            'apiVersion': version,
            'kind': 'Deployment',
            'metadata': metadata,
            'spec': {
                'replicas': replicas,
                'template': {
                    'spec': {
                        'containers': containers
                    }
                }
            }
        }

        if 'labels' in metadata:
            labels = json.loads(json.dumps(metadata.get('labels')))
            config_in['spec']['template']['metadata'] = {"labels": labels}

        config_in['spec']['selector'] = {'matchLabels': {'app': metadata['name']}}

        policy_attrs = [
            {'key': 'deploy_environment', 'value': environment},
            {'key': 'image_pull_secret', 'value': image_pull_secret},
            {'key': 'volumes', 'value': volumes},
            {'key': 'namespace', 'value': namespace},
            {'key': 'strategy', 'value': strategy},
        ]

        return self.build_response(policy_attrs, config_in)

    def populate_config(self):
        available_config = {
            'deployment': self.populate_deployment_config,
            'ingress': self.populate_ingress_config,
            'svc': self.populate_service_config,
            'secret': self.populate_secret_config,
            'multi_container_deployment': self.populate_multi_container_deployment_config,
        }
        config_func = available_config.get(self.kind)
        return config_func(self.input_json)
