# -*- coding:utf-8 -*-

import logging

from fn import _
from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList

from jumeaux.addons.judgement import JudgementExecutor
from jumeaux.addons.utils import exact_match
from jumeaux.models import JudgementAddOnPayload, DiffKeys, Ignore, Condition

logger = logging.getLogger(__name__)


class Config(OwlMixin):
    ignores: TList[Ignore]


class Executor(JudgementExecutor):
    config: Config

    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: JudgementAddOnPayload) -> JudgementAddOnPayload:
        if payload.regard_as_same or payload.remaining_diff_keys.is_none():
            return payload

        def filter_diff_keys(diff_keys: DiffKeys, condition: Condition) -> DiffKeys:
            if any([condition.path.get() and not exact_match(condition.path.get(), payload.path),
                    condition.name.get() and not exact_match(condition.name.get(), payload.name)]):
                return diff_keys

            return DiffKeys.from_dict({
                "added": diff_keys.added.reject(
                    lambda dk: condition.added.any(lambda ig: exact_match(ig, dk))
                ),
                "removed": diff_keys.removed.reject(
                    lambda dk: condition.removed.any(lambda ig: exact_match(ig, dk))
                ),
                "changed": diff_keys.changed.reject(
                    lambda dk: condition.changed.any(lambda ig: exact_match(ig, dk))
                )
            })

        filtered_diff_keys = self.config.ignores.flat_map(_.conditions).reduce(filter_diff_keys,
                                                                               payload.remaining_diff_keys.get())
        logger.debug('-' * 80)
        logger.debug('filter_diff_keys')
        logger.debug('-' * 80)
        logger.debug(filtered_diff_keys.to_pretty_json())

        return JudgementAddOnPayload.from_dict({
            "name": payload.name,
            "path": payload.path,
            "qs": payload.qs,
            "headers": payload.headers,
            "res_one": payload.res_one,
            "res_other": payload.res_other,
            "diff_keys": payload.diff_keys,
            "remaining_diff_keys": filtered_diff_keys,
            "regard_as_same": not (filtered_diff_keys.added or filtered_diff_keys.removed or filtered_diff_keys.changed)
        })
