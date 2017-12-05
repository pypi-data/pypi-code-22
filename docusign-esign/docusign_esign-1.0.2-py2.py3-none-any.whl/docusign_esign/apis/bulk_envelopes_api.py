# coding: utf-8

"""
    DocuSign REST API

    The DocuSign REST API provides you with a powerful, convenient, and simple Web services API for interacting with DocuSign.

    OpenAPI spec version: v2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class BulkEnvelopesApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def delete_recipients(self, account_id, envelope_id, recipient_id, **kwargs):
        """
        Deletes the bulk recipient file from an envelope.
        Deletes the bulk recipient file from an envelope. This cannot be used if the envelope has been sent.  After using this, the `bulkRecipientsUri` property is not returned in subsequent GET calls for the envelope, but the recipient will remain as a bulk recipient.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_recipients(account_id, envelope_id, recipient_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str account_id: The external account number (int) or account ID Guid. (required)
        :param str envelope_id: The envelopeId Guid of the envelope being accessed. (required)
        :param str recipient_id: The ID of the recipient being accessed. (required)
        :return: BulkRecipientsUpdateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.delete_recipients_with_http_info(account_id, envelope_id, recipient_id, **kwargs)
        else:
            (data) = self.delete_recipients_with_http_info(account_id, envelope_id, recipient_id, **kwargs)
            return data

    def delete_recipients_with_http_info(self, account_id, envelope_id, recipient_id, **kwargs):
        """
        Deletes the bulk recipient file from an envelope.
        Deletes the bulk recipient file from an envelope. This cannot be used if the envelope has been sent.  After using this, the `bulkRecipientsUri` property is not returned in subsequent GET calls for the envelope, but the recipient will remain as a bulk recipient.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_recipients_with_http_info(account_id, envelope_id, recipient_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str account_id: The external account number (int) or account ID Guid. (required)
        :param str envelope_id: The envelopeId Guid of the envelope being accessed. (required)
        :param str recipient_id: The ID of the recipient being accessed. (required)
        :return: BulkRecipientsUpdateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'envelope_id', 'recipient_id']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_recipients" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params) or (params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `delete_recipients`")
        # verify the required parameter 'envelope_id' is set
        if ('envelope_id' not in params) or (params['envelope_id'] is None):
            raise ValueError("Missing the required parameter `envelope_id` when calling `delete_recipients`")
        # verify the required parameter 'recipient_id' is set
        if ('recipient_id' not in params) or (params['recipient_id'] is None):
            raise ValueError("Missing the required parameter `recipient_id` when calling `delete_recipients`")


        collection_formats = {}

        resource_path = '/v2/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/bulk_recipients'.replace('{format}', 'json')
        path_params = {}
        if 'account_id' in params:
            path_params['accountId'] = params['account_id']
        if 'envelope_id' in params:
            path_params['envelopeId'] = params['envelope_id']
        if 'recipient_id' in params:
            path_params['recipientId'] = params['recipient_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'DELETE',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='BulkRecipientsUpdateResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get(self, account_id, batch_id, **kwargs):
        """
        Gets the status of a specified bulk send operation.
        Retrieves the status information of a single bulk recipient batch. A bulk recipient batch is the set of envelopes sent from a single bulk recipient file. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get(account_id, batch_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str account_id: The external account number (int) or account ID Guid. (required)
        :param str batch_id: (required)
        :param str count: Specifies the number of entries to return.
        :param str include: Specifies which entries are included in the response. Multiple entries can be included by using commas in the query string (example: ?include=”failed,queued”)   Valid values are:   * all - Returns all entries. If present, overrides all other query settings. This is the default if no query string is provided. * failed - This only returns entries with a failed status. * queued - This only returns entries with a queued status. * sent – This only returns entries with a sent status.  
        :param str start_position: Specifies the location in the list of envelopes from which to start.
        :return: BulkEnvelopeStatus
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_with_http_info(account_id, batch_id, **kwargs)
        else:
            (data) = self.get_with_http_info(account_id, batch_id, **kwargs)
            return data

    def get_with_http_info(self, account_id, batch_id, **kwargs):
        """
        Gets the status of a specified bulk send operation.
        Retrieves the status information of a single bulk recipient batch. A bulk recipient batch is the set of envelopes sent from a single bulk recipient file. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_with_http_info(account_id, batch_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str account_id: The external account number (int) or account ID Guid. (required)
        :param str batch_id: (required)
        :param str count: Specifies the number of entries to return.
        :param str include: Specifies which entries are included in the response. Multiple entries can be included by using commas in the query string (example: ?include=”failed,queued”)   Valid values are:   * all - Returns all entries. If present, overrides all other query settings. This is the default if no query string is provided. * failed - This only returns entries with a failed status. * queued - This only returns entries with a queued status. * sent – This only returns entries with a sent status.  
        :param str start_position: Specifies the location in the list of envelopes from which to start.
        :return: BulkEnvelopeStatus
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'batch_id', 'count', 'include', 'start_position']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params) or (params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `get`")
        # verify the required parameter 'batch_id' is set
        if ('batch_id' not in params) or (params['batch_id'] is None):
            raise ValueError("Missing the required parameter `batch_id` when calling `get`")


        collection_formats = {}

        resource_path = '/v2/accounts/{accountId}/bulk_envelopes/{batchId}'.replace('{format}', 'json')
        path_params = {}
        if 'account_id' in params:
            path_params['accountId'] = params['account_id']
        if 'batch_id' in params:
            path_params['batchId'] = params['batch_id']

        query_params = {}
        if 'count' in params:
            query_params['count'] = params['count']
        if 'include' in params:
            query_params['include'] = params['include']
        if 'start_position' in params:
            query_params['start_position'] = params['start_position']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='BulkEnvelopeStatus',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_recipients(self, account_id, envelope_id, recipient_id, **kwargs):
        """
        Gets the bulk recipient file from an envelope.
        Retrieves the bulk recipient file information from an envelope that has a bulk recipient.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_recipients(account_id, envelope_id, recipient_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str account_id: The external account number (int) or account ID Guid. (required)
        :param str envelope_id: The envelopeId Guid of the envelope being accessed. (required)
        :param str recipient_id: The ID of the recipient being accessed. (required)
        :param str include_tabs:
        :param str start_position:
        :return: BulkRecipientsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_recipients_with_http_info(account_id, envelope_id, recipient_id, **kwargs)
        else:
            (data) = self.get_recipients_with_http_info(account_id, envelope_id, recipient_id, **kwargs)
            return data

    def get_recipients_with_http_info(self, account_id, envelope_id, recipient_id, **kwargs):
        """
        Gets the bulk recipient file from an envelope.
        Retrieves the bulk recipient file information from an envelope that has a bulk recipient.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_recipients_with_http_info(account_id, envelope_id, recipient_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str account_id: The external account number (int) or account ID Guid. (required)
        :param str envelope_id: The envelopeId Guid of the envelope being accessed. (required)
        :param str recipient_id: The ID of the recipient being accessed. (required)
        :param str include_tabs:
        :param str start_position:
        :return: BulkRecipientsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'envelope_id', 'recipient_id', 'include_tabs', 'start_position']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_recipients" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params) or (params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `get_recipients`")
        # verify the required parameter 'envelope_id' is set
        if ('envelope_id' not in params) or (params['envelope_id'] is None):
            raise ValueError("Missing the required parameter `envelope_id` when calling `get_recipients`")
        # verify the required parameter 'recipient_id' is set
        if ('recipient_id' not in params) or (params['recipient_id'] is None):
            raise ValueError("Missing the required parameter `recipient_id` when calling `get_recipients`")


        collection_formats = {}

        resource_path = '/v2/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/bulk_recipients'.replace('{format}', 'json')
        path_params = {}
        if 'account_id' in params:
            path_params['accountId'] = params['account_id']
        if 'envelope_id' in params:
            path_params['envelopeId'] = params['envelope_id']
        if 'recipient_id' in params:
            path_params['recipientId'] = params['recipient_id']

        query_params = {}
        if 'include_tabs' in params:
            query_params['include_tabs'] = params['include_tabs']
        if 'start_position' in params:
            query_params['start_position'] = params['start_position']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='BulkRecipientsResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def list(self, account_id, **kwargs):
        """
        Gets status information about bulk recipient batches.
        Retrieves status information about all the bulk recipient batches. A bulk recipient batch is the set of envelopes sent from a single bulk recipient file. The response includes general information about each bulk recipient batch.   The response returns information about the envelopes sent with bulk recipient batches, including the `batchId` property, which can be used to retrieve a more detailed status of individual bulk recipient batches.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list(account_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str account_id: The external account number (int) or account ID Guid. (required)
        :param str count: The number of results to return. This can be 1 to 20.
        :param str include:
        :param str start_position: The position of the bulk envelope items in the response. This is used for repeated calls, when the number of bulk envelopes returned is too large for one return. The default value is 0.
        :return: BulkEnvelopesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.list_with_http_info(account_id, **kwargs)
        else:
            (data) = self.list_with_http_info(account_id, **kwargs)
            return data

    def list_with_http_info(self, account_id, **kwargs):
        """
        Gets status information about bulk recipient batches.
        Retrieves status information about all the bulk recipient batches. A bulk recipient batch is the set of envelopes sent from a single bulk recipient file. The response includes general information about each bulk recipient batch.   The response returns information about the envelopes sent with bulk recipient batches, including the `batchId` property, which can be used to retrieve a more detailed status of individual bulk recipient batches.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.list_with_http_info(account_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str account_id: The external account number (int) or account ID Guid. (required)
        :param str count: The number of results to return. This can be 1 to 20.
        :param str include:
        :param str start_position: The position of the bulk envelope items in the response. This is used for repeated calls, when the number of bulk envelopes returned is too large for one return. The default value is 0.
        :return: BulkEnvelopesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'count', 'include', 'start_position']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params) or (params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `list`")


        collection_formats = {}

        resource_path = '/v2/accounts/{accountId}/bulk_envelopes'.replace('{format}', 'json')
        path_params = {}
        if 'account_id' in params:
            path_params['accountId'] = params['account_id']

        query_params = {}
        if 'count' in params:
            query_params['count'] = params['count']
        if 'include' in params:
            query_params['include'] = params['include']
        if 'start_position' in params:
            query_params['start_position'] = params['start_position']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='BulkEnvelopesResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def update_recipients(self, account_id, envelope_id, recipient_id, **kwargs):
        """
        Adds or replaces envelope bulk recipients.
        Updates the bulk recipients in a draft envelope using a file upload. The Content-Type supported for uploading a bulk recipient file is CSV (text/csv).  The REST API does not support modifying individual rows or values in the bulk recipients file. It only allows the entire file to be added or replaced with a new file.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_recipients(account_id, envelope_id, recipient_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str account_id: The external account number (int) or account ID Guid. (required)
        :param str envelope_id: The envelopeId Guid of the envelope being accessed. (required)
        :param str recipient_id: The ID of the recipient being accessed. (required)
        :param BulkRecipientsRequest bulk_recipients_request:
        :return: BulkRecipientsSummaryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.update_recipients_with_http_info(account_id, envelope_id, recipient_id, **kwargs)
        else:
            (data) = self.update_recipients_with_http_info(account_id, envelope_id, recipient_id, **kwargs)
            return data

    def update_recipients_with_http_info(self, account_id, envelope_id, recipient_id, **kwargs):
        """
        Adds or replaces envelope bulk recipients.
        Updates the bulk recipients in a draft envelope using a file upload. The Content-Type supported for uploading a bulk recipient file is CSV (text/csv).  The REST API does not support modifying individual rows or values in the bulk recipients file. It only allows the entire file to be added or replaced with a new file.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_recipients_with_http_info(account_id, envelope_id, recipient_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str account_id: The external account number (int) or account ID Guid. (required)
        :param str envelope_id: The envelopeId Guid of the envelope being accessed. (required)
        :param str recipient_id: The ID of the recipient being accessed. (required)
        :param BulkRecipientsRequest bulk_recipients_request:
        :return: BulkRecipientsSummaryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'envelope_id', 'recipient_id', 'bulk_recipients_request']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_recipients" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params) or (params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `update_recipients`")
        # verify the required parameter 'envelope_id' is set
        if ('envelope_id' not in params) or (params['envelope_id'] is None):
            raise ValueError("Missing the required parameter `envelope_id` when calling `update_recipients`")
        # verify the required parameter 'recipient_id' is set
        if ('recipient_id' not in params) or (params['recipient_id'] is None):
            raise ValueError("Missing the required parameter `recipient_id` when calling `update_recipients`")


        collection_formats = {}

        resource_path = '/v2/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/bulk_recipients'.replace('{format}', 'json')
        path_params = {}
        if 'account_id' in params:
            path_params['accountId'] = params['account_id']
        if 'envelope_id' in params:
            path_params['envelopeId'] = params['envelope_id']
        if 'recipient_id' in params:
            path_params['recipientId'] = params['recipient_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'bulk_recipients_request' in params:
            body_params = params['bulk_recipients_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'PUT',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='BulkRecipientsSummaryResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
