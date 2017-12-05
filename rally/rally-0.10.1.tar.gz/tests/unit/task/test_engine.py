# Copyright 2013: Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Tests for the Test engine."""

import collections
import threading

import mock

from rally.common import objects
from rally import consts
from rally import exceptions
from rally.task import context
from rally.task import engine
from rally.task import scenario
from tests.unit import fakes
from tests.unit import test


class MyException(exceptions.RallyException):
    msg_fmt = "MyException"


class TaskEngineTestCase(test.TestCase):

    @staticmethod
    def _make_workload(name, args=None, description=None, contexts=None,
                       sla=None, runner=None, hooks=None, position=0):
        return {"uuid": "foo",
                "name": name,
                "position": position,
                "description": description,
                "args": args,
                "contexts": contexts or {},
                "runner_type": runner[0] if runner else "serial",
                "runner": runner[1] if runner else {},
                "sla": sla or {},
                "hooks": hooks or []}

    def test_init(self):
        config = mock.MagicMock()
        task = mock.MagicMock()
        eng = engine.TaskEngine(config, task, mock.Mock())
        self.assertEqual(eng.config, config)
        self.assertEqual(eng.task, task)

    @mock.patch("jsonschema.validate")
    def test_validate(self, mock_validate):
        config = mock.MagicMock()
        eng = engine.TaskEngine(config, mock.MagicMock(),
                                mock.Mock())
        mock_validate = mock.MagicMock()

        eng._validate_config_syntax = mock_validate.syntax
        eng._validate_config_platforms = mock_validate.platforms
        eng._validate_config_semantic = mock_validate.semantic

        eng.validate()

        mock_validate.syntax.assert_called_once_with(config)
        mock_validate.platforms.assert_called_once_with(config)
        mock_validate.semantic.assert_called_once_with(config)

    @mock.patch("rally.task.engine.TaskConfig")
    def test_validate__wrong_syntax(self, mock_task_config):
        task = mock.MagicMock()
        eng = engine.TaskEngine(mock.MagicMock(), task, mock.Mock())
        eng._validate_config_syntax = mock.MagicMock(
            side_effect=exceptions.InvalidTaskConfig)
        eng._validate_config_platforms = mock.Mock()

        self.assertRaises(exceptions.InvalidTaskException, eng.validate)

        self.assertTrue(task.set_failed.called)
        # the next validation step should not be processed
        self.assertFalse(eng._validate_config_platforms.called)

    @mock.patch("rally.task.engine.TaskConfig")
    def test_validate__wrong_semantic(self, mock_task_config):
        task = mock.MagicMock()
        eng = engine.TaskEngine(mock.MagicMock(), task, mock.Mock())
        eng._validate_config_syntax = mock.MagicMock()
        eng._validate_config_platforms = mock.MagicMock()
        eng._validate_config_semantic = mock.MagicMock(
            side_effect=exceptions.InvalidTaskConfig)

        self.assertRaises(exceptions.InvalidTaskException, eng.validate)
        self.assertTrue(task.set_failed.called)
        # all steps of validation are called, which means that the last one is
        # failed
        self.assertTrue(eng._validate_config_syntax)
        self.assertTrue(eng._validate_config_platforms)
        self.assertTrue(eng._validate_config_semantic)

    @mock.patch("rally.task.engine.scenario.Scenario.get")
    @mock.patch("rally.task.sla.SLA.validate")
    @mock.patch("rally.task.hook.HookTrigger.validate")
    @mock.patch("rally.task.hook.HookAction.validate")
    @mock.patch("rally.task.engine.TaskConfig")
    @mock.patch("rally.task.engine.runner.ScenarioRunner.validate")
    @mock.patch("rally.task.engine.context.Context.validate")
    def test__validate_workload(
            self, mock_context_validate,
            mock_scenario_runner_validate,
            mock_task_config,
            mock_hook_action_validate,
            mock_hook_trigger_validate,
            mock_sla_validate,
            mock_scenario_get):

        mock_context_validate.return_value = []
        mock_sla_validate.return_value = []
        mock_hook_action_validate.return_value = []
        mock_hook_trigger_validate.return_value = []
        default_context = {"foo": "foo_conf"}
        scenario_cls = mock_scenario_get.return_value
        scenario_cls.get_platform.return_value = "default"
        scenario_cls.get_default_context.return_value = default_context

        scenario_name = "Foo.bar"
        runner_type = "MegaRunner"
        hook_conf = {"action": ("c", "c_args"),
                     "trigger": ("d", "d_args")}
        workload = {"name": scenario_name,
                    "runner_type": runner_type,
                    "runner": {},
                    "contexts": {"a": "a_conf"},
                    "hooks": [hook_conf],
                    "sla": {"foo_sla": "sla_conf"},
                    "position": 2}

        eng = engine.TaskEngine(mock.MagicMock(), mock.MagicMock(),
                                mock.Mock())

        eng._validate_workload(workload)

        mock_scenario_runner_validate.assert_called_once_with(
            name=runner_type, context=None, config=None,
            plugin_cfg={}, vtype=None)
        self.assertEqual([mock.call(name="a",
                                    context=None,
                                    config=None,
                                    plugin_cfg="a_conf",
                                    vtype=None),
                          mock.call(name="foo",
                                    context=None,
                                    config=None,
                                    plugin_cfg="foo_conf",
                                    allow_hidden=True,
                                    vtype=None)],
                         mock_context_validate.call_args_list)
        mock_sla_validate.assert_called_once_with(
            config=None, context=None,
            name="foo_sla", plugin_cfg="sla_conf", vtype=None)
        mock_hook_action_validate.assert_called_once_with(
            config=None, context=None, name="c", plugin_cfg="c_args",
            vtype=None)
        mock_hook_trigger_validate.assert_called_once_with(
            config=None, context=None, name="d", plugin_cfg="d_args",
            vtype=None)

    @mock.patch("rally.task.engine.json.dumps")
    @mock.patch("rally.task.engine.scenario.Scenario.get")
    @mock.patch("rally.task.engine.TaskConfig")
    @mock.patch("rally.task.engine.runner.ScenarioRunner.validate")
    def test___validate_workload__wrong_runner(
            self, mock_scenario_runner_validate, mock_task_config,
            mock_scenario_get, mock_dumps):
        mock_dumps.return_value = "<JSON>"
        mock_scenario_runner_validate.return_value = [
            "There is no such runner"]
        scenario_cls = mock_scenario_get.return_value
        scenario_cls.get_default_context.return_value = {}
        workload = self._make_workload(name="sca", runner=("b", {}))
        eng = engine.TaskEngine(mock.MagicMock(), mock.MagicMock(),
                                mock.Mock())

        e = self.assertRaises(exceptions.InvalidTaskConfig,
                              eng._validate_workload, workload)
        self.assertEqual("Input task is invalid!\n\nSubtask sca[0] has wrong "
                         "configuration\nSubtask configuration:\n"
                         "<JSON>\n\nReason(s):\n"
                         " There is no such runner", e.format_message())

    @mock.patch("rally.task.engine.json.dumps")
    @mock.patch("rally.task.engine.scenario.Scenario.get")
    @mock.patch("rally.task.engine.TaskConfig")
    @mock.patch("rally.task.engine.context.Context.validate")
    def test__validate_config_syntax__wrong_context(
            self, mock_context_validate, mock_task_config, mock_scenario_get,
            mock_dumps):
        mock_dumps.return_value = "<JSON>"
        mock_context_validate.return_value = ["context_error"]
        scenario_cls = mock_scenario_get.return_value
        scenario_cls.get_default_context.return_value = {}
        mock_task_instance = mock.MagicMock()
        mock_task_instance.subtasks = [{"workloads": [
            self._make_workload(name="sca"),
            self._make_workload(name="sca", position=1,
                                contexts={"a": "a_conf"})
        ]}]
        eng = engine.TaskEngine(mock.MagicMock(), mock.MagicMock(),
                                mock.Mock())

        e = self.assertRaises(exceptions.InvalidTaskConfig,
                              eng._validate_config_syntax, mock_task_instance)
        self.assertEqual("Input task is invalid!\n\nSubtask sca[1] has wrong "
                         "configuration\nSubtask configuration:\n<JSON>\n\n"
                         "Reason(s):\n context_error", e.format_message())

    @mock.patch("rally.task.engine.json.dumps")
    @mock.patch("rally.task.engine.scenario.Scenario.get")
    @mock.patch("rally.task.sla.SLA.validate")
    @mock.patch("rally.task.engine.TaskConfig")
    def test__validate_config_syntax__wrong_sla(
            self, mock_task_config, mock_sla_validate, mock_scenario_get,
            mock_dumps):
        mock_dumps.return_value = "<JSON>"
        mock_sla_validate.return_value = ["sla_error"]
        scenario_cls = mock_scenario_get.return_value
        scenario_cls.get_default_context.return_value = {}
        mock_task_instance = mock.MagicMock()
        mock_task_instance.subtasks = [{"workloads": [
            self._make_workload(name="sca"),
            self._make_workload(name="sca", position=1,
                                sla={"foo_sla": "sla_conf"})
        ]}]
        eng = engine.TaskEngine(mock.MagicMock(), mock.MagicMock(),
                                mock.Mock())
        e = self.assertRaises(exceptions.InvalidTaskConfig,
                              eng._validate_config_syntax, mock_task_instance)
        self.assertEqual("Input task is invalid!\n\n"
                         "Subtask sca[1] has wrong configuration\n"
                         "Subtask configuration:\n<JSON>\n\n"
                         "Reason(s):\n sla_error", e.format_message())

    @mock.patch("rally.task.engine.json.dumps")
    @mock.patch("rally.task.engine.scenario.Scenario.get")
    @mock.patch("rally.task.hook.HookAction.validate")
    @mock.patch("rally.task.hook.HookTrigger.validate")
    @mock.patch("rally.task.engine.TaskConfig")
    def test__validate_config_syntax__wrong_hook(
            self, mock_task_config, mock_hook_trigger_validate,
            mock_hook_action_validate,
            mock_scenario_get, mock_dumps):
        mock_dumps.return_value = "<JSON>"
        mock_hook_trigger_validate.return_value = []
        mock_hook_action_validate.return_value = ["hook_error"]
        scenario_cls = mock_scenario_get.return_value
        scenario_cls.get_default_context.return_value = {}
        mock_task_instance = mock.MagicMock()
        hook_conf = {"action": ("c", "c_args"),
                     "trigger": ("d", "d_args")}
        mock_task_instance.subtasks = [{"workloads": [
            self._make_workload(name="sca"),
            self._make_workload(name="sca", position=1,
                                hooks=[hook_conf])
        ]}]
        eng = engine.TaskEngine(mock.MagicMock(), mock.MagicMock(),
                                mock.Mock())

        e = self.assertRaises(exceptions.InvalidTaskConfig,
                              eng._validate_config_syntax, mock_task_instance)

        self.assertEqual("Input task is invalid!\n\n"
                         "Subtask sca[1] has wrong configuration\n"
                         "Subtask configuration:\n<JSON>\n\n"
                         "Reason(s):\n hook_error", e.format_message())

    @mock.patch("rally.task.engine.json.dumps")
    @mock.patch("rally.task.engine.scenario.Scenario.get")
    @mock.patch("rally.task.hook.HookTrigger.validate")
    @mock.patch("rally.task.hook.HookAction.validate")
    @mock.patch("rally.task.engine.TaskConfig")
    def test__validate_config_syntax__wrong_trigger(
            self, mock_task_config, mock_hook_action_validate,
            mock_hook_trigger_validate,
            mock_scenario_get, mock_dumps):
        mock_dumps.return_value = "<JSON>"
        mock_hook_trigger_validate.return_value = ["trigger_error"]
        mock_hook_action_validate.return_value = []
        scenario_cls = mock_scenario_get.return_value
        scenario_cls.get_default_context.return_value = {}
        mock_task_instance = mock.MagicMock()
        hook_conf = {"action": ("c", "c_args"),
                     "trigger": ("d", "d_args")}
        mock_task_instance.subtasks = [{"workloads": [
            self._make_workload(name="sca"),
            self._make_workload(name="sca", position=1,
                                hooks=[hook_conf])
        ]}]
        eng = engine.TaskEngine(mock.MagicMock(), mock.MagicMock(),
                                mock.Mock())

        e = self.assertRaises(exceptions.InvalidTaskConfig,
                              eng._validate_config_syntax, mock_task_instance)

        self.assertEqual("Input task is invalid!\n\n"
                         "Subtask sca[1] has wrong configuration\n"
                         "Subtask configuration:\n<JSON>\n\n"
                         "Reason(s):\n trigger_error", e.format_message())

    @mock.patch("rally.task.engine.context.Context")
    @mock.patch("rally.task.engine.TaskConfig")
    @mock.patch("rally.task.engine.objects.Deployment.get",
                return_value="FakeDeployment")
    def test__validate_config_semantic(
            self, mock_deployment_get,
            mock_task_config, mock_context):
        admin = fakes.fake_credential(foo="admin")
        users = [fakes.fake_credential(bar="user1")]
        deployment = fakes.FakeDeployment(
            uuid="deployment_uuid", admin=admin, users=users)

        @scenario.configure("SomeScen.scenario")
        class SomeScen(scenario.Scenario):

            def run(self):
                pass

        mock_task_instance = mock.MagicMock()
        wconf1 = self._make_workload(name="SomeScen.scenario",
                                     contexts={"users": {}})
        wconf2 = self._make_workload(name="SomeScen.scenario",
                                     position=1)
        subtask1 = {"workloads": [wconf1, wconf2]}

        wconf3 = self._make_workload(name="SomeScen.scenario",
                                     position=2)
        subtask2 = {"workloads": [wconf3]}

        mock_task_instance.subtasks = [subtask1, subtask2]
        fake_task = mock.MagicMock()
        eng = engine.TaskEngine(mock_task_instance, fake_task, deployment)

        eng._validate_config_semantic(mock_task_instance)

    @mock.patch("rally.task.engine.TaskConfig")
    @mock.patch("rally.task.engine.TaskEngine._validate_workload")
    def test__validate_config_platforms(
            self, mock__validate_workload, mock_task_config):

        class FakeDeployment(object):
            def __init__(self, credentials):
                self._creds = credentials
                self.get_all_credentials = mock.Mock()
                self.get_all_credentials.return_value = self._creds

        foo_cred1 = {"admin": "admin", "users": ["user1"]}
        foo_cred2 = {"admin": "admin", "users": ["user1"]}
        deployment = FakeDeployment({"foo": [foo_cred1, foo_cred2]})

        workload1 = "workload1"
        workload2 = "workload2"
        subtasks = [{"workloads": [workload1]},
                    {"workloads": [workload2]}]
        config = mock.Mock(subtasks=subtasks)
        eng = engine.TaskEngine({}, mock.MagicMock(), deployment)

        eng._validate_config_platforms(config)

        self.assertEqual(
            [mock.call(w, vtype="platform",
                       vcontext={"platforms": {"foo": foo_cred1},
                                 "task": eng.task})
             for w in (workload1, workload2)],
            mock__validate_workload.call_args_list)
        deployment.get_all_credentials.assert_called_once_with()

    @mock.patch("rally.common.objects.Task.get_status")
    @mock.patch("rally.task.engine.TaskConfig")
    @mock.patch("rally.task.engine.ResultConsumer")
    @mock.patch("rally.task.engine.context.ContextManager.cleanup")
    @mock.patch("rally.task.engine.context.ContextManager.setup")
    @mock.patch("rally.task.engine.scenario.Scenario")
    @mock.patch("rally.task.engine.runner.ScenarioRunner")
    def test_run__update_status(
            self, mock_scenario_runner, mock_scenario,
            mock_context_manager_setup, mock_context_manager_cleanup,
            mock_result_consumer, mock_task_config, mock_task_get_status):

        task = mock.MagicMock()
        mock_task_get_status.return_value = consts.TaskStatus.ABORTING
        eng = engine.TaskEngine(mock.MagicMock(), task, mock.Mock())
        eng.run()
        task.update_status.assert_has_calls([
            mock.call(consts.TaskStatus.RUNNING),
            mock.call(consts.TaskStatus.FINISHED)
        ])

    @mock.patch("rally.task.engine.objects.task.Task.get_status")
    @mock.patch("rally.task.engine.LOG")
    @mock.patch("rally.task.engine.ResultConsumer")
    @mock.patch("rally.task.engine.context.Context")
    @mock.patch("rally.task.engine.scenario.Scenario")
    @mock.patch("rally.task.engine.runner.ScenarioRunner")
    @mock.patch("rally.task.engine.context.ContextManager.cleanup")
    @mock.patch("rally.task.engine.context.ContextManager.setup")
    def test_run_exception_is_logged(
            self, mock_context_manager_setup, mock_context_manager_cleanup,
            mock_scenario_runner, mock_scenario, mock_context,
            mock_result_consumer, mock_log, mock_task_get_status):
        scenario_cls = mock_scenario.get.return_value
        scenario_cls.get_default_context.return_value = {}

        context_cls = mock_context.get.return_value
        context_cls.get_fullname.return_value = "context_a"

        mock_context_manager_setup.side_effect = Exception
        mock_result_consumer.is_task_in_aborting_status.return_value = False

        mock_task_instance = mock.MagicMock()

        mock_task_instance.subtasks = [{
            "title": "foo",
            "description": "Do not launch it!!",
            "context": {},
            "workloads": [
                self._make_workload(name="a.task", description="foo",
                                    contexts={"context_a": {"a": 1}}),
                self._make_workload(name="a.task", description="foo",
                                    contexts={"context_a": {"b": 2}},
                                    position=2)]}]

        deployment = fakes.FakeDeployment(
            uuid="deployment_uuid", admin={"foo": "admin"})
        eng = engine.TaskEngine(mock_task_instance, mock.MagicMock(),
                                deployment)
        eng.run()

        self.assertEqual(2, mock_log.exception.call_count)

    @mock.patch("rally.task.engine.ResultConsumer")
    @mock.patch("rally.task.engine.context.ContextManager.cleanup")
    @mock.patch("rally.task.engine.context.ContextManager.setup")
    @mock.patch("rally.task.engine.scenario.Scenario")
    @mock.patch("rally.task.engine.runner.ScenarioRunner")
    def test_run__task_soft_aborted(
            self, mock_scenario_runner, mock_scenario,
            mock_context_manager_setup, mock_context_manager_cleanup,
            mock_result_consumer):
        scenario_cls = mock_scenario.get.return_value
        scenario_cls.get_platform.return_value = "openstack"
        scenario_cls.get_info.return_value = {"title": ""}
        task = mock.MagicMock()
        mock_result_consumer.is_task_in_aborting_status.side_effect = [False,
                                                                       False,
                                                                       True]
        config = engine.TaskConfig({
            "a.task": [{"runner": {"type": "a", "b": 1},
                        "description": "foo"}],
            "b.task": [{"runner": {"type": "a", "b": 1},
                        "description": "bar"}],
            "c.task": [{"runner": {"type": "a", "b": 1},
                        "description": "xxx"}]
        })
        fake_runner_cls = mock.MagicMock()
        fake_runner = mock.MagicMock()
        fake_runner_cls.return_value = fake_runner
        mock_scenario_runner.get.return_value = fake_runner_cls
        deployment = fakes.FakeDeployment(
            uuid="deployment_uuid", admin={"foo": "admin"})
        eng = engine.TaskEngine(config, task, deployment)

        eng.run()

        self.assertEqual(2, fake_runner.run.call_count)
        self.assertEqual(mock.call(consts.TaskStatus.ABORTED),
                         task.update_status.mock_calls[-1])
        subtask_obj = task.add_subtask.return_value
        subtask_obj.update_status.assert_has_calls((
            mock.call(consts.SubtaskStatus.FINISHED),
            mock.call(consts.SubtaskStatus.FINISHED),
            mock.call(consts.SubtaskStatus.ABORTED),
        ))

    @mock.patch("rally.common.objects.Task.get_status")
    @mock.patch("rally.task.engine.ResultConsumer")
    @mock.patch("rally.task.engine.context.ContextManager.cleanup")
    @mock.patch("rally.task.engine.context.ContextManager.setup")
    @mock.patch("rally.task.engine.scenario.Scenario")
    @mock.patch("rally.task.engine.runner.ScenarioRunner")
    def test_run__task_aborted(
            self, mock_scenario_runner, mock_scenario,
            mock_context_manager_setup, mock_context_manager_cleanup,
            mock_result_consumer, mock_task_get_status):
        task = mock.MagicMock(spec=objects.Task)
        config = engine.TaskConfig({
            "a.task": [{"runner": {"type": "a", "b": 1}}],
            "b.task": [{"runner": {"type": "a", "b": 1}}],
            "c.task": [{"runner": {"type": "a", "b": 1}}]
        })
        fake_runner_cls = mock.MagicMock()
        fake_runner = mock.MagicMock()
        fake_runner_cls.return_value = fake_runner
        mock_task_get_status.return_value = consts.TaskStatus.SOFT_ABORTING
        mock_scenario_runner.get.return_value = fake_runner_cls
        eng = engine.TaskEngine(config, task, mock.Mock())
        eng.run()
        self.assertEqual(mock.call(consts.TaskStatus.ABORTED),
                         task.update_status.mock_calls[-1])
        subtask_obj = task.add_subtask.return_value
        subtask_obj.update_status.assert_called_once_with(
            consts.SubtaskStatus.ABORTED)

    @mock.patch("rally.common.objects.Task.get_status")
    @mock.patch("rally.task.engine.ResultConsumer")
    @mock.patch("rally.task.engine.context.ContextManager.cleanup")
    @mock.patch("rally.task.engine.context.ContextManager.setup")
    @mock.patch("rally.task.engine.scenario.Scenario")
    @mock.patch("rally.task.engine.runner.ScenarioRunner")
    def test_run__subtask_crashed(
            self, mock_scenario_runner, mock_scenario,
            mock_context_manager_setup, mock_context_manager_cleanup,
            mock_result_consumer, mock_task_get_status):
        task = mock.MagicMock(spec=objects.Task)
        subtask_obj = task.add_subtask.return_value
        subtask_obj.add_workload.side_effect = MyException()
        mock_result_consumer.is_task_in_aborting_status.return_value = False
        config = engine.TaskConfig({
            "a.task": [{"runner": {"type": "a", "b": 1}}],
            "b.task": [{"runner": {"type": "a", "b": 1}}],
            "c.task": [{"runner": {"type": "a", "b": 1}}]
        })
        fake_runner_cls = mock.MagicMock()
        fake_runner = mock.MagicMock()
        fake_runner_cls.return_value = fake_runner
        mock_scenario_runner.get.return_value = fake_runner_cls
        eng = engine.TaskEngine(config, task, mock.Mock())
        self.assertRaises(MyException, eng.run)

        task.update_status.assert_has_calls((
            mock.call(consts.TaskStatus.RUNNING),
            mock.call(consts.TaskStatus.CRASHED),
        ))
        subtask_obj.update_status.assert_called_once_with(
            consts.SubtaskStatus.CRASHED)

    @mock.patch("rally.task.engine.TaskConfig")
    def test__prepare_context(self, mock_task_config):

        @context.configure("test1", 1, platform="testing")
        class TestContext1(context.Context):
            pass

        self.addCleanup(TestContext1.unregister)

        @context.configure("test2", 2, platform="testing")
        class TestContext2(context.Context):
            pass

        self.addCleanup(TestContext2.unregister)

        @scenario.configure("test_ctx.test", platform="testing",
                            context={"test1@testing": {"a": 1}})
        class TestScenario(scenario.Scenario):
            pass

        self.addCleanup(TestScenario.unregister)

        task = mock.MagicMock()
        name = "test_ctx.test"
        context_config = {"test1": 1, "test2": 2}

        eng = engine.TaskEngine({}, task, mock.MagicMock())
        result = eng._prepare_context(context_config, name, "foo_uuid")
        expected_result = {
            "task": task,
            "owner_id": "foo_uuid",
            "scenario_name": name,
            "config": {"test1@testing": 1, "test2@testing": 2}
        }
        self.assertEqual(expected_result, result)


class ResultConsumerTestCase(test.TestCase):

    @mock.patch("rally.common.objects.Task.get_status")
    @mock.patch("rally.task.engine.ResultConsumer.wait_and_abort")
    @mock.patch("rally.task.sla.SLAChecker")
    def test_consume_results(
            self, mock_sla_checker, mock_result_consumer_wait_and_abort,
            mock_task_get_status):
        mock_sla_instance = mock.MagicMock()
        mock_sla_checker.return_value = mock_sla_instance
        mock_task_get_status.return_value = consts.TaskStatus.RUNNING
        workload_cfg = {"fake": 2, "hooks": []}
        task = mock.MagicMock()
        subtask = mock.Mock(spec=objects.Subtask)
        workload = mock.Mock(spec=objects.Workload)
        runner = mock.MagicMock()

        results = [
            [{"duration": 1, "timestamp": 3}],
            [{"duration": 2, "timestamp": 2}]
        ]

        runner.result_queue = collections.deque(results)
        runner.event_queue = collections.deque()
        with engine.ResultConsumer(workload_cfg, task, subtask, workload,
                                   runner, False) as consumer_obj:
            pass

        mock_sla_instance.add_iteration.assert_has_calls([
            mock.call({"duration": 1, "timestamp": 3}),
            mock.call({"duration": 2, "timestamp": 2})])

        self.assertEqual([{"duration": 2, "timestamp": 2},
                          {"duration": 1, "timestamp": 3}],
                         consumer_obj.results)

    @mock.patch("rally.task.hook.HookExecutor")
    @mock.patch("rally.task.engine.LOG")
    @mock.patch("rally.task.engine.time.time")
    @mock.patch("rally.common.objects.Task.get_status")
    @mock.patch("rally.task.engine.ResultConsumer.wait_and_abort")
    @mock.patch("rally.task.sla.SLAChecker")
    def test_consume_results_no_iteration(
            self, mock_sla_checker, mock_result_consumer_wait_and_abort,
            mock_task_get_status, mock_time, mock_log, mock_hook_executor):
        mock_time.side_effect = [0, 1]
        mock_sla_instance = mock.MagicMock()
        mock_sla_results = mock.MagicMock()
        mock_sla_checker.return_value = mock_sla_instance
        mock_sla_instance.results.return_value = mock_sla_results
        mock_task_get_status.return_value = consts.TaskStatus.RUNNING
        workload_cfg = {"fake": 2, "hooks": []}
        task = mock.MagicMock()
        subtask = mock.Mock(spec=objects.Subtask)
        workload = mock.Mock(spec=objects.Workload)
        runner = mock.MagicMock()

        results = []
        runner.result_queue = collections.deque(results)
        runner.event_queue = collections.deque()
        with engine.ResultConsumer(
                workload_cfg, task, subtask, workload, runner, False):
            pass

        self.assertFalse(workload.add_workload_data.called)
        workload.set_results.assert_called_once_with(
            full_duration=1, sla_results=mock_sla_results, load_duration=0,
            start_time=None)

    @mock.patch("rally.common.objects.Task.get_status")
    @mock.patch("rally.task.engine.ResultConsumer.wait_and_abort")
    @mock.patch("rally.task.sla.SLAChecker")
    def test_consume_results_sla_failure_abort(
            self, mock_sla_checker, mock_result_consumer_wait_and_abort,
            mock_task_get_status):
        mock_sla_instance = mock.MagicMock()
        mock_sla_checker.return_value = mock_sla_instance
        mock_sla_instance.add_iteration.side_effect = [True, True, False,
                                                       False]
        workload_cfg = {"fake": 2, "hooks": []}
        task = mock.MagicMock()
        subtask = mock.Mock(spec=objects.Subtask)
        workload = mock.Mock(spec=objects.Workload)
        runner = mock.MagicMock()

        runner.result_queue = collections.deque(
            [[{"duration": 1, "timestamp": 1},
              {"duration": 2, "timestamp": 2}]] * 4)

        with engine.ResultConsumer(workload_cfg, task, subtask, workload,
                                   runner, True):
            pass

        self.assertTrue(runner.abort.called)
        task.update_status.assert_called_once_with(
            consts.TaskStatus.SOFT_ABORTING)

    @mock.patch("rally.task.hook.HookExecutor")
    @mock.patch("rally.common.objects.Task.get_status")
    @mock.patch("rally.task.engine.threading.Thread")
    @mock.patch("rally.task.engine.threading.Event")
    @mock.patch("rally.task.sla.SLAChecker")
    def test_consume_results_abort_manually(self, mock_sla_checker,
                                            mock_event, mock_thread,
                                            mock_task_get_status,
                                            mock_hook_executor):
        runner = mock.MagicMock(result_queue=False)

        is_done = mock.MagicMock()
        is_done.isSet.side_effect = (False, True)

        task = mock.MagicMock()
        mock_task_get_status.return_value = consts.TaskStatus.ABORTED
        subtask = mock.Mock(spec=objects.Subtask)
        workload = mock.Mock(spec=objects.Workload)

        workload_cfg = {"fake": 2, "hooks": []}

        mock_hook_executor_instance = mock_hook_executor.return_value

        with engine.ResultConsumer(workload_cfg, task, subtask, workload,
                                   runner, True):
            pass

        mock_sla_checker.assert_called_once_with(workload_cfg)
        mock_hook_executor.assert_called_once_with(workload_cfg, task)
        self.assertFalse(mock_hook_executor_instance.on_iteration.called)
        mocked_set_aborted = mock_sla_checker.return_value.set_aborted_manually
        mocked_set_aborted.assert_called_once_with()

    @mock.patch("rally.common.objects.Task.get_status")
    @mock.patch("rally.task.sla.SLAChecker")
    def test_consume_results_sla_failure_continue(self, mock_sla_checker,
                                                  mock_task_get_status):
        mock_sla_instance = mock.MagicMock()
        mock_sla_checker.return_value = mock_sla_instance
        mock_task_get_status.return_value = consts.TaskStatus.CRASHED
        mock_sla_instance.add_iteration.side_effect = [True, True, False,
                                                       False]
        workload_cfg = {"fake": 2, "hooks": []}
        task = mock.MagicMock()
        subtask = mock.Mock(spec=objects.Subtask)
        workload = mock.Mock(spec=objects.Workload)
        runner = mock.MagicMock()
        runner.result_queue = collections.deque(
            [[{"duration": 1, "timestamp": 4}]] * 4)
        runner.event_queue = collections.deque()

        with engine.ResultConsumer(workload_cfg, task, subtask, workload,
                                   runner, False):
            pass

        self.assertEqual(0, runner.abort.call_count)

    @mock.patch("rally.common.objects.Task.get_status")
    @mock.patch("rally.task.engine.threading.Thread")
    @mock.patch("rally.task.engine.threading.Event")
    @mock.patch("rally.task.sla.SLAChecker")
    def test_consume_results_with_unexpected_failure(self, mock_sla_checker,
                                                     mock_event, mock_thread,
                                                     mock_task_get_status):
        mock_sla_instance = mock.MagicMock()
        mock_sla_checker.return_value = mock_sla_instance
        workload_cfg = {"fake": 2, "hooks": []}
        task = mock.MagicMock()
        subtask = mock.Mock(spec=objects.Subtask)
        workload = mock.Mock(spec=objects.Workload)
        runner = mock.MagicMock()
        runner.result_queue = collections.deque([1])
        runner.event_queue = collections.deque()
        exc = MyException()
        try:
            with engine.ResultConsumer(workload_cfg, task, subtask, workload,
                                       runner, False):
                raise exc
        except MyException:
            pass

        mock_sla_instance.set_unexpected_failure.assert_has_calls(
            [mock.call(exc)])

    @mock.patch("rally.task.engine.CONF")
    @mock.patch("rally.common.objects.Task.get_status")
    @mock.patch("rally.task.engine.ResultConsumer.wait_and_abort")
    @mock.patch("rally.task.sla.SLAChecker")
    def test_consume_results_chunked(
            self, mock_sla_checker, mock_result_consumer_wait_and_abort,
            mock_task_get_status, mock_conf):
        mock_conf.raw_result_chunk_size = 2
        mock_sla_instance = mock.MagicMock()
        mock_sla_checker.return_value = mock_sla_instance
        mock_task_get_status.return_value = consts.TaskStatus.RUNNING
        workload_cfg = {"fake": 2, "hooks": []}
        task = mock.MagicMock(spec=objects.Task)
        subtask = mock.Mock(spec=objects.Subtask)
        workload = mock.Mock(spec=objects.Workload)
        runner = mock.MagicMock()

        results = [
            [{"duration": 1, "timestamp": 3},
             {"duration": 2, "timestamp": 2},
             {"duration": 3, "timestamp": 3}],
            [{"duration": 4, "timestamp": 2},
             {"duration": 5, "timestamp": 3}],
            [{"duration": 6, "timestamp": 2}],
            [{"duration": 7, "timestamp": 1}],
        ]

        runner.result_queue = collections.deque(results)
        runner.event_queue = collections.deque()
        with engine.ResultConsumer(workload_cfg, task, subtask, workload,
                                   runner, False) as consumer_obj:
            pass

        mock_sla_instance.add_iteration.assert_has_calls([
            mock.call({"duration": 1, "timestamp": 3}),
            mock.call({"duration": 2, "timestamp": 2}),
            mock.call({"duration": 3, "timestamp": 3}),
            mock.call({"duration": 4, "timestamp": 2}),
            mock.call({"duration": 5, "timestamp": 3}),
            mock.call({"duration": 6, "timestamp": 2}),
            mock.call({"duration": 7, "timestamp": 1})])

        self.assertEqual([{"duration": 7, "timestamp": 1}],
                         consumer_obj.results)

        workload.add_workload_data.assert_has_calls([
            mock.call(0, {"raw": [{"duration": 2, "timestamp": 2},
                                  {"duration": 1, "timestamp": 3}]}),
            mock.call(1, {"raw": [{"duration": 4, "timestamp": 2},
                                  {"duration": 3, "timestamp": 3}]}),
            mock.call(2, {"raw": [{"duration": 6, "timestamp": 2},
                                  {"duration": 5, "timestamp": 3}]}),
            mock.call(3, {"raw": [{"duration": 7, "timestamp": 1}]})])

    @mock.patch("rally.task.engine.LOG")
    @mock.patch("rally.task.hook.HookExecutor")
    @mock.patch("rally.task.engine.time.time")
    @mock.patch("rally.common.objects.Task.get_status")
    @mock.patch("rally.task.engine.ResultConsumer.wait_and_abort")
    @mock.patch("rally.task.sla.SLAChecker")
    def test_consume_events(
            self, mock_sla_checker, mock_result_consumer_wait_and_abort,
            mock_task_get_status, mock_time, mock_hook_executor, mock_log):
        mock_time.side_effect = [0, 1]
        mock_sla_instance = mock_sla_checker.return_value
        mock_sla_results = mock_sla_instance.results.return_value
        mock_hook_executor_instance = mock_hook_executor.return_value
        mock_hook_results = mock_hook_executor_instance.results.return_value

        mock_task_get_status.return_value = consts.TaskStatus.RUNNING
        workload_cfg = {"fake": 2, "hooks": [{"config": True}]}
        task = mock.MagicMock()
        subtask = mock.Mock(spec=objects.Subtask)
        workload = mock.Mock(spec=objects.Workload)
        runner = mock.MagicMock()
        events = [
            {"type": "iteration", "value": 1},
            {"type": "iteration", "value": 2},
            {"type": "iteration", "value": 3}
        ]
        runner.result_queue = collections.deque()
        runner.event_queue = collections.deque(events)

        consumer_obj = engine.ResultConsumer(workload_cfg, task, subtask,
                                             workload, runner, False)
        stop_event = threading.Event()

        def set_stop_event(event_type, value):
            if not runner.event_queue:
                stop_event.set()

        mock_hook_executor_instance.on_event.side_effect = set_stop_event

        with consumer_obj:
            stop_event.wait(1)

        mock_hook_executor_instance.on_event.assert_has_calls([
            mock.call(event_type="iteration", value=1),
            mock.call(event_type="iteration", value=2),
            mock.call(event_type="iteration", value=3)
        ])

        self.assertFalse(workload.add_workload_data.called)
        workload.set_results.assert_called_once_with(
            full_duration=1,
            load_duration=0,
            sla_results=mock_sla_results,
            hooks_results=mock_hook_results,
            start_time=None)

    @mock.patch("rally.task.engine.threading.Thread")
    @mock.patch("rally.task.engine.threading.Event")
    @mock.patch("rally.common.objects.Task.get_status")
    @mock.patch("rally.task.engine.TaskEngine._prepare_context")
    @mock.patch("rally.task.engine.time.sleep")
    def test_wait_and_abort_on_abort(
            self, mock_sleep, mock_task_engine__prepare_context,
            mock_task_get_status, mock_event, mock_thread):
        runner = mock.MagicMock()
        key = mock.MagicMock()
        task = mock.MagicMock()
        subtask = mock.Mock(spec=objects.Subtask)
        workload = mock.Mock(spec=objects.Workload)
        mock_task_get_status.side_effect = (consts.TaskStatus.RUNNING,
                                            consts.TaskStatus.RUNNING,
                                            consts.TaskStatus.ABORTING)
        mock_is_done = mock.MagicMock()
        mock_event.return_value = mock_is_done
        mock_is_done.isSet.return_value = False

        res = engine.ResultConsumer(key, task, subtask, workload, runner, True)
        res.wait_and_abort()

        runner.abort.assert_called_with()
        # test task.get_status is checked until is_done is not set
        self.assertEqual(3, mock_task_get_status.call_count)

    @mock.patch("rally.task.engine.threading.Thread")
    @mock.patch("rally.task.engine.threading.Event")
    @mock.patch("rally.common.objects.Task.get_status")
    @mock.patch("rally.task.engine.TaskEngine._prepare_context")
    @mock.patch("rally.task.engine.time.sleep")
    def test_wait_and_abort_on_no_abort(
            self, mock_sleep, mock_task_engine__prepare_context,
            mock_task_get_status, mock_event, mock_thread):
        runner = mock.MagicMock()
        key = mock.MagicMock()
        task = mock.MagicMock()
        subtask = mock.Mock(spec=objects.Subtask)
        workload = mock.Mock(spec=objects.Workload)
        mock_task_get_status.return_value = consts.TaskStatus.RUNNING
        mock_is_done = mock.MagicMock()
        mock_event.return_value = mock_is_done

        mock_is_done.isSet.side_effect = [False, False, False, False, True]

        res = engine.ResultConsumer(key, task, subtask, workload, runner, True)
        res.wait_and_abort()

        # check method don't abort runner if task is not aborted
        self.assertFalse(runner.abort.called)
        # test task.get_status is checked until is_done is not set
        self.assertEqual(4, mock_task_get_status.call_count)


class TaskConfigTestCase(test.TestCase):

    def test_init_empty_config(self):
        config = None
        exception = self.assertRaises(Exception,  # noqa
                                      engine.TaskConfig, config)
        self.assertIn("Input task is empty", str(exception))

    @mock.patch("jsonschema.validate")
    def test_validate_json(self, mock_validate):
        config = {}
        engine.TaskConfig(config)
        mock_validate.assert_has_calls([
            mock.call(config, engine.TaskConfig.CONFIG_SCHEMA_V1)])

    @mock.patch("jsonschema.validate")
    def test_validate_json_v2(self, mock_validate):
        config = {"version": 2, "subtasks": []}
        engine.TaskConfig(config)
        mock_validate.assert_has_calls([
            mock.call(config, engine.TaskConfig.CONFIG_SCHEMA_V2)])

    @mock.patch("rally.task.engine.TaskConfig._get_version")
    @mock.patch("rally.task.engine.TaskConfig._validate_json")
    def test_validate_version(self, mock_task_config__validate_json,
                              mock_task_config__get_version):
        mock_task_config__get_version.return_value = 1
        engine.TaskConfig(mock.MagicMock())

    @mock.patch("rally.task.engine.TaskConfig._get_version")
    @mock.patch("rally.task.engine.TaskConfig._validate_json")
    def test_validate_version_wrong_version(
            self, mock_task_config__validate_json,
            mock_task_config__get_version):

        mock_task_config__get_version.return_value = "wrong"
        self.assertRaises(exceptions.InvalidTaskException, engine.TaskConfig,
                          mock.MagicMock)

    def test__adopt_task_format_v1(self):

        # mock all redundant checks :)
        class TaskConfig(engine.TaskConfig):
            def __init__(self):
                pass

        config = collections.OrderedDict()
        config["a.task"] = [{"s": 1, "context": {"foo": "bar"}}, {"s": 2}]
        config["b.task"] = [{"s": 3, "sla": {"key": "value"}}]
        config["c.task"] = [{"s": 5,
                             "hooks": [{"name": "foo",
                                        "args": "bar",
                                        "description": "DESCR!!!",
                                        "trigger": {
                                            "name": "mega-trigger",
                                            "args": {"some": "thing"}
                                        }}]
                             }]
        self.assertEqual(
            {"title": "Task (adopted from task format v1)",
             "subtasks": [
                 {
                     "title": "a.task",
                     "scenario": {"a.task": {}},
                     "s": 1,
                     "contexts": {"foo": "bar"}
                 },
                 {
                     "title": "a.task",
                     "s": 2,
                     "scenario": {"a.task": {}},
                     "contexts": {}
                 },
                 {
                     "title": "b.task",
                     "s": 3,
                     "scenario": {"b.task": {}},
                     "sla": {"key": "value"},
                     "contexts": {}
                 },
                 {
                     "title": "c.task",
                     "s": 5,
                     "scenario": {"c.task": {}},
                     "contexts": {},
                     "hooks": [
                         {"description": "DESCR!!!",
                          "action": {"foo": "bar"},
                          "trigger": {"mega-trigger": {"some": "thing"}}}
                     ]
                 }]},
            TaskConfig._adopt_task_format_v1(config))

    def test_hook_config_compatibility(self):
        cfg = {
            "title": "foo",
            "version": 2,
            "subtasks": [
                {
                    "title": "foo",
                    "scenario": {"xxx": {}},
                    "runner": {"yyy": {}},
                    "hooks": [
                        {"description": "descr",
                         "name": "hook_action",
                         "args": {"k1": "v1"},
                         "trigger": {
                             "name": "hook_trigger",
                             "args": {"k2": "v2"}
                         }}
                    ]
                }
            ]
        }
        task = engine.TaskConfig(cfg)
        workload = task.subtasks[0]["workloads"][0]
        self.assertEqual(
            {"description": "descr",
             "action": ("hook_action", {"k1": "v1"}),
             "trigger": ("hook_trigger", {"k2": "v2"})},
            workload["hooks"][0])
