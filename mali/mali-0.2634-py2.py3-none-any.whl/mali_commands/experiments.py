# -*- coding: utf8 -*-
import click
import requests
import json
from mali_commands.commons import output_result
from mali_commands.options import project_id_option, experiment_id_option, metrics_option, model_weights_hash_option
from mali_commands.options import chart_x_option, chart_x_name_option, chart_y_name_option, chart_y_option, chart_name_option, chart_type_option, \
    chart_scope_option
from mali_commands.utilities.formatters import format_datetime, truncate_long_text, truncate_short_text
import six


def chart_name_to_id(chart_name):
    from hashlib import sha256
    return sha256(six.text_type(chart_name).encode('utf-8').lower().strip()).hexdigest()


@click.group('experiments')
def experiments_commands():
    pass


@experiments_commands.command('list')
@project_id_option(required=True)
@click.pass_context
def list_experiments(ctx, projectid):
    """List experiments of a project.
    """
    list_experiments_path = 'projects/{project_id}/experiments'.format(project_id=projectid)
    result = ctx.obj.handle_api(ctx.obj, requests.get, list_experiments_path)
    experiments = result.get('experiments', [])

    displayed_fields = ['experiment_id', 'created_at', 'display_name', 'description']
    formatters = {
        'created_at': format_datetime,
        'display_name': truncate_short_text,
        'description': truncate_long_text,
    }
    output_result(ctx, experiments, displayed_fields, formatters=formatters)


@experiments_commands.command('updateMetrics')
@project_id_option(required=False)
@experiment_id_option(required=False)
@model_weights_hash_option(required=False)
@metrics_option(required=True)
@click.pass_context
def update_metrics(ctx, projectid, experimentid, weightshash, metrics):
    """Send experiment metrics to an experiment.

    There are 2 ways to identify the experiment: (1) specify both `--projectId` and `--experimentId`
    options or (2) specify `--weightsHash` option. When the model's weights hash is specified, mali
    would look up the experiment that the model belongs to.

    When both `--projectId` and `--experimentId` are specified, the `--weightsHash` option is ignored.

    Example:

    To send metrics to the 5th experiment of the project "123", run

    \b
        mali experiments update_metrics --projectId 123 --experimentId 5 --metrics '{"ex_cost": 99}'

    Or assuming that the model's weights hash "324e16b5e" was generated by this experiment at certain
    epoch or iteration, run

    \b
        mali experiments update_metrics --weightsHash 324e16b5e --metrics '{"ex_cost": 99}'
    """

    update_metrics_path = get_submit_path('projects/{project_id}/experiments/{experiment_id}/metrics', 'model_weights_hashes/{model_weights_hash}/metrics?experiment_only=1', projectid, experimentid, weightshash)
    data = _get_metrics_json(metrics)
    result = ctx.obj.handle_api(ctx.obj, requests.post, update_metrics_path, data)
    output_result(ctx, result, ['ok'])


def get_submit_path(by_project_and_experiment_path, by_model_hash_path, project_id, experiment_id, model_weights_hash, **kwargs):
    def raise_data_missing_error():
        if project_id is not None:
            raise click.BadOptionUsage('Please also specify --experimentId option.')
        elif experiment_id is not None:
            raise click.BadOptionUsage('Please also specify --projectId option.')
        else:
            raise click.BadOptionUsage('Please specify the experiment using (1) --projectId and --experimentId options'
                                       'or (2) --weightsHash options.')

    if project_id is not None and experiment_id is not None:
        return by_project_and_experiment_path.format(project_id=project_id, experiment_id=experiment_id, **kwargs)
    elif model_weights_hash is not None:
        return by_model_hash_path.format(model_weights_hash=model_weights_hash, **kwargs)
    raise_data_missing_error()


def _read_norm_y_values(ys):
    res = []
    dimmention_count = None

    for y in ys:
        if not isinstance(y, list):
            y = [y]
        cur_dim = len(y)
        dimmention_count = dimmention_count or cur_dim
        if dimmention_count != cur_dim:
            raise click.BadOptionUsage("All of the data values arrays must be of the same size")
        res += y
    return res


def _read_norm_x_values(xs):
    res = []
    for type, suffix in [(float, '_float'), (six.integer_types, '_int'), (six.string_types, '_str')]:
        for x in xs:
            if not isinstance(x, type):
                res = []
                break
            res.append(x)
        if len(res) == len(xs):
            return res, suffix
    raise click.BadOptionUsage('X values must be consistent')


def _get_metrics_json(metrics_string):
    try:
        return json.loads(metrics_string)
    except ValueError:
        raise click.BadParameter('The supplied sting is not a valid JSON dictionary format.')


@experiments_commands.command('updateChart')
@model_weights_hash_option(required=False)
@project_id_option(required=False)
@experiment_id_option(required=False)
@chart_name_option(required=True)
@chart_x_name_option(required=False)
@chart_y_name_option(required=False)
@chart_scope_option(required=False)
@chart_type_option(required=False)
@chart_x_option(required=False)
@chart_y_option(required=False)
@click.pass_context
def update_chart(ctx, weightshash, projectid, experimentid, chartname, chartscope, charttype, chartxname, chartyname,
                 chartx, charty):
    """Send experiment external chart to an experiment.

    There are 2 ways to identify the experiment: (1) specify both `--projectId` and `--experimentId`
    options or (2) specify `--weightsHash` option. When the model's weights hash is specified, mali
    would look up the experiment that the model belongs to.

    When both `--projectId` and `--experimentId` are specified, the `--weightsHash` option is ignored.

    To send chart to the 5th experiment "precision recall" chart of the project "123" in the validation scope, run

    \b
        mali experiments updateChart --projectId 123 --experimentId 321  --chartName "precision recall" --chartScope validation  --chartX '[0.1,0.5,0.8]' --chartY '[0.9,0.5,0.2]' --chartXNname "Precision" --chartYName "Recall"

    Or send a chart with multiple y charts:
        mali experiments updateChart --p 123 --e 321  -c "precision recall" -cs validation  -cx '[0.1,0.5,0.8]' -cy '[[0.9, 0.5],[0.5,0.25],[0.2,0.4]' --chartYName '["Func1","Func2"]'

    """
    chart_id = chart_name_to_id(chartname)

    update_chart_path = get_submit_path(
        'projects/{project_id}/experiments/{experiment_id}/chart/{chart_id}',
        'model_weights_hashes/{model_weights_hash}/chart/{chart_id}',
        projectid, experimentid, weightshash, chart_id=chart_id)

    x, x_suffix = _read_norm_x_values(_get_metrics_json(chartx))

    y = _read_norm_y_values(_get_metrics_json(charty))
    y_name = chartyname
    if y_name.startswith('['):
        y_name = _get_metrics_json(y_name)
    if not isinstance(y_name, list):
        y_name = [y_name]
    chartlegends = [chartxname] + y_name
    if len(y) % len(x) is not 0:
        raise click.BadOptionUsage('X and Y arrays must be of the same size')
    data = {'name': chartname, 'labels': chartlegends,
            'x' + x_suffix: x, 'y_data': y, 'chart': charttype,
            'scope': chartscope}
    result = ctx.obj.handle_api(ctx.obj, requests.put, update_chart_path, data)
    output_result(ctx, result, ['ok'])


@experiments_commands.command('updateModelMetrics')
@model_weights_hash_option(required=True)
@metrics_option(required=True)
@click.pass_context
def update_model_metrics(ctx, weightshash, metrics):
    """Send the model's metrics to its corresponding experiment epochs.

    Each model weights hash is attached to certain experiment epochs and thus can be used to send
    metrics that are relevant to those epochs. The model weights hash is a hexadecimal string. To
    calculate the weights hash of a model:

        - Calculate the sha1 strings of the weights for each layers

        - Calculate the sha1 string of the combine hashes. For example, the model has 3 layers with
    the layers' weight hashes: ['abc', '123', 'def'], the model weight hash is `sha1('abc123def')`

    Alternatively, you can use `missinglink-sdk` Python package to calculate the weights hash for
    your model. Each framework callback has its corresponding `get_weights_hash` method.

    WARNING: The same model weights hash can appear in different experiments or different epochs
    (for example, when running the same net twice). As such, this command will send the metrics to
    all these experiments/epochs that it can identify from the hash.

    Example:

    To send metrics of the model which hash is 324e16b5e, run

    \b
        mali experiments update_model_metrics --weightsHash 324e16b5e --metrics '{"ex_cost": 99}'

    """
    update_model_metrics_path = 'model_weights_hashes/{model_weights_hash}/metrics' \
        .format(model_weights_hash=weightshash)
    data = _get_metrics_json(metrics)

    result = ctx.obj.handle_api(ctx.obj, requests.post, update_model_metrics_path, data)
    output_result(ctx, result, ['ok'])
