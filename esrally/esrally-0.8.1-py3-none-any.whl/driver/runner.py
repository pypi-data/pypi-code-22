import sys
import types
import time
import logging
from collections import Counter, OrderedDict

from esrally import exceptions, track

logger = logging.getLogger("rally.driver")

# Mapping from operation type to specific runner
__RUNNERS = {}


def runner_for(operation_type):
    try:
        return __RUNNERS[operation_type]
    except KeyError:
        raise exceptions.RallyError("No runner available for operation type [%s]" % operation_type)


def register_runner(operation_type, runner):
    # we'd rather use callable() but this will erroneously also classify a class as callable...
    if isinstance(runner, types.FunctionType):
        logger.info("Registering runner function [%s] for [%s]." % (str(runner), str(operation_type)))
        __RUNNERS[operation_type] = DelegatingRunner(runner, runner.__name__)
    elif "__enter__" in dir(runner) and "__exit__" in dir(runner):
        logger.info("Registering context-manager capable runner object [%s] for [%s]." % (str(runner), str(operation_type)))
        __RUNNERS[operation_type] = runner
    else:
        logger.info("Registering runner object [%s] for [%s]." % (str(runner), str(operation_type)))
        __RUNNERS[operation_type] = DelegatingRunner(runner, str(runner))


# Only intended for unit-testing!
def remove_runner(operation_type):
    del __RUNNERS[operation_type]


class Runner:
    """
    Base class for all operations against Elasticsearch.
    """

    def __enter__(self):
        return self

    def __call__(self, *args):
        """
        Runs the actual method that should be benchmarked.

        :param args: All arguments that are needed to call this method.
        :return: A pair of (int, String). The first component indicates the "weight" of this call. it is typically 1 but for bulk operations
                 it should be the actual bulk size. The second component is the "unit" of weight which should be "ops" (short for
                 "operations") by default. If applicable, the unit should always be in plural form. It is used in metrics records
                 for throughput and reports. A value will then be shown as e.g. "111 ops/s".
        """
        raise NotImplementedError("abstract operation")

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


class DelegatingRunner(Runner):
    def __init__(self, runnable, name):
        self.runnable = runnable
        self.name = name

    def __call__(self, *args):
        return self.runnable(*args)

    def __repr__(self, *args, **kwargs):
        return "user-defined runner for [%s]" % self.name


def mandatory(params, key, op):
    try:
        return params[key]
    except KeyError:
        raise exceptions.DataError("Parameter source for operation '%s' did not provide the mandatory parameter '%s'. Please add it to your"
                                   " parameter source." % (op, key))


class BulkIndex(Runner):
    """
    Bulk indexes the given documents.
    """

    def __init__(self):
        super().__init__()

    def __call__(self, es, params):
        """
        Runs one bulk indexing operation.

        :param es: The Elasticsearch client.
        :param params: A hash with all parameters. See below for details.
        :return: A hash with meta data for this bulk operation. See below for details.

        It expects a parameter dict with the following mandatory keys:

        * ``body``: containing all documents for the current bulk request.
        * ``bulk-size``: the number of documents in this bulk.
        * ``action_metadata_present``: if ``True``, assume that an action and metadata line is present (meaning only half of the lines
        contain actual documents to index)
        * ``index``: The name of the affected index in case ``action_metadata_present`` is ``False``.
        * ``type``: The name of the affected type in case ``action_metadata_present`` is ``False``.

        The following keys are optional:

        * ``pipeline``: If present, runs the the specified ingest pipeline for this bulk.
        * ``detailed-results``: If ``True``, the runner will analyze the response and add detailed meta-data. Defaults to ``False``. Note
        that this has a very significant impact on performance and will very likely cause a bottleneck in the benchmark driver so please
        be very cautious enabling this feature. Our own measurements have shown a median overhead of several thousand times (execution time
         is in the single digit microsecond range when this feature is disabled and in the single digit millisecond range when this feature
         is enabled; numbers based on a bulk size of 500 elements and no errors). For details please refer to the respective benchmarks
         in ``benchmarks/driver``.


        Returned meta data
        `
        The following meta data are always returned:

        * ``index``: name of the affected index. May be `None` if it could not be derived.
        * ``bulk-size``: bulk size, e.g. 5.000.
        * ``bulk-request-size-bytes``: size of the full bulk requset in bytes
        * ``total-document-size-bytes``: size of all documents contained in the bulk request in bytes
        * ``weight``: operation-agnostic representation of the bulk size (used internally by Rally for throughput calculation).
        * ``unit``: The unit in which to interpret ``bulk-size`` and ``weight``. Always "docs".
        * ``success``: A boolean indicating whether the bulk request has succeeded.
        * ``success-count``: Number of successfully processed items for this request (denoted in ``unit``).
        * ``error-count``: Number of failed items for this request (denoted in ``unit``).

        If ``detailed-results`` is ``True`` the following meta data are returned in addition:

        * ``ops``: A hash with the operation name as key (e.g. index, update, delete) and various counts as values. ``item-count`` contains
          the total number of items for this key. Additionally, we return a separate counter each result (indicating e.g. the number of created
          items, the number of deleted items etc.).
        * ``shards_histogram``: An array of hashes where each hash has two keys: ``item-count`` contains the number of items to which a shard
          distribution applies and ``shards`` contains another hash with the actual distribution of ``total``, ``successful`` and ``failed``
          shards (see examples below).
        * ``bulk-request-size-bytes``: Total size of the bulk request body in bytes.
        * ``total-document-size-bytes``: Total size of all documents within the bulk request body in bytes.

        Here are a few examples:

        If ``detailed-results`` is ``False`` a typical return value is::

            {
                "index": "my_index",
                "weight": 5000,
                "unit": "docs",
                "bulk-size": 5000,
                "success": True,
                "success-count": 5000,
                "error-count": 0
            }

        Whereas the response will look as follow if there are bulk errors::

            {
                "index": "my_index",
                "weight": 5000,
                "unit": "docs",
                "bulk-size": 5000,
                "success": False,
                "success-count": 4000,
                "error-count": 1000
            }

        If ``detailed-results`` is ``True`` a typical return value is::


            {
                "index": "my_index",
                "weight": 5000,
                "unit": "docs",
                "bulk-size": 5000,
                "bulk-request-size-bytes": 2250000,
                "total-document-size-bytes": 2000000,
                "success": True,
                "success-count": 5000,
                "error-count": 0,
                "ops": {
                    "index": {
                        "item-count": 5000,
                        "created": 5000
                    }
                },
                "shards_histogram": [
                    {
                        "item-count": 5000,
                        "shards": {
                            "total": 2,
                            "successful": 2,
                            "failed": 0
                        }
                    }
                ]
            }

        An example error response may look like this::


            {
                "index": "my_index",
                "weight": 5000,
                "unit": "docs",
                "bulk-size": 5000,
                "bulk-request-size-bytes": 2250000,
                "total-document-size-bytes": 2000000,
                "success": False,
                "success-count": 4000,
                "error-count": 1000,
                "ops": {
                    "index": {
                        "item-count": 5000,
                        "created": 4000,
                        "noop": 1000
                    }
                },
                "shards_histogram": [
                    {
                        "item-count": 4000,
                        "shards": {
                            "total": 2,
                            "successful": 2,
                            "failed": 0
                        }
                    },
                    {
                        "item-count": 500,
                        "shards": {
                            "total": 2,
                            "successful": 1,
                            "failed": 1
                        }
                    },
                    {
                        "item-count": 500,
                        "shards": {
                            "total": 2,
                            "successful": 0,
                            "failed": 2
                        }
                    }
                ]
            }
        """
        detailed_results = params.get("detailed-results", False)
        index = params.get("index")

        bulk_params = {}
        if "pipeline" in params:
            bulk_params["pipeline"] = params["pipeline"]

        with_action_metadata = mandatory(params, "action_metadata_present", "bulk-index")
        bulk_size = mandatory(params, "bulk-size", "bulk-index")

        if with_action_metadata:
            # only half of the lines are documents
            response = es.bulk(body=params["body"], params=bulk_params)
        else:
            response = es.bulk(body=params["body"], index=index, doc_type=params["type"], params=bulk_params)

        stats = self.detailed_stats(params, bulk_size, response) if detailed_results else self.simple_stats(bulk_size, response)

        meta_data = {
            "index": str(index) if index else None,
            "weight": bulk_size,
            "unit": "docs",
            "bulk-size": bulk_size
        }
        meta_data.update(stats)
        if not stats["success"]:
            meta_data["error-type"] = "bulk"
        return meta_data

    def detailed_stats(self, params, bulk_size, response):
        ops = {}
        shards_histogram = OrderedDict()
        bulk_error_count = 0
        error_details = set()
        bulk_request_size_bytes = 0
        total_document_size_bytes = 0

        for line_number, data in enumerate(params["body"]):

            line_size = len(data.encode('utf-8'))
            if params["action_metadata_present"]:
                if line_number % 2 == 1:
                    total_document_size_bytes += line_size
            else:
                total_document_size_bytes += line_size

            bulk_request_size_bytes += line_size

        for idx, item in enumerate(response["items"]):
            # there is only one (top-level) item
            op, data = next(iter(item.items()))
            if op not in ops:
                ops[op] = Counter()
            ops[op]["item-count"] += 1
            if "result" in data:
                ops[op][data["result"]] += 1

            if "_shards" in data:
                s = data["_shards"]
                sk = "%d-%d-%d" % (s["total"], s["successful"], s["failed"])
                if sk not in shards_histogram:
                    shards_histogram[sk] = {
                        "item-count": 0,
                        "shards": s
                    }
                shards_histogram[sk]["item-count"] += 1
            if data["status"] > 299 or ("_shards" in data and data["_shards"]["failed"] > 0):
                bulk_error_count += 1
                self.extract_error_details(error_details, data)
        stats = {
            "success": bulk_error_count == 0,
            "success-count": bulk_size - bulk_error_count,
            "error-count": bulk_error_count,
            "ops": ops,
            "shards_histogram": list(shards_histogram.values()),
            "bulk-request-size-bytes": bulk_request_size_bytes,
            "total-document-size-bytes": total_document_size_bytes
        }
        if bulk_error_count > 0:
            stats["error-type"] = "bulk"
            stats["error-description"] = self.error_description(error_details)
        return stats

    def simple_stats(self, bulk_size, response):
        bulk_error_count = 0
        error_details = set()
        if response["errors"]:
            for idx, item in enumerate(response["items"]):
                data = next(iter(item.values()))
                if data["status"] > 299 or data["_shards"]["failed"] > 0:
                    bulk_error_count += 1
                    self.extract_error_details(error_details, data)
        stats = {
            "success": bulk_error_count == 0,
            "success-count": bulk_size - bulk_error_count,
            "error-count": bulk_error_count
        }
        if bulk_error_count > 0:
            stats["error-type"] = "bulk"
            stats["error-description"] = self.error_description(error_details)
        return stats

    def extract_error_details(self, error_details, data):
        if data.get("error") and data["error"].get("reason"):
            error_details.add((data["status"], data["error"]["reason"]))
        else:
            error_details.add((data["status"], None))

    def error_description(self, error_details):
        error_description = ""
        for status, reason in error_details:
            if reason:
                error_description += "HTTP status: %s, message: %s" % (str(status), reason)
            else:
                error_description += "HTTP status: %s" % str(status)
        return error_description

    def __repr__(self, *args, **kwargs):
        return "bulk-index"


class ForceMerge(Runner):
    """
    Runs a force merge operation against Elasticsearch.
    """

    def __call__(self, es, params):
        logger.info("Force merging all indices.")
        import elasticsearch
        try:
            if "max_num_segments" in params:
                es.indices.forcemerge(index="_all", max_num_segments=params["max_num_segments"])
            else:
                es.indices.forcemerge(index="_all")
        except elasticsearch.TransportError as e:
            # this is caused by older versions of Elasticsearch (< 2.1), fall back to optimize
            if e.status_code == 400:
                if "max_num_segments" in params:
                    es.transport.perform_request("POST", "/_optimize?max_num_segments=%s" % (params["max_num_segments"]))
                else:
                    es.transport.perform_request("POST", "/_optimize")
            else:
                raise e

    def __repr__(self, *args, **kwargs):
        return "force-merge"


class IndicesStats(Runner):
    """
    Gather index stats for all indices.
    """

    def __call__(self, es, params):
        es.indices.stats(metric="_all")

    def __repr__(self, *args, **kwargs):
        return "indices-stats"


class NodeStats(Runner):
    """
    Gather node stats for all nodes.
    """

    def __call__(self, es, params):
        es.nodes.stats(metric="_all")

    def __repr__(self, *args, **kwargs):
        return "node-stats"


class Query(Runner):
    """
    Runs a request body search against Elasticsearch.

    It expects at least the following keys in the `params` hash:

    * `index`: The index or indices against which to issue the query.
    * `type`: See `index`
    * `use_request_cache`: True iff the request cache should be used.
    * `body`: Query body

    If the following parameters are present in addition, a scroll query will be issued:

    * `pages`: Number of pages to retrieve at most for this scroll. If a scroll query does yield less results than the specified number of
               pages we will terminate earlier.
    * `items_per_page`: Number of items to retrieve per page.

    Returned meta data

    The following meta data are always returned:

    * ``weight``: operation-agnostic representation of the "weight" of an operation (used internally by Rally for throughput calculation).
                  Always 1 for normal queries and the number of retrieved pages for scroll queries.
    * ``unit``: The unit in which to interpret ``weight``. Always "ops".
    * ``hits``: Total number of hits for this operation.
    * ``timed_out``: Whether the search has timed out. For scroll queries, this flag is ``True`` if the flag was ``True`` for any of the
                     queries issued.

    For scroll queries we also return:

    * ``pages``: Total number of pages that have been retrieved.
    """

    def __init__(self):
        self.scroll_id = None
        self.es = None

    def __call__(self, es, params):
        if "pages" in params and "items_per_page" in params:
            return self.scroll_query(es, params)
        else:
            return self.request_body_query(es, params)

    def request_body_query(self, es, params):
        request_params = params.get("request_params", {})
        if "use_request_cache" in params:
            request_params["request_cache"] = params["use_request_cache"]
        r = es.search(
            index=params.get("index", "_all"),
            doc_type=params.get("type"),
            body=mandatory(params, "body", "query"),
            **request_params)
        hits = r["hits"]["total"]
        return {
            "weight": 1,
            "unit": "ops",
            "hits": hits,
            "timed_out": r["timed_out"],
            "took": r["took"]
        }

    def scroll_query(self, es, params):
        request_params = params.get("request_params", {})
        hits = 0
        retrieved_pages = 0
        timed_out = False
        took = 0
        self.es = es
        # explicitly convert to int to provoke an error otherwise
        total_pages = sys.maxsize if params["pages"] == "all" else int(params["pages"])

        for page in range(total_pages):
            if page == 0:
                r = es.search(
                    index=params.get("index", "_all"),
                    doc_type=params.get("type"),
                    body=mandatory(params, "body", "query"),
                    sort="_doc",
                    scroll="10s",
                    size=params["items_per_page"],
                    request_cache=params.get("use_request_cache"),
                    **request_params
                )
                # This should only happen if we concurrently create an index and start searching
                self.scroll_id = r.get("_scroll_id", None)
            else:
                # This does only work for ES 2.x and above
                # r = es.scroll(body={"scroll_id": self.scroll_id, "scroll": "10s"})
                # This is the most compatible version to perform a scroll across all supported versions of Elasticsearch
                # (1.x does not support a proper JSON body in search scroll requests).
                r = self.es.transport.perform_request("GET", "/_search/scroll", params={"scroll_id": self.scroll_id, "scroll": "10s"})
            hit_count = len(r["hits"]["hits"])
            timed_out = timed_out or r["timed_out"]
            took += r["took"]
            hits += hit_count
            retrieved_pages += 1
            if hit_count == 0:
                # We're done prematurely. Even if we are on page index zero, we still made one call.
                break

        return {
            "weight": retrieved_pages,
            "pages": retrieved_pages,
            "hits": hits,
            "unit": "ops",
            "timed_out": timed_out,
            "took": took
        }

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.scroll_id and self.es:
            try:
                # This does only work for ES 2.x and above
                # self.es.clear_scroll(body={"scroll_id": [self.scroll_id]})

                # This is the most compatible version to clear one scroll id across all supported versions of Elasticsearch
                # (1.x does not support a proper JSON body in clear scroll requests).
                self.es.transport.perform_request("DELETE", "/_search/scroll/%s" % self.scroll_id)
            except BaseException:
                logger.exception("Could not clear scroll [%s]. This will lead to excessive resource usage in Elasticsearch and "
                                 "will skew your benchmark results." % self.scroll_id)
        self.scroll_id = None
        self.es = None
        return False

    def __repr__(self, *args, **kwargs):
        return "query"


class ClusterHealth(Runner):
    """
    Get cluster health
    """

    def __call__(self, es, params):
        from enum import Enum
        from functools import total_ordering
        from elasticsearch.client import _make_path

        @total_ordering
        class ClusterHealthStatus(Enum):
            UNKNOWN = 0
            RED = 1
            YELLOW = 2
            GREEN = 3

            def __lt__(self, other):
                if self.__class__ is other.__class__:
                    return self.value < other.value
                return NotImplemented

        def status(v):
            try:
                return ClusterHealthStatus[v.upper()]
            except (KeyError, AttributeError):
                return ClusterHealthStatus.UNKNOWN

        index = params.get("index")
        request_params = params.get("request-params", {})
        # by default, Elasticsearch will not wait and thus we treat this as success
        expected_cluster_status = request_params.get("wait_for_status", str(ClusterHealthStatus.UNKNOWN))
        # newer ES versions >= 5.0
        if "wait_for_no_relocating_shards" in request_params:
            expected_relocating_shards = 0
        else:
            # older ES versions
            # either the user has defined something or we're good with any count of relocating shards.
            expected_relocating_shards = int(request_params.get("wait_for_relocating_shards", sys.maxsize))

        # This would not work if the request parameter is not a proper method parameter for the ES client...
        # result = es.cluster.health(**request_params)
        result = es.transport.perform_request("GET", _make_path("_cluster", "health", index), params=request_params)
        cluster_status = result["status"]
        relocating_shards = result["relocating_shards"]

        return {
            "weight": 1,
            "unit": "ops",
            "success": status(cluster_status) >= status(expected_cluster_status) and relocating_shards <= expected_relocating_shards,
            "cluster-status": cluster_status,
            "relocating-shards": relocating_shards
        }

    def __repr__(self, *args, **kwargs):
        return "cluster-health"


class PutPipeline(Runner):
    """
    Execute the `put pipeline API <https://www.elastic.co/guide/en/elasticsearch/reference/current/put-pipeline-api.html>`_. Note that this
    API is only available from Elasticsearch 5.0 onwards.
    """

    def __call__(self, es, params):
        es.ingest.put_pipeline(id=mandatory(params, "id", "put-pipeline"),
                               body=mandatory(params, "body", "put-pipeline"),
                               master_timeout=params.get("master_timeout"),
                               timeout=params.get("timeout"),
                               )

    def __repr__(self, *args, **kwargs):
        return "put-pipeline"


class Refresh(Runner):
    """
    Execute the `refresh API <https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-refresh.html>`_.
    """

    def __call__(self, es, params):
        es.indices.refresh(index=params.get("index", "_all"))

    def __repr__(self, *args, **kwargs):
        return "refresh"


# TODO: Allow to use this from (selected) regular runners and add user documentation.
# TODO: It would maybe be interesting to add meta-data on how many retries there were.
class Retry(Runner):
    """
    This runner can be used as a wrapper around regular runners to retry operations.

    It defines the following parameters:

    * ``retries`` (optional, default 0): The number of times the operation is retried.
    * ``retry-wait-period`` (optional, default 0.5): The time in seconds to wait after an error.
    * ``retry-on-timeout`` (optional, default True): Whether to retry on connection timeout.
    * ``retry-on-error`` (optional, default False): Whether to retry on failure (i.e. the delegate returns ``success == False``)
    """

    def __init__(self, delegate):
        self.delegate = delegate

    def __enter__(self):
        self.delegate.__enter__()
        return self

    def __call__(self, es, params):
        import elasticsearch
        import socket

        max_attempts = params.get("retries", 0) + 1
        sleep_time = params.get("retry-wait-period", 0.5)
        retry_on_timeout = params.get("retry-on-timeout", True)
        retry_on_error = params.get("retry-on-error", False)

        for attempt in range(max_attempts):
            last_attempt = attempt + 1 == max_attempts
            try:
                return_value = self.delegate(es, params)
                if last_attempt or not retry_on_error:
                    return return_value
                # we can determine success if and only if the runner returns a dict. Otherwise, we have to assume it was fine.
                elif isinstance(return_value, dict):
                    if return_value.get("success", True):
                        return return_value
                    else:
                        time.sleep(sleep_time)
                else:
                    return return_value
            except (socket.timeout, elasticsearch.exceptions.ConnectionError):
                if last_attempt or not retry_on_timeout:
                    raise
                else:
                    time.sleep(sleep_time)
            except elasticsearch.exceptions.TransportError as e:
                if last_attempt or not retry_on_timeout:
                    raise e
                elif e.status_code == 408:
                    logger.debug("%s has timed out." % repr(self.delegate))
                    time.sleep(sleep_time)
                else:
                    raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.delegate.__exit__(exc_type, exc_val, exc_tb)

    def __repr__(self, *args, **kwargs):
        return "retryable %s" % repr(self.delegate)


# TODO #370: Remove this registration and replace with a new Index runner.
# Old (deprecated) name
register_runner(track.OperationType.Index.name, BulkIndex())
# New name
register_runner(track.OperationType.Bulk.name, BulkIndex())
register_runner(track.OperationType.ForceMerge.name, ForceMerge())
register_runner(track.OperationType.IndicesStats.name, IndicesStats())
register_runner(track.OperationType.NodesStats.name, NodeStats())
register_runner(track.OperationType.Search.name, Query())

# We treat the following as administrative commands and thus already start to wrap them in a retry.
register_runner(track.OperationType.ClusterHealth.name, Retry(ClusterHealth()))
register_runner(track.OperationType.PutPipeline.name, Retry(PutPipeline()))
register_runner(track.OperationType.Refresh.name, Retry(Refresh()))
