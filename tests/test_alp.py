import click
import json
import os
from click.testing import CliRunner

from alp.cli import main


def init_test_config():
    config_path = '/root/.alp/containers_test.json'
    if os.getenv('TEST_MODE') == 'ON':  # pragma: no cover
        config_path = 'containers_test.json'
    if not os.path.exists(config_path):  # pragma: no cover
        config = dict()
        config['broker'] = {
            "volumes": ["/opt/data/rabbitmq/dev/log:/dev/log",
                        "/opt/data/rabbitmq:/var/lib/rabbitmq"],
            "ports": ["8081:15672", "5673:5672"],
            "name": "rabbitmq_sched_test",
            "container_name": "rabbitmq:3-management",
            "mode": "-d"
        }
        config['result_db'] = {
            "volumes": ["/opt/data/mongo_data/results:/data/db"],
            "name": "mongo_results_test",
            "container_name": "mongo",
            "mode": "-d"
        }
        config['model_gen_db'] = {
            "volumes": ["/opt/data/mongo_data/models:/data/db"],
            "name": "mongo_models_test",
            "container_name": "mongo",
            "mode": "-d"
        }
        config['workers'] = []
        config['controlers'] = []

        with open(config_path, 'w') as f:
            f.write(json.dumps(config, indent=4))
    return config_path


config_path = init_test_config()


def test_status():
    runner = CliRunner()
    result = runner.invoke(main, ['--verbose', 'status', config_path])
    assert result.exit_code == 0


def test_service():
    runner = CliRunner()
    for cm in ['start', 'restart', 'stop', 'rm']:
        result = runner.invoke(main, ['--verbose', 'service', cm, config_path])
        assert result.exit_code == 0


def test_update():
    runner = CliRunner()
    result = runner.invoke(main, ['--verbose', 'update', config_path])
    assert result.exit_code == 0


def test_pull():
    runner = CliRunner()
    result = runner.invoke(main, ['--verbose', 'pull', config_path])
    assert result.exit_code == 0
