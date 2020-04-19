from .kubepolicygen import KubePolicyGen
from .util import log, validate_yaml
import json
import click


@click.command()
@click.option('--kind', '-k',
              help='what kind of k8s policy file are you trying to create. support type includes deployment, ingress and svc.')
@click.option('--data', '-d',
              help='Supply payload for the policy file in jsonstring format e.g {"name": "app-1", "version": "v1"} ')
def main(kind, data):
    log('K8s yaml policy file generator', 'blue')
    kube_policy_gen = KubePolicyGen(kind, data)
    response = kube_policy_gen.populate_config()
    if response['status'] == 'error':
        return log('Error occurred: ->' + json.dumps(response['error']), 'red')
    is_valid, policy = validate_yaml(response['data'])
    if not is_valid:
        return log('Error occurred: ->' + policy, 'red')

    filename = kube_policy_gen.kind + '.yaml'
    build_policy = open(filename, 'w')
    build_policy.write(policy)
    build_policy.close()
    click.echo('successfully generate policy file')
    return log('Success: ->' + json.dumps(response['data']), 'green')


if __name__ == '__main__':
    main(prog_name="kubegen")
